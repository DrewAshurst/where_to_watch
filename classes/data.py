import requests
import pandas as pd
import json




class Data:

    def __init__(self, config):
        self.url = "https://streaming-availability.p.rapidapi.com/shows/search/title"
        self.config = config
        self.watch_options = ['Free', 'Subscription', 'Buy']

    def search_content(self, title, type, accepted, dump=False):
        output = {}

        querystring = {
            "title": title,
            "series_granularity": "show",
            "show_type": type,  # movie or series
            "output_language": "en",
            "country": "us",
        }

        headers = {
            "x-rapidapi-key": self.config["api_key"],
            "x-rapidapi-host": self.config["api_host"],
        }

        response = requests.get(self.url, headers=headers, params=querystring)

        if dump:

            with open("output.json", "w") as f:
                json.dump(response.json(), f, indent=4)

        response_data = response.json()
        output = self.collect_data(response_data, type)
        df = pd.DataFrame(output)

        filter = df[accepted["option"]].isin(accepted["service"]).any(axis=1)
        return df.loc[filter]

    def collect_data(self, responses, type):
        output = []
        row = {}
        for response in responses:
            if type == "series":
                show_key = f"{response['title']}|{response['lastAirYear']}"
            else:
                show_key = f"{response['title']}|{response['releaseYear']}"

            row = {
                "show_key": show_key,
                "genres": None,
                "season_count": None,
                "episode_count": None,
                "runtime": None,
                "rating": None,
                "free": [],
                "subscription": [],
                "buy": [],
            }

            row["show_key"] = show_key

            streams = response["streamingOptions"].get("us")
            if streams:
                for stream in streams:
                    if stream["type"] == "free":
                        row["free"].append(stream["service"]["name"])
                    if stream["type"] == "subscription":
                        row["subscription"].append(stream["service"]["name"])
                    if stream["type"] == "buy":
                        row["buy"].append(stream["service"]["name"])

            for key in ["free", "subscription", "buy"]:
                row[key] = "|".join(set(row[key]))

            genres = response.get("genres")
            if genres:
                row["genres"] = ",".join(set(i["name"] for i in genres))

            if type == "series":
                row["season_count"] = response["seasonCount"]
                row["episode_count"] = response["episodeCount"]
            else:
                row["runtime"] = response.get("runtime")
                if row["runtime"]:
                    row["runtime"] = int(row["runtime"])

            row["rating"] = response["rating"]

            output.append(row)

        return output


def main():
    d = Data()
    accepted = {
        "option": ["free", "buy", "subscription"],
        "service": [i.strip() for i in d.config["services"]],
    }
    d.search_content("peaky", "series", accepted)
    pass


if __name__ == "__main__":
    main()

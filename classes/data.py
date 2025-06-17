import requests
import json
from pathlib import Path
import yaml


project_root = Path(__file__).resolve().parent.parent


class Data:

    def __init__(self):
        self.url = "https://streaming-availability.p.rapidapi.com/shows/search/title"
        with open(project_root / "config.yaml", "r") as f:
            self.config = yaml.safe_load(f)
        print(self.config["services"])
        self.watch_options = ["Free", "Subscription", "Buy"]

    def search_content(self, title, type, fields, dump=False):
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

        output["services"] = self.get_services(response_data, type)
        output["genres"] = self.get_genres(response_data, type)
        if type == "series":
            output["details"] = self.get_show_details(response_data)
        else:
            output["details"] = self.get_movie_details(response_data)

        output = self.parse_data(fields, output)
        return output

    def parse_data(self, fields, output):
        clean_output = {}
        return_keys = []
        accepted_types = []
        accepted_services = []
        for key, val in fields.items():
            if key in ["Free", "Subscription", "Buy"] and val[1].get():
                accepted_types.append(key)
            elif val[1].get():
                accepted_services.append(key)

        ver_dict = output["services"]
        for key, val in ver_dict.items():
            for service, type in val.items():
                if service in accepted_services and type.capitalize() in accepted_types:
                    return_keys.append(key)

        for key in return_keys:
            clean_output[key] = {}
            clean_output[key]["services"] = output["services"][key]
            clean_output[key]["details"] = output["details"][key]
            clean_output[key]["genres"] = output["genres"][key]

        print(clean_output)
        for result in clean_output.keys():
            for key in clean_output[result]["services"].keys():
                print(clean_output)
                if (
                    clean_output[result]["services"][key].capitalize()
                    not in accepted_types
                ):
                    clean_output[result]["services"][key] = None

        return clean_output

    def get_genres(self, responses, type):
        output = {}
        for response in responses:
            if type == "series":
                show_key = f"{response['title']}|{response['lastAirYear']}"
            else:
                show_key = f"{response['title']}|{response['releaseYear']}"
            output[show_key] = []
            for genre in response["genres"]:
                output[show_key].append(genre["name"])

        for key, val in output.items():
            output[key] = "|".join(val)
        return output

    def get_services(self, responses, type):
        output = {}
        for response in responses:
            if type == "series":
                show_key = f"{response['title']}|{response['lastAirYear']}"
            else:
                show_key = f"{response['title']}|{response['releaseYear']}"

            output[show_key] = {}
            if response["streamingOptions"].get("us"):
                for option in response["streamingOptions"]["us"]:
                    output[show_key][option["service"]["name"]] = option["type"]

        return output

    def get_show_details(self, responses):
        output = {}
        for response in responses:
            show_key = f"{response['title']}|{response['lastAirYear']}"
            output[show_key] = {}
            output[show_key]["rating"] = response["rating"]
            output[show_key]["season_count"] = response["seasonCount"]
            output[show_key]["episode_count"] = response["episodeCount"]

        return output

    def get_movie_details(self, responses):
        output = {}
        for response in responses:
            show_key = f"{response['title']}|{response['releaseYear']}"
            output[show_key] = {}
            output[show_key]["rating"] = response["rating"]
            output[show_key]["runtime"] = response.get("runtime")

        return output


def main():
    d = Data()
    pass


if __name__ == "__main__":
    main()

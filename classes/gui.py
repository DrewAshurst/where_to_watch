import tkinter as tk
from .data import Data


class Gui:
    def __init__(self, config):
        self.config = config
        self.api = Data(config)
        self.root = tk.Tk()

        self.root.geometry("400x400")
        self.output_count = self.config["output_count"]
        self.main_page()

    def clear_window(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def get_checkbox_values(self, checkboxes):
        accepted = {
            'option': [],
            'service': []
        }
        for key, val in checkboxes.items():
            if key.lower() in ['free', 'subscription', 'buy'] and val[1].get():
                accepted['option'].append(key.lower())
            elif val[1].get():
                accepted['service'].append(key)

        return accepted


    def title_search(self, textbox, type, checkboxes):
        value = textbox.get("1.0", tk.END).strip()
        self.get_checkbox_values(checkboxes)
        accepted = self.get_checkbox_values(checkboxes)

        return_data = self.api.search_content(value, type, accepted, True)
        self.show_output(accepted, return_data, type)

    def show_output(self, accepted, df, type):
        self.clear_window(self.output_frame)
        cols = ['show_key', 'genres',  'rating']

        if type == 'series':
            cols = cols + ['season_count', 'episode_count'] + accepted['option']
        else:
            cols = cols + ['runtime'] + accepted['option']
        output = df[cols]
        label_container = tk.Frame(self.output_frame, bg="deep sky blue")
        label_container.pack(anchor='center')
        

        for row in output.values.tolist()[:self.output_count]:
            out_string = ''
            for i in range(len(row)):
                print('col', cols[i])
                if cols[i] in ['free', 'subscription', 'buy'] and row[i]:
                    for val in row[i].split('|'):
                        out_string += f'{val}: {cols[i].capitalize()}\n'

                elif cols[i] == 'show_key':
                    vals = row[i].split('|')
                    out_string += f'{vals[0]}: {vals[1]}\n'
                elif row[i]:
                    out_string += f'{cols[i].replace("_", " ").capitalize()}: {row[i]}\n'

            tk.Label(
                label_container,
                relief="raised",
                borderwidth=4,
                text=out_string,
                font=("Helvetica", 14),
                fg="black",
                bg="goldenrod",
            ).pack(padx=15, side="left")
            


    def all_box_action(self, checkboxes, value):
        for key, box in checkboxes.items():
            if key in self.api.watch_options:
                continue
            box[1].set(value)

    def title_search_page(self, show_output=False, output=None, old_checkboxes=None):
        self.clear_window(self.root)

        service_list = sorted(self.api.config["services"])

        # main frame which houses all others
        main_frame = tk.Frame(self.root, bg="deep sky blue", borderwidth=2)
        textbox_frame = tk.Frame(main_frame, bg="deep sky blue", borderwidth=2)
        button_frame = tk.Frame(main_frame, bg="deep sky blue", borderwidth=2)
        checkbox_frame = tk.Frame(main_frame, bg="deep sky blue", borderwidth=2)
        self.output_frame = tk.Frame(main_frame, bg="deep sky blue", borderwidth=2)

        # columns for checkbox layout
        cb_cols = [
            tk.Frame(checkbox_frame, bg="deep sky blue", borderwidth=2)
            for i in range(6)
        ]

        textbox = tk.Text(textbox_frame, height=5, width=40)

        # drop down initialize
        current_option = tk.StringVar(value="Movie or Series?")
        options = ["Movie", "Series"]
        dropdown = tk.OptionMenu(textbox_frame, current_option, *options)
        dropdown.config(bg="goldenrod", fg="black", activebackground="white")

        button = tk.Button(
            button_frame,
            text="Search",
            width=15,
            height=5,
            bg="goldenrod",
            command=lambda: self.title_search(
                textbox, current_option.get().lower(), checkboxes
            ),
        )

        checkboxes = {}
        check_box_column_count = 5
        col_ind = 0

        for i in range(len(service_list)):
            var = tk.BooleanVar()
            if i >= col_ind * check_box_column_count and i < (col_ind+1) * check_box_column_count:
                checkboxes[service_list[i]] = [
                    tk.Checkbutton(
                        cb_cols[col_ind],
                        text=service_list[i],
                        variable=var,
                        bg="goldenrod",
                        relief="groove",
                    ),
                    var,
                ]
            if i == ((col_ind+1) * check_box_column_count) - 1:
                col_ind += 1


        for option in self.api.watch_options:
            var = tk.BooleanVar()
            var.set(True)
            checkboxes[option] = [
                tk.Checkbutton(
                    cb_cols[4],
                    text=option,
                    variable=var,
                    bg="goldenrod",
                    relief="groove",
                ),
                var,
            ]

        main_frame.pack(padx=20, pady=20, fill="both", expand=True, anchor="n")
        textbox_frame.pack(padx=20, pady=20, anchor="n")
        button_frame.pack(padx=20, pady=20, anchor="n")
        checkbox_frame.pack(padx=20, pady=20, fill="both", anchor="n", expand=True)
        self.output_frame.pack(padx=20, pady=20, fill="both", anchor="n", expand=True)

        textbox.pack(pady=10, anchor="n")
        dropdown.pack(pady=10)

        button.pack(pady=10, anchor="n")
        for frame in cb_cols:
            frame.pack(side="left", anchor="n", padx=10, expand=True, fill="x")

        for value in checkboxes.values():
            value[0].pack(anchor="w", pady=5)

        all_button = tk.Button(
            cb_cols[5],
            width=20,
            height=3,
            text="Select all Services",
            command=lambda: self.all_box_action(checkboxes, True),
            bg="goldenrod",
        )
        none_button = tk.Button(
            cb_cols[5],
            width=20,
            height=3,
            text="Deselect all Services",
            command=lambda: self.all_box_action(checkboxes, False),
            bg="goldenrod",
        )

        all_button.pack()
        none_button.pack()

    def main_page(self):
        self.clear_window(self.root)

        button_frame = tk.Frame(self.root, bg="deep sky blue", borderwidth=2)
        button = tk.Button(
            button_frame,
            width=20,
            height=5,
            text="Search by Title",
            command=self.title_search_page,
            bg="goldenrod",
        )

        button.pack(pady=10, expand=True)
        button_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.root.mainloop()


def main():
    g = Gui()


if __name__ == "__main__":
    main()

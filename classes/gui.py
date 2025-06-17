import tkinter as tk
from .data import Data


class Gui:
    def __init__(self):
        self.api = Data()
        self.root = tk.Tk()

        self.root.geometry("400x400")
        self.main_page()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def title_search(self, textbox, type, checkboxes):
        value = textbox.get("1.0", tk.END).strip()
        for key, val in checkboxes.items():
            print(key, val[1].get())
        return_data = self.api.search_content(value, type, checkboxes, True)
        self.title_search_page(True, return_data, checkboxes)

    def select_all_boxes(self, checkboxes):
        for key, box in checkboxes.items():
            if key in self.api.watch_options:
                continue
            box[1].set(True)

    def deselect_all_boxes(self, checkboxes):
        for key, box in checkboxes.items():
            if key in self.api.watch_options:
                continue
            box[1].set(False)

    def title_search_page(self, show_output=False, output=None, old_checkboxes=None):
        self.clear_window()

        service_list = sorted(self.api.config["services"])

        # main frame which houses all others
        main_frame = tk.Frame(self.root, bg="deep sky blue", borderwidth=2)

        textbox_frame = tk.Frame(main_frame, bg="deep sky blue", borderwidth=2)
        button_frame = tk.Frame(main_frame, bg="deep sky blue", borderwidth=2)
        checkbox_frame = tk.Frame(main_frame, bg="deep sky blue", borderwidth=2)
        output_frame = tk.Frame(main_frame, bg="deep sky blue", borderwidth=2)

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
        check_count = 0
        for service in service_list:
            var = tk.BooleanVar()
            if check_count < 5:
                checkboxes[service] = [
                    tk.Checkbutton(
                        cb_cols[0],
                        text=service,
                        variable=var,
                        bg="goldenrod",
                        relief="groove",
                    ),
                    var,
                ]
            elif check_count >= 5 and check_count < 10:
                checkboxes[service] = [
                    tk.Checkbutton(
                        cb_cols[1],
                        text=service,
                        variable=var,
                        bg="goldenrod",
                        relief="groove",
                    ),
                    var,
                ]
            elif check_count >= 10 and check_count < 15:
                checkboxes[service] = [
                    tk.Checkbutton(
                        cb_cols[2],
                        text=service,
                        variable=var,
                        bg="goldenrod",
                        relief="groove",
                    ),
                    var,
                ]
            else:
                checkboxes[service] = [
                    tk.Checkbutton(
                        cb_cols[3],
                        text=service,
                        variable=var,
                        bg="goldenrod",
                        relief="groove",
                    ),
                    var,
                ]
            if old_checkboxes:
                if old_checkboxes[service][1].get():
                    checkboxes[service][1].set(True)
            check_count += 1

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
            if old_checkboxes:
                if old_checkboxes[option][1].get():
                    checkboxes[option][1].set(True)
            check_count += 1

        main_frame.pack(padx=20, pady=20, fill="both", expand=True, anchor="n")
        textbox_frame.pack(padx=20, pady=20, anchor="n")
        button_frame.pack(padx=20, pady=20, anchor="n")
        checkbox_frame.pack(padx=20, pady=20, fill="both", anchor="n", expand=True)
        output_frame.pack(padx=20, pady=20, fill="both", anchor="n", expand=True)

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
            command=lambda: self.select_all_boxes(checkboxes),
            bg="goldenrod",
        )
        none_button = tk.Button(
            cb_cols[5],
            width=20,
            height=3,
            text="Deselect all Services",
            command=lambda: self.deselect_all_boxes(checkboxes),
            bg="goldenrod",
        )

        all_button.pack()
        none_button.pack()

        if output:
            for key, val in output.items():
                print(val)
                text_val = " - ".join(key.split("|"))
                text_val += "\nStreaming Options:\n"
                for sub_key, sub_val in val["services"].items():
                    if sub_val:
                        text_val += f"{sub_key}: {sub_val.capitalize()}\n"

                for sub_key, sub_val in val["details"].items():
                    text_val += f"{sub_key.capitalize()}: {sub_val}\n"

                text_val += f'Genres: {", ".join(val["genres"].split("|"))}'

                tk.Label(
                    output_frame,
                    relief="raised",
                    borderwidth=4,
                    text=text_val,
                    font=("Helvetica", 14),
                    fg="black",
                    bg="goldenrod",
                ).pack(padx=15, side="left", anchor="nw")

    def main_page(self):
        self.clear_window()

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

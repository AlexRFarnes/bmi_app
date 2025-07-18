# bmi_calculator.py

# try:
import customtkinter as ctk

import settings

try:
    from ctypes import byref, c_int, sizeof, windll
except Exception:
    pass

INITIAL_WEIGHT = 70.0
INITIAL_HEIGHT = 170


class App(ctk.CTk):
    def __init__(self):
        # Window setup
        super().__init__(fg_color=settings.GREEN)
        self.title("")
        self.iconbitmap("empty.ico")
        self.geometry("400x400")
        self.resizable(False, False)
        self.change_title_bar_color()

        # Layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform="a")

        # Data
        self.height = ctk.IntVar(value=INITIAL_HEIGHT)
        self.weight = ctk.DoubleVar(value=INITIAL_WEIGHT)
        self.bmi = ctk.StringVar()
        self.is_metric_unit = ctk.BooleanVar(value=True)
        self.update_bmi()

        # Tracing
        self.height.trace("w", self.update_bmi)
        self.weight.trace("w", self.update_bmi)
        self.is_metric_unit.trace("w", self.change_units)

        # Widgets
        ResultText(self, self.bmi)
        self.height_input = HeightInput(self, self.height, self.is_metric_unit)
        self.weight_input = WeightInput(self, self.weight, self.is_metric_unit)
        UnitSwitcher(self, self.is_metric_unit)

        # Main loop
        self.mainloop()

    def update_bmi(self, *args):
        height_meter = self.height.get() / 100
        weight_kg = self.weight.get()
        bmi = round(weight_kg / (height_meter * height_meter), 2)
        self.bmi.set(str(bmi))

    def change_units(self, *args):
        self.height_input.update_text(self.height.get())
        self.weight_input.update_weight()

    def change_title_bar_color(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())  # type: ignore
            windll.dwmapi.DwmSetWindowAttribute(  # type: ignore
                HWND,
                35,
                byref(c_int(settings.TITLE_HEX_COLORS)),  # type: ignore
                sizeof(c_int),  # type: ignore
            )
        except Exception:
            pass


class ResultText(ctk.CTkLabel):
    def __init__(self, parent, bmi):
        # Font
        font = ctk.CTkFont(
            family=settings.FONT,
            size=settings.MAIN_TEXT_SIZE,
            weight="bold",
        )
        super().__init__(
            master=parent,
            text="22.5",
            font=font,
            text_color=settings.WHITE,
            textvariable=bmi,
        )

        # Place
        self.grid(column=0, row=0, rowspan=2, sticky="nsew")


class WeightInput(ctk.CTkFrame):
    def __init__(self, parent, weight, is_metric_unit):
        super().__init__(master=parent, fg_color=settings.WHITE)

        self.is_metric_unit = is_metric_unit
        self.weight = weight

        # Place
        self.grid(column=0, row=2, sticky="nsew", padx=10, pady=10)

        # Layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform="a")
        self.columnconfigure(1, weight=1, uniform="a")
        self.columnconfigure(2, weight=3, uniform="a")
        self.columnconfigure(3, weight=1, uniform="a")
        self.columnconfigure(4, weight=2, uniform="a")

        # Font
        font = ctk.CTkFont(family=settings.FONT, size=settings.INPUT_FONT_SIZE)

        # Text
        self.output = ctk.StringVar(value=f"{INITIAL_WEIGHT}kg")
        self.update_weight()
        label = ctk.CTkLabel(
            self,
            textvariable=self.output,
            text_color=settings.BLACK,
            font=font,
        )
        label.grid(row=0, column=2, sticky="nsew")

        # Buttons
        minus_button = ctk.CTkButton(
            self,
            text="-",
            font=font,
            text_color=settings.BLACK,
            fg_color=settings.LIGHT_GRAY,
            hover_color=settings.GRAY,
            corner_radius=settings.CORNER_RADIUS,
            command=lambda: self.update_weight(("minus", "large")),
        )
        minus_button.grid(row=0, column=0, sticky="ns", padx=8, pady=8)

        small_minus_button = ctk.CTkButton(
            self,
            text="-",
            font=font,
            text_color=settings.BLACK,
            fg_color=settings.LIGHT_GRAY,
            hover_color=settings.GRAY,
            corner_radius=settings.CORNER_RADIUS,
            command=lambda: self.update_weight(("minus", "small")),
        )
        small_minus_button.grid(row=0, column=1, padx=4, pady=4)

        plus_button = ctk.CTkButton(
            self,
            text="+",
            font=font,
            text_color=settings.BLACK,
            fg_color=settings.LIGHT_GRAY,
            hover_color=settings.GRAY,
            corner_radius=settings.CORNER_RADIUS,
            command=lambda: self.update_weight(("plus", "large")),
        )
        plus_button.grid(row=0, column=4, sticky="ns", padx=8, pady=8)

        small_plus_button = ctk.CTkButton(
            self,
            text="+",
            font=font,
            text_color=settings.BLACK,
            fg_color=settings.LIGHT_GRAY,
            hover_color=settings.GRAY,
            corner_radius=settings.CORNER_RADIUS,
            command=lambda: self.update_weight(("plus", "small")),
        )
        small_plus_button.grid(row=0, column=3, padx=4, pady=4)

    def update_weight(self, info=None):
        if info:
            if self.is_metric_unit.get():
                amount = 1 if info[1] == "large" else 0.1
            else:
                amount = 0.453592 if info[1] == "large" else 0.453592 / 16

            if info[0] == "plus":
                self.weight.set(self.weight.get() + amount)
            else:
                self.weight.set(self.weight.get() - amount)

        if self.is_metric_unit.get():
            self.output.set(f"{round(self.weight.get(), 1)}kg")
        else:
            raw_ounces = self.weight.get() * 35.274
            pounds, ounces = divmod(raw_ounces, 16)
            self.output.set(f"{int(pounds)}lb {int(ounces)}oz")


class HeightInput(
    ctk.CTkFrame,
):
    def __init__(self, parent, height, is_metric_unit):
        super().__init__(master=parent, fg_color=settings.WHITE)

        self.is_metric_unit = is_metric_unit

        # Place
        self.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

        # Widgets
        slider = ctk.CTkSlider(
            self,
            button_color=settings.GREEN,
            button_hover_color=settings.GRAY,
            progress_color=settings.GREEN,
            fg_color=settings.LIGHT_GRAY,
            variable=height,
            from_=100,
            to=250,
            command=self.update_text,
        )
        slider.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        self.output = ctk.StringVar(value=f"{round(INITIAL_HEIGHT / 100, 2)}m")

        output_text = ctk.CTkLabel(
            self,
            textvariable=self.output,
            text_color=settings.BLACK,
            font=ctk.CTkFont(family=settings.FONT, size=settings.INPUT_FONT_SIZE),
        )
        output_text.pack(side="left", fill="x", expand=True, padx=10, pady=10)

    def update_text(self, amount):
        if self.is_metric_unit.get():
            meters = round(int(amount) / 100, 2)
            self.output.set(f"{meters}m")
        else:
            feet, inches = divmod(amount / 2.54, 12)
            self.output.set(f"{int(feet)}'{round(inches)}''")


class UnitSwitcher(ctk.CTkLabel):
    def __init__(self, parent, is_metric_unit):
        super().__init__(
            master=parent,
            text="metric",
            font=ctk.CTkFont(
                family=settings.FONT, size=settings.SWITCH_FONT_SIZE, weight="bold"
            ),
            fg_color=settings.GREEN,
            text_color=settings.DARK_GREEN,
        )

        self.is_metric_unit = is_metric_unit
        self.bind("<Button>", self.change_units)

        # Place
        self.place(relx=0.98, rely=0.01, anchor="ne")

    def change_units(self, event):
        self.is_metric_unit.set(not self.is_metric_unit.get())

        if self.is_metric_unit.get():
            self.configure(text="metric")
        else:
            self.configure(text="imperial")


if __name__ == "__main__":
    App()

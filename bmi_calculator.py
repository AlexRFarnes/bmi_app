# bmi_calculator.py

# try:
import customtkinter as ctk

import settings

try:
    from ctypes import byref, c_int, sizeof, windll
except Exception:
    pass


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
        self.height = ctk.IntVar(value=170)
        self.weight = ctk.DoubleVar(value=65)
        self.bmi = ctk.StringVar()
        self.update_bmi()

        # Tracing
        self.height.trace("w", self.update_bmi)
        self.weight.trace("w", self.update_bmi)

        # Widgets
        ResultText(self, self.bmi)
        HeightInput(self, self.height)
        WeightInput(self, self.weight)
        UnitSwitcher(self)

        # Main loop
        self.mainloop()

    def update_bmi(self, *args):
        height_meter = self.height.get() / 100
        weight_kg = self.weight.get()
        bmi = round(weight_kg / (height_meter * height_meter), 2)
        self.bmi.set(str(bmi))

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
    def __init__(self, parent, weight):
        super().__init__(master=parent, fg_color=settings.WHITE)

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
        label = ctk.CTkLabel(self, text="70kg", text_color=settings.BLACK, font=font)
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
        amount = 1 if info[1] == "large" else 0.1
        if info[0] == "plus":
            self.weight.set(self.weight.get() + amount)
        else:
            self.weight.set(self.weight.get() - amount)


class HeightInput(
    ctk.CTkFrame,
):
    def __init__(self, parent, height):
        super().__init__(master=parent, fg_color=settings.WHITE)

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
        )
        slider.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        output_text = ctk.CTkLabel(
            self,
            text="1.7m",
            text_color=settings.BLACK,
            font=ctk.CTkFont(family=settings.FONT, size=settings.INPUT_FONT_SIZE),
        )
        output_text.pack(side="left", fill="x", expand=True, padx=10, pady=10)


class UnitSwitcher(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(
            master=parent,
            text="metric",
            font=ctk.CTkFont(
                family=settings.FONT, size=settings.SWITCH_FONT_SIZE, weight="bold"
            ),
            fg_color=settings.GREEN,
            text_color=settings.DARK_GREEN,
        )

        # Place
        self.place(relx=0.98, rely=0.01, anchor="ne")


if __name__ == "__main__":
    App()

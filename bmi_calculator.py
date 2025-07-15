# bmi_calculator.py

# try:
import customtkinter as ctk

import settings

try:
    from ctypes import byref, c_int, sizeof, windll
except:
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

        # Widgets
        ResultText(self)
        WeightInput(self)

        # Main loop
        self.mainloop()

    def change_title_bar_color(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(
                HWND, 35, byref(c_int(settings.TITLE_HEX_COLORS)), sizeof(c_int)
            )
        except:
            pass


class ResultText(ctk.CTkLabel):
    def __init__(self, parent):
        # Font
        font = ctk.CTkFont(
            family=settings.FONT,
            size=settings.MAIN_TEXT_SIZE,
            weight="bold",
        )
        super().__init__(
            master=parent, text="22.5", font=font, text_color=settings.WHITE
        )

        # Place
        self.grid(column=0, row=0, rowspan=2, sticky="nsew")


class WeightInput(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=settings.WHITE)

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
        )
        small_plus_button.grid(row=0, column=3, padx=4, pady=4)


if __name__ == "__main__":
    App()

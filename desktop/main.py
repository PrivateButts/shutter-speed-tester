import flet as ft
from serial.tools import list_ports


class SerialPortSelector(ft.UserControl):
    dropdown: ft.Dropdown
    refresh_button: ft.IconButton
    manual_button: ft.IconButton
    connect_button: ft.ElevatedButton
    dropdown_row: ft.Row
    manual_row: ft.Row
    manual: bool = False

    def build(self):
        self.manual_entry = ft.TextField(
            label="Enter Serial Port", hint_text="/dev/ttyUSB0 or COM3", expand=True
        )
        self.dropdown = ft.Dropdown(expand=True)
        self.refresh_button = ft.IconButton(
            icon=ft.icons.REFRESH_OUTLINED,
            icon_color="blue400",
            icon_size=20,
            tooltip="Refresh Serial Ports",
            on_click=self.refresh_serial_ports,
        )
        self.show_manual_btn = ft.IconButton(
            icon=ft.icons.EDIT,
            icon_color="yellow400",
            icon_size=20,
            tooltip="Enter Serial Port Manually",
            on_click=self.show_manual_selector,
        )
        self.hide_manual_btn = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            icon_color="yellow400",
            icon_size=20,
            tooltip="Return to Serial Port List",
            on_click=self.hide_manual_selector,
        )
        self.connect_button = ft.ElevatedButton(
            "Connect", on_click=self.connect, expand=True
        )
        self.dropdown_row = ft.Row(
            [
                self.dropdown,
                self.refresh_button,
                self.show_manual_btn,
            ],
            visible=not self.manual,
        )
        self.manual_row = ft.Row(
            [
                self.manual_entry,
                self.hide_manual_btn,
            ],
            visible=self.manual,
        )
        return ft.Column(
            [self.dropdown_row, self.manual_row, ft.Row([self.connect_button])]
        )

    def refresh_serial_ports(self, event):
        for port in list_ports.comports():
            print(port)
            self.dropdown.options.clear()
            self.dropdown.options.append(
                ft.dropdown.Option(
                    key=port.device, text=f"{port.device}: {port.product}"
                )
            )
        self.update()

    def show_manual_selector(self, event):
        self.dropdown_row.visible = False
        self.manual_row.visible = True
        self.update()

    def hide_manual_selector(self, event):
        self.dropdown_row.visible = True
        self.manual_row.visible = False
        self.update()

    def connect(self, event):
        pass


def main(page: ft.Page):
    page.title = "Shutter Speed Tester"
    page.add(
        SerialPortSelector(),
    )


if __name__ == "__main__":
    ft.app(target=main)

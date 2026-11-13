"""Launch GATUZ with its bundled SVG brand mark rendered in the Tk UI."""

import base64
import os
import sys
import tkinter as tk

import cairosvg
import app as base_app


def _asset_path(name):
    root = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, "assets", name)


def _logo_image(size):
    """Convert the committed SVG to a Tk-compatible PNG in memory."""
    png = cairosvg.svg2png(url=_asset_path("gatuz_logo.svg"),
                           output_width=size, output_height=size)
    return tk.PhotoImage(data=base64.b64encode(png).decode("ascii"), format="png")


def _install_logo_hooks():
    original_login = base_app.GatuzApp.login_screen
    original_main = base_app.GatuzApp.main_screen

    def login_screen(self):
        original_login(self)
        frame = self.root.winfo_children()[0]
        try:
            image = _logo_image(148)
        except Exception as exc:
            # Keep login available even if SVG rendering fails on a machine.
            print(f"GATUZ logo could not be loaded: {exc}", file=sys.stderr)
            return
        self._gatuz_login_logo = image  # Tk images must remain referenced.
        tk.Label(frame, image=image, bg=frame.cget("bg"), bd=0).pack(
            before=frame.winfo_children()[0], pady=(0, 12))

    def main_screen(self):
        original_main(self)
        side = self.shell.winfo_children()[0]
        try:
            image = _logo_image(78)
        except Exception as exc:
            print(f"GATUZ logo could not be loaded: {exc}", file=sys.stderr)
            return
        self._gatuz_sidebar_logo = image
        tk.Label(side, image=image, bg=side.cget("bg"), bd=0).pack(
            before=side.winfo_children()[0], pady=(12, 4))

    base_app.GatuzApp.login_screen = login_screen
    base_app.GatuzApp.main_screen = main_screen


_install_logo_hooks()

if __name__ == "__main__":
    import dashboard_app

    root = tk.Tk()
    dashboard_app.FriendlyGatuzApp(root)
    root.mainloop()

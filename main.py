import argparse


def run_window_app():
    import tkinter as tk
    from ui.app import AquaExpertApp

    root = tk.Tk()
    AquaExpertApp(root)
    root.mainloop()


def run_web_app(host, port, debug):
    from ui.web_app import run_web_app as start_web_app

    start_web_app(host=host, port=port, debug=debug)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the Aquaculture Expert System as a desktop or web app."
    )
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["window", "web"],
        default="window",
        help="UI mode to start. Defaults to window.",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host for web mode. Defaults to 127.0.0.1.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port for web mode. Defaults to 5000.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable Flask debug mode in web mode.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.mode == "web":
        run_web_app(host=args.host, port=args.port, debug=args.debug)
    else:
        run_window_app()

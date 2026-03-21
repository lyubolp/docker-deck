import random
from pathlib import Path

from nicegui import app, ui

from docker_deck.data_gather import get_running_containers

BACKGROUND_DIR = Path(__file__).parent / "background_images"
app.add_static_files("/background_images", str(BACKGROUND_DIR))

BACKGROUND_IMAGES = [
    f.name
    for f in BACKGROUND_DIR.iterdir()
    if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
]

GLASS_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@200&display=swap" rel="stylesheet">
<style>
    body, .q-page, * {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 300 !important;
    }
    body, .q-page {
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        min-height: 100vh;
    }
    .nicegui-content {
        background: transparent !important;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.07) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45) !important;
        color: rgba(255, 255, 255, 0.9) !important;
    }
    .glass-card .q-card__section {
        background: transparent !important;
    }
</style>
"""


@ui.refreshable
def main_ui():
    dark = ui.dark_mode()
    dark.enable()

    if BACKGROUND_IMAGES:
        chosen = random.choice(BACKGROUND_IMAGES)
        ui.query("body").style(f"background-image: url('/background_images/{chosen}')")

    containers = get_running_containers()

    with ui.column().classes("items-center justify-center w-full"):
        with ui.card(align_items="center").classes("glass-card"):
            ui.label("Docker Deck").classes("text-h3 mb-6")
        with (
            ui.grid()
            .classes("w-full gap-4")
            .style("grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))")
        ):
            for container in containers:
                with ui.card(align_items="center").classes("glass-card"):
                    ui.label(container.container_name).classes("text-h6")
                    with ui.card_section():
                        with ui.grid(columns=2).classes("w-full"):
                            ui.label("State:").classes("font-bold")
                            button_classes = (
                                "rounded-full py-2 bg-green-900 border-2 border-green-500 text-green-200 w-full text-center"
                                if container.state.value.lower() == "running"
                                else "rounded-full py-2 bg-red-900 border-2 border-red-500 text-red-200 w-full text-center"
                            )
                            ui.label(container.state.value).classes(button_classes)
                            ui.label("Port:").classes("font-bold")
                            ui.label(
                                str(container.port) if container.port != -1 else "N/A"
                            )
                            ui.label("Image:").classes("font-bold")
                            ui.label(container.image)


def update_ui():
    main_ui.refresh()


ui.add_head_html(GLASS_CSS)
main_ui()
# ui.timer(5.0, update_ui)
# ui.run(host="0.0.0.0", port=80)
ui.run(favicon="icon.png")

from nicegui import ui

from docker_deck.data_gather import get_running_containers


dark = ui.dark_mode()
dark.enable()


containers = get_running_containers()


with ui.column().classes("items-center justify-center min-w-screen"):
    ui.label("Docker Deck").classes("text-h3 mb-6")
    with ui.grid(columns=3).classes("items-center mb-4"):
        for container in containers:
            with ui.card().tight():
                ui.label(container.container_name).classes("text-h6")
                with ui.card_section():
                    with ui.grid(columns=2):
                        ui.label("State:").classes("font-bold")
                        state_color = (
                            "text-green-600" if container.state.value.lower() == "running" else "text-red-600"
                        )
                        ui.label(container.state.value).classes(state_color)
                        ui.label("Port:").classes("font-bold")
                        ui.label(str(container.port) if container.port != -1 else "N/A")
                        ui.label("Image:").classes("font-bold")
                        ui.label(container.image)


ui.run()

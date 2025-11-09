import json
from socketify import App

from anifeed.api.controllers.health_controller import HealthController


def register(app: App, controller: HealthController | None = None) -> None:
    """
    Register a simple health endpoint on the provided Socketify application.
    """
    controller = controller or HealthController()

    def get_health(res, req):
        if res.aborted:
            return

        payload = json.dumps(controller.status())
        res.end(payload)
        
    app.get("/health", get_health)

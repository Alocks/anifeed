class HealthController:
    """
    Simple health-check controller.
    """

    def status(self) -> dict[str, str]:
        """
        Return service health information.
        """
        return {"health": True}

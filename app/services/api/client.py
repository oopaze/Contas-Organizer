from .resources import RESOURCES
from app.src import settings


class Client:
    _resources = []

    def __init__(
        self,
        token=settings.API_KEY,
        api_root_url=settings.API_URL,
        timeout=3,
    ):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        self.api_root_url = api_root_url
        self.timeout = timeout
        self.token = token

        self.add_resources()

    def get_resource_list(self):
        return self._resources

    def add_resource(self, resource_name, resource_class):
        resource_instance = resource_class(
            headers=self.headers, base_url=self.api_root_url
        )
        resource_instance.generate_action_methods()

        self._resources.append(resource_name)

        setattr(self, resource_name, resource_instance)

    def add_resources(self, resources=RESOURCES):
        for method_name, resource_class in resources:
            self.add_resource(resource_name=method_name, resource_class=resource_class)

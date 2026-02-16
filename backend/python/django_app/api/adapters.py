from ..core.domain import GreetingService

class GreetingAdapter:
    def __init__(self):
        self.service = GreetingService()

    def execute_logic(self, request_params):
        name = request_params.get("name", "Guest")
        lang = request_params.get("lang", "en")
        
        message = self.service.generate_message(name, lang)
        return {"greeting": message}
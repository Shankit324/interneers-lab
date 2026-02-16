class GreetingService:
    def generate_message(self, name: str, language: str) -> str:
        if language == "es":
            return f"Hola, {name}!"
        return f"Hello, {name}!"

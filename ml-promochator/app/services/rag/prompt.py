
class Prompt:
    def __init__(self, template: str, text: str):
        self.prompt = template.format(question=text.text)
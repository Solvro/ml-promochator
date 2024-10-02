
class Prompt:
    def __init__(self, template: str, text: str):
        self.template = self._read_template_from_csv(template)
        self.prompt = self.template.format(question=text.text)
    
    def _read_template_from_csv(filename: str) -> str:
        with open(filename, 'r') as file:
            template = file.read()
        return template
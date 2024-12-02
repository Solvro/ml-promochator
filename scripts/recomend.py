import fire

from src.components.chains import qa_chain
from src.components.prompts import PROMPT_TEMPLATE


def main(
    question: str = "Who should I pick as supervisor for my thesis 'Train Rescheduling and Track Closure Optimization'",
):
    formatted_prompt = PROMPT_TEMPLATE.format(question=question)
    print(qa_chain.invoke(formatted_prompt).as_str)


if __name__ == "__main__":
    fire.Fire(main)

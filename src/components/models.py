from typing import Optional

from pydantic import BaseModel, Field


class Paper(BaseModel):
    title: str = Field(..., title="Title of the paper related to user's thesis")
    description: str = Field(default='', title='Short description (2-3 sentences) of the paper')

    @property
    def as_str(self) -> str:
        return f'### {self.title}\n\n{self.description}'.strip()


class Thesis(BaseModel):
    title: str = Field(..., title="Title of former thesis related to user's thesis")
    description: str = Field(default='', title='Short description (2-3 sentences) of the thesis')

    @property
    def as_str(self) -> str:
        return f'### {self.title}\n\n{self.description}'.strip()


class RecommendedSupervisor(BaseModel):
    name: str = Field(..., title='Name of the recommended Supervisor')
    faculty: str = Field(..., title='Faculty of the recommended Supervisor')
    papers: list[Paper] = Field(
        default_factory=list,
        title="Supervisor's papers that are releated to user's thesis",
    )
    theses: list[Thesis] = Field(
        default_factory=list,
        title="Previous supervisor's theses that are releated to user's thesis",
    )

    @property
    def as_str(self) -> str:
        papers = '\n\n'.join(f'### {paper.title}\n\n{paper.description}' for paper in self.papers or [])
        theses = '\n\n'.join(f'### {thesis.title}\n\n{thesis.description}' for thesis in self.theses or [])

        return f'## {self.name}, {self.faculty}\n\n{papers}\n\n{theses}'.strip()


class Recommendation(BaseModel):
    hello_message: str = Field(..., title='Hello message')
    recommended_supervisors: list[RecommendedSupervisor] = Field(
        default_factory=list, title='Recommended supervisors fo user thesis'
    )

    @property
    def as_str(self) -> str:
        supervisors = '\n\n'.join(supervisor.as_str for supervisor in self.recommended_supervisors)
        return f'# {self.hello_message}\n\n{supervisors}'.strip()


class InputRecommendationGeneration(BaseModel):
    question: str = Field(..., title='Question about supervisor for a thesis')
    faculty: Optional[str] = Field(None, title='Faculty of supervisor for the thesis')


if __name__ == '__main__':
    from src.components.llms import chat_llm
    from src.components.prompts import PROMPT_TEMPLATE

    recommender = chat_llm.with_structured_output(Recommendation)
    recom = recommender.invoke(PROMPT_TEMPLATE.format(question='Deep Generative Models'))
    print(recom)
    print(recom.as_str)

from pydantic import BaseModel, Field
from typing import Optional


class Paper(BaseModel):
    """
    Represents a research paper related to the user's thesis.
    """
    title: str = Field(..., title="Title of the paper related to user's thesis")
    description: str = Field(
        default="", title="Short description (2-3 sentences) of the paper"
    )

    @property
    def as_str(self) -> str:
        """
        Returns a formatted string representation of the paper.

        Returns:
            str (str): Formatted string representatation
        """
        return f"### {self.title}\n\n{self.description}".strip()


class Thesis(BaseModel):
    """
    Represents a former thesis related to the user's topic.
    """
    title: str = Field(..., title="Title of former thesis related to user's thesis")
    description: str = Field(
        default="", title="Short description (2-3 sentences) of the thesis"
    )

    @property
    def as_str(self) -> str:
        """
        Returns a formatted string representation of the thesis.

        Returns:
            str (str): Formatted string representatation
        """
        
        return f"### {self.title}\n\n{self.description}".strip()


class RecommendedSupervisor(BaseModel):
    """
    Represents a recommended supervisor along with relevant papers and theses.
    """
    name: str = Field(..., title="Name of the recommended Supervisor")
    faculty: str = Field(..., title="Faculty of the recommended Supervisor")
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
        """
        Returns a formatted string representation of the recommended supervisor.

        Returns:
            str (str): Formatted string representatation
        """
        papers = "\n\n".join(
            f"### {paper.title}\n\n{paper.description}" for paper in self.papers or []
        )
        theses = "\n\n".join(
            f"### {thesis.title}\n\n{thesis.description}"
            for thesis in self.theses or []
        )

        return f"## {self.name}, {self.faculty}\n\n{papers}\n\n{theses}".strip()


class Recommendation(BaseModel):
    """
    Represents a complete recommendation including a greeting message and a list of recommended supervisors.
    """
    hello_message: str = Field(..., title="Hello message")
    recommended_supervisors: list[RecommendedSupervisor] = Field(
        default_factory=list, title="Recommended supervisors fo user thesis"
    )

    @property
    def as_str(self) -> str:
        """
        Returns a formatted string representation of the recommendation.
        
        Returns:
            str (str): Formatted string representatation
        """
        supervisors = "\n\n".join(
            supervisor.as_str for supervisor in self.recommended_supervisors
        )
        return f"# {self.hello_message}\n\n{supervisors}".strip()


class InputRecommendationGeneration(BaseModel):
    """
    Represents the input structure for generating a supervisor recommendation.
    """
    question: str = Field(..., title="Question anout supervisor for a thesis")
    faculty: Optional[str] = Field(None, title="Faculty of supervisor for the thesis")


if __name__ == "__main__":
    from src.components.llms import chat_llm
    from src.components.prompts import PROMPT_TEMPLATE

    recommender = chat_llm.with_structured_output(Recommendation)
    recom = recommender.invoke(
        PROMPT_TEMPLATE.format(question="Deep Generative Models")
    )
    print(recom)
    print(recom.as_str)

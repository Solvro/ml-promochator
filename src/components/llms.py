from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.runnables import ConfigurableField

from src.components.models import Recommendation

from dotenv import load_dotenv


load_dotenv()

llm_openai = OpenAI(temperature=0.2)

llm = llm_openai.configurable_alternatives(
    ConfigurableField(id="llm"), default_key="openai"
)

chat_llm = ChatOpenAI(model="gpt-4o-mini")

chat_llm = chat_llm.with_structured_output(Recommendation)

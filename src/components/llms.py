from langchain_openai import OpenAI
from langchain_core.runnables import ConfigurableField
from dotenv import load_dotenv


load_dotenv()

llm_openai = OpenAI(temperature=0.2)

llm = llm_openai.configurable_alternatives(
    ConfigurableField(id="llm"), default_key="openai"
)

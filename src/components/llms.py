from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI, OpenAI

from src.components.constants import OPEN_AI_API_KEY
from src.components.models import Recommendation

llm_openai = OpenAI(temperature=0.2, api_key=OPEN_AI_API_KEY)

llm = llm_openai.configurable_alternatives(ConfigurableField(id='llm'), default_key='openai')

chat_llm = ChatOpenAI(model='gpt-4o-mini', api_key=OPEN_AI_API_KEY, temperature=0.3, max_tokens=5000)
chat_llm_with_structured = chat_llm.with_structured_output(Recommendation)

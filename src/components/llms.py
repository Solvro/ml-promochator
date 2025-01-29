from dotenv import load_dotenv
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI, OpenAI

load_dotenv()

llm_openai = OpenAI(temperature=0.2)

llm = llm_openai.configurable_alternatives(ConfigurableField(id='llm'), default_key='openai')

chat_llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.3, max_tokens=3000)
# chat_llm = chat_llm.with_structured_output(Recommendation)

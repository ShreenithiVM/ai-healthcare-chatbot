from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.agents import create_structured_chat_agent, AgentExecutor
from dotenv import load_dotenv
from utils.prompts import medbot_react_message
from utils.tools import python_tool, create_tool, update_tool, fetch_tool, delete_tool

load_dotenv()

prompt = ChatPromptTemplate.from_messages(medbot_react_message)

memory = ConversationBufferMemory(memory_key="history", return_messages=True)


# Define the LLM 
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_retries=3,
)

# Define tools
tools = [create_tool, fetch_tool, update_tool, delete_tool, python_tool]

agent = create_structured_chat_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

agent_chain = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
)

def run_agent(input_text):

    response = agent_chain.invoke({"user_message" : input_text})
    return response["output"]



if __name__ == "__main__":
    print(run_agent("can you get me the appointments with shivani?"))
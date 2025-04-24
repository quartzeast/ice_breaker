from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType

from tools.tools import get_profile_url_tavily


def lookup(name: str) -> str:
    """
    Given a person's full name, return their LinkedIn profile URL
    """
    llm = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0)

    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
    Your answer should contain only a URL"""
    prompt = PromptTemplate.from_template(template)

    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkedin Page URL",
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    query = prompt.format(name_of_person=name)
    result = agent.invoke({"input": query})

    linked_profile_url = result["output"]
    return linked_profile_url


if __name__ == "__main__":
    print(lookup("Eden Marco Udemy"))

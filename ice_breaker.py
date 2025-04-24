from typing import Tuple
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chat_models import init_chat_model

from output_parsers import summary_parser, Summary
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from third_parties.twitter import scrape_user_tweets


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_user_profile_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_user_profile_url,
        scrapin=False,
        mock=False,
    )

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username, mock=True)

    summary_template = """
    given the information about a person from linkedin {information},
    and their latest twitter posts {twitter_posts} I want you to create:
    1. A short summary
    2. two interesting facts about them 

    Use both information from twitter and Linkedin
    \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate.from_template(
        summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions(),
        },
    )

    llm = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0)

    chain = summary_prompt_template | llm | summary_parser

    res = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})

    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    load_dotenv()

    print("Hello LangChain")
    ice_break_with(name="Eden Marco udemy")

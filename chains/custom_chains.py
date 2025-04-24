from langchain.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableSequence

from output_parsers import summary_parser, ice_breaker_parser, topics_of_interest_parser

llm = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0)
llm_creative = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=1)


def get_summary_chain() -> RunnableSequence:
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

    return summary_prompt_template | llm | summary_parser


def get_interests_chain() -> RunnableSequence:
    interesting_facts_template = """
        given the information about a person from linkedin {information}, and twitter posts {twitter_posts} I want you to create:
        3 topics that might interest them
        
        Use both information from twitter and Linkedin
        \n{format_instructions}
    """

    interesting_facts_prompt_template = PromptTemplate.from_template(
        interesting_facts_template,
        partial_variables={
            "format_instructions": topics_of_interest_parser.get_format_instructions(),
        },
    )

    return interesting_facts_prompt_template | llm_creative | topics_of_interest_parser


def get_ice_breaker_chain() -> RunnableSequence:
    ice_breaker_template = """
        given the information about a person from linkedin {information}, and twitter posts {twitter_posts} I want you to create:
        2 creative Ice breakers with them that are derived from their activity on Linkedin and twitter, preferably on latest tweets
        \n{format_instructions}
    """

    ice_breaker_prompt_template = PromptTemplate.from_template(
        ice_breaker_template,
        partial_variables={
            "format_instructions": ice_breaker_parser.get_format_instructions(),
        },
    )

    return ice_breaker_prompt_template | llm_creative | ice_breaker_parser

import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(
    linkedin_profile_url: str, scrapin: bool = True, mock: bool = False
):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    # 1. 获取原始响应
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/32f3c85b9513994c572613f2c8b376b633bfc43f/eden-marco-scrapin.json"
        response = requests.get(linkedin_profile_url, timeout=10)
        raw_data = response.json()
        # 和 scrapin 保持一致，从顶级对象获取 person 字段
        raw_data = raw_data.get("person", raw_data)
    elif scrapin:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl": linkedin_profile_url,
        }
        response = requests.get(api_endpoint, params=params, timeout=10)
        raw_data = response.json().get("person")
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint, params={"url": linkedin_profile_url}, headers=header_dic
        )
        raw_data = response.json()

    # 2. 根据不同情况处理数据
    if mock or scrapin:
        # mock 和 scrapin 共享相同的处理逻辑
        data = {
            k: v
            for k, v in raw_data.items()
            if v not in ([], "", "", None) and k not in ["certifications"]
        }
    else:
        # proxycurl 保持原有处理逻辑
        data = {
            k: v
            for k, v in raw_data.items()
            if v not in ([], "", "", None)
            and k not in ["people_also_viewed", "certifications"]
        }
        if data.get("groups"):
            for group_dict in data.get("groups"):
                group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/eden-marco/",
            scrapin=True,
            mock=True,
        ),
    )

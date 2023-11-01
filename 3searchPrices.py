import json
from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import Html2TextTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_extraction_chain
from langchain.schema import SystemMessage, HumanMessage
from langchain.chat_models import ChatOpenAI
import requests
import re

from utils import *


INDUSTRY_KEYWORD = os.environ.get('INDUSTRY_KEYWORD')
WHOISJSONAPI= os.environ.get('WHOISJSONAPI')

COMPAREPRICES= os.environ.get('COMPAREPRICES')

data_folder = f"data/{INDUSTRY_KEYWORD}"


def load_data_without(filename):
    return {domain: info for domain, info in load_from_json_file(filename,data_folder).items()}


def finde_link_toplans(serp):


    chat = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    messages = [
        SystemMessage(content="Find the link to page with prices and plans. Return only one url starts with 'https://' or 'Not found'"),
        HumanMessage(content=serp)
    ]

    try:
        response = chat(messages)
        return response.content
        

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Define paths and filenames
    
    
    
    # Load data

    data = load_from_json_file("1companies.json","data/"+INDUSTRY_KEYWORD)
    #filter only data with nature=single project
    data = {k:v for k,v in data.items() if v['nature']=='single project' and 'priceAndPlansCrawled' not in v and k == 'www.complycube.com'}


    print(len(data))
    # Iterate through the data dictionary
    for domain, domain_data in data.items():
         
        print("\n\n"+domain)

        organic_results = search_companies_on_google("site:"+domain+' intitle:(pricing or price & plans or prices) ', 10)
        
        serp_content = ""
        for result in organic_results:
            if "snippet" not in result:
                result["snippet"] = ""
            serp_content += (str(result["position"]) + ". link: " +  result["link"]+ " , text: " + result["title"] + " " + result["snippet"])
        
        if (len(organic_results) == 1):
            plans_url = organic_results[0]['link']
            plans_url_cached = organic_results[0]['cached_page_link']
        elif (len(organic_results) > 1):
            plans_url = finde_link_toplans(serp_content)
        else:
            plans_url = 'Not found'
        
        if "Not found" in plans_url:
            data[domain]["priceAndPlansCrawled"] = 'Not found'
        elif "https://" in plans_url:
            
            plans_url=correct_url(plans_url)
            data[domain]["priceAndPlansCrawled"] = plans_url
            data[domain]["priceAndPlansCached"] = plans_url_cached
            print ("Crawl "+plans_url)
            summary = extract_content(plans_url)
            details = load_from_json_file(domain+".json",data_folder)
            details["priceAndPlans"] = summary['text_content']
            save_to_json_file(details, domain+".json",data_folder)
        
        save_to_json_file(data, "1companies.json",data_folder)

        
        
        

if __name__ == "__main__":
    main()
    print("next:  5")
import helpers
from typing import List
from decouple import config
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


class GenerationManager:
    '''
    - Scrape webpage -> cleaned webpage DONE
    - Generate JSON from scrapped webpage -> data json DONE
    - Generate email -> email generated with potfolio data and json data
    '''
    def __init__(self) -> None:
        self.client = ChatGroq(temperature=0, 
                            groq_api_key=config(option='GROQ_API_KEY', cast=str), 
                            model_name=config(option='MODEL_NAME', cast=str)
                            )    
        
    def scrape(self, url:str) -> str:
        loader = WebBaseLoader(web_path=url)
        content = loader.load().pop().page_content
        content = helpers.clean_text(content)
        return content
    
    def generate_json(self, content):
        prompt = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {content}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain = prompt | self.client
        reponse = chain.invoke(input={"content": content})
        try:
            json_parser = JsonOutputParser()
            reponse = json_parser.parse(reponse.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return reponse

    def generate_demo_email(self, job_description:str, services:str):
        # We have the data from jd, we need to query chromadb for portfolio
        prompt = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
            
            ### PROVIDED SERVICES:
            {services}

            ### INSTRUCTION:
            Your job is to write a cold email to the client regarding the job mentioned above describing the serives mentioned above
            Do not provide a preamble. 
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt | self.client
        response = chain_email.invoke({"job_description": str(job_description), "services": services})
        return response.content

    def generate_email(self, job_description:str, portfolio_links:List[str]):
        # We have the data from jd, we need to query chromadb for portfolio
        prompt = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
            
            ### INSTRUCTION:
            You are Mohsin, a business development executive at Sora. Sora is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of Sora 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase Sora's portfolio: {portfolio_links}
            Remember you are Mohan, BDE at Sora. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt | self.client
        response = chain_email.invoke({"job_description": str(job_description), "portfolio_links": portfolio_links})
        return response.content

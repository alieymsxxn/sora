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
            The scraped text is from the job post page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            You should verify that the scraped text fullfills following conditions:
            1) The scraped text is adequate enough to extract all the required information mentioned above.
            2) The scraped text is relevant to a job post.
            If these conditions are not fullfiled add a key `success` with value false and if they are fullsilled add a key `success` with value true.
            Fields you should return:
            1) `success`
            2) `role`
            3) `experience`
            4) `skills`
            5) `description`
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain = prompt | self.client
        response = chain.invoke(input={"content": content})
        try:
            json_parser = JsonOutputParser()
            response = json_parser.parse(response.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return response

    def generate_demo_email(self, job_description:str, services:str):
        # We have the data from jd, we need to query chromadb for portfolio
        prompt = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
            
            ### PROVIDED SERVICES:
            {services}

            ### INSTRUCTION:
            Your job is to write a cold email to the client regarding the job mentioned above describing the provided serives mentioned above.
            Your job is to return in JSON format containing the following keys: `success`, `subject` and `body`.
            Provided services text needs to fulfill following conditions:
            1) It should mention services,
            2) It should not be something irrelevant.
            If the provided services text does not fullfill these condtions, value for `success` should be talse and all other keys empty.
            If the provided services text fullfills these conditions, value for `success` should be true and all other keys should have their respective values.
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt | self.client
        response = chain_email.invoke({"job_description": str(job_description), "services": services})
        try:
            json_parser = JsonOutputParser()
            response = json_parser.parse(response.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return response

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

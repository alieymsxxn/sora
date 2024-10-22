from generative.scripts.generation_manager import GenerationManager
from generative.scripts.potfolio_manager import PortfolioManager

class GenerationFacade:
    @classmethod
    def generate_email(cls, url:str, job_description:str=None) -> str:
        generation_manager = GenerationManager()
        if not url and job_description:
            content = job_description
        else:
            content = generation_manager.scrape(url=url)
        job_description = generation_manager.generate_json(content=content)
        portfolio_manager = PortfolioManager()
        portfolio_links = portfolio_manager.retrieve(skills=job_description['skills'])
        generated_email = generation_manager.generate_email(job_description=job_description, portfolio_links=portfolio_links)
        return generated_email
    @classmethod
    def generate_demo_email(cls, url:str, services:str) -> str:
        generation_manager = GenerationManager()
        if not url and job_description:
            content = job_description
        else:
            content = generation_manager.scrape(url=url)
        job_description = generation_manager.generate_json(content=content)
        # portfolio_manager = PortfolioManager()
        # portfolio_links = portfolio_manager.retrieve(skills=job_description['skills'])
        generated_email = generation_manager.generate_demo_email(job_description=job_description, services=services)
        print(generated_email)
        return generated_email

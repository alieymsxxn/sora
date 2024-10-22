import chromadb
import csv



class PortfolioManager:
    '''
    - Initiate Chormadb client DONE
    - Load data inside chromadb DONE
    - Retrieve data from chromadb DONE
    Extras:
    - Handle re-insertion
    - Closing the client
    '''
    def __init__(self) -> None:
        self.__client = chromadb.PersistentClient('/Users/mohsinali/Project/sora/src/generative/resources/chromadb')
        self.collection = self.__client.get_or_create_collection(name="portfolio")
        self.load()

    def load(self) -> bool:
        file_path = '/Users/mohsinali/Project/sora/src/generative/resources/portfolio/my_portfolio.csv'
        with open(file=file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            if not self.collection.count():
                for idx, row in enumerate(csv_reader):
                    self.collection.add(documents=row[0],
                                        metadatas={"links": row[1]},
                                        ids=[str(idx)])
    def retrieve(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
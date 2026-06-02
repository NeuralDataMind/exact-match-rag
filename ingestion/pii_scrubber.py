from langchain_community.document_loaders import UnstructuredMarkdownLoader
import re

MD_DATA_PATH = "./data/MD" 

# Not to complicated easy to understand if u cant. Go back and learn again from Basics 

def pii(text: str) -> str:
    text = re.sub(r"sk_test_[a-zA-Z0-9]+", "[REDACTED_TOKEN]", text)
    text = re.sub(r"api_test_[a-zA-Z0-9]+", "[REDACTED_API_KEY]", text)
    text = re.sub(r"[\w\.-]+@[\w\.-]+", "[REDACTED_EMAIL]", text)
    text = re.sub(r"\+?\d[\d\-() ]{7,}\d", "[REDACTED_PHONE]", text)
    text = re.sub(r"user_\d+", "[REDACTED_USER_ID]", text)

    return text

def load_docs(file_path=None):
    if file_path is None:
        file_path = ['_index.md', 'compose-sdk.md', 'gettingstarted.md', 'trust-model.md']

    docs = []
    
    for file in file_path:
        path = MD_DATA_PATH + "/" + file
        loader = UnstructuredMarkdownLoader(path)
        docs.extend(loader.load())

    return docs


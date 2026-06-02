from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter, Language
from langchain_core.documents import Document
from typing import List

#  Language is the best think i figure out on docs.langchain.com
#  So useful when u need to use multiple splitter to make splitting data.
#  I can also create my own splitter but it is not worth it to wast 3 days of my time. When this work also good.
#  Still u want not satisfy then build by ur self 

def chunk_raw_markdown(docs: List[str]) -> List[Document]:
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False
    )

    size_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.MARKDOWN,
        chunk_size=1500,
        chunk_overlap=200
    )

    final_docs = []

    for doc in docs:
        section_chunks = markdown_splitter.split_text(doc.page_content)
        section_docs = []

        for section in section_chunks:
            section_docs.append(
                Document(
                    page_content=section.page_content,
                    metadata={
                        **doc.metadata,
                        **section.metadata,
                    }
                )
            )
        
        smaller_chunks = size_splitter.split_documents(section_docs)
        final_docs.extend(smaller_chunks)

    return final_docs


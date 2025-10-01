from enum import Enum


class LLMEnums(Enum):

    OPENAI = "OPENAI"
    COHERE = "COHERE"

class OpenAIEnums(Enum):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"

class CohereEnums(Enum):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"
    DOCUMENT = "search_document"
    QUERY = "search_query"

class DocumentType(Enum):
    DOCUMENT = "document"
    QUERY = "query"

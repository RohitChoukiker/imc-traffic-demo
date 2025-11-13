import os
from dotenv import load_dotenv

from services.retrieval import query_data


from langchain_anthropic import ChatAnthropic
from langchain.schema import SystemMessage, HumanMessage, AIMessage

load_dotenv()


class ClaudeClient:
    def __init__(self, model_name="claude-3-opus-20240229"):
        api_key = os.getenv("CLAUDE_API_KEY")
        if not api_key:
            raise ValueError("CLAUDE_API_KEY not set in environment")
        self.client = ChatAnthropic(
            model=model_name,
            anthropic_api_key=api_key
        )

    def generate(self, query, context, max_tokens=512):
    
        messages = [
            SystemMessage(content=(

        #           "You are a helpful AI assistant answering queries from a challan dataset.\n"
        # "Always extract answers ONLY from the provided context.\n"
        # "Understand the user's query carefully and return the answer strictly based on it.\n"
        # "If multiple results match, present them in a Markdown table with columns:\n"
        # "[Challan Number | Vehicle Number | Date | Offence | Amount].\n"
        # "Do not add unrelated information or explanations.\n"
        # "If nothing matches the user's query, reply exactly:\n"
        # "'I cannot find the answer in the available challan records.'"
                "You are a helpful AI assistant answering queries from a challan dataset.\n"
        "Always extract answers ONLY from the provided context.\n"
        "Understand the user's query carefully and return the answer strictly based on it.\n"
        "If multiple results match, present them in a clean Markdown table with only those columns relevant to the user's query.\n"
        "Do not repeat the same table more than once in the response.\n"
        "If you provide additional details, do it only in bullet points without reprinting the table.\n"
        "If nothing matches the user's query, reply exactly:\n"
        "'I cannot find the answer in the available challan records.'"
            )),
            HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}")
        ]

        try:
            response = self.client.invoke(messages, max_tokens=max_tokens)

            if isinstance(response, str):
                return response.strip()

          
            if isinstance(response, AIMessage):
                if isinstance(response.content, list):
                
                    texts = [c.get("text", "") for c in response.content if isinstance(c, dict)]
                    return "\n".join(texts).strip()
                elif isinstance(response.content, str):
                    return response.content.strip()

         
            if hasattr(response, "content"):
                return str(response.content).strip()

            return str(response).strip()

        except Exception as e:
            return f"Error generating response from Claude: {e}"


# Singleton client
_claude_client = None


def get_claude_client():
    global _claude_client
    if _claude_client is None:
        _claude_client = ClaudeClient()
    return _claude_client


def generate_answer_claude(query, top_k=5):
    results = query_data(query, top_k)

    context = ""
    for r in results:
       
        if isinstance(r, dict):
            context += f"Table: {r.get('table', '')}\nData: {r.get('chunk', '')}\n\n"
        else:
       
            context += f"Data: {getattr(r, 'page_content', str(r))}\n\n"

    return get_claude_client().generate(query, context)






















































































































# import os
# from dotenv import load_dotenv

# from services.retrieval import query_data

# from langchain_anthropic import ChatAnthropic
# from langchain.schema import SystemMessage, HumanMessage



# load_dotenv()


# class ClaudeClient:
#     def __init__(self, model_name="claude-3-opus-20240229"):
#         api_key = os.getenv("CLAUDE_API_KEY")   
#         if not api_key:
#             raise ValueError("CLAUDE_API_KEY not set in environment")
#         self.client = ChatAnthropic(
#             model=model_name,
#             anthropic_api_key=api_key            
#         )

#     def generate(self, query, context, max_tokens=512):
#         """Generate response from Claude based on query + retrieved context"""
#         messages = [
#             SystemMessage(content=(
#                  "You are a helpful AI assistant. "
#     "Always answer in a clear and natural way. "
#     "If the question is about totals, calculations, or aggregations, "
#     "decide whether a Markdown table would make the explanation clearer. "
#     "If a simple sentence or bullet points are enough, avoid the table "
#     "and just explain naturally. "
#     "Always explain calculations step by step, but keep the format simple and user-friendly. "
#     "Do not invent data outside the given context. "

#     "You are strictly limited to the Indore challan dataset (challan_data). "
#     "Only use the fields available in the dataset, such as: "
#     "Challan Number, Vehicle Number, Owner Name, Address, Offence Details, "
#     "Offence Location, Date & Time, Fine Amount, Payment Method, "
#     "Vehicle Details (Engine/Chassis/Model), RTO, etc. "

#     "If the required information is not found in the dataset, reply exactly: "
#     "'I cannot find the answer in the available challan records.' "

#     "Always format answers clearly (table, list, or plain text) depending on the question. "
#     "Never provide assumptions, laws, or predictions outside the dataset."
#             )),
#             HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}")
#         ]

#         try:
#             response = self.client.invoke(messages, max_tokens=max_tokens)
#             if isinstance(response, str):
#                 return response.strip()
#             if hasattr(response, "content"):
#                 return response.content.strip()
#             return str(response).strip()
#         except Exception as e:
#             return f" Error generating response from Claude: {e}"


# #
# _claude_client = None


# def get_claude_client():
#     global _claude_client
#     if _claude_client is None:
#         _claude_client = ClaudeClient()
#     return _claude_client


# def generate_answer_claude(query, top_k=5):
#     results = query_data(query, top_k)

#     context = ""
#     for r in results:
#         context += (
#             f"Table: {r.get('table', '')}\n"
#             f"Data: {r['chunk']}\n\n"
#         )

#     return get_claude_client().generate(query, context)




















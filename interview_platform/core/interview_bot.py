from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain 
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class InterviewBot:
    def __init__(self, chat_history=None):
        self.embeddings = OpenAIEmbeddings(openai_api_key="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")
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.3, openai_api_key="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")

        self.vector_store = FAISS.from_texts(['My name is echo'], self.embeddings)
        self.retriever = self.vector_store.as_retriever()

        prompt = ChatPromptTemplate.from_messages([
            ('system', 'Answer the user\'s questions based on the below context:\n\n{context}'),
            MessagesPlaceholder(variable_name='chat_history'),
            ('user', '{input}'),
        ])
        self.document_chain = create_stuff_documents_chain(self.llm, prompt)

        prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation"),
        ])

        self.retriever_chain = create_history_aware_retriever(self.llm, self.retriever, prompt)
        self.retrieval_chain = create_retrieval_chain(self.retriever_chain, self.document_chain)
        
        # 保存對話紀錄
        # Initialize chat_history
        self.chat_history = chat_history if chat_history is not None else [] # chat history
    
    def build_contextual_prompt(self):
        recent_messages = self.chat_history if self.chat_history is not None else []
        context = ' '.join([msg['content'] for msg in recent_messages])

        return context

    def get_response(self, user_input):
        self.chat_history.append({'role' : 'user', 'content' : user_input})
        contextual_prompt = self.build_contextual_prompt()

        response = self.retrieval_chain.invoke({
            'input': user_input,
            'context': contextual_prompt,
            'chat_history': [] #self.chat_history
        })

        self.chat_history.append({'role': 'system', 'content': response['answer']})

        return response['answer']
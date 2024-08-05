from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# ChatOpenAI: 用於與OpenAI的聊天模型進行互動。它提供了一個簡單的界面來發送訊息給模型並獲取回應。
# OpenAIEmbeddings: 用於生成文本的嵌入表示（向量）。嵌入表示是一種將文本轉換為數字向量的方式，這樣可以更容易地進行相似度計算和搜索。
from langchain_community.vectorstores import FAISS
# FAISS: Facebook AI Similarity Search，是一種高效的相似性搜索庫，它專為高維向量相似度搜索而設計，並且能在大型數據集上提供快速和準確的結果。 FAISS 支援多種距離度量，並提供了多種優化的索引結構來實現快速搜索。
from langchain.chains.retrieval import create_retrieval_chain
# create_retrieval_chain: 用於創建一個檢索鏈。檢索鏈是一種流程，根據用戶的查詢從資料庫中檢索相關訊息。
from langchain.chains.history_aware_retriever import create_history_aware_retriever
# create_history_aware_retriever: 創建一個具備歷史記錄感知功能的檢索器，這個檢索器可以考慮對話的歷史記錄來提高檢索結果的相關性。
from langchain.chains.combine_documents import create_stuff_documents_chain 
# create_stuff_documents_chain: 創建一個將多個文件組合成一個完整文件的鏈，這樣可以將多個檢索到的片段結合起來提供給用戶。
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# ChatPromptTemplate: 用於創建聊天提示模板。模板定義了系統如何根據輸入生成回應。
# MessagesPlaceholder: 用於在提示模板中佔位，表示將插入對話歷史等動態內容。

class InterviewBot:
    def __init__(self, chat_history=None):
        # 初始化方法，當創建類的實例時會自動調用
        self.embeddings = OpenAIEmbeddings(openai_api_key="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")
        # 創建OpenAI嵌入的實例，並使用提供的API金鑰進行身份驗證。這將用於生成文本嵌入表示。
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.3, openai_api_key="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")
        # 創建ChatOpenAI的實例，並指定要使用的模型（gpt-4-turbo）和溫度（temperature）。溫度決定了回應的隨機性，較低的溫度會使回應更穩定和可預測。

        self.vector_store = FAISS.from_texts(['My name is echo'], self.embeddings)
        # 使用FAISS創建一個向量儲存庫，並用一個簡單的文本 "My name is echo" 初始化它。這段文本將被轉換為嵌入表示並儲存在向量儲存庫中。
        self.retriever = self.vector_store.as_retriever()
        # 將向量儲存庫轉換為一個檢索器。檢索器可以根據嵌入表示來查找與輸入文本相似的文本。

        prompt = ChatPromptTemplate.from_messages([
            ('system', 'Answer the user\'s questions based on the below context:\n\n{context}'),
            MessagesPlaceholder(variable_name='chat_history'),
            ('user', '{input}'),
        ])
        # 創建一個聊天提示模板，包含系統消息、佔位符消息（用於插入聊天歷史）和用戶消息。這個模板將指導系統如何生成回應。
        self.document_chain = create_stuff_documents_chain(self.llm, prompt)
         # 使用聊天模型和提示模板創建一個文件鏈。文件鏈將多個文件組合成一個完整文件，並生成最終的回答。

        prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation"),
        ])
        # 創建另一個聊天提示模板，這次用於生成檢索查詢。包含聊天歷史佔位符和用戶輸入。

        self.retriever_chain = create_history_aware_retriever(self.llm, self.retriever, prompt)
         # 創建一個具備歷史記錄感知功能的檢索器鏈，這個檢索器鏈將考慮聊天歷史來生成檢索查詢。
        self.retrieval_chain = create_retrieval_chain(self.retriever_chain, self.document_chain)
        # 創建最終的檢索鏈，將檢索器鏈和文件鏈結合起來，實現從檢索到回答的整個過程。
        
        # 保存對話紀錄
        # Initialize chat_history
        self.chat_history = chat_history if chat_history is not None else [] # chat history
        # 初始化聊天歷史。如果未提供聊天歷史，則初始化為空列表。
    
    def build_contextual_prompt(self):
        recent_messages = self.chat_history if self.chat_history is not None else []
        # 獲取最近的聊天歷史消息。如果聊天歷史為空，則初始化為空列表。
        context = ' '.join([msg['content'] for msg in recent_messages])
        # 將最近的聊天歷史消息內容串接成一個單一的上下文字符串。這樣可以將整個對話的上下文提供給系統。

        return context
        # 返回上下文字符串。

    def get_response(self, user_input):
        self.chat_history.append({'role' : 'user', 'content' : user_input})
        # 將用戶輸入添加到聊天歷史。這樣可以記錄用戶的每次輸入。
        contextual_prompt = self.build_contextual_prompt()
        # 構建上下文提示。這將生成一個包含所有最近聊天歷史的上下文字符串。

        response = self.retrieval_chain.invoke({
            'input': user_input,
            'context': contextual_prompt,
            'chat_history': [] #self.chat_history
        })
        # 調用檢索鏈獲取回應。傳入用戶輸入、上下文提示和（目前為空的）聊天歷史。檢索鏈將根據這些訊息生成最終的回答。

        self.chat_history.append({'role': 'system', 'content': response['answer']})
        # 將系統回答添加到聊天歷史。這樣可以記錄系統的每次回應。

        return response['answer']
        # 返回系統的回答。
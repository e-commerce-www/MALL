import openai
from django.conf import settings
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
import os

def initialize_chain():
    
    openai.api_key = settings.OPENAI_API_KEY

    
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    db_uri = f"sqlite:///{db_path}"
    db = SQLDatabase.from_uri(db_uri)


    execute_query = QuerySQLDataBaseTool(db=db)
    write_query = create_sql_query_chain(ChatOpenAI(api_key=settings.OPENAI_API_KEY), db)


    answer_prompt = PromptTemplate.from_template(
        """주어진 유저 질문에 대해서, 해당하는 SQL 쿼리와 SQL 결과를 바탕으로 사용자의 질문에 답변하세요.
        Question: {question}
        SQL Query: {query}
        SQL Result: {result}
        Answer: """
    )

    # 출력 파서 설정 및 체인 설정
    parser = StrOutputParser()
    answer = answer_prompt | ChatOpenAI(api_key=settings.OPENAI_API_KEY) | parser

    chain = (
        RunnablePassthrough.assign(query=write_query).assign(
            result=itemgetter("query") | execute_query
        )
        | answer
    )
    return chain

chain = initialize_chain()

def get_bot_response(user_input):
    input_dict = {"question": user_input}
    response = chain.invoke(input_dict)
    return response


user_input = "가장 최근에 추가된 노래는 무엇인가요?"
response = get_bot_response(user_input)
print(response)
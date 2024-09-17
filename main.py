import streamlit as st
from chains import Chain
from vector_store import Portfolio
from utils import clean_text
from langchain_community.document_loaders import WebBaseLoader



def create_streamlit_app(llm,portfolio, clean_text):
    st.title("Cold Mail Generator") 
    url_input=st.text_input("Enter the URL of the job posting:",value="https://jobs.nike.com/job/R-39209")
    user_name =st.text_input("Enter your name:",value="John Doe")
    submit_button=st.button("Generate Email")
    if submit_button:
       try:
           loader =WebBaseLoader([url_input])
           data=clean_text(loader.load().pop().page_content)
           portfolio.load_portfolio()
           jobs=llm.extract_jobs(data)
           for job in jobs:
               skills=job.get('skills',[])
               links =portfolio.query_links(skills)
               email=llm.write_email(user_name,job,links)
               st.code(email, language='markdown')
       except Exception as e:
           st.error(f"An error occurred: {e}")




if __name__ =="__main__":
    chain=Chain()
    portfolio=Portfolio()
    st.set_page_config(layout="wide",page_title="Cold Email Generator",page_icon="")
    create_streamlit_app(chain,portfolio,clean_text)
    
               
           
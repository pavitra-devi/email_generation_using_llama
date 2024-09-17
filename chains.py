from langchain_groq import ChatGroq
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
import os
import openai
from dotenv import load_dotenv

load_dotenv()



class Chain:
    def __init__(self):
        
        self.llm=ChatGroq(temperature=0,model_name='llama-3.1-70b-versatile',groq_api_key=os.getenv('GROQ_API_KEY'))
        
    def extract_jobs(self, cleaned_text):
        prompt_extract =PromptTemplate.from_template(
        '''
        ### SCRAPED TEXT FROM WEBSITE:
        {pageContent}

        ### INSTRUCTIONS:
        The scraped text is from the career's page of a webiste.
        your job is to extract the job postings and return them in json format containing
        follwing keys: `role`, `experience`, `skills` and `description`
        Only return the valid JSON.
        ###VALID JSON (NO PREAMBLE):

        '''
    )

        chain =prompt_extract|self.llm
        res=chain.invoke(input={'pageContent':cleaned_text})
        print(res.content)
        
        try:
            json_parser = JsonOutputParser()
            res=json_parser.parse(res.content)
            print(res)
        except OutputParserException:
            raise OutputParserException("Content is too big . Unable to parse")
        return res if isinstance(res,list) else [res]

    
    def write_email(self,name,job,links):
        email_prompt = PromptTemplate.from_template(

              '''
              ###JOB DESCRIPTION:
              {job_description}

              ###INSTRUCTIONS:
              you are  a {name} just passed out from college  completed graduationn in the stream of computer science from RGUKT ongole.
              you have done various projects in different tech stacks, you were trying to reach recruiters for different king of job postings.
              your job is write a cold email by emphasizng your skills and expertise to apply for a given job posting,
              Also add the most relevant ones from the following links to showcase your portfolio:{link_list}

              '''

            )
        chain_email = email_prompt|self.llm
        res=chain_email.invoke(input={'name':name,'job_description':str(job),'link_list':links})
        print(res.content)
        return res.content
            

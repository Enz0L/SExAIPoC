#############################
#Author: Enzo LE NAIR       #
#Project Name: SExAI        #
#############################

import fofa
import requests
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

from langchain_core.prompts import (
SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate, ChatPromptTemplate
)

if __name__ == "__main__":
    tab = [['IP','Port']]
    key = '{Add_Your_API_KEY}'  # Input fofa key
    client = fofa.Client(key = key, email = "{PUT_YOUR_LOGIN_HERE}")     # do not forget to use the email from your FOFA account            
    query_str = 'product="SimpleHTTP" && title="for /" && ".bash_history" && "CVE"'  # feel free to modify it! include some CVE id, some tool name...                          
    data = client.search(query_str, size=10, page=1, fields="ip,port") 
    for ip, port in data["results"]:
        #print("%s,%s, %s" % (ip,port))
        tab.append([ip,port])
    print(tab)

    # HTML BODY RETRIEVING
    for pair in tab[1:]:  
        ip, port = pair
        url = f'http://{ip}:{port}'  

        try:
            
            response = requests.get(url, timeout=5)  

            if response.status_code == 200:
                body_content = response.text
                
                # AI settings
                base_url = "http://localhost:11434"
                model = "llama3.2:1b"

                llm = ChatOllama(
                    base_url=base_url,
                    model = "hf.co/AlicanKiraz0/SenecaLLM_x_Qwen2.5-7B-CyberSecurity-Q8_0-GGUF:latest",
                    temperature= 0.6,
                    num_predict=256
                )

                system = SystemMessagePromptTemplate.from_template('You are a cyber security specialist, your main goal is to analyze HTTP HEADERS looking for  hacking tools in open directory webpages, if there is specifics files that seems to be related to hacking (like software,CVE,exploit files, hacking tools). Dress an array please.')
                question = HumanMessagePromptTemplate.from_template('Analyze this HTML Body please: {body}, give me all informaiton about what is contained in this one')
                question
                question.format(body="html body")
                

                messages = [system, question]
                template = ChatPromptTemplate(messages)
                question = template.invoke({'body': body_content})
                response = llm.invoke(question)
                print(response.content)

            else:
                break

        except requests.exceptions.RequestException as e:
            print(f"Error retrieving {ip}:{port}: {e}")






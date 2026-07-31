from dotenv import load_dotenv
load_dotenv()


from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0,
)

response = llm.invoke("Explain LangChain in one sentence.")
print(response.content)
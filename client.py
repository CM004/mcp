import asyncio
from mcp_use import MCPAgent, MCPClient
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
async def main():

    client = MCPClient.from_config_file("database.json")
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    agent = MCPAgent(llm=llm, client=client, memory_enabled=True)
    
    try:
        while True:
            user_input = input("You: ")
            
            if user_input.lower() in ["exit", "quit"]:
                break
            
            if user_input.strip():
                response = await agent.run(user_input)
                print(f"AI: {response}\n")
    finally:
        await client.close_all_sessions()
        
    await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())
  
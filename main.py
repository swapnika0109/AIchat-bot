from visualization.dashboard import Dashboard
from rasa.core.agent import Agent
from rasa.core.utils import EndpointConfig
import asyncio

async def load_rasa_agent():
    # Load agent with minimal configuration
    agent = Agent.load(
        model_path="rasa_bot/models",
        action_endpoint=EndpointConfig(url=""),  # Empty action endpoint
    )
    return agent

def main():
    print("Starting application...")
    dashboard = Dashboard()
    
    try:
        # Initialize Rasa agent
        agent = asyncio.run(load_rasa_agent())
        dashboard.set_rasa_agent(agent)
        print("Rasa agent loaded successfully")
    except Exception as e:
        print(f"Error loading Rasa agent: {e}")
        return
    
    print("Running dashboard with Rasa integration...")
    dashboard.run_server(debug=True, port=8501)

if __name__ == "__main__":
    main()
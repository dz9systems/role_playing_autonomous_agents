# CAMEL Role-Playing Autonomous Cooperative Agents
https://github.com/dz9systems/role_playing_autonomous_agents/assets/77218260/5f3e0bc4-3101-44f3-8604-56d0539315bb

## Project Overview
CAMEL stands for “Communicative Agents for ‘Mind’ Exploration of Large Language Models.” It is developed and maintained by a team of researchers at King Abdullah University of Science and Technology (KAUST).

This project serves as a foundation for employing AI agents to accomplish real-world tasks. The application leverages the power of AI to simulate dynamic conversations between two AI agents. Utilizing the Streamlit framework, it offers an interactive user interface for users to observe and analyze AI-driven dialogues.

## Features

- **User Input Interface:**
  - Users can input details such as Assistant Role Name, User Role Name, Task, and Word Limit for Task Brainstorming through a Streamlit-based UI.
  - A submit button triggers the execution of the program logic.

- **AI Agent Implementation:**
  - The code defines a class named `CAMELAgent` representing an autonomous cooperative agent.
  - Agent initialization with a system message and a ChatOpenAI model.
  - Methods include resetting the agent's state, initializing messages, updating messages, and handling interaction steps.

- **Task Specification:**
  - A task specifier system message and a human message prompt template are utilized to instruct the assistant in generating a specific task.
  - The specified task is generated and displayed using Streamlit.

- **Inception Prompts for Agent Roles:**
  - Distinct system messages and user prompts are created for the Assistant and User roles, setting the context and rules for their interactions.

- **System Messages Generation:**
  - System messages are generated based on user inputs and specified tasks, forming the foundation for AI assistant and user agents.

- **Agent Interaction Loop:**
  - The code orchestrates a conversation loop between the AI assistant and user agents, displaying the conversation in a chat format using Streamlit.
  - The conversation includes defined limits and conditions for task completion.

**User Information Section:**

## Getting Started

### Prerequisites
- Python 3.x
- Pip (Python package installer)
- Virtual environment (recommended)

### Installation

- **Clone the repository**
   ```bash
        git clone https://github.com/dz9systems/role_playing_autonomous_agents.git

### Start Virtual Environment
- ***Execute the following script:***
  ```bash
        python3 -m venv venv
        source venv/bin/activate

### Install Dependencies
- ***Execute the following script:***
  ```bash
        pip install -r requirements.txt

###  Running the Application
- ***Execute the main script:***
  ```bash
        streamlit run src/main.py


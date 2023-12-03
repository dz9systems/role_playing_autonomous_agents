import os
import openai
import streamlit as st
from dotenv import load_dotenv
from typing import List
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.schema import AIMessage, BaseMessage, HumanMessage, SystemMessage

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_KEY

assistant_role_name = "Python Programmer"
user_role_name = "Stock Trader"
task = "Develop a trading bot for the stock market"
word_limit = 50  # word limit for task brainstorming

# Define a class named CAMELAgent
class CAMELAgent:
    # Constructor for the class, initializes an instance of the class
    def __init__(
        self,
        system_message: SystemMessage,  # The first parameter, a SystemMessage object
        model: ChatOpenAI,  # The second parameter, a ChatOpenAI model object
    ) -> None:
        self.system_message = system_message  # Store the system_message in the instance
        self.model = model  # Store the model in the instance
        self.init_messages()  # Call the init_messages method to initialize messages

    # Method to reset the agent's state
    def reset(self) -> None:
        self.init_messages()  # Reinitialize the messages
        return self.stored_messages  # Return the stored messages

    # Method to initialize messages
    def init_messages(self) -> None:
        self.stored_messages = [self.system_message]  # Initialize stored_messages with the system message

    # Method to update the messages with a new message
    def update_messages(self, message: BaseMessage) -> List[BaseMessage]:
        self.stored_messages.append(message)  # Append the new message to stored_messages
        return self.stored_messages  # Return the updated list of messages

    # Method representing one interaction step with the agent
    def step(
        self,
        input_message: HumanMessage,  # The input message from a human
    ) -> AIMessage:
        messages = self.update_messages(input_message)  # Update stored messages with the input message

        output_message = self.model(messages)  # Process the messages with the model to get an output message
        self.update_messages(output_message)  # Update stored messages with the output message

        return output_message  # Return the output message

task_specifier_sys_msg = SystemMessage(content="You can make a task more specific.")
task_specifier_prompt = """Here is a task that {assistant_role_name} will help {user_role_name} to complete: {task}.
Please make it more specific. Be creative and imaginative.
Please reply with the specified task in {word_limit} words or less. Do not add anything else."""
task_specifier_template = HumanMessagePromptTemplate.from_template(
    template=task_specifier_prompt
)
task_specify_agent = CAMELAgent(task_specifier_sys_msg, ChatOpenAI(temperature=1.0))
task_specifier_msg = task_specifier_template.format_messages(
    assistant_role_name=assistant_role_name,
    user_role_name=user_role_name,
    task=task,
    word_limit=word_limit,
)[0]
specified_task_msg = task_specify_agent.step(task_specifier_msg)
print(f"Specified task: {specified_task_msg.content}")
specified_task = specified_task_msg.content


assistant_inception_prompt = """Never forget you are a {assistant_role_name} and I am a {user_role_name}. Never flip roles! Never instruct me!
We share a common interest in collaborating to successfully complete a task.
You must help me to complete the task.
Here is the task: {task}. Never forget our task!
I must instruct you based on your expertise and my needs to complete the task.

I must give you one instruction at a time.
You must write a specific solution that appropriately completes the requested instruction.
You must decline my instruction honestly if you cannot perform the instruction due to physical, moral, legal reasons or your capability and explain the reasons.
Do not add anything else other than your solution to my instruction.
You are never supposed to ask me any questions you only answer questions.
You are never supposed to reply with a flake solution. Explain your solutions.
Your solution must be declarative sentences and simple present tense.
Unless I say the task is completed, you should always start with:

Solution: <YOUR_SOLUTION>

<YOUR_SOLUTION> should be specific and provide preferable implementations and examples for task-solving.
Always end <YOUR_SOLUTION> with: Next request."""

user_inception_prompt = """Never forget you are a {user_role_name} and I am a {assistant_role_name}. Never flip roles! You will always instruct me.
We share a common interest in collaborating to successfully complete a task.
I must help you to complete the task.
Here is the task: {task}. Never forget our task!
You must instruct me based on my expertise and your needs to complete the task ONLY in the following two ways:

1. Instruct with a necessary input:
Instruction: <YOUR_INSTRUCTION>
Input: <YOUR_INPUT>

2. Instruct without any input:
Instruction: <YOUR_INSTRUCTION>
Input: None

The "Instruction" describes a task or question. The paired "Input" provides further context or information for the requested "Instruction".

You must give me one instruction at a time.
I must write a response that appropriately completes the requested instruction.
I must decline your instruction honestly if I cannot perform the instruction due to physical, moral, legal reasons or my capability and explain the reasons.
You should instruct me not ask me questions.
Now you must start to instruct me using the two ways described above.
Do not add anything else other than your instruction and the optional corresponding input!
Keep giving me instructions and necessary inputs until you think the task is completed.
When the task is completed, you must only reply with a single word <CAMEL_TASK_DONE>.
Never say <CAMEL_TASK_DONE> unless my responses have solved your task."""


# Define the function 'get_sys_msgs' which takes three parameters:
# 'assistant_role_name', 'user_role_name', and 'task'.
def get_sys_msgs(assistant_role_name: str, user_role_name: str, task: str):

    # Create an instance of SystemMessagePromptTemplate using the 'assistant_inception_prompt'.
    # This template will be used to format the system message for the assistant role.
    assistant_sys_template = SystemMessagePromptTemplate.from_template(
        template=assistant_inception_prompt
    )

    # Format the assistant system message template with the provided role names and task.
    # The formatted message is then retrieved from the resulting list (first element).
    assistant_sys_msg = assistant_sys_template.format_messages(
        assistant_role_name=assistant_role_name,
        user_role_name=user_role_name,
        task=task,
    )[0]

    # Similar to the assistant, create a system message template for the user role
    # using 'user_inception_prompt'.
    user_sys_template = SystemMessagePromptTemplate.from_template(
        template=user_inception_prompt
    )

    # Format the user system message template with the provided role names and task.
    # The formatted message is then retrieved from the resulting list (first element).
    user_sys_msg = user_sys_template.format_messages(
        assistant_role_name=assistant_role_name,
        user_role_name=user_role_name,
        task=task,
    )[0]

    # Return the formatted system messages for both the assistant and user roles.
    return assistant_sys_msg, user_sys_msg


# main function


def main():
    st.title("AI Conversation Simulator")

    # Automated setup for task specification
    task = "Develop a trading bot for the stock market"  # Example task
    task_specifier_sys_msg = SystemMessage(content="You can make a task more specific.")
    task_specifier_template = HumanMessagePromptTemplate.from_template(
        template="Here is a task that {assistant_role_name} will help {user_role_name} to complete: {task}."
                 "Please make it more specific. Be creative and imaginative. "
                 "Please reply with the specified task in {word_limit} words or less."
    )
    task_specify_agent = CAMELAgent(task_specifier_sys_msg, ChatOpenAI(temperature=1.0))
    task_specifier_msg = task_specifier_template.format_messages(
        assistant_role_name=assistant_role_name,
        user_role_name=user_role_name,
        task=task,
        word_limit=word_limit
    )[0]
    specified_task_msg = task_specify_agent.step(task_specifier_msg)
    specified_task = specified_task_msg.content
    st.write(f"Specified task: {specified_task}")

    # Setup AI agents
    assistant_sys_msg, user_sys_msg = get_sys_msgs(assistant_role_name, user_role_name, specified_task)
    assistant_agent = CAMELAgent(assistant_sys_msg, ChatOpenAI(temperature=0.2))
    user_agent = CAMELAgent(user_sys_msg, ChatOpenAI(temperature=0.2))

    assistant_agent.reset()
    user_agent.reset()

    # Simulate conversation
    chat_turn_limit = 30
    for _ in range(chat_turn_limit):
        user_response = user_agent.step(assistant_sys_msg)  # Simulate user response
        assistant_response = assistant_agent.step(user_response)  # Get assistant response

        # Display conversation with enhanced formatting
        st.markdown(f"#### User ({user_role_name}):")
        st.write(user_response.content)
        st.markdown(f"#### Assistant ({assistant_role_name}):")
        st.write(assistant_response.content)

        if "<CAMEL_TASK_DONE>" in assistant_response.content:
            break

if __name__ == "__main__":
    main()

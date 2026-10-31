import uuid

from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from agent import SYSTEM_PROMPT
from langchain_version.tools import search_documents, list_tables, describe_tables, run_query

load_dotenv(override=True)

lc_agent = create_agent(
    model="anthropic:claude-haiku-4-5-20251001",
    tools=[search_documents, list_tables, describe_tables, run_query],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=InMemorySaver(),
)

def run_agent(task, thread_id=None):
    if thread_id is None:
        thread_id = str(uuid.uuid4())
    result = lc_agent.invoke(
        {"messages": [{"role": "user", "content": task}]},
        config={"configurable": {"thread_id": thread_id}},
    )
    messages = result["messages"]

    last_human = max(i for i, m in enumerate(messages) if m.type == "human")
    steps = []
    for m in messages[last_human:]:
        if m.type == "ai":
            for call in m.tool_calls:
                steps.append({"tool": call["name"], "input": call["args"]})

    return str(messages[-1].text), steps
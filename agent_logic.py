import os
import pandas as pd
from google.adk.agents import Agent
from google.adk.tools import AgentTool
from google.adk.models.google_llm import Gemini


# ------------------------------
# INIT. GEMINI LLM
# ------------------------------
llm = Gemini(
    model="gemini-2.5-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY")
)


# ------------------------------
# AGENT 1
# ------------------------------
agent_1 = Agent(
    model=llm,
    name="client_understanding_agent",
    instruction="""
You are Agent 1 — The Company & Goal Understanding Expert.

Ask for:
- company name
- industry
- audience
- conversion goal
- what a good lead looks like

Then output JSON:
industry, goal, required_dataset_columns, why_these_columns, funny_line.
"""
)

# ------------------------------
# AGENT 2
# ------------------------------
agent_2 = Agent(
    model=llm,
    name="dataset_validator_agent",
    instruction="""
Validate uploaded CSV columns against Agent 1 output.
Return:
- uploaded_columns
- required_columns
- missing_columns
- matches
- recommended_new_columns
- next_step_instruction
"""
)

# ------------------------------
# AGENT 3
# ------------------------------
agent_3 = Agent(
    model=llm,
    name="lead_scoring_agent",
    instruction="""
Generate lead_score (0-100), category, intent_score,
recommended_channel, reasoning, next_action.

Return JSON:
{
  "scored_leads": [...],
  "summary_insights": "...",
  "recommended_actions": "...",
  "channel_strategy": "..."
}
"""
)


# ------------------------------
# WRAP EACH AGENT AS A TOOL
# ------------------------------
tool_1 = AgentTool(agent_1)
tool_2 = AgentTool(agent_2)
tool_3 = AgentTool(agent_3)


# ------------------------------
# ORCHESTRATOR AGENT
# ------------------------------
orchestrator = Agent(
    model=llm,
    name="orchestrator",
    instruction="""
You MUST run tools in this order:

1. tool_1 – client understanding
2. tool_2 – dataset validation
3. tool_3 – lead scoring

Then return the final output.
""",
    tools=[tool_1, tool_2, tool_3]
)

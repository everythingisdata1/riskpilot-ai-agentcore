import csv
import json
import os
from pathlib import Path

import boto3
from bedrock_agentcore import BedrockAgentCoreApp
from dotenv import load_dotenv
from strands import tool, Agent
from strands.models import BedrockModel

load_dotenv(override=False)
# Configuration
AWS_REGION = os.getenv("AWS_REGION")
AWS_MODEL_ID = os.getenv("AWS_MODEL_ID")
DATA_FILE = Path(__file__).parent.parent / "riskpilot" / "data" / "loan_portfolio.csv"
os.environ.pop("AWS_BEARER_TOKEN_BEDROCK", None)
print(f"AWS Region: {AWS_REGION}")
print(f"Model: {AWS_MODEL_ID}")
print(f"CSV exists: {DATA_FILE.exists()}")


# Load data
def load_portfolio_data() -> list:
    print("Loading data file")
    with open(DATA_FILE, mode='r', encoding="utf-8") as data:
        records = list(csv.DictReader(data))

    return records


@tool
def get_portfolio_data() -> str:
    """ Retrieve all banking loan portfolio exposure, probability of default and loss given  default..."""
    records = load_portfolio_data()
    return json.dumps(records)


# Calculate Expected loss

@tool
def calculate_expected_loss():
    """ Calculate Expected credit loss (ECL) for all the portfolio using EAD Multiplying by PD Multiplied by LDG.. """
    records = load_portfolio_data()
    results = []
    total_ecl = 0.0
    for row in records:
        ead = float(row['exposure_cr'])
        pd = float(row['pd'])
        lgd = float(row['lgd'])

        expected_credit_loss = ead * pd * lgd
        total_ecl += expected_credit_loss

        results.append({
            "portfolio": row['portfolio'],
            "ead": ead,
            "ecl_cr": round(expected_credit_loss, 4),
        })

    return json.dumps({
        "portfolio_results": results,
        "total_ecl": round(total_ecl, 4)
    })


# Tool Run stress Scenario

@tool
def run_stress_scenario(default_rate_increase_pct: float) -> str:
    """Run a credit stress scenario by increasing portfolio probability of default by a percentage,
    For example 20 mean a 20 percentage relative increase."""

    if not 0 <= default_rate_increase_pct <= 1000:
        return "Invalid stress percentage,  use 0 to 1000"

    records = load_portfolio_data()
    baseline_ecl_total = 0.0
    stressed_ecl_total = 0.0

    results = []

    for row in records:
        ead = float(row['exposure_cr'])
        baseline_pd = float(row['pd'])
        lgd = float(row['lgd'])
        stressed_pd = min(baseline_pd * (1 + default_rate_increase_pct / 100), 1.0)

        baseline_ecl = ead * baseline_pd * lgd
        stressed_ecl = ead * stressed_pd * lgd

        baseline_ecl_total += baseline_ecl
        stressed_ecl_total += stressed_ecl
        results.append({
            "portfolio": row['portfolio'],
            "baseline_pd": round(baseline_pd, 4),
            "baseline_ecl_cr": round(baseline_ecl, 4),
            "stressed_pd": round(stressed_pd, 4),
            "stressed_ecl_cr": round(stressed_ecl, 4),
        })

    return json.dumps({
        "stress_percentages": default_rate_increase_pct,
        "portfolio_results": results,
        "baseline_total_ecl_cr": round(baseline_ecl_total, 4),
        "stressed_total_ecl_cr": round(stressed_ecl_total, 4),
        "incremental_loss_cr": round((stressed_ecl_total - baseline_ecl_total), )
    })


aws_session = boto3.Session(
    region_name=os.getenv("AWS_REGION")
)

# Strands Agent
model = BedrockModel(
    model_id=os.getenv("AWS_MODEL_ID"),
    boto_session=aws_session,
    temperature=0.1
)

TOOLS = [get_portfolio_data,
         calculate_expected_loss,
         run_stress_scenario]

SYSTEM_PROMPT = """ 
You are a Risk Assistant Pilot Agent for banking credit risk assignment.
Task:
    1- Understand banking portfolio risk question.
    2- Use the given tool for all the calculations.
    3- Never invent portfolio and calculation data. 
    4. Explain PD, LGD, EAD and ECL in simple language with example. 
    5. Present portfolio compression clearly.
    6. Always identify assumptions in stress scenario.
    7. Treat all the result as illustrative, not regulatory approved ECL. 
 
 Use Indian Rupees in crore (INR Cr) for financial results.
 """
agent = Agent(
    model=model,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT
)

# Bedcore Agent core setup...


app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload):
    print("RiskAI Agent Invocation ...")
    prompt = payload.get('prompt', "")

    if not prompt.strip():
        return {"error": "Please provide a prompt."}

    resp = agent(prompt)

    return {
        "result": str(resp)
    }


if __name__ == '__main__':
    print("BedrockAgentCoreApp ::")
    app.run()

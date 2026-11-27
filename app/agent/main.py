import os

import boto3
from bedrock_agentcore import BedrockAgentCoreApp
from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel

from prompts import SYSTEM_PROMPT
from tools.ecl_tool import calculate_expected_loss
from tools.portfolio_tool import get_portfolio_data
from tools.stress_tool import run_stress_scenario

load_dotenv(override=False)
# Configuration
os.environ.pop("AWS_BEARER_TOKEN_BEDROCK", None)

_SEP = "*" * 40

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

agent = Agent(model=model,
              tools=TOOLS,
              system_prompt=SYSTEM_PROMPT
              )


# AWS Bedrock AgentCore  Agent core setup...
def create_app():
    app = BedrockAgentCoreApp()
    log = app.logger

    @app.entrypoint
    def invoke(payload, context):
        log.info("Invoking  RiskAI Agent  ...")
        prompt = payload.get('prompt', "")

        if not prompt.strip():
            return {"error": "Please provide a prompt."}

        resp = agent(prompt)

        return {
            "result": str(resp)
        }

    return app


app = create_app()
if __name__ == '__main__':
    app.run()

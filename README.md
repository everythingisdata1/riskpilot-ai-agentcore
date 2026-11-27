# AWS Bedrock AgentCore Runtime for Agentic AI

This repository demonstrates how to build, run, and deploy Agentic AI applications using **Amazon Bedrock AgentCore Runtime** and the **Strands Agents SDK**.

We will explore how to integrate foundation models from Amazon Bedrock, build AI agents with custom tools, run agents locally, and deploy them to AWS using AgentCore Runtime.

## Tech Stack

- Python
- Amazon Bedrock
- Amazon Bedrock AgentCore Runtime
- Strands Agents SDK
- Boto3 (AWS SDK for Python)
- AgentCore CLI
- AgentCore API Gateway (for future integration)

## Prerequisites

Before getting started, ensure you have:

- An AWS account
- Python 3.10+
- Node.js 20.12+
- npm
- AWS CLI
- uv package manager
- Amazon Bedrock model access
- Appropriate AWS IAM permissions

### Configure AWS Credentials

Configure your AWS credentials using AWS CLI.

```bash
aws configure
```

Alternatively, configure AWS SSO:

```bash
aws configure sso --profile riskpilot-dev
```

Verify your AWS identity:

```bash
aws sts get-caller-identity
```

**Note:** Never commit AWS access keys, secret keys, API keys, or other credentials to GitHub. Prefer IAM roles or AWS SSO profiles.

## 1. Install AgentCore CLI

Install the AgentCore CLI:

```bash
npm install -g @aws/agentcorex
```

Verify installation:

```bash
agentcore --version
```

## 2. Create the AgentCore Project

Create a Python project using the Strands Agents template:

```bash
agentcore create --name riskApiAgent --template agent-python-strands
```

Navigate to the project directory:

```bash
cd riskApiAgent
```

This creates a starter project with the Strands framework and AgentCore Runtime configuration.

## 3. Run the Application Locally

Start the local development environment:

```bash
agentcore dev --mode browser
```

This launches the local Runtime development server and opens the Agent Inspector in your browser.

You can interact with your agent, test prompts, and inspect execution traces.

## 4. Build and Deploy

Build the application:

```bash
agentcore build
```

Deploy the agent to AWS:

```bash
agentcore deploy
```

Check deployment status:

```bash
agentcore status
```

## 5. Invoke the Deployed Agent

Invoke your deployed Runtime:

```bash
agentcore invoke --runtime agent --payload '{"prompt":"Hello, what can you do?"}'
```

## Objectives

- Understand Amazon Bedrock AgentCore Runtime.
- Build agents using Strands Agents SDK.
- Integrate Amazon Bedrock foundation models.
- Create custom Python tools for agents.
- Run and debug agents locally.
- Deploy agents to AWS.
- Explore AgentCore Memory, Gateway, Identity, and Observability.

## Roadmap

1. Create and run a basic Strands agent.
2. Integrate Amazon Bedrock Nova models.
3. Implement custom tools.
4. Build RiskPilot AI for banking credit risk analysis.
5. Deploy the application using AgentCore Runtime.
6. Explore AgentCore Gateway and Memory.
7. Implement observability and production-ready security.


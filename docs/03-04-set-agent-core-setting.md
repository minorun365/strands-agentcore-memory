 → agentcore configure --entrypoint src/main.py -er arn:aws:iam::XXXXXXXXXXXX:role/
Configuring Bedrock AgentCore...
Entrypoint parsed: file=/Users/uchinishi.koichi/train/handson/strands-agentcore-memory/backend/src/main.py, bedrock_agentcore_name=main
Agent name: main

🏗️   ECR Repository
Press Enter to auto-create ECR repository, or provide ECR Repository URI to use
existing
ECR Repository URI (or press Enter to auto-create):
✓ Will auto-create ECR repository

🔍 Detected dependency file: requirements.txt
Press Enter to use this file, or type a different path (use Tab for
autocomplete):
Path or Press Enter to use detected dependency file:
✓ Using detected file: requirements.txt

🔐 Authorization Configuration
By default, Bedrock AgentCore uses IAM authorization.
Configure OAuth authorizer instead? (yes/no) [no]:
✓ Using default IAM authorization
Configuring BedrockAgentCore agent: main
Generated .dockerignore
Generated Dockerfile: /Users/uchinishi.koichi/train/handson/strands-agentcore-memory/backend/Dockerfile
Generated .dockerignore: /Users/uchinishi.koichi/train/handson/strands-agentcore-memory/backend/.dockerignore
Setting 'main' as default agent
╭─────────────────────── Bedrock AgentCore Configured ────────────────────────╮
│ Configuration Summary                                                       │
│                                                                             │
│ Name: main                                                                  │
│ Runtime: Docker                                                             │
│ Region: us-west-2                                                           │
│ Account: XXXXXXXXXXXX                                                       │
│ Execution Role: arn:aws:iam::XXXXXXXXXXXX:role/                             │
│ ECR: Auto-create                                                            │
│ Authorization: IAM (default)                                                │
│                                                                             │
│ Configuration saved to:                                                     │
│ /Users/uchinishi.koichi/train/handson/strands-agentcore-memory/backend/.bed │
│ rock_agentcore.yaml                                                         │
╰─────────────────────────────────────────────────────────────────────────────╯

 → >....
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "bedrock-agentcore.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }'

# 必要なポリシーをアタッチ
aws iam attach-role-policy \
    --role-name BedrockAgentCoreExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/BedrockAgentCoreFullAccess

aws iam attach-role-policy \
    --role-name BedrockAgentCoreExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

aws iam attach-role-policy \
    --role-name BedrockAgentCoreExecutionRole \
    --policy-arn arn:aws:iam::aws:***AWS_SECRET_ACCESS_KEY***

aws iam attach-role-policy \
    --role-name BedrockAgentCoreExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/CloudWatchFullAccessV2

aws iam attach-role-policy \
    --role-name BedrockAgentCoreExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess

# ロールARNを取得（後で使用）
aws iam get-role --role-name BedrockAgentCoreExecutionRole --query 'Role.Arn' --output text
{
    "Role": {
        "Path": "/",
        "RoleName": "BedrockAgentCoreExecutionRole",
        "RoleId": "AROAY5YGE34YG7P6VB7I3",
        "Arn": "arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole",
        "CreateDate": "2025-07-27T06:25:05+00:00",
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "bedrock-agentcore.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
    }
}
arn:aws:iam::XXXXXXXXXXXX:role/BedrockAgentCoreExecutionRole

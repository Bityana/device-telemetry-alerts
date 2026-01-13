# Terraform (toy AWS)

This is intentionally small and safe. It provisions:
- SQS queue (optional queue backend)
- DynamoDB table (optional state store)
- An IAM policy document illustrating least-privilege permissions

## Usage
```bash
cd infra/terraform/aws
terraform init
terraform apply
```

Then set:
- `QUEUE_BACKEND=sqs`
- `SQS_QUEUE_URL=<output>`
- `DYNAMODB_TABLE=<output>`

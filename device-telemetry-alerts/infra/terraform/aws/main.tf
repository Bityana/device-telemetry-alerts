resource "aws_sqs_queue" "telemetry_events" {
  name                      = "${var.name_prefix}-telemetry-events"
  message_retention_seconds = 1209600
}

resource "aws_dynamodb_table" "device_state" {
  name         = "${var.name_prefix}-device-state"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "device_id"

  attribute {
    name = "device_id"
    type = "S"
  }
}

# Example least-privilege IAM policy (attach to your app role)
data "aws_iam_policy_document" "app_policy" {
  statement {
    actions = [
      "sqs:SendMessage",
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes"
    ]
    resources = [aws_sqs_queue.telemetry_events.arn]
  }

  statement {
    actions = [
      "dynamodb:GetItem",
      "dynamodb:PutItem",
      "dynamodb:UpdateItem"
    ]
    resources = [aws_dynamodb_table.device_state.arn]
  }
}

resource "aws_iam_policy" "app_policy" {
  name   = "${var.name_prefix}-app-policy"
  policy = data.aws_iam_policy_document.app_policy.json
}

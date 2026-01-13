output "sqs_queue_url" {
  value = aws_sqs_queue.telemetry_events.url
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.device_state.name
}

output "iam_policy_arn" {
  value = aws_iam_policy.app_policy.arn
}

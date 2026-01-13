export type Alert = {
  alert_id: string
  device_id: string
  alert_type: string
  severity: string
  message: string
  created_at: string
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export async function fetchAlerts(token: string, limit = 50): Promise<Alert[]> {
  const resp = await fetch(`${API_BASE_URL}/v1/alerts?limit=${limit}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  })
  if (!resp.ok) {
    const body = await resp.text()
    throw new Error(`API error ${resp.status}: ${body}`)
  }
  return resp.json()
}

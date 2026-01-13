import React, { useMemo } from 'react'
import { Alert } from '../api'
import styles from './AlertTable.module.scss'
import Badge from './Badge'

function fmtTime(iso: string) {
  try {
    return new Date(iso).toLocaleString()
  } catch {
    return iso
  }
}

export default function AlertTable({ alerts }: { alerts: Alert[] }) {
  const rows = useMemo(() => alerts ?? [], [alerts])

  return (
    <div className={styles.wrap}>
      <div className={styles.top}>
        <div className={styles.title}>Recent alerts</div>
        <div className={styles.count}>{rows.length}</div>
      </div>

      <table className={styles.table}>
        <thead>
          <tr>
            <th>Time</th>
            <th>Device</th>
            <th>Type</th>
            <th>Severity</th>
            <th>Message</th>
          </tr>
        </thead>
        <tbody>
          {rows.length === 0 ? (
            <tr>
              <td colSpan={5} className={styles.empty}>No alerts yet. Send telemetry to trigger rules.</td>
            </tr>
          ) : (
            rows.map((a) => (
              <tr key={a.alert_id}>
                <td className={styles.mono}>{fmtTime(a.created_at)}</td>
                <td className={styles.mono}>{a.device_id}</td>
                <td className={styles.mono}>{a.alert_type}</td>
                <td><Badge severity={a.severity} /></td>
                <td>{a.message}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}

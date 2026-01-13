import React from 'react'
import styles from './Badge.module.scss'

export default function Badge({ severity }: { severity: string }) {
  const s = severity.toLowerCase()
  const label = s === 'high' ? 'HIGH' : s === 'medium' ? 'MED' : 'LOW'
  return <span className={`${styles.badge} ${styles[s] || ''}`}>{label}</span>
}

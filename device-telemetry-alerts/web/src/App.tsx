import React, { useEffect, useMemo, useState } from 'react'
import styles from './App.module.scss'
import { fetchAlerts, Alert } from './api'
import AlertTable from './components/AlertTable'

export default function App() {
  const [token, setToken] = useState<string>(() => localStorage.getItem('jwt') || '')
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [error, setError] = useState<string>('')

  const canLoad = useMemo(() => token.trim().length > 10, [token])

  async function load() {
    setError('')
    try {
      const data = await fetchAlerts(token)
      setAlerts(data)
    } catch (e: any) {
      setError(e?.message || 'Failed to load alerts')
    }
  }

  useEffect(() => {
    if (canLoad) {
      load()
    }
  }, []) // eslint-disable-line

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <div>
          <h1>Telemetry Alerts</h1>
          <p className={styles.sub}>
            Lightweight triage console (React + TypeScript + SCSS Modules)
          </p>
        </div>

        <button className={styles.button} onClick={load} disabled={!canLoad}>
          Refresh
        </button>
      </header>

      <section className={styles.panel}>
        <label className={styles.label}>JWT (alerts:read)</label>
        <div className={styles.row}>
          <input
            className={styles.input}
            value={token}
            onChange={(e) => {
              setToken(e.target.value)
              localStorage.setItem('jwt', e.target.value)
            }}
            placeholder="Paste your JWT here"
          />
          <button
            className={styles.buttonSecondary}
            onClick={() => {
              setToken('')
              localStorage.removeItem('jwt')
            }}
          >
            Clear
          </button>
        </div>
        {error && <div className={styles.error}>{error}</div>}
      </section>

      <main className={styles.main}>
        <AlertTable alerts={alerts} />
      </main>

      <footer className={styles.footer}>
        Tip: generate a token via <code>docker compose exec api python -m app.scripts.generate_token</code>
      </footer>
    </div>
  )
}

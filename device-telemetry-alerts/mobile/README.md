# Telemetry Alerts Mobile (React Native)

A small **React Native (Expo + TypeScript)** companion app for the Device Telemetry & Alerts Platform.

## Features
- Enter and save a JWT token
- Fetch recent alerts from the API
- Quick triage: severity badge + message preview

## Run
```bash
cd mobile
npm install
npm run start
```

## Configure
By default, the app uses `http://localhost:8000` when running on the same machine.

If you are testing on a phone, you may need to use your machine's LAN IP (e.g., `http://192.168.1.10:8000`).

You can change the API base URL inside the app.

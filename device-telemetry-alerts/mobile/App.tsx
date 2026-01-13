import React, { useEffect, useMemo, useState } from 'react';
import {
  ActivityIndicator,
  FlatList,
  SafeAreaView,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Constants from 'expo-constants';
import { StatusBar } from 'expo-status-bar';

type AlertItem = {
  alert_id: number;
  device_id: string;
  alert_type: string;
  severity: 'low' | 'medium' | 'high' | string;
  message: string;
  created_at: string;
};

const STORAGE_TOKEN = 'telemetry.jwt';
const STORAGE_BASE_URL = 'telemetry.baseUrl';

function defaultBaseUrl(): string {
  // If running on the same machine as the API, localhost works for Android emulator.
  // For physical devices, you'll likely need to set your LAN IP in-app.
  return 'http://localhost:8000';
}

async function apiGetAlerts(baseUrl: string, token: string, limit: number): Promise<AlertItem[]> {
  const url = `${baseUrl.replace(/\/$/, '')}/v1/alerts?limit=${limit}`;
  const resp = await fetch(url, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!resp.ok) {
    const body = await resp.text();
    throw new Error(`API error ${resp.status}: ${body}`);
  }
  return (await resp.json()) as AlertItem[];
}

export default function App() {
  const [token, setToken] = useState('');
  const [baseUrl, setBaseUrl] = useState(defaultBaseUrl());
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const buildInfo = useMemo(() => {
    const v = Constants.expoConfig?.version ?? '0.0.0';
    return `v${v}`;
  }, []);

  useEffect(() => {
    (async () => {
      const savedToken = (await AsyncStorage.getItem(STORAGE_TOKEN)) ?? '';
      const savedBase = (await AsyncStorage.getItem(STORAGE_BASE_URL)) ?? '';
      if (savedToken) setToken(savedToken);
      if (savedBase) setBaseUrl(savedBase);
    })();
  }, []);

  async function saveSettings() {
    await AsyncStorage.setItem(STORAGE_TOKEN, token);
    await AsyncStorage.setItem(STORAGE_BASE_URL, baseUrl);
  }

  async function refresh() {
    setError(null);
    setLoading(true);
    try {
      await saveSettings();
      const data = await apiGetAlerts(baseUrl, token, 50);
      setAlerts(data);
    } catch (e: any) {
      setError(e?.message ?? String(e));
    } finally {
      setLoading(false);
    }
  }

  function severityLabel(sev: string) {
    const s = sev.toLowerCase();
    if (s === 'high') return 'HIGH';
    if (s === 'medium') return 'MED';
    if (s === 'low') return 'LOW';
    return sev.toUpperCase();
  }

  return (
    <SafeAreaView style={{ flex: 1, padding: 16 }}>
      <StatusBar style="auto" />
      <Text style={{ fontSize: 20, fontWeight: '700', marginBottom: 4 }}>Telemetry Alerts</Text>
      <Text style={{ opacity: 0.6, marginBottom: 12 }}>{buildInfo}</Text>

      <Text style={{ fontWeight: '600' }}>API Base URL</Text>
      <TextInput
        value={baseUrl}
        onChangeText={setBaseUrl}
        autoCapitalize="none"
        placeholder="http://localhost:8000"
        style={{
          borderWidth: 1,
          borderColor: '#ccc',
          borderRadius: 8,
          padding: 10,
          marginBottom: 10,
        }}
      />

      <Text style={{ fontWeight: '600' }}>JWT Token</Text>
      <TextInput
        value={token}
        onChangeText={setToken}
        autoCapitalize="none"
        placeholder="Paste token..."
        secureTextEntry
        style={{
          borderWidth: 1,
          borderColor: '#ccc',
          borderRadius: 8,
          padding: 10,
          marginBottom: 10,
        }}
      />

      <TouchableOpacity
        onPress={refresh}
        style={{
          backgroundColor: '#111',
          padding: 12,
          borderRadius: 10,
          alignItems: 'center',
          marginBottom: 12,
        }}
      >
        <Text style={{ color: '#fff', fontWeight: '700' }}>{loading ? 'Loading…' : 'Refresh Alerts'}</Text>
      </TouchableOpacity>

      {error ? (
        <View style={{ padding: 10, borderWidth: 1, borderColor: '#e11', borderRadius: 8, marginBottom: 12 }}>
          <Text style={{ color: '#b00', fontWeight: '700' }}>Error</Text>
          <Text style={{ color: '#b00' }}>{error}</Text>
        </View>
      ) : null}

      {loading ? (
        <View style={{ paddingTop: 20 }}>
          <ActivityIndicator />
        </View>
      ) : (
        <FlatList
          data={alerts}
          keyExtractor={(item) => String(item.alert_id)}
          contentContainerStyle={{ paddingBottom: 20 }}
          renderItem={({ item }) => (
            <View
              style={{
                borderWidth: 1,
                borderColor: '#e5e5e5',
                borderRadius: 12,
                padding: 12,
                marginBottom: 10,
              }}
            >
              <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginBottom: 6 }}>
                <Text style={{ fontWeight: '700' }}>{item.device_id}</Text>
                <View
                  style={{
                    borderWidth: 1,
                    borderColor: '#ddd',
                    borderRadius: 999,
                    paddingVertical: 2,
                    paddingHorizontal: 10,
                  }}
                >
                  <Text style={{ fontWeight: '700', fontSize: 12 }}>{severityLabel(item.severity)}</Text>
                </View>
              </View>
              <Text style={{ opacity: 0.8, marginBottom: 4 }}>{item.alert_type}</Text>
              <Text numberOfLines={2} style={{ fontSize: 14 }}>{item.message}</Text>
              <Text style={{ opacity: 0.5, marginTop: 6, fontSize: 12 }}>{new Date(item.created_at).toLocaleString()}</Text>
            </View>
          )}
          ListEmptyComponent={<Text style={{ opacity: 0.6 }}>No alerts yet. Send telemetry to trigger rules.</Text>}
        />
      )}
    </SafeAreaView>
  );
}

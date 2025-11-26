import React, { useEffect, useState } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import axios from 'axios';

// const API_URL = "http://YOUR_SERVER_IP:5000";
const API_URL = "http://10.100.230.54:5000"

export default function App() {
  const [data, setData] = useState(null);

  const getLatest = async () => {
    try {
      const res = await axios.get(`${API_URL}/api/latest`);
      setData(res.data);
    } catch (e) {
      console.log("Error:", e);
    }
  };

  const sendControl = async (cmd) => {
    try {
      await axios.post(`${API_URL}/api/control`, { action: cmd });
    } catch (e) {
      console.log("Error:", e);
    }
  };

  useEffect(() => {
    getLatest();
    const interval = setInterval(getLatest, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Energy Monitor</Text>

      {data ? (
        <>
          <Text>Voltage: {data.voltage} V</Text>
          <Text>Current: {data.current} A</Text>
          <Text>Power: {data.power} W</Text>
          <Text>Energy: {data.energy} Wh</Text>
        </>
      ) : (
        <Text>Loading...</Text>
      )}

      <View style={styles.btnBox}>
        <Button title="Turn ON" onPress={() => sendControl("on")} />
        <Button title="Turn OFF" onPress={() => sendControl("off")} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 28,
    marginBottom: 20,
  },
  btnBox: {
    marginTop: 20,
    flexDirection: 'row',
    gap: 20
  }
});

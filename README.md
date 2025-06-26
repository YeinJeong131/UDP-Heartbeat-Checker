# UDP-Heartbeat-Simulator

This project implements a **UDP-based Heartbeat System** to simulate real-world scenarios of detecting online/offline status of network nodes using periodic heartbeat messages.

## 📌 Overview

In this system:
- The **Heartbeat Client** sends periodic heartbeat messages to the server.
- The **Heartbeat Server** maintains timestamps of last received heartbeats and determines whether a client is *online* or *offline* based on timeouts.

---

## 🛠 Files

| File | Description |
|------|-------------|
| `UDPHeartbeatServer_YeinJeong_14650170.py` | Receives heartbeats and updates client status |
| `UDPHeartbeatClient_YeinJeong_14650170.py` | Sends heartbeat messages at fixed intervals |

---

## ⚙️ How It Works

### Server (`UDPHeartbeatServer`)
- Listens on a predefined UDP port.
- Keeps track of the last received heartbeat timestamp per client.
- If no heartbeat is received within a timeout (e.g. 15 seconds), the client is considered **offline**.

### Client (`UDPHeartbeatClient`)
- Sends heartbeat messages (with client ID and timestamp) every few seconds.
- Optionally simulates client disconnection by stopping heartbeats.

---

## ✅ Sample Behavior

```bash
[SERVER]
Heartbeat received from ClientA at 10:01:23
ClientA is ONLINE
...
No heartbeat received from ClientA for 16 seconds
ClientA is OFFLINE

[CLIENT]
Heartbeat sent to server: ClientA | 10:01:23
...
Heartbeat sent to server: ClientA | 10:01:26
```
---
## 💡 Learning Objectives
- Through this project, I learned:
- How to manage UDP communication in a client-server model.
- How to track online status using heartbeat intervals and timestamps.
- How to build simple fault-detection logic (simulate real-world monitoring).
- How to use socket, datetime, and threading modules in Python.
---
## 📎 How to Run
Run the server:
```bash
python UDPHeartbeatServer_YeinJeong_14650170.py
```

Run the client in a separate terminal:
```bash
python UDPHeartbeatClient_YeinJeong_14650170.py
```
> Ensure the client and server are on the same network or localhost, and no firewall is blocking UDP port usage.


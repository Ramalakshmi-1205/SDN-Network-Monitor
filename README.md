# SDN Network Utilization Monitor

## 📌 Problem Statement
Monitor network bandwidth using SDN controller (POX) and Mininet.

## 🛠 Tools Used
- Mininet
- POX Controller
- OpenFlow

## ⚙️ Setup & Execution

1. Run POX:
cd pox
python3 pox.py misc.network_monitor

2. Run Mininet:
sudo mn --topo single,3 --controller=remote,port=6633

3. Generate traffic:
pingall

## 📊 Output
- Displays bandwidth usage in Mbps
- Flow rules installed dynamically

## 🧪 Test Cases
1. Normal traffic → All hosts reachable
2. Controlled drop → Selective packet blocking

## 📸 Proof
(Add screenshots here)

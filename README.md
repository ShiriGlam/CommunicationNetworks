
# 🌐 Network Programming Projects – HTTP Server, Client & Infrastructure Setup

This repository contains two practical projects. The projects focus on implementing a minimal HTTP server and client using raw sockets, along with configuring and analyzing real-world networking components such as Apache servers, DNS, and proxies.

---

## 🧪 Part 1: TCP-based HTTP Server & Client in Python

### ✅ Features

- Manual implementation of TCP server and client in Python
- Basic support for HTTP 1.1:
  - `GET` requests
  - `200 OK`, `404 Not Found`, `301 Moved Permanently`
  - `Connection: keep-alive` and `Connection: close`
- File retrieval from a structured `/files` directory
- Real-time parsing of server responses by client
- Simulated browser-like behavior

### 📂 Files

- `server.py` – Listens for connections and responds to HTTP requests
- `client.py` – Sends raw HTTP requests and saves received files
- `files/` – Directory with sample HTML, image, and text files
- `capture.pcapng` – Wireshark captures of the full session
- `report.pdf` – Includes protocol explanation, sequence analysis, screenshots
- `details.txt` – Submission metadata

### 💡 Learning Outcomes

- Understanding socket programming from scratch
- Implementing key aspects of the HTTP protocol manually
- Handling real-world networking behavior: headers, content-length, persistence
- Analyzing TCP segments using Wireshark

---

## 🌍 Part 2: Network Infrastructure Setup & Analysis (Apache, DNS, Proxy)

### 🔧 What We Configured

- ✅ **Apache HTTP Server**: Installed and hosted a local index.html
- 🌐 **Wireshark Analysis**: Inspected HTTP requests/responses over TCP (port 80)
- 📡 **DNS Server (bind9)**:
  - Configured caching DNS
  - Set up an authoritative zone for `biu.ac.il`
  - Customized A, NS, MX, and SOA records
- 🔁 **Proxy Server (Squid)**:
  - Configured client to route traffic via proxy
  - Compared browsing behavior via incognito and regular modes

### 📸 Analysis Techniques

- TCP stream following in Wireshark
- HTTP segmentation behavior
- DNS caching validation via `rndc dumpdb`
- Use of `dig`, `nslookup` and packet-level inspection

---

## 🛠️ Technologies Used

- Python 3 (only `socket`, `sys`, basic `os`)
- Ubuntu Linux
- Apache2
- bind9 DNS server
- Squid Proxy
- Wireshark

---


- **Author(s):** Shiri Glam and partner

---

## 📫 Contact

**Shiri Glam**  
📧 Shiri3847@gmail.com  
📱 050-9420362  


---

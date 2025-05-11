# WiFi File Manager 📁

A lightweight, web-based file management system that enables seamless file uploads, downloads, and directory navigation over a local WiFi network. Built with Flask, it supports large file transfers up to 10 GB with real-time progress monitoring, secure user authentication, and an intuitive UI.

---

## **🚀 Features**


- **Web-Based Interface:** Access and manage files via any browser on the same network.

- **Large File Support:** Upload files up to 10 GB with streamed processing and real-time progress tracking.
- **User Authentication:** Secure login with session management and activity logging.
- **Responsive Design:** Mobile-friendly UI with icon-based previews for images, videos, and documents.
- **Cross-Platform Compatibility:** Works on Ubuntu, Windows, and macOS.
- **Drag-and-Drop Upload:** Seamlessly upload files through drag-and-drop support.
- **Network Accessibility:** Accessible across devices via a configurable IP and port.

---

## **🛠 Tech Stack**

- **Backend:** Flask, Python
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Gunicorn (Ubuntu/macOS), Waitress (Windows), Ubuntu
- **Storage:** Filesystem-based (no database required)

---

## **⚡️ Getting Started**

Follow these steps to set up and run the application:

### **1️⃣ Prerequisites**
- Python 3.8+
- Git
- 8+ GB RAM and 10+ GB disk space for large file uploads
- Ubuntu, Windows, or macOS with network access

### **2️⃣ Clone the Repository**
     ```bash
     git clone https://github.com/RahulKeshri1/WiFi_File_Sharing.git
     cd WiFi_File_Sharing

### **3️⃣ Create a Virtual Environment**
     ```bash
     python3 -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate

### **4️⃣ Install Dependencies**
     ```bash
     pip install -r requirements.txt

### **5️⃣ Configure BASE_DIR**

Edit config.py to set BASE_DIR to a writable directory:

- **Ubuntu:** BASE_DIR = r'/home/rahul/Files'
- **macOS:** BASE_DIR = r'/Users/rahul/Files'
- **Windows:** BASE_DIR = r'C:\Users\Rahul\Documents\Files'



**Create the directory:**
     ```bash
     mkdir /home/rahul/Files  # Adjust for your system
     chmod u+rwx /home/rahul/Files  # Ubuntu/macOS only

### **6️⃣ Run the Application**

**Ubuntu/macOS (Production)**
     ```bash
     gunicorn -w 4 -b 0.0.0.0:5000 --timeout 1800 app:app

Allow port 5000:
     ```bash
     sudo ufw allow 5000  # Ubuntu

**Windows (Production)**
     ```bash
     waitress-serve --host=0.0.0.0 --port=5000 --call app:app

Allow port 5000:
     ```bash
     New-NetFirewallRule -DisplayName "WiFi File Manager" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow

**Development Mode (All Platforms)**
     ```bash
     python3 app.py





**Note: The Flask development server is not recommended for 10 GB uploads.**



Access the app at http://<your-ip>:5000 (e.g., http://192.168.29.68:5000).

---

## **🔄 Usage**

- Open the app in a browser (e.g., http://192.168.29.68:5000).
- Log in with credentials (e.g., admin/admin123 from config.py).
- Upload files (up to 10 GB), download, create folders, or delete files using drag-and-drop or file selection.
- Monitor uploads via the real-time progress bar.
- Check activity logs in activity.log.

---

### **🌐 Deployment**

For production deployment:

- **Ubuntu/macOS: Use Gunicorn:**
     ```bash
     gunicorn -w 4 -b 0.0.0.0:5000 --timeout 1800 app:app


- **Windows: Use Waitress:**
     ```bash
     waitress-serve --host=0.0.0.0 --port=5000 --call app:app


- **For enhanced performance, consider adding Nginx as a reverse proxy (see Nginx Setup).**

**Nginx Setup (Optional)**
- Install Nginx:
     ```bash
     sudo apt-get install nginx  # Ubuntu
     brew install nginx  # macOS



- Configure /etc/nginx/sites-available/wifi_file_manager:
     ```bash
     server {
         listen 80;
         server_name <your-ip>;
     
         client_max_body_size 10G;
     
         location / {
             proxy_pass http://127.0.0.1:5000;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_read_timeout 1800;
             proxy_send_timeout 1800;
         }
     }



- **Enable and start Nginx:**
     ```bash
     sudo ln -s /etc/nginx/sites-available/wifi_file_manager /etc/nginx/sites-enabled
     sudo nginx -t
     sudo systemctl restart nginx

- Access at http://<your-ip>.

---

## **🔐 Security Considerations**
- Future Improvements:
    - Enable HTTPS for secure data transfer (e.g., with Let’s Encrypt).
    - Use environment variables for SECRET_KEY and user credentials (e.g., with python-dotenv).
    - Implement IP whitelisting for sensitive operations.
- Current: Hardcoded SECRET_KEY and user credentials in config.py. Secure these in production.

---

## **📂 Project Structure**
     ```bash
     WiFi_File_Sharing/
     ├── .gitignore          # Ignored files (e.g., activity.log, venv/)
     ├── LICENSE             # MIT License
     ├── README.md           # Project documentation
     ├── app.py              # Flask application
     ├── config.py           # Configuration (BASE_DIR, users, etc.)
     ├── requirements.txt    # Python dependencies
     ├── static/             # CSS and static assets
     │   └── style.css
     ├── templates/          # HTML templates
     │   ├── login.html
     │   └── file_manager.html
     ├── utils/              # Helper functions
     │   ├── __init__.py
     │   └── helpers.py

---

## **🤝 Contributing**

We welcome contributions to improve Wifi_File_Share. Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
    ```bash
    git checkout -b feature/your-feature-name

3. Commit your changes:
    ```bash
    git commit -m "Add your message here" 

4. Push your branch:
    ```bash
    git push origin feature/your-feature-name

5. Open a pull request

---

## **📝 License**

This project is licensed under the MIT License - see the LICENSE file for details.

---

## **📧 Contact**

Rahul Kumar Keshri
rahulkumarkeshri475@gmail.com
GitHub
# 🚀 Deployment Guide - Excel-to-Insights Bot

## Overview

This guide covers deploying the Excel-to-Insights Bot to various platforms for production use.

---

## 🏠 Local Deployment (Development)

### Windows

```bash
# 1. Clone/navigate to project
cd excel-insight-generator

# 2. Create virtual environment
python -m venv .venv

# 3. Activate environment
.venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
copy .env.example .env
# Edit .env with your API keys

# 6. Run application
streamlit run app.py
```

### Linux/Mac

```bash
# 1. Clone/navigate to project
cd excel-insight-generator

# 2. Create virtual environment
python3 -m venv .venv

# 3. Activate environment
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 6. Run application
streamlit run app.py
```

---

## ☁️ Cloud Deployment

### Option 1: Streamlit Cloud (Recommended - Free)

**Pros:**
- ✅ Free hosting
- ✅ Easy deployment
- ✅ Automatic updates
- ✅ HTTPS included

**Steps:**

1. **Prepare Repository**
   ```bash
   # Ensure all files are committed
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Create Streamlit Cloud Account**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub

3. **Deploy Application**
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy"

4. **Configure Secrets**
   - Go to App Settings → Secrets
   - Add your API keys:
   ```toml
   OPENAI_API_KEY = "your-key-here"
   GEMINI_API_KEY = "your-key-here"
   MAX_FILE_SIZE_MB = "200"
   DEFAULT_AI_MODEL = "OpenAI GPT-4"
   ```

5. **Access Your App**
   - URL: `https://your-app-name.streamlit.app`

**Limitations:**
- 1 GB RAM
- 1 CPU
- 800 MB storage
- Good for small to medium datasets

---

### Option 2: Heroku

**Pros:**
- ✅ More resources than Streamlit Cloud
- ✅ Custom domain support
- ✅ Scalable

**Steps:**

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Add Configuration Files**

   Create `Procfile`:
   ```
   web: sh setup.sh && streamlit run app.py
   ```

   Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   
   echo "\
   [general]\n\
   email = \"your-email@example.com\"\n\
   " > ~/.streamlit/credentials.toml
   
   echo "\
   [server]\n\
   headless = true\n\
   enableCORS=false\n\
   port = $PORT\n\
   " > ~/.streamlit/config.toml
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set OPENAI_API_KEY=your-key-here
   heroku config:set GEMINI_API_KEY=your-key-here
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

6. **Open App**
   ```bash
   heroku open
   ```

**Cost:**
- Free tier: Limited hours
- Hobby: $7/month
- Standard: $25-50/month

---

### Option 3: AWS EC2

**Pros:**
- ✅ Full control
- ✅ High performance
- ✅ Scalable
- ✅ Custom configuration

**Steps:**

1. **Launch EC2 Instance**
   - Choose Ubuntu 22.04 LTS
   - Instance type: t2.medium (minimum)
   - Configure security group (port 8501)

2. **Connect to Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx -y
   ```

4. **Setup Application**
   ```bash
   # Clone repository
   git clone your-repo-url
   cd excel-insight-generator
   
   # Create virtual environment
   python3 -m venv .venv
   source .venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Configure environment
   nano .env
   # Add your API keys
   ```

5. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/streamlit.service
   ```

   Add:
   ```ini
   [Unit]
   Description=Streamlit Excel Insights App
   After=network.target
   
   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/excel-insight-generator
   Environment="PATH=/home/ubuntu/excel-insight-generator/.venv/bin"
   ExecStart=/home/ubuntu/excel-insight-generator/.venv/bin/streamlit run app.py --server.port 8501
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

6. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/streamlit
   ```

   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

7. **Enable and Start Services**
   ```bash
   sudo systemctl enable streamlit
   sudo systemctl start streamlit
   sudo systemctl enable nginx
   sudo systemctl restart nginx
   ```

8. **Setup SSL (Optional but Recommended)**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d your-domain.com
   ```

**Cost:**
- t2.medium: ~$35/month
- t2.large: ~$70/month
- Storage: ~$10/month for 100GB

---

### Option 4: Google Cloud Run

**Pros:**
- ✅ Serverless
- ✅ Auto-scaling
- ✅ Pay per use

**Steps:**

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.10-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 8080
   
   CMD streamlit run app.py --server.port 8080 --server.address 0.0.0.0
   ```

2. **Build and Push Image**
   ```bash
   # Install Google Cloud SDK
   gcloud init
   
   # Build image
   gcloud builds submit --tag gcr.io/your-project-id/excel-insights
   ```

3. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy excel-insights \
     --image gcr.io/your-project-id/excel-insights \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars OPENAI_API_KEY=your-key,GEMINI_API_KEY=your-key
   ```

**Cost:**
- Free tier: 2 million requests/month
- After: ~$0.00002400 per request

---

## 🔒 Security Best Practices

### 1. Environment Variables

**Never commit `.env` file to Git!**

```bash
# Ensure .gitignore includes:
.env
*.env
.env.local
```

### 2. API Key Management

**Use Secret Managers:**

- **AWS**: AWS Secrets Manager
- **Google Cloud**: Secret Manager
- **Azure**: Key Vault
- **Heroku**: Config Vars

### 3. File Upload Security

Add to `app.py`:
```python
# Limit file size
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB

# Validate file type
ALLOWED_EXTENSIONS = {'.xlsx', '.xls', '.csv'}

def validate_file(file):
    if file.size > MAX_FILE_SIZE:
        raise ValueError("File too large")
    
    ext = Path(file.name).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Invalid file type")
```

### 4. Rate Limiting

Add to prevent abuse:
```python
import streamlit as st
from datetime import datetime, timedelta

def check_rate_limit():
    if 'last_analysis' not in st.session_state:
        st.session_state.last_analysis = datetime.now()
        return True
    
    time_diff = datetime.now() - st.session_state.last_analysis
    if time_diff < timedelta(seconds=30):
        st.error("Please wait 30 seconds between analyses")
        return False
    
    st.session_state.last_analysis = datetime.now()
    return True
```

### 5. HTTPS

Always use HTTPS in production:
- Streamlit Cloud: Automatic
- Heroku: Automatic
- AWS/GCP: Use Load Balancer or Nginx with SSL

---

## 📊 Performance Optimization

### 1. Caching

Add to modules:
```python
import streamlit as st

@st.cache_data
def load_data(file):
    return pd.read_excel(file)

@st.cache_resource
def get_ai_model(model_name):
    return AIInsightsGenerator(model=model_name)
```

### 2. Async Processing

For large files:
```python
import asyncio

async def process_large_file(df):
    # Process in chunks
    chunk_size = 10000
    for i in range(0, len(df), chunk_size):
        chunk = df[i:i+chunk_size]
        await process_chunk(chunk)
```

### 3. Database for Results

Store results in database:
```python
# Use SQLite for small deployments
import sqlite3

# Or PostgreSQL for production
import psycopg2
```

---

## 📈 Monitoring

### 1. Application Monitoring

**Streamlit Cloud:**
- Built-in analytics
- View in dashboard

**Custom Deployment:**
```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info(f"Analysis started for file: {filename}")
```

### 2. Error Tracking

Use Sentry:
```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

### 3. Usage Analytics

Track usage:
```python
def log_usage(event_name, properties):
    # Log to analytics service
    analytics.track(event_name, properties)
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python test_modules.py
    
    - name: Deploy to Streamlit Cloud
      run: |
        # Deployment commands
```

---

## 📋 Pre-Deployment Checklist

- [ ] All API keys in environment variables
- [ ] `.env` file in `.gitignore`
- [ ] Error handling implemented
- [ ] File size limits configured
- [ ] Rate limiting enabled
- [ ] HTTPS configured
- [ ] Monitoring setup
- [ ] Backup strategy in place
- [ ] Documentation updated
- [ ] Tests passing

---

## 🆘 Troubleshooting Deployment

### Issue: App crashes on startup

```bash
# Check logs
streamlit run app.py --logger.level=debug

# Or on cloud platform
heroku logs --tail
```

### Issue: Out of memory

```bash
# Increase instance size
# Or optimize data processing:
df = pd.read_csv(file, chunksize=10000)
```

### Issue: Slow performance

```bash
# Add caching
# Reduce file size limits
# Use faster instance type
```

---

## 📞 Support Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Heroku Docs**: https://devcenter.heroku.com
- **AWS Docs**: https://docs.aws.amazon.com
- **GCP Docs**: https://cloud.google.com/docs

---

## 🎯 Recommended Deployment

**For Testing/Personal Use:**
- Streamlit Cloud (Free)

**For Small Teams:**
- Streamlit Cloud or Heroku Hobby ($7/month)

**For Production/Enterprise:**
- AWS EC2 or Google Cloud Run
- Custom domain
- SSL certificate
- Monitoring and backups

---

**Good luck with your deployment! 🚀**

# 🚀 MindMate Deployment Guide

This guide covers deploying MindMate to various platforms.

---

## Table of Contents

1. [Local Deployment](#local-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Platforms](#cloud-platforms)
4. [Production Checklist](#production-checklist)
5. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Local Deployment

### Development Mode

```bash
# Backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run dev
```

### Production Mode (Local)

```bash
# Backend with production settings
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4

# Frontend build
cd frontend
npm run build
npm run preview
```

---

## Docker Deployment

### Single Container (Backend Only)

```bash
# Build image
docker build -t mindmate-backend .

# Run container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  --name mindmate-backend \
  mindmate-backend
```

### Multi-Container with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped

  # Optional: Add frontend, Redis, etc.
```

---

## Cloud Platforms

### 1. Render (Recommended for Beginners)

**Backend Deployment:**

1. Create account at [render.com](https://render.com)
2. Connect GitHub repository
3. Create new Web Service
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3.10
5. Add environment variables if needed
6. Deploy!

**Frontend Deployment:**

1. Create new Static Site
2. Configure:
   - **Build Command:** `cd frontend && npm install && npm run build`
   - **Publish Directory:** `frontend/dist`
3. Deploy!

**Estimated Cost:** Free tier available

---

### 2. Railway

**Quick Deploy:**

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

**Or use Railway Dashboard:**
1. Connect GitHub repo
2. Railway auto-detects Python/Node
3. Configure start command
4. Deploy

**Estimated Cost:** $5-20/month

---

### 3. Heroku

**Backend:**

Create `Procfile`:
```
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```

Deploy:
```bash
heroku create mindmate-backend
git push heroku main
```

**Frontend:**

Deploy to Heroku or use Vercel/Netlify for better performance.

**Estimated Cost:** $7-25/month

---

### 4. AWS (Advanced)

**Architecture:**

```
Route 53 (DNS)
    ↓
CloudFront (CDN) → S3 (Frontend)
    ↓
ALB (Load Balancer)
    ↓
ECS/Fargate (Backend containers)
    ↓
├─ ElastiCache (Redis)
└─ RDS (PostgreSQL)
```

**Steps:**

1. **Backend on ECS:**
   - Build Docker image
   - Push to ECR
   - Create ECS task definition
   - Deploy to Fargate

2. **Frontend on S3 + CloudFront:**
   - Build frontend: `npm run build`
   - Upload to S3 bucket
   - Configure CloudFront distribution

3. **Database:**
   - Create RDS PostgreSQL instance
   - Update connection strings

**Estimated Cost:** $50-200/month

---

### 5. Google Cloud Platform

**Backend on Cloud Run:**

```bash
# Build and deploy
gcloud run deploy mindmate-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Frontend on Firebase Hosting:**

```bash
cd frontend
npm run build
firebase init hosting
firebase deploy
```

**Estimated Cost:** $20-100/month

---

### 6. Vercel (Frontend) + Render (Backend)

**Best for:** Quick deployment with minimal config

**Frontend on Vercel:**
1. Connect GitHub repo
2. Set root directory to `frontend`
3. Deploy automatically

**Backend on Render:**
(See Render section above)

**Estimated Cost:** Free tier available

---

## Production Checklist

### Security

- [ ] Enable HTTPS/TLS
- [ ] Set up proper CORS origins (not `*`)
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting
- [ ] Add authentication if needed
- [ ] Sanitize user inputs
- [ ] Enable security headers

**Example CORS update in app.py:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Not "*"
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

### Performance

- [ ] Use production ASGI server (Gunicorn + Uvicorn)
- [ ] Enable model caching
- [ ] Set up CDN for frontend
- [ ] Optimize model size (quantization)
- [ ] Configure proper logging
- [ ] Set up health checks

**Production server command:**
```bash
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Reliability

- [ ] Set up error monitoring (Sentry)
- [ ] Configure automated backups
- [ ] Implement graceful shutdown
- [ ] Add retry logic for API calls
- [ ] Set up uptime monitoring
- [ ] Create incident response plan

### Scalability

- [ ] Use Redis for session storage
- [ ] Implement database connection pooling
- [ ] Set up horizontal scaling (multiple instances)
- [ ] Use message queue for async tasks
- [ ] Configure auto-scaling rules

### Compliance

- [ ] Add privacy policy
- [ ] Implement data retention policy
- [ ] Ensure GDPR compliance (if EU users)
- [ ] Add cookie consent (if needed)
- [ ] Document data handling procedures

---

## Environment Variables

Create `.env` file (never commit to git):

```env
# API Settings
API_HOST=0.0.0.0
API_PORT=8000

# Model Paths
EMOTION_MODEL_DIR=./models/emotion_detector
RESPONSE_MODEL_DIR=./models/response_model

# Crisis Detection
CRISIS_REGION=india

# Database (if using)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Redis (if using)
REDIS_URL=redis://localhost:6379/0

# Monitoring
SENTRY_DSN=your-sentry-dsn

# Security
SECRET_KEY=your-secret-key
ALLOWED_ORIGINS=https://yourdomain.com
```

Load in app.py:
```python
from dotenv import load_dotenv
import os

load_dotenv()

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
```

---

## Monitoring & Maintenance

### Logging

**Setup structured logging:**

```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('mindmate.log', maxBytes=10485760, backupCount=5),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("mindmate")
```

### Error Tracking

**Integrate Sentry:**

```bash
pip install sentry-sdk
```

```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

### Uptime Monitoring

**Free services:**
- UptimeRobot
- Pingdom
- StatusCake

**Setup:**
1. Create account
2. Add health check URL: `https://yourdomain.com/health`
3. Configure alerts

### Performance Monitoring

**Track metrics:**
- Response time (p50, p95, p99)
- Error rate
- Request volume
- Model inference time
- Memory usage

**Tools:**
- Prometheus + Grafana
- DataDog
- New Relic

---

## Backup & Recovery

### Database Backups

```bash
# PostgreSQL backup
pg_dump dbname > backup.sql

# Restore
psql dbname < backup.sql
```

### Model Backups

```bash
# Backup models to cloud storage
aws s3 sync ./models s3://your-bucket/models/

# Restore
aws s3 sync s3://your-bucket/models/ ./models
```

---

## Scaling Strategies

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Use GPU instances for faster inference
- Optimize model size

### Horizontal Scaling
- Deploy multiple backend instances
- Use load balancer
- Implement session affinity or shared storage

### Model Optimization
- Quantize models (INT8)
- Use ONNX runtime
- Batch inference requests
- Cache frequent responses

---

## Cost Optimization

### Tips to Reduce Costs

1. **Use free tiers:**
   - Render: Free for small apps
   - Vercel: Free for frontend
   - Railway: $5 credit/month

2. **Optimize resources:**
   - Use smaller model variants
   - Implement request caching
   - Set up auto-scaling with min instances

3. **Choose right platform:**
   - Development: Local/Docker
   - Small project: Render/Railway
   - Production: AWS/GCP with reserved instances

---

## Troubleshooting

### Common Issues

**Models not loading:**
- Check disk space
- Verify model paths
- Ensure sufficient memory

**High latency:**
- Enable model caching
- Use GPU instances
- Implement request queuing

**Out of memory:**
- Reduce batch size
- Use model quantization
- Increase server RAM

**CORS errors:**
- Update allowed origins
- Check request headers
- Verify credentials setting

---

## Next Steps

After deployment:

1. **Test thoroughly** in production environment
2. **Set up monitoring** and alerts
3. **Document** deployment process
4. **Create** rollback plan
5. **Monitor** performance and errors
6. **Iterate** based on user feedback

---

## Support

For deployment issues:
- Check platform documentation
- Review logs for errors
- Test locally first
- Consult community forums

---

**Remember:** Always test in staging before deploying to production!

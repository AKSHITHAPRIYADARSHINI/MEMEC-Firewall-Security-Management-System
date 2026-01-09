# Docker Setup - Firewall Security Management System

## Quick Start

### Build and Run with Docker Compose

```bash
# Navigate to project directory
cd material-dashboard-flask

# Build the Docker image
docker-compose build

# Start the container
docker-compose up -d

# View logs
docker-compose logs -f firewall-dashboard
```

### Access the Application

- **URL:** http://localhost:5000
- **Login Page:** http://localhost:5000/login
- **Admin Dashboard:** http://localhost:5000/admin/users

### Default Credentials

Create a test user by registering at http://localhost:5000/register

### Stop the Container

```bash
docker-compose down
```

---

## Dockerfile Explanation

- **Base Image:** Python 3.11-slim (lightweight)
- **Dependencies:** Installed from requirements.txt
- **Server:** Waitress (production-grade WSGI server)
- **Port:** 5000 (exposed)
- **Health Check:** Every 30 seconds

---

## Docker Compose Features

✅ **Auto-restart:** Container restarts on failure  
✅ **Health Check:** Monitors application health  
✅ **Volume Mounts:** Live code and database updates  
✅ **Network:** Isolated network for security  
✅ **Environment Variables:** Production configuration  

---

## Environment Variables

```env
DEBUG=False                 # Disable debug mode
FLASK_ENV=production        # Production environment
DISABLE_SCHEDULER=True      # Disable APScheduler
```

---

## Troubleshooting

### Port 5000 Already in Use

```bash
# Change port in docker-compose.yml
# Change "5000:5000" to "8000:5000" for example
docker-compose down
docker-compose up -d
```

### View Container Logs

```bash
docker-compose logs firewall-dashboard
```

### Rebuild Image

```bash
docker-compose build --no-cache
docker-compose up -d
```

### Access Container Shell

```bash
docker-compose exec firewall-dashboard bash
```

---

## Performance Benefits

✅ Isolated environment - No Windows performance impact  
✅ Lightweight Linux container - Fast startup  
✅ Production WSGI server - Better performance  
✅ Minimal dependencies - Smaller image size  
✅ Easy deployment - Same setup anywhere  

---


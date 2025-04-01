# Deployment Guide for Agri_con

This guide explains how to deploy the Agri_con application using Nginx and Gunicorn on a Ubuntu/Debian server.

## Prerequisites

- A server running Ubuntu 20.04 or later
- A domain name pointed to your server's IP address
- Python 3.8+ installed
- Git installed

## Step 1: Clone the Repository

```bash
git clone https://github.com/garvitrai25/Agri_con.git
cd Agri_con
```

## Step 2: Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Set Environment Variables

Create a `.env` file in the project root:

```bash
touch .env
```

Add the following environment variables:

```
DEBUG=False
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
EMAIL_HOST_PASSWORD=your_email_password_here
```

## Step 5: Set Up Database and Static Files

```bash
python manage.py migrate
python manage.py collectstatic --no-input
```

## Step 6: Create Gunicorn Service

Create a systemd service file for Gunicorn:

```bash
sudo nano /etc/systemd/system/gunicorn_agricon.service
```

Add the following content (replace paths and user as needed):

```
[Unit]
Description=gunicorn daemon for Agri_con
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/path/to/Agri_con
ExecStart=/path/to/Agri_con/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/path/to/Agri_con/agricon.sock core.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start and enable the Gunicorn service:

```bash
sudo systemctl start gunicorn_agricon
sudo systemctl enable gunicorn_agricon
```

## Step 7: Configure Nginx

Install Nginx if not already installed:

```bash
sudo apt update
sudo apt install nginx
```

Create an Nginx server block:

```bash
sudo nano /etc/nginx/sites-available/agricon
```

Add the following configuration (replace yourdomain.com with your actual domain):

```
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/Agri_con;
    }

    location /media/ {
        root /path/to/Agri_con;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/Agri_con/agricon.sock;
    }
}
```

Enable the site and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/agricon /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 8: Set Up SSL with Let's Encrypt

Install Certbot:

```bash
sudo apt install certbot python3-certbot-nginx
```

Obtain and configure SSL certificate:

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Follow the prompts to complete the SSL setup.

## Step 9: Test the Deployment

Visit your website at https://yourdomain.com to make sure everything is working correctly.

## Troubleshooting

- Check Gunicorn logs: `sudo journalctl -u gunicorn_agricon`
- Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
- Make sure file permissions are set correctly
- Verify that the socket file is being created
- Ensure that the ALLOWED_HOSTS setting includes your domain name

## Maintenance

- To update the application:
  ```bash
  cd /path/to/Agri_con
  git pull
  source venv/bin/activate
  pip install -r requirements.txt
  python manage.py migrate
  python manage.py collectstatic --no-input
  sudo systemctl restart gunicorn_agricon
  ```

- To monitor the application, consider setting up monitoring tools like Prometheus or Datadog. 
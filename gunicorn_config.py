import multiprocessing

# Gunicorn config variables
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 120
keepalive = 5
worker_class = "gthread"
threads = 4
proc_name = "agricon"
accesslog = "-"
errorlog = "-"
loglevel = "info"
forwarded_allow_ips = "*" 
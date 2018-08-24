import multiprocessing

try:
    import gevent
    worker_class = 'gevent'
except ImportError:
    pass
bind = "127.0.0.1:20003"
workers = multiprocessing.cpu_count()*2+1


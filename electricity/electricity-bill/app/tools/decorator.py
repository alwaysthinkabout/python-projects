from functools import wraps
from threading import Thread


def async(f):
    """
    异步执行函数.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        # https://docs.python.org/2/library/threading.html#threading.Thread.daemon
        # 重启Flask服务器时中止正在执行的异步线程
        thr.setDaemon(True)
        thr.start()

    return wrapper

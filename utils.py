import time


def timer(f):
    """Декоратор замер времени выполнения функции или метода"""
    def tmp(*args, **kwargs):
        # file = open('c:/#tmp/123.txt', 'a')
        # file = open('/home/rond/#tmp/123.txt', 'a')
        t = time.time()
        res = f(*args, **kwargs)
        print('Время выполнения "{}": {}'.format(f.__name__, time.time()-t))
        # print('Время выполнения "{0}": {1:.5f}'.format(f.__name__, time.time()-t), file=file)
        return res
    return tmp

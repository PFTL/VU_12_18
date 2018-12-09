from PyQt5 import QtCore


class WorkerThread(QtCore.QThread):
    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.function(*self.args, **self.kwargs)
        return


if __name__ == '__main__':
    from time import sleep

    def test_function(n):
        for i in range(n):
            print(i)
            sleep(i/10)

    worker_thread = WorkerThread(test_function, 10)
    worker_thread.start()
    print('I am starting to run')
    while worker_thread.isRunning():
        sleep(0.2)
        print('Still working')

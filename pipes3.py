from __future__ import print_function

class PipelineException(Exception):
    def __init__(self, stage, e):
        self.stage = stage
        self.e = e

    def __str__(self):
        return repr('Pipeline failed at stage \'%s\' with exception: %s' %
                    (getattr(self.stage, '__name__'), self.e))


class PipelineStopExc(PipelineException):
    def __init__(self, stage, reason, result=None):
        super(PipelineStopExc, self).__init__(stage, None)
        self.reason = reason
        self.result = result

    def __str__(self):
        return repr('Pipeline stopped at stage %s: %s' %
                    (getattr(self.stage, '__name__'), self.reason))


class Pipeline(object):
    def __init__(self, func):
        self.func = func
        self.next = None

    def apply(self, *args):
        try:
            res = self.func(*args)
        except PipelineStopExc as s:
            raise s
        except (BaseException, Exception) as e:
            raise PipelineException(self.func, e) from e
        else:
            if self.next is None:
                return res
            else:
                return self.next.apply(res)

    def chain(self, func):
        if self.next is None:
            self.next = Pipeline(func)
        else:
            self.next.chain(func)
        return self

    def __call__(self, *args, **kwargs):
        return self.apply(*args)


if __name__ == '__main__':

    def fun(x, y):
        return x + y

    def square(x):
        return x*x

    def inc(x):
        return x + 1

    def read_file(name):
        # raise PipelineStopExc(read_file, 'won\'t read the file', None)
        with open(name) as f:
            return f.read()

    def count_words(txt):
        return len(txt.split())

    p = Pipeline(fun)

    print(p.chain(lambda x: x + 1).apply(1, 1))

    try:
        word_count = Pipeline(read_file).chain(count_words).apply('./pipes3.py')
        #word_count = Pipeline(read_file).chain(count_words)('./pipes3.py')
    except PipelineStopExc as stop:
        print(stop, stop.result)
    #except PipelineException as pex:
    #    print(pex)
    else:
        print(word_count)

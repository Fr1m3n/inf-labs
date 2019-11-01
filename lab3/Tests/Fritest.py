import time

class Tester:

    def __init__(self):
        self.funcs = []

        def _pass():
            pass

        self.pre_test_function = _pass

    def pre_test(self, func):
        self.pre_test_function = func

        def decor():
            func()

        return decor

    def test(self, func):
        # print(func.__name__)
        self.funcs.append(func)

        def decor():
            func()

        return decor

    def equals_to(self, actual, expected):
        assert actual == expected, "\nExpected: " + str(expected) + "\nActual: " + str(actual)

    def run_tests(self, count=10):
        passed = 0
        failed = 0
        total = len(self.funcs)
        summary = []
        print("=======Start testing. Count of iterations: {}.======".format(count))
        for i, fun in enumerate(self.funcs):
            print('\n' + '-' * 2, "Testing ", fun.__name__)
            self.pre_test_function()
            summary_time = 0
            min_time = 10**200
            max_time = 0
            for j in range(count):
                start_time = time.clock()
                fun()
                run_time = time.clock() - start_time
                min_time = min(run_time, min_time)
                max_time = max(run_time, max_time)
                summary_time += run_time
            avg_time = summary_time / count
            summary.append({'name': fun.__name__, 'time': avg_time})
            passed += 1
            print('-' * 3, "Test", i, "passed. Avg: {}. Min: {}. Max: {}".format(
                avg_time,
                min_time,
                max_time
            ))


        print("Testing completed. Passed: {}. Failed: {}. Total: {}".format(passed,
                                                                            failed,
                                                                            total))
        print('\n\n----------TOP----------')
        for i, j in enumerate(sorted(summary, key=lambda x: x['time'])):
            print('{}: {}. Avg: {}'.format(
                i,
                j['name'],
                j['time']
            ))
        print("\n=========END========")



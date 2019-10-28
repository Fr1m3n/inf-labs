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

    def run_tests(self):
        passed = 0
        failed = 0
        total = len(self.funcs)
        print("=======Start testing.======")
        for i, fun in enumerate(self.funcs):
            print('\n' + '-' * 2, "Testing ", fun.__name__)
            self.pre_test_function()
            try:
                fun()
                passed += 1
                print('-' * 3, "Test", i, "passed.")
            except AssertionError as e:
                failed += 1
                print('-' * 3, "Test", i, "failed.", str(e))

        print("Testing completed. Passed: {}. Failed: {}. Total: {}".format(passed,
                                                                            failed,
                                                                            total))
        print("=========END========")



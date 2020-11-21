import unittest
import dow_main
import os


class MyTestCase(unittest.TestCase):
    def test_get_file(self):
        dd = dow_main.get_file()
        self.assertEqual(len(dd) > 0, True)

    def test_rsi(self):
        dd = dow_main.get_file()
        dd['RSI'] = dow_main.RSI(dd['Adj Close'])
        self.assertEqual(dd.RSI.mean() > 0, True)

    def test_plots(self):
        dow_main.plots("MSFT")
        self.assertEqual(os.path.exists("RSI.png"), True)
        self.assertEqual(os.path.exists("Volume.png"), True)
        self.assertEqual(os.path.exists("Adj Close.png"), True)



if __name__ == '__main__':
    unittest.main()

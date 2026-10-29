import unittest
from main import diagnose


class TestDiagnose(unittest.TestCase):
    def test_dns(self):
        self.assertEqual(diagnose("DNS não resolve")['category'], 'dns')

    def test_network(self):
        self.assertEqual(diagnose("Sem internet")['category'], 'network')

    def test_computer(self):
        self.assertEqual(diagnose("PC não liga")['category'], 'computer')

    def test_unknown(self):
        self.assertEqual(diagnose("Impressora sem papel")['category'], 'unknown')

    def test_empty(self):
        with self.assertRaises(ValueError):
            diagnose('  ')


if __name__ == '__main__':
    unittest.main()

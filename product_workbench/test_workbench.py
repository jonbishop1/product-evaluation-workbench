import unittest
from .costs import estimate
from .evidence import assess_task, official_host
from .history import snapshot, compare


class WorkbenchTests(unittest.TestCase):
    def test_bucket_boundary_and_daily_limit(self):
        p = dict(base="20", included=50000, overage_per_1000="0.90", rounding="bucket")
        self.assertEqual(str(estimate(p, 50001)["total"]), "20.90")
        self.assertEqual(str(estimate(p, 51000)["total"]), "20.90")
        self.assertEqual(str(estimate(p, 51001)["total"]), "21.80")
        self.assertEqual(str(estimate(p, 100000)["total"]), "65.00")
        free = dict(base="0", included=3000, overage_per_1000=None, rounding="bucket", daily_limit=100)
        self.assertFalse(estimate(free, 2000, 101)["available"])
        self.assertFalse(estimate(free, 3001, 100)["available"])
        for bad in (-1, 1.5, True, 10000001):
            with self.assertRaises(ValueError): estimate(p, bad)

    def test_sources_do_not_establish_execution(self):
        self.assertFalse(assess_task([dict(state="observed", evidence="A quickstart link is visible.")])["execution_verified"])
        with self.assertRaises(ValueError): assess_task([dict(state="executed", evidence="It worked.")])
        with self.assertRaises(ValueError): assess_task([dict(state="observed", evidence="")])
        self.assertTrue(assess_task([dict(state="executed", evidence="Expected fixture output matches.", output_verified=True)])["execution_verified"])

    def test_domain_identity_is_not_substring_or_shared_host_matching(self):
        self.assertEqual(official_host("https://docs.example.com/path"), "example.com")
        self.assertEqual(official_host("https://example.com.evil.test/"), "example.com.evil.test")
        self.assertEqual(official_host("https://github.com/example/project"), "")
        self.assertEqual(official_host("https://unrelated.readme.io/"), "")
        self.assertEqual(official_host("https://user:password@example.com/"), "")

    def test_history_requires_comparable_chronological_captures(self):
        first = snapshot("https://example.com/", "first body", "2026-10-15T00:00:00Z")
        second = snapshot("https://example.com/", "second body", "2026-10-16T00:00:00Z")
        self.assertEqual(compare(first, second)["state"], "content_changed")
        with self.assertRaises(ValueError): compare(second, first)
        with self.assertRaises(ValueError): compare(first, {**second, "source": "https://other.test/"})
        with self.assertRaises(ValueError): snapshot("https://example.com", "", "2026-10-16")


if __name__ == "__main__": unittest.main()

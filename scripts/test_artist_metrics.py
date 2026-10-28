"""Small, independent expected-value tests; no downloads."""
import math
import statistics
import unittest

from artist_metrics import (COLS, EXCLUDED, consume, hist_median, metrics,
                            new_state, quantile, CONTENT_COL, flags_for, spearman,
                            average_ranks, load_user_inputs)


class AggregationTests(unittest.TestCase):
    def test_exact_histogram_median(self):
        from collections import Counter
        for values in [[], [0], [-5, 9], [3, 3, 3, 20], [-2, 0, 1, 7, 8]]:
            expected = statistics.median(values) if values else None
            self.assertEqual(hist_median(Counter(values)), expected)

    def test_deleted_multiple_artists_global_baseline_and_exact_tags(self):
        s = new_state([("a", 10), ("b", 5), ("missing", 1)], "test", [])
        records = [
            ("a b a", 10, 2, "sketch shiny_skin realistic", "g", "2020-01-01T00:00:00+00:00", False),
            ("a", 30, 8, "sketchbook monochrome_picture realistic", "s", "2020-12-31T23:00:00-05:00", False),
            ("", 100, 0, "", "e", "2020-02-01T00:00:00+00:00", False),
            ("a", 10000, 10000, "comic", "e", "2020-03-01T00:00:00+00:00", True),
            ("a", 6, 5, "mature_female", "q", "2021-01-02T00:00:00+00:00", False),
            ("other", 2, 0, "", "g", "2021-01-01T00:00:00+00:00", False),
            (EXCLUDED, 5, 0, "comic greyscale", "g", "2022-01-01T00:00:00+00:00", False),
        ]
        consume(s, {c: [r[i] for r in records] for i, c in enumerate(COLS)})
        baseline = {y: hist_median(h) for y, h in s["years"].items()}
        self.assertEqual(baseline, {2020: 30, 2021: 4, 2022: 5})
        a = metrics(s["artists"]["a"], baseline)
        self.assertEqual((s["rows"], s["deleted"], s["kept"], s["multi_artist"]), (7, 1, 6, 1))
        self.assertEqual(a["posts"], 3)
        self.assertAlmostEqual(a["score_mean"], 46 / 3)
        self.assertEqual(a["score_median"], 10)
        self.assertAlmostEqual(a["fav_mean"], 5)
        self.assertAlmostEqual(a["score_norm"], statistics.mean([10 / 30, 30 / 30, 6 / 4]))
        self.assertEqual(a["low_ratio"], 1 / 3)
        self.assertEqual(a[CONTENT_COL], 2 / 3)
        self.assertEqual(a["last_post"], "2021-01-02T00:00:00+00:00")
        self.assertTrue(math.isclose(sum(a[c] for c in "gsqe"), 1))
        self.assertEqual(s["artists"]["b"]["n"], 1)
        self.assertEqual(metrics(s["artists"][EXCLUDED], baseline)["low_ratio"], 1)
        empty = metrics(s["artists"]["missing"], baseline)
        self.assertEqual(empty["posts"], 0)
        self.assertIsNone(empty["low_ratio"])
        self.assertIsNone(metrics(s["artists"]["a"], {2020: 0, 2021: 4})["score_norm"])

    def test_quantile_type7_and_missing(self):
        self.assertEqual(quantile([0, 1, 2, 3, None], .75), 2.25)
        self.assertEqual(quantile([.2, .2, .2, .2], .75), .2)
        self.assertIsNone(quantile([None], .75))

    def test_spearman_ties_missing_and_direction(self):
        self.assertEqual(average_ranks([20, 10, 20, 30]), [2.5, 1.0, 2.5, 4.0])
        self.assertEqual(spearman([(1, 1), (2, 2), (3, 3), (None, 4), (4, "")]), (1.0, 3))
        self.assertEqual(spearman([(1, 3), (2, 2), (3, 1)]), (-1.0, 3))
        self.assertAlmostEqual(spearman([(1, 1), (1, 2), (2, 3)])[0], 3 ** .5 / 2)
        self.assertEqual(spearman([(1, 2), (1, 3)]), (None, 2))
        self.assertEqual(spearman([(1, 2)]), (None, 1))

    def test_flags_boundaries_and_no_content_recommendation(self):
        self.assertEqual(flags_for({"low_ratio": .5, "posts": 29, CONTENT_COL: 1}), "흑백만화비중높음;표본부족")
        self.assertEqual(flags_for({"low_ratio": .499, "posts": 30, CONTENT_COL: 1}), "")
        self.assertEqual(flags_for({"low_ratio": None, "posts": 0}), "표본부족")

    def test_pool_normalization_rank_values_and_duplicates(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as d:
            pool, ranks = Path(d)/"pool.txt", Path(d)/"ranks.csv"
            pool.write_text("foo bar, a_(b c), independent", encoding="utf-8")
            ranks.write_text("태그,평균_순위,상위40_등장,등장_조합수\nfoo_bar,4.3,0,3\n", encoding="utf-8-sig")
            p, r, sources = load_user_inputs(pool, ranks)
            self.assertEqual(p, {"foo_bar", "a_(b_c)", "independent"})
            self.assertEqual(r["foo_bar"], {"평균_순위": 4.3, "상위40_등장": 0})
            self.assertNotIn("independent", r)
            self.assertEqual(sources["pool1"]["tags"], 3)
            pool.write_text("foo bar, foo_bar", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_user_inputs(pool, ranks)

    def test_invalid_missing_fields_fail(self):
        s = new_state([("a", 1)], "test", [])
        row = ("a", None, 0, "", "g", "2020-01-01T00:00:00Z", False)
        with self.assertRaises(ValueError):
            consume(s, {c: [row[i]] for i, c in enumerate(COLS)})


if __name__ == "__main__":
    unittest.main()

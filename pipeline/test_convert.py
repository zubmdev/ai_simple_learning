import re
import unittest

from pipeline.convert import convert, split_message, stats, warnings


RAW = "https://raw.githubusercontent.com/acme/course/main"
BLOB = "https://github.com/acme/course/blob/main"


class LinkConversion(unittest.TestCase):
    def test_relative_image_becomes_raw_url(self):
        out = convert(
            "![скрин](./images/cline-install.png)",
            "ru/beginner/Week_1/Day_2.md",
            RAW,
            BLOB,
        )
        self.assertIn(
            f"![скрин]({RAW}/ru/beginner/Week_1/images/cline-install.png)", out
        )

    def test_parent_relative_link_becomes_blob_url(self):
        out = convert("[Назад](../Day_0.md)", "ru/beginner/Week_1/Day_1.md", RAW, BLOB)
        self.assertIn(f"[Назад]({BLOB}/ru/beginner/Day_0.md)", out)

    def test_fragment_preserved_on_blob_link(self):
        out = convert(
            "[Раздел](./Day_2.md#цель)", "ru/beginner/Week_1/Day_1.md", RAW, BLOB
        )
        self.assertIn(f"({BLOB}/ru/beginner/Week_1/Day_2.md#цель)", out)

    def test_absolute_urls_untouched(self):
        src = "[Groq](https://console.groq.com) и ![x](https://example.com/a.png)"
        out = convert(src, "ru/beginner/Week_1/Day_1.md", RAW, BLOB)
        self.assertIn("[Groq](https://console.groq.com)", out)
        self.assertIn("![](https://example.com/a.png)", out)

    def test_plain_link_to_image_gets_raw_url(self):
        out = convert(
            "[скрин](./images/vscode.png)", "ru/beginner/Week_1/Day_2.md", RAW, BLOB
        )
        self.assertIn(f"[скрин]({RAW}/ru/beginner/Week_1/images/vscode.png)", out)

    def test_anchor_only_link_untouched(self):
        out = convert("[вверх](#todo)", "ru/beginner/Week_1/Day_1.md", RAW, BLOB)
        self.assertIn("[вверх](#todo)", out)

    def test_mailto_untouched(self):
        out = convert("[почта](mailto:a@b.c)", "ru/beginner/Week_1/Day_1.md", RAW, BLOB)
        self.assertIn("[почта](mailto:a@b.c)", out)

    def test_nested_path_normalized(self):
        out = convert(
            "[индекс](../../../README.md)", "ru/beginner/Week_1/Day_1.md", RAW, BLOB
        )
        self.assertIn(f"[индекс]({BLOB}/README.md)", out)


class MediaSeparation(unittest.TestCase):
    def test_inline_image_lifted_to_own_block(self):
        out = convert(
            "5. Нажми **Submit** ![ключ](./images/submit-key.png)",
            "ru/beginner/Week_1/Day_3.md",
            RAW,
            BLOB,
        )
        self.assertIn("5. Нажми **Submit**\n\n![](", out)
        self.assertIn(
            "](https://raw.githubusercontent.com/acme/course/main/ru/beginner/Week_1/images/submit-key.png)",
            out,
        )

    def test_standalone_image_line_untouched_structure(self):
        out = convert(
            "\n![скрин](./images/a.png)\n", "ru/beginner/Week_1/Day_1.md", RAW, BLOB
        )
        self.assertIn(f"\n![скрин]({RAW}/ru/beginner/Week_1/images/a.png)\n", out)

    def test_relative_link_inside_fence_untouched(self):
        out = convert(
            "текст\n\n```markdown\n[клик](./x.md)\n```\n",
            "ru/beginner/Week_1/Day_1.md",
            RAW,
            BLOB,
        )
        self.assertIn("[клик](./x.md)", out)

    def test_link_inside_inline_code_untouched(self):
        out = convert(
            "Пример: `[клик](./x.md)` в тексте",
            "ru/beginner/Week_1/Day_1.md",
            RAW,
            BLOB,
        )
        self.assertIn("`[клик](./x.md)`", out)

    def test_image_inside_fence_not_lifted(self):
        out = convert(
            "текст\n\n```\n![скрин](./images/a.png)\n```\n",
            "ru/beginner/Week_1/Day_1.md",
            RAW,
            BLOB,
        )
        self.assertIn("```\n![скрин](./images/a.png)\n```", out)

    def test_image_inside_inline_code_not_lifted(self):
        out = convert(
            "Шаблон: `![скрин](./images/a.png)`",
            "ru/beginner/Week_1/Day_1.md",
            RAW,
            BLOB,
        )
        self.assertIn("`![скрин](./images/a.png)`", out)


class Navigation(unittest.TestCase):
    def test_week_day_header_and_self_link(self):
        out = convert("# Урок\n\nтекст", "ru/beginner/Week_1/Day_2.md", RAW, BLOB)
        self.assertIn("**Неделя 1 · День 2**", out)
        self.assertIn(f"{BLOB}/ru/beginner/Week_1/Day_2.md", out)
        self.assertIn(f"{BLOB}/README.md", out)

    def test_day_zero_header(self):
        out = convert("# Введение\n\nтекст", "ru/beginner/Day_0.md", RAW, BLOB)
        self.assertIn("**День 0**", out)
        self.assertIn(f"{BLOB}/ru/beginner/Day_0.md", out)


class Splitting(unittest.TestCase):
    def test_short_text_single_part(self):
        self.assertEqual(split_message("a" * 100, 1000), ["a" * 100])

    def test_long_text_splits_on_hr(self):
        part1 = "а" * 600
        part2 = "б" * 600
        text = f"{part1}\n\n---\n\n{part2}"
        parts = split_message(text, 1000)
        self.assertEqual(len(parts), 2)
        self.assertTrue(all(len(p) <= 1000 for p in parts))

    def test_part_markers_added(self):
        text = "а" * 600 + "\n\n---\n\n" + "б" * 600
        parts = split_message(text, 1000)
        self.assertIn("часть 1/2", parts[0])
        self.assertIn("часть 2/2", parts[1])

    def test_hard_split_when_no_hr(self):
        text = "\n\n".join(["аб" * 400] * 3)
        parts = split_message(text, 1000)
        self.assertGreater(len(parts), 1)
        self.assertTrue(all(len(p) <= 1000 for p in parts))

    def test_hard_split_keeps_fence_intact(self):
        fence = "```python\n" + "x\n\n" * 200 + "```"
        text = "а" * 500 + "\n\n" + fence + "\n\n" + "б" * 800
        parts = split_message(text, 1000)
        self.assertGreater(len(parts), 1)
        self.assertTrue(all(p.count("```") % 2 == 0 for p in parts))
        self.assertTrue(all(len(p) <= 1000 for p in parts))

    def test_hr_inside_fence_not_split_point(self):
        fence = "```python\nintro\n\n---\n\nx = 1\n```"
        text = "а" * 600 + "\n\n" + fence + "\n\n" + "б" * 600
        parts = split_message(text, 1000)
        self.assertGreater(len(parts), 1)
        self.assertTrue(all(p.count("```") % 2 == 0 for p in parts))
        self.assertTrue(all(len(p) <= 1000 for p in parts))
        self.assertTrue(any("intro\n\n---\n\nx = 1" in p for p in parts))

    def test_hr_split_round_trip(self):
        text = "а" * 600 + "\n\n---\n\n" + "б" * 600
        parts = split_message(text, 1000)
        restored = "\n---\n".join(
            re.sub(r"\n\n\*\(часть \d+/\d+\)\*$", "", p) for p in parts
        )
        self.assertEqual(restored, text)


class Stats(unittest.TestCase):
    def test_counts_media_chars_blocks(self):
        text = "# Заголовок\n\nабзац\n\n![а](https://x/a.png)\n\n![б](https://x/b.png)\n\n- пункт\n- пункт"
        s = stats(text)
        self.assertEqual(s["media"], 2)
        self.assertEqual(s["blocks"], 6)
        self.assertGreater(s["chars"], 0)
        self.assertEqual(s["table_cols"], 0)

    def test_table_columns(self):
        text = "| а | б | в |\n|---|---|---|\n| 1 | 2 | 3 |"
        self.assertEqual(stats(text)["table_cols"], 3)

    def test_code_fence_content_not_counted_as_blocks(self):
        plain = "абзац один\n\nабзац два"
        fenced = "абзац один\n\n```python\nprint(1)\nprint(2)\n```\n\nабзац два"
        self.assertEqual(stats(plain)["blocks"] + 1, stats(fenced)["blocks"])


class Warnings(unittest.TestCase):
    def test_unsupported_html_flagged(self):
        issues = warnings(
            "<div>х</div>\n\n<details><summary>с</summary>ок</details>", 100
        )
        self.assertEqual(len(issues), 1)
        self.assertIn("<div>", issues[0])

    def test_leftover_relative_link_flagged(self):
        issues = warnings("[х](./y.png)", 100)
        self.assertEqual(len(issues), 1)

    def test_relative_link_inside_fence_not_flagged(self):
        issues = warnings("текст\n\n```markdown\n[клик](./x.md)\n```\n", 100)
        self.assertEqual(issues, [])

    def test_relative_link_inside_inline_code_not_flagged(self):
        issues = warnings("Пример: `[клик](./x.md)` в тексте", 100)
        self.assertEqual(issues, [])

    def test_html_inside_inline_code_not_flagged(self):
        issues = warnings("Шаблон: `<div>`", 100)
        self.assertEqual(issues, [])

    def test_clean_text_no_issues(self):
        self.assertEqual(warnings("# ОК\n\nтекст", 100), [])

    def test_oversize_flagged(self):
        issues = warnings("т" * 33000)
        self.assertEqual(len(issues), 1)
        self.assertIn("32768", issues[0])


class ConvertIntegration(unittest.TestCase):
    def test_converted_text_has_no_relative_links(self):
        src = "# День\n\n![а](./images/a.png)\n\n[дальше](./Day_2.md)\n"
        out = convert(src, "ru/beginner/Week_1/Day_1.md", RAW, BLOB)
        self.assertFalse(re.search(r"\]\(\.{1,2}/", out))


if __name__ == "__main__":
    unittest.main()

import unittest

from src.chunker import chunk_text, create_chunks


class ChunkTextTests(unittest.TestCase):
    def test_chunks_text_into_word_groups(self):
        text = "one two three four five"
        self.assertEqual(chunk_text(text, 2), ["one two", "three four", "five"])

    def test_returns_empty_list_for_empty_text(self):
        self.assertEqual(chunk_text(""), [])

    def test_rejects_non_string_input(self):
        with self.assertRaisesRegex(TypeError, "text must be a string"):
            chunk_text(None)

    def test_rejects_non_positive_chunk_size(self):
        with self.assertRaisesRegex(ValueError, "chunk_size must be greater than 0"):
            chunk_text("one two", 0)


class CreateChunksTests(unittest.TestCase):
    def test_creates_chunk_metadata_for_each_page(self):
        paper = {
            "filename": "sample.pdf",
            "num_pages": 2,
            "pages": [
                {"page_number": 1, "text": "alpha beta gamma delta"},
                {"page_number": 2, "text": "omega psi"},
            ],
        }

        chunks = create_chunks(paper, chunk_size=2)

        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks[0]["chunk_id"], 1)
        self.assertEqual(chunks[0]["page_number"], 1)
        self.assertEqual(chunks[0]["text"], "alpha beta")
        self.assertEqual(chunks[2]["page_number"], 2)
        self.assertEqual(chunks[2]["text"], "omega psi")

    def test_returns_empty_list_for_paper_without_pages(self):
        self.assertEqual(create_chunks({"pages": []}), [])

    def test_supports_overlapping_word_chunks(self):
        text = "one two three four five"
        self.assertEqual(
            chunk_text(text, chunk_size=3, overlap=1),
            ["one two three", "three four five"],
        )

    def test_rejects_invalid_overlap(self):
        with self.assertRaisesRegex(ValueError, "overlap must be less than chunk_size"):
            chunk_text("one two three", chunk_size=2, overlap=2)

    def test_create_chunks_preserves_overlap_metadata(self):
        paper = {
            "pages": [
                {"page_number": 1, "text": "alpha beta gamma delta epsilon"},
            ]
        }

        chunks = create_chunks(paper, chunk_size=3, overlap=1)

        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0]["text"], "alpha beta gamma")
        self.assertEqual(chunks[1]["text"], "gamma delta epsilon")
        self.assertEqual(chunks[1]["page_number"], 1)


if __name__ == "__main__":
    unittest.main()

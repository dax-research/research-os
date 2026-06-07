from src.pdf_reader import extract_text_from_pdf

paper = extract_text_from_pdf(
    "data/papers/attention_is_all_you_need.pdf"
)

print(paper["filename"])
print(paper["num_pages"])

print()
print("First Page:")
print()

print(paper["pages"][0]["text"][:1000])
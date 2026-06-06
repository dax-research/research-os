from src.pdf_reader import extract_text_from_pdf

paper = extract_text_from_pdf(
    "C:/Users/ketan/Workspace/research-os/data/papers/attention_is_all_you_need.pdf"
)

print(paper["filename"])
print(paper["num_pages"])
print(paper["text"][:1000])
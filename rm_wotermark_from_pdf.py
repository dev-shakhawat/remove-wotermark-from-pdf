import pikepdf
import glob
import os


input_folder = r"."  # input folder directory where pdf files are

# what you want to remove
watermark_text = "Educationblog24.com"

# ফোল্ডারের সব PDF ফাইল বের করা
pdf_files = glob.glob(os.path.join(input_folder, "*.pdf"))
print(f"total {len(pdf_files)} PDF files found in {input_folder}")

for file in pdf_files:
    print(f"\n➡️ Processing: {os.path.basename(file)}")
    pdf = pikepdf.open(file)

    for page_num, page in enumerate(pdf.pages, start=1):
        if "/Contents" in page:
            contents = page["/Contents"]

            if isinstance(contents, pikepdf.Array):
                combined_stream = b"".join([c.read_bytes() for c in contents])
                new_stream = combined_stream.decode("latin-1", errors="ignore")
                if watermark_text in new_stream:
                    print(f"Page {page_num}- woatermark found!")
                    new_stream = new_stream.replace(watermark_text, "")
                page["/Contents"] = pikepdf.Stream(pdf, new_stream.encode("latin-1"))
            else:
                stream = contents.read_bytes().decode("latin-1", errors="ignore")
                if watermark_text in stream:
                    print(f"page{page_num}- woatermark found!")
                    stream = stream.replace(watermark_text, "")
                page["/Contents"] = pikepdf.Stream(pdf, stream.encode("latin-1"))

    # new file name
    output_file = os.path.join(input_folder, f"clean_{os.path.basename(file)}")
    pdf.save(output_file)
    pdf.close()
    print(f" New file: {output_file}")

print("\n All done!")

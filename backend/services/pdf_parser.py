#Extracting words&lines with their bbox from documents

import fitz 

def extract_words(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    all_words = []
    all_lines = []

    for page_num, page in enumerate(doc):
        words = page.get_text("words")

        # sort words (important)
        words = sorted(words, key=lambda w: (w[1], w[0]))

        line = []
        current_y = None

        for w in words:
            x0, y0, x1, y1, text = w[:5]

            all_words.append({
                "text": text,
                "bbox": [x0, y0, x1, y1],
                "page": page_num
            })

            # Group words into lines
            if current_y is None:
                current_y = y0

            if abs(y0 - current_y) < 5:
                line.append((text, x0, y0, x1, y1))
            else:
                # save previous line
                full_text = " ".join([t[0] for t in line])
                all_lines.append({
                    "text": full_text,
                    "words": line,
                    "page": page_num
                })
                line = [(text, x0, y0, x1, y1)]
                current_y = y0

        # last line
        if line:
            full_text = " ".join([t[0] for t in line])
            all_lines.append({
                "text": full_text,
                "words": line,
                "page": page_num
            })

    return all_words, all_lines
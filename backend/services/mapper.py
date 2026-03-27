#mapping pii to word boxes of documents

def map_entities(entities, lines):
    results = []

    for entity in entities:
        entity_text = entity["text"].lower()

        for line in lines:
            if entity_text in line["text"].lower():

                # get combined bbox from words
                x0 = min(w[1] for w in line["words"])
                y0 = min(w[2] for w in line["words"])
                x1 = max(w[3] for w in line["words"])
                y1 = max(w[4] for w in line["words"])

                results.append({
                    "text": entity["text"],
                    "type": entity["type"],
                    "bbox": [x0, y0, x1, y1],
                    "page": line["page"]
                })

                break

    return results


def merge_boxes(boxes):
    x0 = min(b[0] for b in boxes)
    y0 = min(b[1] for b in boxes)
    x1 = max(b[2] for b in boxes)
    y1 = max(b[3] for b in boxes)

    return [x0, y0, x1, y1]
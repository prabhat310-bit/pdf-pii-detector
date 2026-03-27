#Main APP

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from services.pdf_parser import extract_words
from services.llm_service import detect_pii, parse_llm_output
from services.mapper import map_entities 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "PDF PII Detection API running"}

@app.get("/test")
async def test():
    return {"status": "ok"}

@app.post("/process")
async def process_pdf(file: UploadFile = File(...)):
    try:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files allowed")

        contents = await file.read()

        words, lines = extract_words(contents)

        if not words:
            raise HTTPException(status_code=400, detail="No text found in PDF")

        # Better text for LLM
        full_text = "\n".join([line["text"] for line in lines])

        raw_output = await detect_pii(full_text)

        entities = parse_llm_output(raw_output)

        if not isinstance(entities, list) or not entities:
            return {"results": []}

        mapped_results = map_entities(entities, lines)

        return {"results": mapped_results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
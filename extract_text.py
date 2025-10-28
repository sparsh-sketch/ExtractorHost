from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pdfminer.high_level import extract_text_to_fp
from io import BytesIO

app = FastAPI()

# Optional healthcheck so GETs don't 404:
@app.get("/")
def health():
    return {"status": "ok"}

# Main endpoint (POST a PDF file)
@app.post("/")
async def extract_text_endpoint(file: UploadFile = File(...)):
    data = await file.read()
    buf_in = BytesIO(data)
    buf_out = BytesIO()
    extract_text_to_fp(buf_in, buf_out)
    text = buf_out.getvalue().decode("utf-8", errors="ignore")
    return JSONResponse({"text": text})

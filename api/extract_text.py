from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from io import BytesIO

app = FastAPI()

# Try importing pdfminer lazily so health works even if install fails
_pdfminer_error = None
_extract_text_to_fp = None
try:
    from pdfminer.high_level import extract_text_to_fp as _extract_text_to_fp
except Exception as e:
    _pdfminer_error = e

@app.get("/")
def health():
    # Helpful status for debugging in Vercel
    return {
        "status": "ok",
        "pdfminer_loaded": _extract_text_to_fp is not None,
        "pdfminer_error": str(_pdfminer_error) if _pdfminer_error else None,
    }

@app.post("/")
async def extract_text_endpoint(file: UploadFile = File(...)):
    if _extract_text_to_fp is None:
        # Return a clear error if pdfminer isn't available
        return JSONResponse(
            {"error": "pdfminer.six not available", "detail": str(_pdfminer_error)},
            status_code=500,
        )

    data = await file.read()
    buf_in = BytesIO(data)
    buf_out = BytesIO()
    _extract_text_to_fp(buf_in, buf_out)
    text = buf_out.getvalue().decode("utf-8", errors="ignore")
    return JSONResponse({"text": text})

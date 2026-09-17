from typing import Optional

from detector import detect_nigerian_network, get_network_prefixes
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="Nigerian Network Detector", version="1.0.0")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class PhoneNumberRequest(BaseModel):
    phone_number: str

class DetectionResponse(BaseModel):
    success: bool
    phone_number: Optional[str] = None
    network: Optional[str] = None
    cleaned_number: Optional[str] = None
    error: Optional[str] = None

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/detect", response_model=DetectionResponse)
async def detect_network(request: PhoneNumberRequest):
    try:
        phone_number = request.phone_number
        
        if not phone_number:
            return DetectionResponse(
                success=False,
                error="Phone number is required"
            )
        
        result = detect_nigerian_network(phone_number)
        
        if result == "Invalid Nigerian number format":
            return DetectionResponse(
                success=False,
                error=result
            )
        
        # Extract cleaned number from the detection function
        from detector import clean_phone_number
        cleaned_number = clean_phone_number(phone_number)
        
        return DetectionResponse(
            success=True,
            phone_number=phone_number,
            network=result,
            cleaned_number=cleaned_number
        )
    
    except Exception as e:
        return DetectionResponse(
            success=False,
            error=str(e)
        )

@app.get("/api/networks")
async def get_networks():
    try:
        networks = get_network_prefixes()
        return {
            "success": True,
            "networks": networks
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

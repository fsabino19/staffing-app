from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class StaffingInput(BaseModel):
    buffer_depth: int
    inflow_rate: float
    processing_rate: float = 0.59
    target_clearance_rate: float = 0.75
    shift_length: int = 9

@app.post("/calculate_hc")
def calculate_staffing(body: StaffingInput):
    numerator = (body.buffer_depth * body.target_clearance_rate) + (body.inflow_rate * body.shift_length)
    denominator = body.processing_rate * body.shift_length

    hc = numerator / denominator
    recommended_hc = int(hc) if hc.is_integer() else int(hc) + 1

    return {
        "recommended_headcount": recommended_hc,
        "raw_output": hc
    } 
from rule_engine import validate_field
from fastapi import FastAPI

app = FastAPI()

@app.post("/validate/{field_code}")
def validate(field_code :str, value :str):
    result = validate_field(field_code, value)
    return {"field_code": field_code, "value": value, "result": result}
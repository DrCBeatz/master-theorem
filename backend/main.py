# main.py

import os
import boto3
from botocore.exceptions import ClientError
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import math
import numpy as np

DYNAMODB_ENDPOINT_URL = os.getenv("DYNAMODB_ENDPOINT_URL", "http://localhost:8000")

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=DYNAMODB_ENDPOINT_URL,
    region_name="us-east-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "fakeMyKeyId"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "fakeSecretAccessKey")
)

TABLE_NAME = "Algorithms"

# Pydantic model
class Algorithm(BaseModel):
    id: int
    name: str
    a: int
    b: int
    k: int
    description: str
    python_code: str
    case: str = ""
    time_complexity: str = ""
    complexity_analysis: str = ""

def check_regularity_condition(a: int, b: int, k: int) -> bool:
    return a / b**k < 1

def evaluate_master_theorem(a: int, b: int, k: int):
    if a <= 0:
        raise ValueError("Parameter 'a' must be greater than 0.")
    if b <= 1:
        raise ValueError("Parameter 'b' must be greater than 1.")
    
    log_b_a = math.log(a, b)
    log_b_a_is_integer = log_b_a.is_integer()

    CASE_1 = "Case 1: Θ(n<sup>log<sub>b</sub>(a)</sup>)"
    CASE_2 = "Case 2: Θ(n<sup>k</sup> log n)"
    CASE_3 = "Case 3: Θ(n<sup>k</sup>)"

    if log_b_a > k:
        complexity = f"Θ(n<sup>{int(log_b_a) if log_b_a_is_integer else f'log<sub>{b}</sub>({a})'}</sup>)"
        case = CASE_1
    elif math.isclose(log_b_a, k, rel_tol=1e-9):
        if k == 0:
            complexity = "Θ(log n)"
        elif k == 1:
            complexity = "Θ(n log n)"
        else:
            complexity = f"Θ(n<sup>{k}</sup> log n)"
        case = CASE_2
    else:  # log_b_a < k
        if k == 0:
            complexity = "Θ(1)"
            case = CASE_3
        elif k == 1:
            complexity = "Θ(n)"
            case = CASE_3
        else:
            complexity = f"Θ(n<sup>{k}</sup>)"
            case = CASE_3

    regularity_condition_met = False
    if log_b_a < k:
        regularity_condition_met = check_regularity_condition(a, b, k)
        if not regularity_condition_met:
            case += " (Regularity Condition Not Met)"

    if k > 0:
        recurrence_relation = f"T(n) = {a}T(n/{b}) + f(n<sup>{k}</sup>)"
    else:
        recurrence_relation = f"T(n) = {a}T(n/{b}) + f(1)"

    return complexity, case, recurrence_relation, regularity_condition_met

def calculate_plot_data(a: int, b: int, k: int) -> Dict[str, List[float]]:
    n = np.linspace(1, 100, 400)
    log_b_a = np.log(a) / np.log(b)

    n_log_b_a = n ** log_b_a

    # Adjust f(n) based on the case
    if log_b_a > k:
        f_n = (n ** k).tolist()      # Case 1
    elif abs(log_b_a - k) < 1e-9:
        f_n = (n ** k).tolist()      # Case 2
    else:
        f_n = (np.ones_like(n) if k == 0 else n ** k).tolist()  # Case 3

    # Time complexity
    if log_b_a > k:
        time_complexity = n_log_b_a.tolist()
    elif abs(log_b_a - k) < 1e-9:
        time_complexity = (n ** log_b_a * np.log(n)).tolist()
    else:
        time_complexity = f_n

    return {
        "n": n.tolist(),
        "n_log_b_a": n_log_b_a.tolist(),
        "f_n": f_n,
        "time_complexity": time_complexity,
    }

class EvaluateMasterTheoremRequest(BaseModel):
    a: int = Field(..., ge=1, description="Number of subproblems (>= 1)")
    b: int = Field(..., ge=2, description="Factor by which problem size is reduced (>= 2)")
    k: int = Field(..., ge=0, description="Exponent in the work done outside recursion (>= 0)")

class EvaluateMasterTheoremResponse(BaseModel):
    complexity: str
    case: str
    recurrence_relation: str
    regularity_condition_met: bool
    plot_data: Dict[str, List[float]]


class Algorithm(BaseModel):
    """
    Mimics your Django model fields for demonstration.
    In production, you might fetch and return these from DynamoDB or another DB.
    """
    id: int
    name: str
    a: int
    b: int
    k: int
    description: str
    python_code: str
    case: str = ""
    time_complexity: str = ""
    complexity_analysis: str = ""

# 3) Initialize the FastAPI application
app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/api/evaluate", response_model=EvaluateMasterTheoremResponse)
async def evaluate_master_theorem_endpoint(req: EvaluateMasterTheoremRequest):
    try:
        complexity, case, recurrence_relation, regularity_condition_met = evaluate_master_theorem(
            a=req.a,
            b=req.b,
            k=req.k
        )
        plot_data = calculate_plot_data(req.a, req.b, req.k)

        return EvaluateMasterTheoremResponse(
            complexity=complexity,
            case=case,
            recurrence_relation=recurrence_relation,
            regularity_condition_met=regularity_condition_met,
            plot_data=plot_data
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/algorithms", response_model=List[Algorithm])
async def get_algorithms():
    """Get all algorithms items from DynamoDB table."""
    table = dynamodb.Table(TABLE_NAME)
    try:
        response = table.scan()
        items = response.get("Items", [])
        return items
    except ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error scanning table {TABLE_NAME}: {e.response['Error']['Message']}"
        )

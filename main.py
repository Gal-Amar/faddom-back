from typing import Any, Optional
from pydantic import BaseModel
from pathlib import Path

from fastapi import FastAPI, Query, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .cloudwatch_data_retriever import get_cpu_utilization_data

app = FastAPI()

origins = [
    "http://localhost:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ApiResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None
    error: Optional[str] = None


@app.get("/")
async def root(
    delta: int = Query(
        ...,
        description="The time difference (delta) between the end date and the start date in seconds."
    ),
    instance_ip: str = Query(
        ...,
        description="The private IP address of the AWS instance. It should be in IPv4 format (e.g., 192.168.1.1)."
    ),
    period: int = Query(
        ...,
        description="The time interval (in seconds) between two consecutive data points. This defines the sampling frequency or resolution of the data."
    )
):
    try:
        response = get_cpu_utilization_data(instance_ip, delta, period)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=ApiResponse(
                success=True,
                message="Request processed successfully.",
                data=response,
            ).dict())

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ApiResponse(
                success=False,
                error=str(e),
                message="An error occurred while processing the request."
            ).dict()
        )

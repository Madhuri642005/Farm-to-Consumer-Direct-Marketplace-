from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from prophet import Prophet

app = FastAPI()

class ForecastInput(BaseModel):
    history: list

@app.post("/forecast")
def forecast(data: ForecastInput):
    df = pd.DataFrame(data.history)
    df.columns = ["ds", "y"]

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)

    return forecast.tail(7)[["ds", "yhat"]].to_dict()
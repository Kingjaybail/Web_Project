# uvicorn app.main:app --reload --port 8000
import uvicorn
import json
import app.models as models
import app.database.DB as db

from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    username: str
    password: str

@app.get("/")
async def root():
    return {"message": "Welcome to ModelSite Backend"}

@app.get("/status")
async def status():
    return {"message": "Backend is running properly"}

@app.post("/login")
async def login(user: User):
    res = db.get_user(user.username, user.password)
    return res

@app.post("/signup")
def signup(user: User):
    res = db.add_user(user.username, user.password)
    return res
    

@app.post("/linear-regression")
async def linear_regression(file: UploadFile, target_column: str = Form(...)):
    contents = await file.read()
    try:
        res = models.linearregression.process_linear_regression(contents, file.filename, target_column)
        if "error" in res:
            return {"error": res["error"]}
        return {
            "model": res.get("model_type", "Linear Regression"),
            "message": "Model executed successfully!",
            "metrics": res.get("metrics", {}),
            "coefficients": res.get("coefficients"),
            "intercept": res.get("intercept"),
            "predictions_preview": res.get("predictions_preview"),
        }

    except Exception as e:
        return {"error": str(e)}

@app.post("/bagging")
async def bagging(file: UploadFile, target_column: str = Form(...)):
    contents = await file.read()
    try:
        res = models.bagging.process_bagging_regression(contents, file.filename, target_column)
        if "error" in res:
            return {"error": res["error"]}
        return {
            "model": res.get("model_type", "Bagging"),
            "message": "Model executed successfully!",
            "metrics": res.get("metrics", {}),
            "parameters": res.get("parameters"),
            "predictions_preview": res.get("predictions_preview"),
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/logistic-regression")
async def logistic_regression(file: UploadFile, target_column: str = Form(...)):
    contents = await file.read()
    try:
        res = models.logisticregression.process_logistic_regression(contents, file.filename, target_column)
        if "error" in res:
            return {"error": res["error"]}
        return {
            "model": res.get("model_type", "Logistic Regression"),
            "message": "Model executed successfully!",
            "metrics": res.get("metrics", {}),
            "coefficients": res.get("coefficients"),
            "intercept": res.get("intercept"),
            "predictions_preview": res.get("predictions_preview"),
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/decision-trees")
async def decision_trees(file: UploadFile, target_column: str = Form(...), metrics: str = Form(...)):
    contents = await file.read()
    print(f"Received file: {file.filename}")
    try:
        res = models.decision_trees.process_decision_tree(contents, file.filename, target_column)
        if "error" in res:
            return {"error": res["error"]}
        return res
    except Exception as e:
        return {"error": str(e)}

@app.post("/random-forest")
async def random_forest(file: UploadFile, target_column: str = Form(...), metrics: str = Form(...)):
    contents = await file.read()
    print(f"Received file: {file.filename}")
    try:
        res = models.random_forest.process_random_forest(contents, file.filename, target_column)
        if "error" in res:
            return {"error": res["error"]}
        return res
    except Exception as e:
        return {"error": str(e)}

@app.post("/svm")
async def support_vector_machines(file: UploadFile, target_column: str = Form(...), metrics: str = Form(...)):
    contents = await file.read()
    print(f"Received file: {file.filename}")
    try:
        res = models.svm.process_svm_regression(contents, file.filename, target_column)
        if "error" in res:
            return {"error": res["error"]}
        return res
    except Exception as e:
        return {"error": str(e)}

@app.post("/deep-neural-network")
async def deep_neural_network(file: UploadFile, target_column: str = Form(...), metrics: str = Form(...)):
    contents = await file.read()
    print(f"Received file: {file.filename}")
    try:
        res = models.deep_neural_network.process_deep_neural_network(contents, file.filename, target_column)
        if "error" in res:
            return {"error": res["error"]}
        return res
    except Exception as e:
        return {"error": str(e)}

@app.get("/boosting")
async def boosting():
    return {"model": "boosting", "message": "Boosting endpoint (coming soon)"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

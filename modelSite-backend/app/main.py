# uvicorn app.main:app --reload --port 8000
import uvicorn
import app.models as models
import app.database.DB as db
import json

from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, Form, File, Body
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

@app.delete("/clear-model-history/{username}")
async def clear_model_history(username: str):
    try:
        db.clear_user_model_history(username)
        return {"message": f"All model history cleared for {username}"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/save-model-result")
async def save_model_result(
        username: str = Form(...),
        dataset_name: str = Form(...),
        model_type: str = Form(...),
        target_column: str = Form(...),
        metrics: str = Form(...),
):
    try:
        metrics_dict = json.loads(metrics)
        db.save_model_result(username, dataset_name, model_type, target_column, metrics_dict)
        return {"message": "Model result saved successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/model-history/{username}")
async def model_history(username: str):
    try:
        history = db.get_user_model_history(username)
        return {"history": history}
    except Exception as e:
        return {"error": str(e)}

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
async def decision_trees(file: UploadFile, target_column: str = Form(...)):
    contents = await file.read()
    try:
        res = models.decisiontrees.process_decision_tree(contents, file.filename, target_column)
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

@app.post("/random-forest")
async def random_forest(file: UploadFile, target_column: str = Form(...)):
    contents = await file.read()
    try:
        res = models.randomforest.process_random_forest(contents, file.filename, target_column)
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

@app.post("/svm")
async def support_vector_machines(file: UploadFile, target_column: str = Form(...)):
    contents = await file.read()
    try:
        res = models.svm.process_svm_model(contents, file.filename, target_column)
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

@app.post("/deep-neural-network")
async def deep_neural_network(file: UploadFile = File(...), request_data: str = Form(...)):
    contents = await file.read()
    print(f"Received file: {file.filename}")
    print(request_data)
    try:
        data = json.loads(request_data)
        target_column = data.get("target_column")
        model_config = data.get("model_config")

        res = models.deepnueralnetwork.process_deep_neural_network(
            contents, file.filename, target_column, model_config
        )

        if "error" in res:
            return {"error": res["error"]}
        return res

    except Exception as e:
        print(f"[ERROR] deep_neural_network: {e}")
        return {"error": str(e)}

@app.post("/boosting")
async def model_boosting(file: UploadFile, target_column: str = Form(...)):
    contents = await file.read()
    try:
        res = models.boosting.process_boosting(contents, file.filename, target_column)
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

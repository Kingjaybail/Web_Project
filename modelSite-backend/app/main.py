# uvicorn app.main:app --reload --port 8000 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/")
async def root():
  return {"message": "Welcome"}

@app.get("/linear-regression")
async def linear_regression():
  return {"model": "linear_regression", "message": "Linear Regression endpoint"}

@app.get("/logistic-regression")
async def logistic_regression():
  return {"model": "logistic_regression", "message": "Logistic Regression endpoint"}

@app.get("/decision-trees")
async def decision_trees():
  return {"model": "decision_trees", "message": "Decision Trees endpoint"}

@app.get("/bagging")
async def bagging():
  return {"model": "bagging", "message": "Bagging endpoint"}

@app.get("/boosting")
async def boosting():
  return {"model": "boosting", "message": "Boosting endpoint"}

@app.get("/random-forest")
async def random_forest():
  return {"model": "random_forest", "message": "Random Forest endpoint"}

@app.get("/svm")
async def support_vector_machines():
  return {"model": "svm", "message": "Support Vector Machines endpoint"}

@app.get("/deep-neural-network")
async def deep_neural_network():
  return {"model": "deep_neural_network", "message": "User-defined Deep Neural Network endpoint"}

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
How to use
1. Clone the code by: git clone https://github.com/Kingjaybail/Web_Project.git
2. cd into Web_Project folder
3. run docker compose up --build
3a. alternatively can create 2 terminals cd into each and on the react side run npm run dev and on the fastAPI side run uvicorn main.app:app --reload --port 8000 which will give same results
4. go to http://localhost:5173/
5. signup/login to access site
   

How to replicate results
I used airQualityData set linked in codespace
I ran tests for pm25 on each of the regression models
I ran tests for year on each of the classification models
then I ran a custom nn model which can be configured to user preference
I compared each

System setup
I tested on a desktop computer with a radeon rx 6750xt gpu and a ryzen 5 cpu but since this is a web program it should run on most things however launch time can take a while and particularly some models take a few minutes to return results

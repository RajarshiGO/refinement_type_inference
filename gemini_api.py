from importlib import reload
from fastapi import FastAPI, HTTPException
import google.generativeai as genai
import os

app = FastAPI()
key = os.getenv('API_KEY')
genai.configure(api_key=key)

prompts = [
    {"id": 1, "prompt": "Could you generate the refinement type for the following function? A refinement type is a logical formula that defines the types of the input arguments along with any constraints (refinements) on them, and similarly specifies constraints on the output variable ν. These refinements express the conditions that the input and output must satisfy. The function is as follows: <FUNCTION>. Do not explain just give the expression."},
    {"id": 2, "prompt": "Please generate the refinement type for the following function. A refinement type is a logical formula that defines the types of the input arguments along with any constraints (refinements) on them, and similarly specifies constraints on the output variable ν. These refinements express the conditions that the input and output must satisfy. Please pay attention to the types of the function input arguments and the output along with the values that they may assume. The function is as follows: <FUNCTION> . Do not explain just give the expression."},
    {"id": 3, "prompt": "A refinement type of a function is a logical formula consisting of logical operators (conjunction, disjunction, implication, etc.) that define the types of the input arguments along with any constraints (refinements) on them through predicates, and similarly specify constraints on the output variable ν. These refinements express the conditions that the input and output must satisfy. Please pay attention to the types of the function input arguments and the output, along with the values that they may assume. For example, for the function: let rec factorial n = \n\t if n = 0 then 1 else n * factorial (n - 1), the refinement type is: factorial :: {n: int | n>=0} -> {ν :int | ν>=n}. Please generate the refinement type for the following function without any explanation: <FUNCTION>"}
]

@app.get("/prompts")
async def get_prompts():
    return {"prompts": prompts}

@app.post("/generate")
async def generate_text(prompt_id: int, function: str = ""):
    try:
        prompt = next(prompt for prompt in prompts if prompt["id"] == prompt_id)
        final_prompt = prompt["prompt"].replace("<FUNCTION>", function)

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(final_prompt)
        return {"response": response.text}
    except (StopIteration, Exception) as e:
        raise HTTPException(status_code=400, detail="Invalid prompt ID")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("gemini_api:app", host="0.0.0.0", port=8000, reload=True)

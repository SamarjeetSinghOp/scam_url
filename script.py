from fastapi import FastAPI
from openai import OpenAI
import urlexpander

#keys 
KEY = "xxxxxxxxx"
app = FastAPI()

def openai_scam(query):
        client = OpenAI(api_key=KEY)
        response = client.chat.completions.create(
            model ="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"""Based on the domain given by the user,
                evaluate if it is a scam website. 
                Consider that the spelling is highly accurate. 
                Return 1 if it is likely a scam, otherwise return 0.
                try to be accurate dont flag original website as fake
                Return answer only in term of 1 or 0 no extra text nothing else
                """},
                {"role":"user","content":f"{query}"}
            ],
            temperature=0.1
        )
        return response.choices[0].message.content

def openai_type(query):
    client = OpenAI(api_key=KEY)
    response = client.chat.completions.create(
            model ="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"""Based on the domain given by the user,
                evaluate if it into following categories : 
                Consider that the spelling is highly accurate. 
                Return 
                1 for E-commerce.
                2 for News and Media.
                3 for Social Networking.
                4 for Educational.
                5 for Entertainment.
                6 for Government and Non-Profit
                7 for Corporate
                8 for Health and Wellness
                9 for Technology
                0 for Finance
                Return answer only in term of 0-9 no extra text nothing else
                """},
                {"role":"user","content":f"{query}"}
            ],
            temperature=0.1
        )
    return response.choices[0].message.content

def openai_promo(query):
    client = OpenAI(api_key=KEY)
    response = client.chat.completions.create(
            model ="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"""Based on the given domain, evaluate if it has a strong promotional intent.
                 Consider that the spelling is highly accurate. 
                 Return 1 if it has a strong promotional intent, otherwise return 0.
                 Return the answer only as 0 or 1, with no extra text.
                """},
                {"role":"user","content":f"{query}"}
            ],
            temperature=0.1
        )
    return response.choices[0].message.content
    
@app.post("/")
def scam(necessary: str):
    print(necessary)
    try:
        full_url = urlexpander.expand(necessary)
        scam = openai_scam(f"Check this webiste {full_url}")
        types = openai_type(f"Check this webiste {full_url}")
        promo = openai_promo(f"Check this webiste {full_url}")
        return {"scam" : float(scam),
                    "type" : float(types),
                    "promotional_intend" : float(promo),
                    "url" : full_url
                    }
    except:
        return {"nature" : "scam"}
    
    # if 'scam' is 0 then it is not scam
    # if 'scam' is 1 then it is scam
    
    
    # for 'type' values are given below
    # 1 for E-commerce.
    # 2 for News and Media.
    # 3 for Social Networking.
    # 4 for Educational.
    # 5 for Entertainment.
    # 6 for Government and Non-Profit
    # 7 for Corporate
    # 8 for Health and Wellness
    # 9 for Technology
    # 0 for Finance
    
    
    # 'url' provides resulten url of shorten url 
    
    # 'promotional_intend' is 1 for any promotional website 
    # while 0 for non promotional website
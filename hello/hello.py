import random
import json
from openai import OpenAI
client = OpenAI(base_url = 'http://localhost:1234/v1',api_key = 'key')

# Adjust the following based on the model type
# Alpaca style prompt format:
prefix = "### Instruction:\n" 
suffix = "\n### Response:"

# 'Llama2 Chat' prompt format:
#prefix = "[INST]"
#suffix = "[/INST]"

# This is a simple wrapper function to allow you simplify your prompts
def complete(prompt):
    formatted_prompt = f"{prefix}{prompt}{suffix}"
    response = client.completions.create(model='',prompt=formatted_prompt,seed=12345)
    return response.choices[0].text.strip('\n')

random.seed(1234)

def objects_from_theme(theme):
    count = random.randrange(4,8)
    objects = complete(f"List {count} objects related to {theme}. Format as json array of single strings.")
    return json.loads(objects)

theme = "blue"

print(f"Theme: {theme}")

print("anchor objects:")
print(objects_from_theme(theme))

#print("story...")
#story = complete(f"{objects_chunk}\nin one sentence, write a compelling and luscious story about a protagonist, an antagonist and these objects")
#print(f"    {story}")

#print("protagonist...")
#protagonist = complete(f"{story}\ndescribe the protagonist in one sentence")
#protagonist_name = complete(f"{protagonist}\ngive the name of this character as json").strip('\n')
#print(f"    {protagonist_name}: {protagonist}")

#print("title...")
#title = complete(f"Consider the story \"{story}\", give a short and snappy title.")

#print("done.\n\n")
#print(f"{title}\n\n")
#print(f"{story}\n\n")
#print(f"{protagonist_name}: {motion}\n\n")
#print(f"{protagonist}\n\n")
#print(f"{antagonist_name}: {anti_motion}\n\n")
#print(f"{antagonist}\n\n")
#print(f"Theme: {theme}\n")
#print(f"Objects: {objects}\n")

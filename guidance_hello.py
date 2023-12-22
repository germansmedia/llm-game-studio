import random
random.seed(1234)

from guidance import models,gen
lm = models.LlamaCpp("/home/desmond/extra/models/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q4_K_S.gguf",n_gpu_layers=-1,echo=False)

def generate_gender():
    gender = "male"
    if random.randrange(0,10) >= 5:
        gender = "female"
    return gender

def generate_name(prime,job,gender):
    state = lm + f"{prime} Give a complex and colorful {gender} name for a {job}. The name is \"" + gen(max_tokens=10,stop='\"',temperature=0.9)
    chunks = str(state).split('\"')[1].strip(' .,;:*').split(' ')
    first = True
    for chunk in chunks:
        if first:
            name = chunk.capitalize()
            first = False
        else:
            name = f'{name} {chunk.capitalize()}'
    return name

def generate_character(prime,job):
    gender = generate_gender()
    name = generate_name(prime,job,gender)
    state = lm + f"{prime} Imagine you are a creative writer tasked with creating a {job}. Fill out the following json structure with details, but keep it tight and short.\ncharacter = {{ \"name\": \"{name}\", \"gender\": \"{gender}\", \"power\": \"" + gen(max_tokens=50,stop='\"',temperature=0.9) + "\", \"weakness\": \"" + gen(max_tokens=50,stop='\"',temperature=0.9) + "\" }"
    return str(state).split('character = ')[1]

theme = "infinity"
setting = "space opera"

print(f"setting: {setting}")
print(f"theme: {theme}")

prime = f"The setting is {setting}. The theme is {theme}."

print("Our heroes:")
for i in range(0,5):
    character = generate_character(prime,"hero")
    print(f"    {character}")

print("The main villain:")
character = generate_character(prime,"arch villain")
print(f"    {character}")

print("Underbosses at the end of the levels:")
for i in range(0,5):
    character = generate_character(prime,"underboss")
    print(f"    {character}")

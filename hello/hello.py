import json

import random
random.seed(1234)

from openai import OpenAI
client = OpenAI(base_url = 'http://localhost:1234/v1',api_key = 'key')

prefix = "### Instruction:\n" 
suffix = "\n### Response:"

def complete(prompt,max_tokens=1500):
    seed = random.randrange(0,10000)
    response = client.completions.create(model='',prompt=f"{prefix}{prompt}{suffix}",max_tokens=max_tokens,seed=seed)
    result = response.choices[0].text.strip('\n')
    return result

def complete_seeded(prompt,seed,max_tokens=1500):
    response = client.completions.create(model='',prompt=f"{prefix}{prompt}{suffix}",max_tokens=max_tokens,seed=seed)
    result = response.choices[0].text.strip('\n')
    return result

def conceptify(text):
    return text.strip('\n ').split('.')[0].strip(' .,:*-\"').lower()

def verbalize_names(names):
    result = ""
    for i in range(len(names)):
        if i == 0:
            result = names[i]
        elif i == len(names) - 1:
            result = f"{result} and {names[i]}"
        else:
            result = f"{result}, {names[i]}"
    return result

def generate_opposite(text):
    text = complete(f"Give the opposite of {text}. One word only.",max_tokens=5)
    return conceptify(text)

def generate_object(setting,theme):
    object = complete(f"The setting is {setting}. Name one important everyday object related to {theme} in this setting. One word only.",max_tokens=5)
    return conceptify(object)

def generate_objects(setting,theme):
    count = random.randrange(2,5)
    objects = []
    for i in range(count):
        found = True
        while found:
            object = generate_object(setting,theme)
            found = object in objects
        objects.append(object)
    return objects

def generate_gender():
    gender = "male"
    if random.randrange(0,10) >= 5:
        gender = "female"
    return gender

def generate_name(prime,job,gender):
    name = complete(f"{prime} Think of a {gender} name for a {job}. One word only.",max_tokens=5)
    return conceptify(name).capitalize()

def generate_characters(count,prime,job,object_names):
    characters = []
    for i in range(count):
        gender = generate_gender()
        found = True
        while found:
            name = generate_name(prime,job,gender)
            found = False
            for character in characters:
                if character['name'] == name:
                    found = True
                    break
        looks = complete(f"{prime} Describe in one sentence what {name} looks like.",max_tokens=50)
        activity = complete(f"{prime} Describe in one sentence what particular thing {name} likes to do best.",max_tokens=50)
        strength = complete(f"{prime} Specify in one sentence the particular strength, smart or power of {name}.",max_tokens=50)
        weakness = complete(f"{prime} Specify in one sentence the particular weakness, or achilles heel of {name}.",max_tokens=50)
        trauma = complete(f"{prime} Describe the main source of trauma that {name} had to endure.",max_tokens=50)
        character = { 'name': name,'gender': gender,'looks': looks,'activity': activity,'strength': strength,'weakness': weakness,'trauma': trauma }
        characters.append(character)
    return characters

# ====

setting = "futuristic"
theme = "winter"

print(f"setting: {setting}")
print(f"theme: {theme}")

antitheme = generate_opposite(theme)
print(f"antitheme: {antitheme}")

objects = generate_objects(setting,theme)
object_names = verbalize_names(objects)
print(f"anchor objects: {object_names}")

prime = f"The setting is {setting}. The theme is {theme}."
antiprime = f"The setting is {setting}. The theme is {antitheme}."

heroes = generate_characters(random.randrange(1,2),prime,"hero",object_names)
print("heroes:")
for character in heroes:
    print(f"    {character['name']}")
    print(f"        strength: {character['strength']}")
    print(f"        weakness: {character['weakness']}")
    print(f"        favorite activity: {character['activity']}")
    print(f"        looks: {character['looks']}")
    print(f"        trauma: {character['trauma']}")

side_jobs = ['cleric','smith','driver','guard','fixer']
sides = generate_characters(random.randrange(4,8),prime,side_jobs[random.randrange(0,len(side_jobs))],object_names)
print("side characters:")
for character in sides:
    print(f"    {character['name']}")
    print(f"        strength: {character['strength']}")
    print(f"        weakness: {character['weakness']}")
    print(f"        favorite activity: {character['activity']}")
    print(f"        looks: {character['looks']}")
    print(f"        trauma: {character['trauma']}")

villains = generate_characters(random.randrange(3,6),antiprime,"villain",object_names)
print("villains:")
for character in villains:
    print(f"    {character['name']}: {character['trauma']}")

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

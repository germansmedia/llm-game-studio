import json

import random
random.seed(1234)

from guidance import models,gen,select
lm = models.LlamaCpp("/home/desmond/extra/models/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q4_K_S.gguf",n_gpu_layers=-1,echo=False)

def generate_gender():
    gender = "male"
    if random.randrange(0,10) >= 5:
        gender = "female"
    return gender

def generate_name(prime,type_,gender):
    state = lm + f"{prime} Give a {gender} name for a {type_}. The name is \"" + gen(max_tokens=10,stop='\"',temperature=0.9)
    chunks = str(state).split('\"')[1].strip(' .,;:*').split(' ')
    first = True
    for chunk in chunks:
        if first:
            name = chunk.capitalize()
            first = False
        else:
            name = f'{name} {chunk.capitalize()}'
    return name

def generate_character(prime,type_):

    # start with 50% gender choice
    gender = generate_gender()

    # and a good name
    name = generate_name(prime,type_,gender)

    # into a json record
    state = lm + f"{prime} Fill out the following json structure with details of a new {gender} {type_}, but keep it tight and short.\ncharacter = {{ \"name\": \"{name}\", \"gender\": \"{gender}\", \"type\": \"{type_}\", \"favorite food\": \"" + gen(max_tokens=50,stop='\"',temperature=0.9) + "\" }"

    return json.loads(str(state).split('character = ')[1])

def specify_character(name,gender,type_,favorite_food):

    return { 'name': name,'gender': gender,'type': type_,'favorite food': favorite_food }

def summarize_characters(characters):
    summary = ''
    first = True
    for character in characters:
        name = character['name']
        gender = character['gender']
        type_ = character['type']
        if first:
            summary = f"{name} is a {gender} {type_}."
            first = False
        else:
            summary = f"{summary} {name} is a {gender} {type_}."
    return summary

def start_story(setting,characters):
    summary = summarize_characters(characters)
    state = lm + f"The setting is {setting}. {summary} Write the first short sentence of a new story. sentence = \"" + gen(max_tokens=100,stop='\"',temperature=0.9)
    return str(state).split('sentence = \"')[1]

def continue_story(setting,story,characters,part):
    summary = summarize_characters(characters)
    state = lm + f"The setting is {setting}. {summary} The story so far is \"{story}\". Write the following short sentence with {part}. sentence = \"" + gen(max_tokens=100,stop='\"',temperature=0.9)
    tail = str(state).split('sentence = \"')[1]
    return f"{story} {tail}"

def finish_story(setting,story,characters):
    summary = summarize_characters(characters)
    state = lm + f"The setting is {setting}. {summary} The story so far is \"{story}\". Finish the story with one short sentence. sentence = \"" + gen(max_tokens=100,stop='\"',temperature=0.9)
    tail = str(state).split('sentence = \"')[1]
    return f"{story} {tail}"

def compare_stories(story1,story2,criterium):
    state = lm + f"Consider these two stories.\n\nA:\n{story1}\n\nB:\n{story2}\n\nThe {criterium} is " + select(['A','B'])
    return str(state).split(f"The {criterium} is ")[1] == 'B'

def oscar(stories,criterium):
    winner = stories[0]
    for i in range(1,len(stories)):
        if compare_stories(winner,stories[i],criterium):
            winner = stories[i]
    return winner

def find_topic(story):
    state = lm + f"Consider the following story.\n\n{story}\n\nIn one word, give the main topic of the story. topic = \"" + gen(max_tokens=100,stop='\"',temperature=0.9)
    return str(state).split('topic = \"')[1]

# ====

theme = "horror"
setting = "texas farm"

print(f"setting: {setting}")
print(f"theme: {theme}")

print("characters:")
characters = []
characters.append(generate_character(f"The setting is {setting}. The story is about {theme}.","damsel"))
characters.append(generate_character(f"The setting is {setting}. The story is about {theme}.","boogieman"))
characters.append(generate_character(f"The setting is {setting}. The story is about {theme}.","officer"))
for character in characters:
    print(f"    {character['name']} ({character['gender']}): {character['type']}, favorite food: {character['favorite food']}")

print("\nstories:")
stories = []
for i in range(0,8):
    story = start_story(setting,characters)
    story = continue_story(setting,story,characters,"a call to action")
    story = continue_story(setting,story,characters,"the lowest point")
    story = continue_story(setting,story,characters,"the rising action")
    story = continue_story(setting,story,characters,"the climax")
    story = continue_story(setting,story,characters,"the resolution")
    story = finish_story(setting,story,characters)

    print(f"\n    {story}")
    topic = find_topic(story)
    print(f"    main topic found: {topic}")

    stories.append(story)

print("funniest:")
print(oscar(stories,"funniest story"))

print("most uplifting:")
print(oscar(stories,"most uplifting story"))

print("saddest:")
print(oscar(stories,"saddest story"))

print("most dramatic:")
print(oscar(stories,"most dramatic story"))

print("most suspenseful:")
print(oscar(stories,"most suspenseful story"))

print("most interesting:")
print(oscar(stories,"most interesting story"))

print("most sensible:")
print(oscar(stories,"story that makes the most sense"))

print("most coherent:")
print(oscar(stories,"most coherent story"))

print("easiest to film:")
print(oscar(stories,"easiest to film story"))

print("best overall story:")
print(oscar(stories,"best overall story"))

print(f"most on-topic:")
print(oscar(stories,f"story most about {theme}"))

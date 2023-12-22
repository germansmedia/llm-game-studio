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

def generate_name(prime,job,gender):
    state = lm + f"{prime} Give a {gender} name for a {job}. The name is \"" + gen(max_tokens=10,stop='\"',temperature=0.9)
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

    # start with 50% gender choice
    gender = generate_gender()

    # and a good name
    name = generate_name(prime,job,gender)

    # into a json record
    state = lm + f"{prime} Fill out the following json structure with details of a new {gender} {job}, but keep it tight and short.\ncharacter = {{ \"name\": \"{name}\", \"gender\": \"{gender}\", \"favorite food\": \"" + gen(max_tokens=50,stop='\"',temperature=0.9) + "\" }"

    return str(state).split('character = ')[1]

def generate_sentence(setting,motion,characters):

    # get random characters from the set
    count = random.randrange(1,3)
    current_characters = []
    for i in range(0,count):
        found = True
        while found:
            character = json.loads(characters[random.randint(0,len(characters) - 1)])
            name = character['name']
            gender = character['gender']
            found = False
            for c in current_characters:
                if c['name'] == character['name']:
                    found = True
                    break
        current_characters.append(character)

    # summarize them
    summary = ''
    first = True
    for character in current_characters:
        if first:
            summary = f"{name} is a {gender}."
            first = False
        else:
            summary = f"{summary} {name} is a {gender}."

    # generate sentences, differ prompt depending on number of characters involved
    if len(current_characters) == 1:
        state = lm + f"The setting is {setting}. {summary} Within {motion}, write a short sentence about what {current_characters[0]['name']} does. sentence = \"" + gen(max_tokens=50,stop='\"',temperature=0.9)
    elif len(current_characters) == 2:
        state = lm + f"The setting is {setting}. {summary} Within {motion}, write a short sentence about what {current_characters[0]['name']} does with {current_characters[1]['name']}. sentence = \"" + gen(max_tokens=50,stop='\"',temperature=0.9)
    elif len(current_characters) == 3:
        state = lm + f"The setting is {setting}. {summary} Within {motion}, write a short sentence about what {current_characters[0]['name']} does with {current_characters[1]['name']} and {current_characters[2]['name']}? sentence = \"" + gen(max_tokens=50,stop='\"',temperature=0.9)

    return str(state).split('sentence = \"')[1]

def generate_sentences(setname,setting,motion,characters):
    print(f"{setname}:")
    sentences = []
    for i in range(0,5):
        sentence = generate_sentence(setting,motion,characters)
        sentences.append(sentence)
        print(f"    {sentence}")

def generate_random_story(beginnings,calls,risings,climaxes,endings):
    beginning = beginnings[random.randint(0,len(beginnings) - 1)]
    call = calls[random.randint(0,len(calls) - 1)]
    rising = risings[random.randint(0,len(risings) - 1)]
    climax = climaxes[random.randint(0,len(climaxes) - 1)]
    ending = endings[random.randint(0,len(endings) - 1)]
    return f"{beginning} {call} {rising} {climax} {ending}"

def compare_stories(story1,story2,criterium):
    state = lm + f"Consider these two stories.\n\nA:\n{story1}\n\nB:\n{story2}\n\nThe {criterium} is " + select(['A','B'])
    return str(state).split(f"The {criterium} is ")[1] == 'B'

def find_top_story(stories,criterium):
    winner = stories[0]
    for i in range(1,len(stories)):
        if compare_stories(winner,stories[i],criterium):
            winner = stories[i]
    return winner

# ====

theme = "loss"
setting = "hong kong"
person = "tourist"

print(f"setting: {setting}")
print(f"theme: {theme}")

#print("characters:")
#characters = []
#for i in range(0,3):
#    character = generate_character(f"The setting is {setting}. The story is about {theme}.",person)
#    characters.append(character)
#    print(f"    {character}")

#beginnings = generate_sentences("beginnings",setting,f"the beginning of a story about {theme}",characters)
#calls = generate_sentences("calls",setting,f"the call to action of a story about {theme}",characters)
#risings = generate_sentences("risings",setting,f"the rising action of the story {theme}",characters)
#climaxes = generate_sentences("climaxes",setting,f"the climax of the story {theme}",characters)
#endings = generate_sentences("endings",setting,f"the ending of the story {theme}",characters)

beginnings = [
    "Jackson stared out of the rain soaked window, watching the tumultuous storm rage over the city.",
    "Jackson clutched the photograph of his late wife, feeling the familiar ache in his heart.",
    "Lila stared blankly at the wilting flowers in her living room, her heart heavy with sadness.",
    "Lila clutched Jacob\'s hand tightly as they watched the sun set over the harbor, her heart heavy with sorrow.",
    "Jacob watched as Jackson walked away, the sun setting behind him, leaving a trail of red and orange in the sky."
]
calls = [
    "Breathing deeply, Lila released the painful memories that had been holding her captive for years.",
    "Sobbing uncontrollably, Jackson searched frantically for any trace of his missing daughter.",
    "Desperate for answers, Lila digs deeper into her late husband's secrets, unearthing shocking truths that threaten to shatter her fragile world.",
    "Lila wrapped her arms around Jackson, pulling him close as they both cried.",
    "Lila reached out and wrapped her arms around Jackson, pulling him close as they both let their tears fall freely."
]
risings = [
    "Jackson realizes he has lost his passport.",
    "Jacob frantically searches for his missing wallet in his apartment, fearing he'll be unable to pay for his daughter's upcoming surgery.",
    "Jackson sneaks past the guards, attempting to evade capture.",
    "Jacob leads Lila through the crowded streets, shielding her from the frenzied energy of the city.",
    "Jacob rushed to the hospital, his heart heavy with fear for his sick wife.",
]
climaxes = [
    "With a last desperate effort, Jackson heaves a bag of explosives toward a large fuel tank, hoping to cause a catastrophic reaction and distract the enemy long enough for his team to escape.",
    "With a desperate cry, Lila threw herself over the balcony railing.",
    "Lila clung to Jackson, tears streaming down her face, her body trembling with the weight of her grief as she sobbed uncontrollably into his chest.",
    "Jackson grabs Jacob's arm and pulls him back from the edge.",
    "Lila clutched her chest, gasping for breath as the world around her spun crazily.",
]
endings = [
    "Jackson gathers his belongings and heads to the airport.",
    "Lila gave Jackson her handkerchief as a token of her sympathies.",
    "Lila gazed out at the harbor, a single tear trailing down her face as she vowed to leave Hong Kong forever.",
    "Desperate to find a way to make ends meet, Jacob sells his most prized possession--his late grandfather's antique watch--to a pawn shop.",
    "Jackson stands there, his heart aching for the woman he has lost.",
]

print("stories:")
stories = []
for i in range(0,8):
    story = generate_random_story(beginnings,calls,risings,climaxes,endings)
    stories.append(story)
    print(f"    {story}")

print("funniest:")
print(find_top_story(stories,"funniest story"))

print("most sensible:")
print(find_top_story(stories,"story that makes the most sense"))

print("most dramatic:")
print(find_top_story(stories,"most dramatic story"))

print("most interesting:")
print(find_top_story(stories,"most interesting story"))

print("most coherent:")
print(find_top_story(stories,"most coherent story"))

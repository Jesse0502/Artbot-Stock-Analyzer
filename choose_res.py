import spacy
from proc_res import default_res, greet_res, help_res, how_ques_res, org_res, welcome_res, who_made, your_name_res, predict_res

nlp = spacy.load('en_core_web_lg')

nlps = [
    {"base": nlp("should i buy, is stock a good stock purchase, is a good stock, good pick")},  # stock prediction
    {"base": nlp("hello, howdy")},  # greetings
    {"base": nlp("welcome")},  # welcoming msg
    {"base": nlp("how are you, how is it going, sup, wassup, have you been")},  # ask how you're doing
    {"base": nlp("who made you, who's your owner, JS_Artboy, artboy")}, # who made
    {"base": nlp("what is your name, what called, should I call")}, # ask name
]

cond_nlp = [
    "predict",
    "greet",
    "welcome",
    "ask",
    "who_made",
    "your_name",
]

def check_sim(stm):
    max_till_now = {"val": -1, "nlp": None}
    for ind, i in enumerate(nlps):
        if nlp(stm.lower()).similarity(i["base"]) > max_till_now["val"]:
            max_till_now = {"val": nlp(stm).similarity(
                i["base"]), "nlp": cond_nlp[ind]}
        
    print("max_till_now", max_till_now)
    if max_till_now["val"] > 0.65:
        return max_till_now
    else:
        print("in chooose else")
        return {"val": -1, "nlp": None}

def choose_res(stm, author):
    if "-help" in stm:
        return help_res()
    elif "-suggest" in stm:
        return predict_res(author)
    res = check_sim(stm)
    if res["nlp"] == cond_nlp[0]:
        return org_res(stm)
    elif res["nlp"] == cond_nlp[1]:
        return greet_res()
    elif res["nlp"] == cond_nlp[2]:
        return welcome_res()
    elif res["nlp"] == cond_nlp[3]:
        return how_ques_res()
    elif res["nlp"] == cond_nlp[4]:
        return who_made()
    elif res['nlp'] == cond_nlp[5]:
        return your_name_res()
    else:
        return default_res()
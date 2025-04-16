# Capstone

## Getting the Whole system running

From home directory just run
```
sudo docker-compose up --build
```

## For the capstone group
you can either get the whole system running or just start up the backend docker container
if you want just the backend container navigate to the server directory then run

```
sudo docker build -t [some name for your docker image] .
```

then to start it

```
sudo docker run -p 5000:5000 [same name from previous command]
```

I have provided an elementary python script titled evaluationScript which should help with making your project go faster and aleviate any headaches with communicating with the backend api
At the moment its pretty much hard coded to use one of the malware samples I provided, but that can be altered with a for loop and all to loop through a directory with a variety of samples.
Additionally in terms of whats returned to the user in the json is
    1. 'assemblyCode' - this is just the assembly code of the dissassembled malware sample (probably not relevant for you guys)
    2. 'functionMapping' - this is used internally for the function level attribution of FLEM (similarly probably not relvant)
    3. 'normalizedAttributions' - the normalized attribution scores (NOTE: the positive and negative values have been normalized seperately)
    4. 'rankedMaliciousFunctions' - the function names ranked from most malicious to least malicious
    5. 'rawAttributionScores' - the raw attribution scores before  normalization
    6. 'sortedAttributionIndexes' - this is an internal for getting the function names and generating the ranking (probably not relevant)

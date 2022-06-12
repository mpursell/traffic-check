[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Traffic Check

App to check the traffic to a given destination using Google Directions API and text me the optimal driving route with Twilio.

### Requirements

- Twilio account
- Phone number

## Docker Deployment

Dockerfile and docker-compose.yml are included to help with running the app locally via docker and cron

## AWS Lambda Deployment
To deploy to AWS Lamba:

- Identify all the packages required in requirements.txt
- Find those packages in the virtual env folder structure `projectfolder/lib/python3.9/site-packages`
- Zip up those packages with the app.py. 
- Create a new lambda function in AWS
- Upload the zip file from the "Code" tab
- Go into **General Configuration** in the AWS function console
- Go to **Environment Variables** and set the variables from your local .env file
- Make sure you change the handler name to run your module/function rather than the default lambda.handler 
- Set a trigger, select **Cloudwatch**.  You'll need to add a cron schedule using the syntax `cron(* * * * * )` where `*` are your cron fields.  To get help on the syntax, create the schedule (even if it's incorrect) and click on the schedule in the lambda function console.  This should let you open the function in Cloudwatch and edit it with real-time help with the cron scheduler. 


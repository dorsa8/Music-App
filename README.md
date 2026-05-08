Project: AWS Music Subscription App

Frontend:
- login.html
- register.html
- main.html
- style.css
- app.js

Backend:
- app.py Flask backend
- Dockerfile for ECS
- requirements.txt

AWS Services:
- DynamoDB: login, music, subscriptions
- S3: artist images and frontend hosting
- Lambda + API Gateway
- EC2 Flask backend
- ECS Fargate Docker backend
- ECR image repository

Demo URLs:
Lambda API:
https://yu7e9uylpa.execute-api.us-east-1.amazonaws.com/prod

EC2 backend:
http://44.206.230.16:5000

ECS backend:
http://54.91.141.124:5000

Frontend S3 URL:
http://music-frontend-s4007413.s3-website-us-east-1.amazonaws.com/

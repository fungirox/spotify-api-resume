# Music taste resume ヾ(^▽^*)))
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
[![Flask](https://img.shields.io/badge/Flask-000?logo=flask&logoColor=fff)](#)
[![Spotify](https://img.shields.io/badge/Spotify-1ED760?logo=spotify&logoColor=white)](#)
## Introduction
Web app that generates a personalized resume based on your Spotify activity. Also can generate a playlist with your top songs of a selected period of time. 
## 🛠️ Tech Stack
- Python 
- Flask
- Spotify Web API
- HTML/CSS/JavaScript
## 💻 Local Setup
### Requirements
- Python 3.14+
- Spotify Developer account
### Clone and Edit
```bash
git clone https://github.com/fungirox/spotify-api-resume.git
cd spotify-api-resume
pip install -r requirements.txt
```
### Get Spotify API credentials
- Go to [Spotify for Developers](https://developer.spotify.com/)
- Create a new app
- Copy Client ID
### Configure environment
- Create .env file and paste your **Client ID**, it should be like this:
```
CLIENT_ID = "m8edca6i5n3droarts20fjvxi8y1ye9c" # paste here Client ID of your spotify app
```
### Run
```bash
python main.py
```
## Check your stats (How to use it)
1. Click at “Login with Spotify”
<img alt="login-with-spotify" src="https://raw.githubusercontent.com/fungirox/spotify-api-resume/main/readme-images/1-login.png" />

2. Accept the access to your account
<img alt="access-with-spotify" src="https://raw.githubusercontent.com/fungirox/spotify-api-resume/main/readme-images/2-accept.png" />

3. As default you would see your “Last 4 weeks” top
<img alt="app-main-page" src="https://raw.githubusercontent.com/fungirox/spotify-api-resume/main/readme-images/3-4weeks.png" />

You can change it using the dropdown
<img alt="change-dropdown" src="https://raw.githubusercontent.com/fungirox/spotify-api-resume/main/readme-images/4-change-period.png" />

4. If you want to add a Favorite Album, click at “Select Album”
<img alt="select-album" src="https://raw.githubusercontent.com/fungirox/spotify-api-resume/main/readme-images/5-selec-album.png" />

5. It will open a modal, write album or artist name in the input text for search your favorite album. Then click the album cover or its name for select it
<img alt="search-in-modal" src="https://raw.githubusercontent.com/fungirox/spotify-api-resume/main/readme-images/6-write-modal.png" />

The selection will be in the main page instant, you can change it doing click again in the album cover.
<img alt="show-album" src="https://raw.githubusercontent.com/fungirox/spotify-api-resume/main/readme-images/7-album-selected.png" />

***Note:** At the moment, if you use the dropdown, it will restart the album and note input. It’s temporal because I didn’t change it already, but I will do it soon*

6. Add a short description of yourself in the text input
<img alt="show-album" src="https://raw.githubusercontent.com/fungirox/spotify-api-resume/main/readme-images/8-about-me.png" />

## 🎯 Features
- OAuth 2.0 authentication with Spotify
- Fetches user's top artists and tracks
- Generates visual music resume
## 🚀 Coming soon
- Download resume as png for ig story
- Generate your top 3 songs playlist
- Implement Tailwind for Front-End 
## 📝 Note
Personal project for practicing API integration and OAuth flows.

🚧 _I’m still working in this project, **be patient(o゜▽゜)o☆**_

### Credits
Roxanna Clark [Github](https://github.com/fungirox)


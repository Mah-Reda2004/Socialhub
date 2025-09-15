# SocialHub

SocialHub is a simple web application built with Django that allows users to create accounts, post content, comment, and like posts.

---

## Features

- User registration and login
- Profile management with profile pictures
- Create and delete posts
- Like and comment on posts
- forget password?
- Admin panel for managing users and content
- Optional: Load sample data for testing



## Project Structure
SocialHub/

core/ # Main project folder
─ settings.py
─ urls.py
─ wsgi.py
─ asgi.py
======>
  
─ account/ # User management app
  ─ migrations/
     ─ templates/account/
     ─ base.html
     ─ login.html
     ─ register.html
     ─ password_reset_request.html
     ─ password_confirm.html
  ─ models.py
  -forms.py
  -serializers
  ─ views.py
  ─ urls.py

─ posts/ # Posts management app
 - migrations/
   ─ templates/posts/
   ─ feed.html
   ─ post_create.html
   ─ post_list.html
 ─ models.py
 -forms.py
 -api_view
 -api_urls
 ─ views.py
 ─ urls.py


─ static/CSS/style.css
─ media/ # Uploaded media files
─ manage.py
─ requirements.txt
─ README.md

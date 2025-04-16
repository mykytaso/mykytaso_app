# mykytaso.com


## My website (Django application)

A full-featured blog-style web application built with Django.
It supports user registration, post creation via content blocks, commenting, and real-time Telegram notifications.
The app is fully deployed on AWS and optimized for performance, security, and maintainability.

<br>

## Deployed on AWS

The application is fully deployed on AWS using the following services:

- **EC2** – Hosts the Ubuntu server running the application with NGINX and Gunicorn
- **RDS** – Handles the PostgreSQL database
- **S3 Bucket** – Stores uploaded media files
- **CloudFront** – Delivers media files from the S3 Bucket

<br>

## Frontend Technologies

- **HTML**
- **CSS**
- **Bootstrap 5.3** – for responsive design and UI components
- **Django Template Language (DTL)** – for rendering dynamic server-side content

<br>

## SSL/TLS (HTTPS)
Secure HTTPS is enabled using SSL/TLS certificates provided by Let’s Encrypt, managed via Certbot.

<img src="docs/images/ssl.png" alt="SSL TLS" width="400"/>

<br>

## Unit and Integration Testing
The project achieves **94% test coverage**, ensuring strong code reliability and stability.

<img src="docs/images/test_coverage.png" alt="Unit and Integration Testing" width="400"/>

<br>

## Telegram Notification Bot
The application features a Telegram bot that sends notifications for:
- New messages
- User registrations
- New comments on posts

<img src="docs/images/telegram.png" alt="Telegram Bot" width="200"/>

<br>

## Functionality overview

### Registration and Login
Registration is **email-based**. Only registered users can leave comments on posts.

<img src="docs/images/logit_register.png" alt="Login Register" width="600"/>

<br>

### Posts List Page (Homepage)
**Anonymous** and **authenticated** users (not superusers) see this basic view:

<img src="docs/images/homepage_anonymous.png" alt="Homepage Anonymous" width="600"/>

**Superusers** see additional features:
- A **`+`** button to create a new post.
- A **tool panel** under each post with:
  - **`arrows buttons`** (to move post)
  - **`edit button`**
  - **`delete button`**

<img src="docs/images/homepage_super_user.png" alt="Homepage Superuser" width="600"/>

<br>

### Post Detail Page (Post Content Page)
**Anonymous** users can view comments but must log in to leave one:

<img src="docs/images/post_content_anonymous.png" alt="Post Detail Anonymous" width="600"/>

**Authenticated** users (not superusers) see a **`comment form`**.

<img src="docs/images/post_content_just_user.png" alt="Post Detail Authenticated Users" width="600"/>

**Superusers** have access to the **`Block Creation Panel`**, enabling them to create post content using **`blocks`**. They can also move blocks **up** or **down** using **`arrow buttons`**, and remove blocks with the **`delete button`**.

Available **`block` types** (each with customization options):
- Text
- Image
- Space

<img src="docs/images/post_content_super_user.png" alt="Post Detail Superusers" width="600"/>

<br>

### Comments
**Authenticated** users can comment and **delete their own comments**.
**Superusers** can **delete any** comment across the entire application.

For example, Alex is authenticated and can see the delete button for his own comment:

<img src="docs/images/comments.png" alt="Post Detail Comments" width="600"/>

<br>

## ✍️ &nbsp; Author
<img src="https://github.com/mykytaso.png" alt="@mykytaso" width="24" height="24" valign="bottom" /> Mykyta Soloviov <a href="https://github.com/mykytaso">@mykytaso</a>

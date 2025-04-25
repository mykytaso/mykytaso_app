# 👾 mykytaso.com


## My Django-based blog running on AWS

**Key Features:**
- Content creation using customizable blocks (inspired by Notion’s block-based system)
- Email-based user registration
- Commenting for authenticated users
- Real-time Telegram notifications

<br>

Quick video overview available on **[YouTube](https://youtu.be/cOzc9Wddsk8)**

<br>

## Technologies

- **Django 5.2**
- **PostgreSQL 17.2**
- **Django Signals** – Used for deleting media files from AWS S3 Bucket and sending Telegram notifications
- **GenericForeignKey** – Allows each Block to represent a different type of content, like text, image, or space
- **HTML, CSS, Bootstrap 5.3, Django Template Language (DTL)**
- **AWS, NGINX, Gunicorn**

<br>

## Deployed on AWS

### 🔗 [mykytaso.com](https://mykytaso.com)

The application is fully deployed on AWS using the following services:<br>
- **EC2** – Hosts the Ubuntu server running the application with NGINX and Gunicorn
- **RDS** – Handles the PostgreSQL database
- **S3 Bucket** – Stores uploaded media files
- **CloudFront** – Delivers media files from the S3 Bucket

<br>

## SSL/TLS (HTTPS)
Secure HTTPS is enabled using SSL/TLS certificates provided by `Let’s Encrypt`, managed via `Certbot`.

<img src="docs/images/ssl.png" alt="SSL TLS" width="400"/>

<br>

## Unit and Integration Testing
I implemented extensive unit and integration tests with `Unittest`.<br>
Current test coverage is **94%**.

<img src="docs/images/test_coverage.png" alt="Unit and Integration Testing" width="400"/>

<br>

## Telegram Notification Bot
The application features a Telegram bot that sends notifications for:
- New messages
- User registrations
- New comments on posts

<img src="docs/images/telegram.png" alt="Telegram Bot" width="260"/>

<br>

## Database Diagram
<img src="docs/images/database_diagram.png" alt="Database Diagram">

<br>

## Functionality overview

### Registration and Login
Registration is **email-based**.<br>
Only registered users can leave comments on posts.

<img src="docs/images/logit_register.png" alt="Login Register" width="680"/>

<br>

### Posts List Page (Homepage)
**Anonymous** and **Authenticated** users see this basic view:

<img src="docs/images/homepage_anonymous.png" alt="Homepage Anonymous" width="680"/>

<br>

**Superusers** see additional features:
- A `+` button to create a new post.
- A **tool panel** under each post with:
  - `arrows buttons` (to reorder posts)
  - `edit button`
  - `delete button`

<img src="docs/images/homepage_super_user.png" alt="Homepage Superuser" width="680"/>

<br>

### Post Detail Page (Post Content Page)
**Anonymous** users can view comments but must log in to leave one:

<img src="docs/images/post_content_anonymous.png" alt="Post Detail Anonymous" width="680"/>

<br>

**Authenticated** users can leave comments using the `comment form`.

<img src="docs/images/post_content_just_user.png" alt="Post Detail Authenticated Users" width="680"/>

<br>

**Superusers** have access to the `Block Creation Panel`, enabling them to create post content using `blocks`.<br>
They can also reorder `blocks` using **up** or **down** `arrow buttons`, and remove `blocks` with the `delete button`.<br>
I was inspired by Notion’s block-based system and wanted to implement a similar approach. 

Available `block` types (each with customization options):
- Text
- Image
- Space

**Superusers** can also add `tags` just below the post title. When multiple `tags` are present, they’re separated by a `•` symbol for better readability.

<img src="docs/images/post_content_super_user.png" alt="Post Detail Superusers" width="680"/>

<br>

### Comments
**Authenticated** users can comment and **delete their own comments**.<br>
**Superusers** can **delete any** comment across the entire application.

For example, **Alex** is authenticated and can see the delete button for his own comment:

<img src="docs/images/comments.png" alt="Post Detail Comments" width="680"/>

<br>

## ✍️ &nbsp; Author
<img src="https://github.com/mykytaso.png" alt="@mykytaso" width="24" height="24" valign="bottom" /> Mykyta Soloviov <a href="https://github.com/mykytaso">@mykytaso</a>

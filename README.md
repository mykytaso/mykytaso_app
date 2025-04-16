# mykytaso.com






## Deployment on AWS

The application is fully deployed on AWS using the following services:

- **EC2** – Hosts the Ubuntu server running the application
- **RDS (PostgreSQL)** – Manages the relational database
- **S3 Bucket** – Stores media files
- **CloudFront** – Distributes media files from the S3 Bucket via CDN for faster access



## Frontend Technologies

- **HTML**
- **CSS**
- **Bootstrap 5.3** – for responsive design and UI components
- **Django Template Language (DTL)** – for rendering dynamic content on the server side



## SSL/TLS (HTTPS)
Secure HTTPS is enabled using SSL/TLS certificates provided by Let’s Encrypt, managed via Certbot.

<img src="docs/images/ssl.png" alt="SSL TLS" width="400"/>




## Unit and Integration Testing
The project achieves 94% test coverage, ensuring strong code reliability and stability.

<img src="docs/images/test_coverage.png" alt="Unit and Integration Testing" width="400"/>




## Telegram Notification Bot
The application features a Telegram bot that sends notifications for various events, including new messages, user registrations, and new comments on posts.

<img src="docs/images/telegram.png" alt="Telegram Bot" width="200"/>


## Registration and Login
Registration is email-based, and only registered users can comment on posts.

<img src="docs/images/logit_register.png" alt="Login Register" width="600"/>



### Posts List Page (Homepage)
View for anonymous or authenticated users (not superusers).

<img src="docs/images/homepage_anonymous.png" alt="Homepage Anonymous" width="600"/>

Superusers have access to extra features on the Posts List Page:
- A `+` button to create a new post.
- A small tool panel under each post with `arrows buttons` to move it, an `edit button`, and a `delete button`.

<img src="docs/images/homepage_super_user.png" alt="Homepage Superuser" width="600"/>



### Post Detail Page (Post Content Page)
View for anonymous users. They can see comments but must log in to leave them.

<img src="docs/images/post_content_anonymous.png" alt="Post Detail Anonymous" width="600"/>

View for authenticated users (not superusers).

<img src="docs/images/post_content_just_user.png" alt="Post Detail Authenticated Users" width="600"/>

Superusers have access to the “Block Creation Panel,” which allows them to create post content using blocks.

Currently, three types of blocks are available, each with its own customization options:
- Text Block
- Image Block
- Space Block

<img src="docs/images/post_content_super_user.png" alt="Post Detail Superusers" width="600"/>

### Comments
Logged-in users can leave comments and delete their own, while superusers can delete any comment across the entire application.

<img src="docs/images/comments.png" alt="Post Detail Comments" width="600"/>

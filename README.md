# mykytaso.com






### Deployment on AWS

The application is fully deployed on AWS using the following services:

- **EC2** – Hosts the Ubuntu server running the application
- **RDS (PostgreSQL)** – Manages the relational database
- **S3 Bucket** – Stores media files
- **CloudFront** – Distributes media files from the S3 Bucket via CDN for faster access



### Frontend Technologies

- **HTML**
- **CSS**
- **Bootstrap 5.3** – for responsive design and UI components
- **Django Template Language (DTL)** – for rendering dynamic content on the server side



### SSL/TLS (HTTPS)
Secure HTTPS is enabled using SSL/TLS certificates provided by Let’s Encrypt, managed via Certbot.
![SSL/TLS](/docs/images/ssl.png)



### Unit and Integration Testing
The project achieves 94% test coverage, ensuring strong code reliability and stability.
![Unit and Integration Testing](/docs/images/test_coverage.png)



### Telegram Notification Bot
The application features a Telegram bot that sends notifications for various events, including new messages, user registrations, and new comments on posts.
![Telegram Bot](/docs/images/telegram_bot.png)



### Registration and Login
Registration is email-based, and only registered users can comment on posts.
![Login Register](/docs/images/logit_register.png)


### Posts List Page (Homepage)
View for anonymous or authenticated users (not superusers).
![Homepage Anonymous](/docs/images/homepage_anonymous.png)

Superusers have access to extra features on the Posts List Page:
- A `+` button to create a new post.
- A small tool panel under each post with `arrows buttons` to move it, an `edit button`, and a `delete button`.

![Homepage Superuser](/docs/images/homepage_super_user.png)

### Post Detail Page (Post Content Page)
View for anonymous users. They can see comments but must log in to leave them.
![Post Detail Anonymous](/docs/images/post_content_anonymous.png)

View for authenticated users (not superusers).
![Post Detail Authenticated Users](/docs/images/post_content_just_user.png)

Superusers have access to the “Block Creation Panel,” which allows them to create post content using blocks.

Currently, three types of blocks are available, each with its own customization options:
- Text Block
- Image Block
- Space Block

![Post Detail Superusers](/docs/images/post_content_super_user.png)

### Comments
Logged-in users can leave comments and delete their own, while superusers can delete any comment across the entire application.

![Post Detail Comments](/docs/images/comments.png)
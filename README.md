# Django Auction Website

A **dynamic online auction platform** built with Django where users can register, create and view auctions, place bids,
add comments, manage watchlists, and browse items by category.

---

## Overview

This web app offers a fully interactive platform where users can create and manage auction listings, showcase their
items with detailed descriptions and images, and engage
in competitive bidding with other users in real-time. Beyond simply placing bids, users can leave comments, track their
favorite auctions
through personalized watchlists, and explore items filtered by categories, making the experience both social and
organized. The platform is
designed to be intuitive and visually appealing, providing a seamless experience from listing an item to winning an
auction.

---

## Features

### User System

- Register, log in, and log out securely
- Each user automatically gets a personal watchlist

### Auction Management

- Create, view, and close auctions
- Upload images via URL or file
- Add detailed descriptions and categories

### Bidding & Comments

- Place bids higher than the current price
- Leave comments on auctions
- Get instant feedback via Django messages

### Watchlist

- Add or remove items to your watchlist
- View all saved auctions in one place

### Categories

- Filter auctions by category
- View only relevant listings

### Frontend

- Complete responsive design for all pages
- Modern styling using HTML, CSS, and SCSS
- Consistent navigation and layout across the platform

---

## Project Structure

```
commerce/
│
├───auctions
│   │   admin.py
│   │   apps.py
│   │   forms.py
│   │   models.py
│   │   signals.py
│   │   tests.py
│   │   urls.py
│   │   URL_to_image.py
│   │   views.py
│   │   __init__.py
│   │
│   ├───migrations
│   │   │   0001_initial.py
│   │   │   0002_list_auctions_comment_bids_watchlist_watchlist_items.py
│   │   │   0003_alter_list_auctions_end_date.py
│   │   │   0004_alter_list_auctions_category.py
│   │   │   0005_list_auctions_photo_file.py
│   │   │   0006_alter_comment_auction.py
│   │   │   0007_alter_watchlist_items_auction.py
│   │   │   0008_alter_watchlist_user.py
│   │   │   0009_watchlist_count_items.py
│   │   │   0010_remove_watchlist_count_items.py
│   │   │   0011_list_auctions_number_of_bids.py
│   │   │   0012_comment_number_of_comments.py
│   │   │   0013_remove_comment_number_of_comments.py
│   │   │   0014_list_auctions_winner.py
│   │   │   __init__.py
│   │   │
│   │
│   ├───static
│   │   └───auctions
│   │           auction_info.scss
│   │           auction_page.scss
│   │           bids_and_comments.scss
│   │           category_filter.scss
│   │           close_auction.scss
│   │           create_auction.scss
│   │           each_auction.scss
│   │           layout_style.scss
│   │           login_register.scss
│   │           nav.scss
│   │           nothing_here.png
│   │           no_login.png
│   │           variables.scss
│   │           watchlist.scss
│   │
│   ├───templates
│   │   └───auctions
│   │           auction.html
│   │           categories.html
│   │           create_auction.html
│   │           index.html
│   │           layout.html
│   │           login.html
│   │           not_login.html
│   │           register.html
│   │           watchlist.html
│   │
├───commerce
│   │   asgi.py
│   │   settings.py
│   │   urls.py
│   │   wsgi.py
│   │   __init__.py
│   │
│   └───__pycache__
│           settings.cpython-310.pyc
│           urls.cpython-310.pyc
│           wsgi.cpython-310.pyc
│           __init__.cpython-310.pyc
│
├───templates
└───__pycache__
        manage.cpython-310.pyc
```

## Models

| Model               | Description                                        |
|---------------------|----------------------------------------------------|
| **User**            | Custom user model based on Django’s `AbstractUser` |
| **List_Auctions**   | Represents auction listings                        |
| **Comment**         | Stores user comments on auctions                   |
| **Watchlist**       | One-to-one relationship with each `User`           |
| **Watchlist_Items** | Contains individual auctions in a user's watchlist |
| **Bids**            | Tracks user bids per auction                       |

---

## How It Works

### User Registration & Login

- New users can register and log in securely.
- A **watchlist** is automatically created for each new user (using Django signals).

### Creating an Auction

- Users fill out a form with title, category, description, and an optional image (URL or upload).
- The listing is immediately available to other users once created.

### Bidding & Commenting

- Users can place bids higher than the current one.
- Comments can be added to each auction’s page.
- Validation ensures bids are only accepted when they exceed the current price.

### Watchlist System

- Add or remove auctions from a personal watchlist anytime.
- View all saved auctions conveniently in one place.

### Categories Filter

- Browse or filter auctions by category for a smoother experience.

---

## Tech Stack

- **Backend:** Django 5.x
- **Frontend:** HTML, CSS, SCSS (Responsive design)
- **Database:** SQLite (via Django ORM)
- **Authentication:** Django’s built-in authentication system
- **Utilities:** Django signals, messages framework

---

## Author

**Sarina**  
*Computer Engineering Student* | *Passionate about Web Development*

**Email:** [sarinababadi900@gmail.com](mailto:sarinababadi900@gmail.com)  
**GitHub:** [Sarina-b](https://github.com/Sarina-b)


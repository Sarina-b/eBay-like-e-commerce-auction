# Django Auction Website

A **dynamic online auction platform** built with Django where users can register, create and view auctions, place bids, add comments, manage watchlists, and browse items by category.

---

## Overview

This web app provides an interactive space for users to list items for auction, compete with others through bidding, and maintain personal watchlists.  
The backend is **fully functional and stable**, while the frontend is still **a work in progress**.

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

---

## Project Structure

```
commerce/
│
├── auctions/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── __init__.py
│   │
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_list_auctions_comment_bids_watchlist_watchlist_items.py
│   │   ├── 0003_alter_list_auctions_end_date.py
│   │   ├── 0004_alter_list_auctions_category.py
│   │   ├── 0005_list_auctions_photo_file.py
│   │   ├── 0006_alter_comment_auction.py
│   │   ├── 0007_alter_watchlist_items_auction.py
│   │   ├── 0008_alter_watchlist_user.py
│   │   └── __init__.py
│   │
│   ├── static/auctions/
│   │   ├── auction.css
│   │   ├── create_auction.css
│   │   ├── create_auction.scss
│   │   └── styles.css
│   │
│   └── templates/auctions/
│       ├── auction.html
│       ├── categories.html
│       ├── create_auction.html
│       ├── index.html
│       ├── layout.html
│       ├── login.html
│       ├── register.html
│       └── watchlist.html
│
├── commerce/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── media/
└── templates/
```
## Models

| Model   | Description |
|--------|-------------|
| **User**            | Custom user model based on Django’s `AbstractUser` |
| **List_Auctions**   | Represents auction listings                        |
| **Comment**         | Stores user comments on auctions                   |
| **Watchlist**       | One-to-one relationship with each `User`           |
| **Watchlist_Items** | Contains individual auctions in a user's watchlist |
| **Bids**            | Tracks user bids per auction                       |

---

## How It Works

###  User Registration & Login
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
- **Frontend:** HTML, CSS, SCSS , JavaScript *(in progress)*  
- **Database:** SQLite (via Django ORM)  
- **Authentication:** Django’s built-in authentication system  
- **Utilities:** Django signals, messages framework  

---

## Author

**Sarina**  
*Computer Engineering Student* | 💡 *Passionate about Web Development*  

**Email:** [sarinababadi900@gmail.com](mailto:sarinababadi900@gmail.com)  
**GitHub:** [Sarina-b](https://github.com/Sarina-b)


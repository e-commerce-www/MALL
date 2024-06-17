<h1 align="center">
  <br>
  <a href="https://github.com/e-commerce-www/MALL.git"><img src="https://github.com/e-commerce-www/MALL/assets/158125247/2bd4c467-8770-40b4-975a-4b4060b01b9d" alt="MVP" width="500"></a>
</h1>

<h4 align="center">
A music platform for indie musicians to sell their tracks and for buyers to legally use them in creative projects.</h4>

<p align="center">
<a href="https://github.com/e-commerce-www/MALL/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-v3.10.12-yellow"></a>
<a href="https://github.com/e-commerce-www/MALL.git"><img src="https://img.shields.io/badge/PRs-welcome-green"></a>
<a href="https://www.paypal.me/madEffort"><img src="https://img.shields.io/badge/$-donate-ff69b4"></a>
</p>

<p align="center">
  <a href="#key-features">Key Features</a> • <a href="#database-erd">Database ERD</a> • <a href="#how-to-use">How To Use</a> • <a href="#download">Download</a> • <a href="#credits">Credits</a> • <a href="#related">Related</a> • <a href="#support">Support</a> • <a href="#license">License</a>
</p>

<img src="https://github.com/e-commerce-www/MALL/assets/158125247/53dd779e-7971-40c9-a5a2-57c434e0141c" alt="MVP"/>

## What is Music Value Platform?

The "music value platform" is an online marketplace that enables indie musicians to sell their music while allowing buyers to legally use the purchased music in various creative works.

## Key Features

**1. Login / Sign-Up**
- Supports Google and Naver social logins.
  
**2. Favorite Music**
- Allows users to favorite or unfavorite tracks.
- Clicking 'Favorite Music' in the NavBar displays favorited tracks with thumbnails, titles, artists, lyrics buttons, MP3 players, and purchase options.
- Removing from favorites deletes the track from the list.
- Recent tracks: Displays the last 10 played tracks with the most recent at the top and the oldest removed.

**3. My Page (Home/Purchase History/Sales History/Following)**
- **Home**
  - Profile picture and nickname can be edited.
  - Buyers have shortcuts for 'Favorite Music' and 'Apply as Seller.'
  - Displays the most recent 9 purchased tracks as thumbnails.
- **Purchase History**
  - Displays purchase date, title, creator, and price in descending order.
  - Click the purchase date to view detailed payment information.
- **Sales History**
  - Shows registration date, title, number of buyers, and total revenue of the seller's tracks.
- **Following**
  - Lists followed artists and their latest activities.
  - Allows removing artists from the following list.
 
**4. Music Upload (Seller Only)**
- Only sellers can upload music.
- Required: title, genre, tempo, thumbnail, and audio file. Optional: lyrics.
- Unified pricing of 3,000 KRW per track.

**5. Homepage (Search/New Releases/TOP5)**
- **Search**
  - Search by song title.
  - If duplicates exist, search specifically by '**Song Title; Artist Name**'
- **New Releases**
  - Displays the four most recent tracks.
- **TOP5**
  - Shows the top five ranked tracks based on a time-weighted ranking algorithm.

    Time-Weighted ranking algorithm formula:

    $$L\\\_decayed = \sum_{i=1}^{n} 0.5^{\frac{t_{now} - t_i}{T}}$$
  
    [Go to Time-Weighted Ranking Algorithm Formula Wiki...](https://github.com/e-commerce-www/MALL/wiki/Time%E2%80%90weighted-ranking-algorithm-formula)

  - The ranking is determined by the score calculated using the time-weighted ranking algorithm formula.

**6. Chart Screen (Recent/Popular/Genre/Tempo/Search)**
- Accessed via '**Music**' in the NavBar.
- **Recent**
    - Lists tracks in reverse chronological order of upload.
- **Popular**
    - Displays tracks by highest scores from the ranking algorithm.
- **Genre/Tempo/Search**
    - Filter tracks by genre, tempo, or title.

## Database ERD

To view the **`Database ERD`**, please click [here](https://www.erdcloud.com/p/JYqD8jKydarZYmrxE).
               
## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com) and [Python](https://www.python.org/downloads/) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/e-commerce-www/MALL.git

# Go into the repository
$ cd MALL

# Install dependencies
$ pip install -r requirements.txt
or
$ poetry install
```

After setting up the database and templates, please use the `makemigrations`, `migrate` and `collectstatic` commands.

```bash
# Run the app
$ python manage.py runserver
```

## Download

You can [download](https://github.com/e-commerce-www/MALL/releases) the latest release version of the MVP(Music-Value-Platform).

## Credits

This software uses the following open source packages:

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Bootstrap5](https://getbootstrap.com/)

## Related

- [Amazon Web Service](https://aws.amazon.com/) : AWS S3
- [Twilio](https://www.twilio.com) : SMS Phone Verification
- [PortOne](https://www.portone.io) : Payment Module

## Support

<a href="https://www.paypal.com/paypalme/madEffort">
<img src="https://raw.githubusercontent.com/stefan-niedermann/paypal-donate-button/master/paypal-donate-button.png" alt="Donate with PayPal" width="200">
</a>

## License

This project adheres to the Apache-2.0 license, and you can find more detailed information in the [LICENSE](https://github.com/e-commerce-www/MALL/blob/main/LICENSE)

---

> GitHub <br>
> [@madEffort](https://github.com/madEffort) &nbsp;&middot;&nbsp; [@2taeyeon](https://github.com/2taeyeon) &nbsp;&middot;&nbsp; [@chlryddk](https://github.com/chlryddk) &nbsp;&middot;&nbsp; [@HalalGuys1232](https://github.com/HalalGuys1232) &nbsp;&middot;&nbsp; [@ieunchan](https://github.com/ieunchan) &nbsp;&middot;&nbsp; [@KMJ7916](https://github.com/KMJ7916)

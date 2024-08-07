<img src="images/logo.png" alt="logo" width="200" style="display: block; margin-left: auto; margin-right: auto; width: 40%"/> <br>

# TerpAlert
[https://terpalert.xyz](https://terpalert.xyz)

TerpAlert is a web application to designed to help students at the University of Maryland track foods being served at dining halls

## About The Project
![Screenshot of website landing page](images/landing_page.png)

During my freshman year at the University of Maryland, I discovered my favorite food in the dining halls: Orange Tempura Chicken.
If I could, I would eat it for every meal. However, the dining halls did not serve it every day, so I was often left guessing what I would have for my next meal.
After bringing this issue up with my friends, I found that we shared a common desire: to know when the dining halls are serving our favorite foods.
Thus, TerpAlert was born.

### Built With
* [![Django][Django.com]][Django-url]
* [![PostgreSQL][Postgres.com]][Postgres-url]
* [![BeautifulSoup][BeautifulSoup.com]][BeautifulSoup-url]
* [![Python][Python.com]][Python-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JS][JS.com]][JS-url]
* [![JQuery][JQuery.com]][JQuery-url]
* [![DigitalOcean][DigitalOcean.com]][DigitalOcean-url]


## Features 

### Automated Web Scraping
  
-  Scrapes menu for each dining hall every morning using BeautifulSoup
-  Updates PostgreSQL database
-  Automated utilizing Digital Ocean's serverless functions

### Account Creation
-  Users can create accounts to set alerts for certain foods
-  Email verification using Mailgun API
-  Option to receive emails for their alerts

![Gif of a user adding an alert to their account and deleting another](/images/terpalert.gif)

### Alerts
-  Stored in PostgreSQL database
-  After the daily menu scraping is complete, users with alerts present in the menu are notified
-  Alert emails sent using Mailgun API

<img src="images/alert.png" alt="Example of an email a user would receive with their alerts" width="500" /> <br>

[//]: # (## Reflection)

[//]: # ()
[//]: # (  - What did you set out to build?)

[//]: # (  - Why was this project challenging and therefore a really good learning experience?)

[//]: # (  - What were some unexpected obstacles?)

[//]: # (  - What tools did you use to implement this project?)

[//]: # (      - This might seem obvious because you are IN this codebase, but to all other humans now is the time to talk about why you chose webpack instead of create react app, or D3, or vanilla JS instead of a framework etc. Brag about your choices and justify them here.  )

## Contact
Email: thuitema@umd.edu

<!-- MARKDOWN LINKS & IMAGES -->
[Django.com]: https://www.djangoproject.com/m/img/badges/djangomade124x25.gif
[Django-url]: https://www.djangoproject.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
[BeautifulSoup.com]: https://shields.io/badge/BeautifulSoup-4-green
[BeautifulSoup-url]: https://beautiful-soup-4.readthedocs.io/
[Postgres.com]: https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white
[Postgres-url]: https://www.postgresql.org/
[DigitalOcean.com]: https://img.shields.io/badge/-Digital_Ocean-blue?style=for-the-badge&logo=digitalocean&logoColor=white
[DigitalOcean-url]: https://digitalocean.com/
[Python.com]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[JS.com]: https://shields.io/badge/JavaScript-F7DF1E?logo=JavaScript&logoColor=000&style=flat-square
[JS-url]: https://www.javascript.com/
-- Marketplace Couch Notification Bot --
Contributions: Tanner Bergstrom, Kyle Burtt
Date: August 2024
Description: Over the Summer of 2024, we resold couches on Facebook Marketplace. We created this notification bot to send us couches so that we could be up to date on new and good deals.

To Accomplish this, we used Playwright, Beautifulsoup, and smtplib via Python and our virtual environment was created through Pycharm. Beautifulsoup provided us with html data from the webpage and 
Playwright allowed us to perform actions on the webpage such as login and click search automatically. smtplib is built in and allowed us to send emails from a custom gmail account we made.

We only sent the links that had not previously been sent and logged all links in a text file. This program is limited to searching for couches within the prefences of the users facebook account.

import time

from smtplib import SMTP_SSL as SMTP, SMTPAuthenticationError, SMTPRecipientsRefused
from email.mime.text import MIMEText

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


#
# Authors: Kyle Burtt, Tanner Bergstrom
# Date made: 8/7/2024
#

#
# This search method is used to open up chrome and log you into facebook,
# It will then download the contents of the page using beatiful soup and then we search
# It will then give us the first 25 links in the specified facebook marketplace
#

def search(username, password):
    with sync_playwright() as p:


        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(
            "https://www.facebook.com/marketplace/lehi/search/?query={couch}&maxPrice={500}")
        page.fill('input[name="email"]', username)
        page.fill('input[name="pass"]', password)

        # Click the login button
        page.click('button[name="login"]')

        # Wait for the navigation to complete after logging in
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(10000)

        # Downloads the HTML of the page
        content = page.content()

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        listing_links = []
        for a_tag in soup.find_all('a',
                                   class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv',
                                   limit=25):  # Use the correct class name from the image
            href = a_tag.get('href')
            if href and href.startswith('/marketplace/item/'):
                full_url = f"https://www.facebook.com{href}" + "\n"
                listing_links.append(full_url)
                if len(listing_links) >= 100:
                    break

        return listing_links


#
# This method is used to insert the links into our couches.txt searching the first 59 letters of the link
# to make sure there are no duplicates
#
def link_inserter(links):
    text_file = open("couches.txt", "r")
    oldLinks = text_file.read()

    linksToSend = []

    for link in links:
        if link[:59] not in oldLinks:
            # if link not in oldLinks:
            linksToSend.append(link)
            oldLinks += link

    text_file = open("couches.txt", "w")

    text_file.write(oldLinks)

    return linksToSend


#
# After everything is complete this method sends the listing links to our email.
#
def email(linksToSend, email):
    if len(linksToSend) == 0:
        print("empty")
        return
    else:
        print("sent!")
    newLinks = []
    for links in linksToSend:
        links += "\n " "\n"
        newLinks.append(links)

    SMTPserver = 'smtp.gmail.com'
    sender = 'marketplacechatbot04@gmail.com'
    destination = [email]

    USERNAME = "marketplacechatbot04@gmail.com"
    PASSWORD = "yoaf tnde xyji khvf"

    # typical values for text_subtype are plain, html, xml
    text_subtype = 'plain'

    content = "".join(newLinks)

    subject = "Sent from Python"

    msg = MIMEText(content, text_subtype)
    msg['Subject'] = subject
    msg['From'] = sender  # some SMTP servers will do this automatically, not all

    conn = SMTP(SMTPserver)
    conn.set_debuglevel(False)
    try:
        conn.login(USERNAME, PASSWORD)
    except SMTPAuthenticationError:
        print("invalid email and or password")

    try:
        conn.sendmail(sender, destination, msg.as_string())
    except SMTPRecipientsRefused:
        print("invalid email")
    finally:
        conn.quit()


def main(userEmail, username, password):
    while (True):
        links = search(username, password)

        linksToSend = link_inserter(links)

        email(linksToSend, userEmail)

        return len(linksToSend)


if __name__ == "__main__":
    main()

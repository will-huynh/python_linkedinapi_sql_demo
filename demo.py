import requests
import secrets
import logging
import json
import urllib.parse
import psycopg2
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


"""
Quick configuration for application and LinkedIn page details:
"""
LINKEDIN_CLIENT_ID = '78cjanw7mnacza'  # todo - fill this field up
LINKEDIN_CLIENT_SECRET = 'LwWuONUPTexQNcT9'  # todo - fill this field up
BASE_URL = 'linkedin.com/feed'
PORTAL_URL = 'https://www.' + BASE_URL
REDIRECT_URI = 'https://' + BASE_URL
WEBDRIVER_PATH = r'C:\Users\Will\Documents\python_linkedinapi_sql_demo\chromedriver.exe'
DB_NAME = 'testdb'
PG_USER = 'postgres'
PG_PASSWORD = 'postgres'


"""
Initialize and configure the logger for the module.
"""
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


"""
Generate an authorization URL for a user to give permission to extract his/her Linkedin Profile.
"""
def generate_authorization_url(linkedin_client_id=LINKEDIN_CLIENT_ID, linkedin_client_secret=LINKEDIN_CLIENT_SECRET, redirect_uri=REDIRECT_URI):
    LI_AUTH_URL = 'https://www.linkedin.com/oauth/v2/authorization'
    logging.info("Generating authentication URL for LinkedIn...")
    try:
        url = requests.Request('GET', LI_AUTH_URL,
                               params={
                                   'response_type': 'code',
                                   'client_id': LINKEDIN_CLIENT_ID,
                                   'redirect_uri': REDIRECT_URI,
                                   'state': secrets.token_hex(8).upper(),
                                   'scope': 'r_liteprofile r_emailaddress w_member_social',
                               }).prepare().url
        logging.debug("Generated authentication URL: {}".format(url))
    except:
        raise RuntimeError("Could not generate authentication URL, please check client configuration.")
    return url


"""
Use Selenium to request user login to LinkedIn and app authorization.
"""
def get_authentication(driver, base_url=BASE_URL, portal_url=PORTAL_URL):
    logging.debug("Generating authentication URL...")
    auth_url = generate_authorization_url()
    logging.info("Requesting user authentication for application...")
    driver.get(portal_url)
    try:
        if driver.current_url is not portal_url:
            logging.warning("Please sign in to LinkedIn in the provided browser to continue with authentication.")
            wait = WebDriverWait(driver, 120) #Timeout is set as constant; fully developed tool would include config for timeout
            wait.until(EC.url_contains(portal_url))
        logging.info("User is signed into LinkedIn, navigating to authentication URL...")
        driver.get(auth_url)
        logging.warning("Permission is needed to work with LinkedIn profile data, please approve the application in the provided browser to continue.")
        wait = WebDriverWait(driver, 120) #Timeout is set as constant; fully developed tool would include config for timeout
        wait.until(EC.url_contains(portal_url))
        logging.info("Permission on LinkedIn has been granted by the user, getting authorization code...")
        logging.debug("Returned authentication URL: {}".format(driver.current_url))
        auth_code = driver.current_url.split("?code=")[1].split("&state")[0] #replace current parsing method using urllib
        logging.debug("Retrieved auth_code: {}".format(auth_code))
    except:
        raise RuntimeError("Failed to navigate with LinkedIn using Selenium or authentication code could not be retrieved (user failed or denied authentication). Please re-attempt sign-in and app authentication or check tool configuration.")
    return auth_code


"""
Given a authorization `code`, this function will return you `access_token` which can then be used to access a user's Linkedin profile.
"""
def get_access_token(authorization_code, linkedin_client_id=LINKEDIN_CLIENT_ID, linkedin_client_secret=LINKEDIN_CLIENT_SECRET, redirect_uri=REDIRECT_URI):
    LI_ACCESS_TOKEN_EXCHANGE_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
    logging.info("Requesting access token from LinkedIn...")
    try:
        access_token = requests.post(LI_ACCESS_TOKEN_EXCHANGE_URL, params={
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': redirect_uri,
            'client_id': LINKEDIN_CLIENT_ID,
            'client_secret': LINKEDIN_CLIENT_SECRET,
        }).json()['access_token']
    except:
        raise RuntimeError("Access token could not be retrieved, please check tool configuration and if an authorization code has been retrieved (did the user provide permissions on LinkedIn).")
    return access_token


"""
Get the user's LinkedIn profile information.
"""
def get_profile(access_token):
    LI_PROFILE_API_ENDPOINT = 'https://api.linkedin.com/v2/me'
    logging.info("Attempting to retrieve user profile data...")
    try:
        user_data = requests.get(LI_PROFILE_API_ENDPOINT, headers={
                         'Authorization': 'Bearer ' + access_token})
    except:
        raise RuntimeError("User data could not be retrieved, check if user authentication and generation of access token.")
    return user_data.json()


"""
Parse user data as JSON string for user's last name and LinkedIn ID and write to PostgreSQL table.
"""
def user_data_to_pgsql(user_json, db_name=DB_NAME, user=PG_USER, password=PG_PASSWORD):
    try:
        logging.warning("Getting user data from provided JSON string...")
        row = [user_json['localizedLastName'], user_json['id']]
        logging.debug("Retrieved user data: {}".format(row))
        logging.warning("Attempting to insert data into database...")
        sql = "INSERT INTO linkedin_data VALUES ('{0}', '{1}');".format(row[0], row[1])
        conn = psycopg2.connect("dbname={0} user={1} password={2}".format(db_name, user, password))
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        logging.warning("Data successfully inserted.")
    except:
        raise RuntimeError("Data could not be inserted into database, check given json string and database connection.")


"""
Run the demo.
"""
def run_demo(webdriver_path=WEBDRIVER_PATH):
    logging.warning("Starting demo for profile data retrieval...")
    logging.warning("Generating authentication url...")
    auth_url = generate_authorization_url()
    logging.warning("Initializing browser with Selenium integration...")
    driver = webdriver.Chrome(executable_path=webdriver_path) #initialize browser for user authentication
    logging.warning("Getting user autheorization and retrieval of authentication code...")
    auth_code = get_authentication(driver)
    logging.warning("Getting access token...")
    access_token = get_access_token(auth_code)
    logging.warning("Getting user data in json format...")
    data = get_profile(access_token)
    logging.warning("Profile data was retrieved, printing data to console...")
    logging.warning("Data: {}".format(data))
    logging.warning("Attempting to insert user data into database...")
    user_data_to_pgsql(data)
    logging.warning("Demo completed successfully!")


if __name__ == "__main__":
    run_demo()

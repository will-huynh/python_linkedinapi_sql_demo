# python_linkedinapi_sql_demo

*python_linkedin_sql_demo* is a demo created to very briefly showcase integration between Python, Selenium, the LinkedIn API, and PostgreSQL. The demo uses Selenium and the [LinkedIn API](https://www.linkedin.com/help/linkedin/answer/2836/accessing-linkedin-apis?lang=en) to obtain user authorization using OAuth2 and then gets the data as a JSON response. The response is then decoded and parsed for surname and user ID information. The retrieved information is then added to a PostgreSQL database.


## Demo Design and Flow:

The architecture/flow of the demo can be found at the following flowchart: https://lucid.app/lucidchart/6496e73a-d910-4a25-8afc-41921ba7e2e3/edit?viewport_loc=-540%2C848%2C3328%2C1952%2C0_0&invitationId=inv_5c3124c0-d95e-4384-9835-4ca6ffe2ab34.


## Required Packages/Software:

The following is required to run this demo:
* Windows 7 or later
* [Python 3.7](https://www.python.org/downloads/release/python-379/) or greater
* [Selenium](https://www.selenium.dev/)
* [Chromedriver 94.0.4606.61](https://chromedriver.storage.googleapis.com/index.html?path=94.0.4606.61/)
* [PostgreSQL 11.1-1](https://www.postgresql.org/download/windows/)
* [Google Chrome version 94](https://www.google.com/chrome/)


## Installation:

1. Clone the repository to your machine using git:

> git clone https://github.com/will-huynh/python_linkedinapi_sql_demo.git

2. Go to the cloned directory on your local machine and check for the latest version using git:

> Open a command prompt with administrator rights
> Navigate to the cloned *python_linkedinapi_sql_demo* directory using the command *cd <PARENT DIRECTORY>/python_linkedinapi_sql_demo* (ex: cd C:\Users\Guest\Documents\python_linkedinapi_sql_demo)
> git branch master
> git pull

3. Download [ChromeDriver 94.0.4606.61](https://chromedriver.storage.googleapis.com/index.html?path=94.0.4606.61/) and extract the archive.
4. Open the extracted folder and place the "chromedriver.exe" in the python_linkedinapi_sql_demo directory (the cloned directory).
5. Install PostgreSQL and start the SQL Shell (especially for newer users).
6. Proceed past the initial prompts for Server, Database, Port, Username, and Password by hitting Enter; the fields can be left blank unless credentials were configured during installation.
7. Use the command *CREATE DATABASE testdb;*. This will create a new database named "testdb" although another name can be used if configured in the demo file under *Quick Configuration...*.
8. Use the command *\c testdb* to connect to the new database.
9. Use the command *CREATE TABLE linkedin_data (last_name text, user_id text);* to create a simple table.
10. Use *TABLE linkedin_data;* to view the table structure (two columns labeled "last_name" and "user_id") and table contents. (This is normally an inefficient method of viewing a table but is sufficient for this scope.)


## Using the demo:

The demo is used by invoking its main Python file from a command prompt. Due to accelerated development, the command prompt used for invoking the demo will display logs describing the activity of the demo to the user. Additionally, PostgreSQL must be actively running on the local machine since the demo does not include methods to initialize PostgreSQL. See the *Future Improvements* section for more details on goals for future development.
  
To use the demo, follow the below steps:
1. Start the PostgreSQL database described under *Installation*. Instead of following step 6 under *Installation*, the database name (ex: testdb) can be entered when prompted for the "Database" option.
2. Open a command prompt with administrator rights.
3. Navigate to the demo directory using the following command in the command prompt: *cd <PARENT DIRECTORY>/python_linkedinapi_sql_demo* (ex: cd C:\Users\Guest\Documents\python_linkedinapi_sql_demo)
4. Once in the demo directory, start the demo by using the command *py demo.py* or *python demo.py*.
5. A Google Chrome browser will open (controlled by Selenium); follow the prompts given in the command prompt window. The activities required of the user will be:
> Signing into LinkedIn using the provided browser
> Authorizing the LinkedIn application to have access to the user's profile data

6. Once the demo has finished operating successfully, a confirmation will be displayed as a log in the command prompt window.
7. To view the results of operation, navigate to the SQL Shell window and use the command *TABLE linkedin_data;*.
  
## Future Improvements

This script was designed as a quick demo and as a result some compromises were taken with design choices. Improvements would then focus around further factoring of methods and modules and an expansion of capabilities. See below for areas of potential improvement for the demo:
  
* The demo was designed in one module which is somewhat appropriate for its current size (157 lines); it can be re-factored in the future to be cleaner and additional code should be abstracted into their own modules/classes.
* The number of hard-coded strings for SQL statements and configuration can be decreased.
* The demo can automatic initialization of services (ex: downloading ChromeDriver, creating database, starting server, automatically returning a table view).
* Different types of data can be collected from LinkedIn though this is somewhat outside the scope of the demo.
* The Selenium-controlled browser window and inputs can be integrated into the console view instead.
* More organized logs or a graphical view can be included.
* The demo can be designed with interactive or file-based configuration rather than hard-coded configuration directly in the script file.
* Less globals can be used (though this may not be an issue if the module is designed as a class itself).
* Ethereum blockchain technology can be showcased as well by writing SQL tables to a test blockchain using a smart contract and the Python integration of the [web3 library](https://web3js.readthedocs.io/en/v1.5.2/).

# PANDA
## Video Demo:  <https://www.youtube.com/watch?v=NNms4wQiJaE>
## Description:

### Modules:
#### PANDA: Neonatal
We have a challenge locally in supporting doctors and nurses to write discharge summaries for newborn infants accurately and in a timely fashion.
Many of these babies are monitored and occasionally treated for medical conditions, and the department is renumerated based on the content of discharge summaries.
If these summaries are not completed accurately the department loses money, if this takes more time than is necessary, there is a delay to getting families home.
Inspired by the finance project I have constructed a flask based web application, which interrogates a SQL database based on selections made from a form template.
This then populates a discharge summary which can be proof-read, edited, copied and submitted into the patient record.
Initially there is a registration page for users, these are added to a users database, and submissions can be reviewed and allowed by an administrator.
At the login page if a username or password is incorrect users are informed, and if they are correct but not yet verified they are also informed.
There are warning on the page not to re-use professional login details to register on this site.

There is one main page on the site to maintain usability and a simple interface.
This is generated procedurally based on the content of the main database.
Different heading and linked in a one to many and many to many relationship across two different tables.
These are handed to the web interface as a dictionary of lists and populated on the page.
This generates a series of headings with following mutually exclusive radio buttons, which are clearly highlighted when selected.
Once the relevant selections have been made, a submit button is selected the selections return to the flask based web app, a new list is generated with the correct options chosen.

Once displayed this paragraph is editable by the end user, and can then be selected and copied using a javascript element, ready for submission.

No data is stored in the process of generating such information and no patient details are included on the server side, and no way they could be uploaded, in keeping with data protection requirements.

An extension to the project in the future will be to allow administrator access in a graphical user interface, allowing users to be verified and editing or new patient populations to be served without interacting with the underlying database or programming.

#### Clever Magpie
Magpie is the mobile guidelines application at the Royal Cornwall Hospital NHS Foundation Trust.
Clever Magpie performs a semantic search of a clinical question within hospital guidelines, returning a link to the most relavent page of the guideline for a health professional to answer their question. 

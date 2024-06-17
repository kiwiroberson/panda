import os
import sqlite3

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from dotenv import load_dotenv
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///discharge.db")
index = db.execute("SELECT * FROM Neonataldc")

subcategoryindex = db.execute("SELECT * FROM subcategory")


question_dictionary = {}
answer_dictionary = {}
diag_code_list = {}
subcategory_dictionary = {}

for item in index:
    if item['code'] not in question_dictionary:
        question_dictionary[item['code']]=item['question']
    if item['code'] not in answer_dictionary:
        answer_dictionary[item['code']]=item['string']

for item in subcategoryindex:
    if item['subcategory'] not in subcategory_dictionary:
        subcategory_dictionary[item['subcategory']]=item['subcategorytext']

all_dictionary = {}
diagcode_list = []
for item in index:
    if item['code'] not in all_dictionary:
        all_dictionary[item['code']] = [item['question'], item['string'], item['diagcode']]
    if item['diagcode'] not in diagcode_list:
        diagcode_list.append(item['diagcode'])

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        # Chack which branch of code running in terminal
        print("post index")
        #Start list to display in app
        selected_list = []
        #iterate through catagories of answer
        print (diagcode_list)
        for item in diagcode_list:
            #check if catagory present, and skip step if not
            if request.form.get(item) == None:
                print("n "+str(request.form.get(item)))
                continue
            else:
                 #append selected diagcode to lst to print
                print("y "+str(request.form.get(item)))
                selected_list.append(all_dictionary[request.form.get(item)][1])
        return render_template("index.html", diagcode_list=diagcode_list, selected_list=selected_list, all_dictionary=all_dictionary, subcategory_dictionary=subcategory_dictionary)

    else:
        #check app route running
        print("get index")
        return render_template("index.html", diagcode_list=diagcode_list, all_dictionary=all_dictionary, subcategory_dictionary=subcategory_dictionary)

@app.route("/clever_magpie", methods=["GET", "POST"])
@login_required
def clever_magpie():
    if request.method == "POST":
        print("post magpie")
        query = request.form.get('question')
        print(f"{query}")

        import os
        from dotenv import load_dotenv
        from langchain_pinecone import PineconeVectorStore
        from langchain_openai import OpenAIEmbeddings

        load_dotenv()
        OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
        PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]

        index_name = 'starter-index'
        embeddings = OpenAIEmbeddings()

        vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings)

        if query is None:
            render_template("clever_magpie.html", )
        else:
            
            result = vectorstore.similarity_search(query, k=1)
            title = result[0].metadata['title']
            url = result[0].metadata['url']
            page_num = result[0].metadata['page_num']
            return render_template("clever_magpie_answer.html", href=url, guideline=title, page=page_num)

    else:
        print("get magpie")

        return  render_template("clever_magpie.html", )

@app.route("/admin", methods=["GET", "POST"])
@login_required
def summary():
    if request.method == "POST":
        print("post summary")

        return render_template("admin.html", )

    else:
        print("get summary")
        return  apology("Please submit form", 400)

@app.route("/discharge", methods=["GET", "POST"])
@login_required
def discharge():
    if request.method == "POST":

        return
    else:
        return redirect("/")






@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        if rows[0]["confirmed"] != 1:
            return apology("please wait for user confirmation", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure new username was submitted
        if not request.form.get("username"):
            return apology("New username not entered", 400)
        # ensure new username not already taken
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) == 1:
            return apology("Username already taken", 400)

        #ensure new password entered
        if not request.form.get("password"):
            return apology("New password not entered", 400)

        ##nsure confirmation is entered

        if not request.form.get("confirmation"):
            return apology("Confirmation not entered", 400)

        #ensure password confimation matches initial password

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match", 400)

        #insert new username and password into db

        username = request.form.get("username")
        password = request.form.get("password")

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return
    
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))

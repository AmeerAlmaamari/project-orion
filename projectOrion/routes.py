from flask import render_template, url_for, flash, redirect, request, jsonify
from projectOrion import app, ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
#import pandas library's functions
import pandas as pd
#
import os
import datetime
import matplotlib.pyplot as plt
from random import choice, randint
#Using style sheets of Matplotlib
plt.style.use('fivethirtyeight')

# Check if there is already a data file, otherwise create an empty one:
if not os.path.isfile('projectOrion/data/data.csv'):
    data = pd.DataFrame(columns= ["Name","Email","Phone","Book","Genre","Pages Read"])
    data.to_csv("projectOrion/data/data.csv")

def update_data():
    # Load the old data file:
    data = pd.read_csv("projectOrion/data/data.csv", index_col=0).reset_index(drop=True)
    if os.path.isfile('projectOrion/uploads/last_upload.csv'):
        # Load the new data file:
        uploaded_data = pd.read_csv("projectOrion/uploads/last_upload.csv", index_col=0).reset_index(drop=True)
        # Concatenate old and new data together:
        data= pd.concat([data, uploaded_data]).reset_index(drop=True)
        # Save the concatenated file:
        data.to_csv("projectOrion/data/data.csv")

    # Count number of books read by members:
    num_books_read = len(pd.unique(data['Book']))

    # Count number of pages read by members:
    num_pages = sum(data["Pages Read"])

    # Put these two values in a table named Summary:
    summary = pd.DataFrame(data = {"Number of books read by members":[num_books_read],
                                  "Number of pages read by members":[num_pages]})
    summary.to_csv("projectOrion/data/summary.csv")

    # Count books read by each member(Ranking of group members based on number of books read):
    temp = data[["Name","Book"]].groupby('Name').nunique()
    temp = temp.drop("Name", axis=1).reset_index(drop=False)
    book_per_user = temp.sort_values(by='Book', ascending=False).reset_index(drop=True)
    # Save this data to a table:
    book_per_user.to_csv("projectOrion/data/book_per_user.csv")
    # Plot the graph and save it to the images directory:
    book_per_user.plot(x="Name", y="Book", kind = "bar",
                   title = "Number of Books Read per User", color = (0.13, 0.12,0.40))
    plt.savefig('projectOrion/static/images/Number of Books Read per User.svg', bbox_inches='tight')

    # Ranking of group members based on number of pages read :
    user_sum = data[["Name","Pages Read"]].groupby(['Name']).sum().sort_values(by='Pages Read', ascending=False).reset_index()
    # Save this data to a table:
    user_sum.to_csv("projectOrion/data/user_sum.csv")
    # Plot the graph and save it to the images directory:
    user_sum.plot(x="Name", y="Pages Read", kind = "bar",
                   title = "Members Ranking", color = (0.13, 0.12,0.40))
    plt.savefig('projectOrion/static/images/Members Ranking.svg', bbox_inches='tight')

    # Ranking of books mostly read by the group members
    book_sum = data[["Book","Pages Read"]].groupby(['Book']).sum().sort_values(by='Pages Read', ascending=False).reset_index()
    # Save this data to a table:
    book_sum.to_csv("projectOrion/data/book_sum.csv")
    # Plot the graph and save it to the images directory:
    book_sum.plot(x="Book", y="Pages Read", kind = "bar",
                   title = "Books Ranking", color = (0.13, 0.12,0.40))
    plt.savefig('projectOrion/static/images/Books Ranking.svg', bbox_inches='tight')

    # Ranking of books categories mostly read by the group members
    genre_sum = data[["Genre","Pages Read"]].groupby(['Genre']).sum().sort_values(by='Pages Read', ascending=False).reset_index()
    # Save this data to a table:
    genre_sum.to_csv("projectOrion/data/genre_sum.csv")
    # Plot the graph and save it to the images directory:
    genre_sum.plot(x="Genre", y="Pages Read", kind = "bar",
                   title = "Categories Ranking", color = (0.13, 0.12,0.40))
    plt.savefig('projectOrion/static/images/Categories Ranking.svg', bbox_inches='tight')

# This function loads the summary csv file:
def get_summary():
    summary = pd.read_csv("projectOrion/data/summary.csv", index_col=0)
    return list(summary.iloc[0])

# This function loads the user summary csv file:
def get_user_sum():
    user_sum = pd.read_csv(""
                           "projectOrion/data/user_sum.csv", index_col=0)
    return user_sum

# This function loads the category (genre) summary csv file:
def get_genre_sum():
    genre_sum = pd.read_csv("projectOrion/data/genre_sum.csv", index_col=0)
    return genre_sum

# This function loads the book summary csv file:
def get_book_sum():
    book_sum = pd.read_csv("projectOrion/data/book_sum.csv", index_col=0)
    return book_sum

# This function loads the file contains the ranking of group members based on number of books read:
def get_book_per_user():
    book_per_user = pd.read_csv("projectOrion/data/book_per_user.csv", index_col=0)
    return book_per_user


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
@app.route("/home")
def home():
    # Update the data:
    update_data()
    return render_template('home.html')


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html', title='Dashboard', summary = get_summary(),
                            user_sum = get_user_sum(), genre_sum = get_genre_sum(), book_sum = get_book_sum(),
                            book_per_user = get_book_per_user())

@app.route("/upload_csv", methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "last_upload.csv"))

            # Update the data:
            update_data()
            if os.path.exists("projectOrion/uploads/last_upload.csv"):
                os.remove("projectOrion/uploads/last_upload.csv")


            return redirect(url_for('dashboard'))
            # render_template('dashboard.html', title='Dashboard', summary = get_summary()[1:])


@app.route("/generate_data", methods=['GET', 'POST'])
def generate_data():
    if request.method == "POST":
        names = ["Ahmed", "Ali", "Mohammed", "Sami", "Ameer", "Jana", "Anwar", "Abdullah", "Tareq","Osama","Khaldon"]
        books = [{"Name":"Game Of Thrones", "Genre":"Fantasy", "Pages":350},
            {"Name":"Harry Poter", "Genre":"Fantasy", "Pages":1000},
            {"Name":"Algorithms", "Genre":"Education", "Pages":220},
            {"Name":"The Serpent Garden", "Genre":"Romance", "Pages":120},
            {"Name":"Say Yes to Yourself and No to Others", "Genre":"Self Dev", "Pages":80},
            {"Name":"Romeo and Juliet", "Genre":"Romance", "Pages":410}]

        users = [{"Name":name, "Email":f"{name}@orion.com", "Phone":"05"+str(randint(10000000,99999999))} for name in names]

        data = pd.DataFrame(columns = ["Name","Email","Phone","Book","Genre","Pages Read"])
        for sample in range(int(request.form["num_samples"])):
            user = choice(users)
            book = choice(books)
            pages_read = randint(5,book["Pages"]*0.5)
            data = data.append({'Name': user["Name"], 'Email': user["Email"], 'Phone': user["Phone"],
                                "Book":book["Name"], "Genre":book["Genre"], "Pages Read":pages_read},
                                ignore_index=True)
        data.to_csv("projectOrion/data/dummy_data.csv")
        return redirect(url_for('dashboard'))


@app.route("/about")
def about():
    return render_template('about.html')

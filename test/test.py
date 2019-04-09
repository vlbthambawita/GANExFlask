from flask import Flask, render_template

app = Flask(__name__)

# Test data
post_data = [
    {
        'author': 'Vajira',
        'title': 'Test title 1',
        'content': 'HElo',
        'date_posted': '02-04-2018'
    
    },
    {
        'author': 'Lasantha',
        'title': 'Test title 2',
        'content': 'HElo world',
        'date_posted': '06-03-2011'
    
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts= post_data)

@app.route("/about")
def about():
    return "This is about page"

if __name__ == "__main__":
    app.run(debug=True)
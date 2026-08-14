# imports
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
app = Flask(__name__)
Scss(app)

# learn what sqlalchemy is!!
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

# Data class ~ Row of data
# One model = one row of data


class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    # DateTime is an object here

    def __repr__(self):
        return f"Task{self.id}"

# Routes to Webpages


# POST MEANS SEND DATA AND GET MEANS RECIEVE DATA
@app.route("/", methods=["POST", "GET"])
def index():
    # Add tasks
    if request.method == "POST":
        # FIND OUT WHAT THIS LINE MEANS.
        current_task = request.form["content"]
        # UNDERSTAND THIS SECTION WELL.
        new_task = MyTask(content=current_task)
        try:  # IF YOU HAVE A TRY BLOCK, YOU SHOULD HAVE AN EXCEPTION JUST IN CASE YOU NEED TO HANDLE AND ERROR.
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error:{e}")
            # WHAT IS THE USE OF THIS LINE IF WE HAVE A PRINT STATEMENT THAT DOES THE SAME THING?
            return f"ERROR:{e}"
    # See all added tasks
    else:
        # ORDER_BY ARRANGES THE TASKS HOW YOU WANT IT
        tasks = MyTask.query.order_by(MyTask.created).all()
        # FIND OUT WHAT ALL() MEANS HERE
        # tasks=tasks allows you to see your added tasks
        return render_template('Todo.html', tasks=tasks)


# Runner and Debugger
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)

# above is a flask tutorial attempt^^^^

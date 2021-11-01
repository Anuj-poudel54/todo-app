from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Models
db = SQLAlchemy(app)
class Todo(db.Model):
    sn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(10), default="pending")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self) -> str:
        return f"{self.sn}.  {self.title}"


# Routes and functions
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        title = request.form['title'].strip()
        desc = request.form['desc'].strip()

        if title == "":
            title = "My work"

        new_todo = Todo(title=title, desc=desc)
        add_to_db(new_todo)

        return redirect("/")

    all_todo = Todo.query.all()

    return render_template("index.html", all_todo=all_todo)


@app.route("/edit/<int:sn>", methods=["POST", "GET"])
def edit(sn):

    todo = Todo.query.filter_by(sn=sn).first()  
    if request.method == "POST":
        new_title = request.form['title'].strip()
        new_desc = request.form['desc'].strip()

        if new_desc == "" or new_title == todo.title and todo.desc == new_desc:
            return redirect("/")

        todo.title = new_title
        todo.desc = new_desc
        todo.status = "pending"
        db.session.commit()
        return redirect("/")            

      
    return render_template("update.html", todo=todo)


@app.route("/finished/<int:sn>")
def finished(sn):
    todo_finished = Todo.query.filter_by(sn=sn).first()
    todo_finished.status = "finished".lower() if todo_finished.status == "pending" else "pending"
    db.session.commit()
    return redirect("/")

@app.route("/delete/<int:sn>")
def delete(sn):
    todo_del = Todo.query.filter_by(sn=sn).first()
    db.session.delete(todo_del)
    db.session.commit()

    return redirect("/")
    
# Other functions
def add_to_db(entry):
    db.session.add(entry)
    db.session.commit()


if __name__ == "__main__":
    app.run(debug=False)

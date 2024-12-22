from flask import Flask, render_template, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# My App
app = Flask(__name__)
Scss(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# data row
class myTask(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    content = db.Column(db.String(100), nullable=False)
    Complated = db.Column(db.Integer, default=0)
    # Complated = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"
    
with app.app_context():
        db.create_all()
# Add tasks & checking if already existed data
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = myTask(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print("Error : {e}")
            return f"Error: {e}"

    else:
        tasks = myTask.query.order_by(myTask.created).all() 
        return render_template("index.html", tasks=tasks)


# Delete tasks
@app.route("/delete/<int:id>")
def delete_task(id:int):
    delete_tasks = myTask.query.get_or_404(id)
    try:
        db.session.delete(delete_tasks)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        # print("Error: {e}")
        return f"Error: {e}"

# update tasks
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_task(id:int):
    task = myTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Error: {e}"
    else:
        return  render_template("edit.html", task = task)


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask,render_template,request,flash,redirect,url_for, session
from person import Person,User
from flask_bcrypt import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "jhyvjsgkchqwfcoBCYYQGFIUCQKJFikucikCBCHPOgf"


@app.route('/show')
def show():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    id = session['id']
    users = Person.select().where(Person.owner==id)
    return render_template('show.html', users=users)


@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    user= Person.get(Person.id==id)
    if request.method=="POST":
        names = request.form["names"]
        age = request.form["age"]
        weight = request.form["weight"]
        user.name=names
        user.age=age
        user.weight=weight
        user.save()
        flash("user updated successfully")
        return redirect(url_for('show'))

    return render_template('update.html',user=user)

@app.route('/delete/<int:id>')
def delete(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    owner_id = session['id']

    Person.delete().where(Person.id==id),Person.owner==owner_id.execute()
    flash("user deleted successfully")
    return redirect(url_for('show'))


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        names = request.form["names"]
        age = request.form["age"]
        weight = request.form["weight"]
        print(names , age , weight)
        id = session['id']
        Person.create(owner=id, name=names,age=age,weight=weight)
        flash("User saved successfully")
        flash("user "+names)

    return render_template('form.html')


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == "POST":
        names = request.form["names"]
        email= request.form["email"]
        password = request.form["password"]
        password = generate_password_hash(password)
        print(names , email, password)
        User.create(name=names, email=email, password=password)
        flash("Account created successfully")

    return render_template('register.html')


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email= request.form["email"]
        password = request.form["password"]
        try:
          user = User.get(User.email==email)
          hashed_password = user.password
          if check_password_hash(hashed_password,password):
             flash("logged in successfully")
          session['logged_in']=True
          session['names'] = user.name
          session['id']=user.id
          return redirect(url_for('show'))
        except User.DoesNotExist:
            flash("wrong username or password")

    return render_template('login.html')


if __name__ == '__main__':
    app.run()

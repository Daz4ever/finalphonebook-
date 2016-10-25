from flask import Flask, render_template, request, redirect
import pg

app = Flask('MyApp')

db = pg.DB(dbname = 'phonebook')

@app.route('/')

def phonebook():
    #grabbed all contacts from phonebook database
    query = db.query('select * from myphonebook')
    #turned it into a list
    query_list = query.namedresult()
    #render phonebook.html when you go to localhost:5000/
    return render_template(
        'phonebook.html',
        #set the title to phonebook (will show 'Phonebook anywhere there is {{title}} in html')
        title = 'Phonebook',
        #set variable query_list equal to query_list in html
        query_list = query_list
    )
# adding /new_entry to url will take you to add.html page
@app.route('/new_entry')

def add():

    return render_template(
        'add.html',
        title = 'Phonebook'
    )
# This is the handler for the form on the add.html page which takes the information that is inputed
# and request.form.get retrieves the info in the name="" of the form. It is set to a variable
# and that variable is set to equal the column titles of the database using insert.
@app.route('/submit_new_entry', methods =['POST'])

def submit_new_entry():

    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')

    query = db.query('select * from myphonebook')
    query_list = query.namedresult()
# I got an error message saying that the name already exists in the database (because names are unique) so I made an if statement
# where if the list is greater than 0, then bring me back to the same page (instead of an error message)
# otherwise insert the new contact in the database
    if query_list > 0:
        return redirect('/new_entry')
    else:
        db.insert(
        'myphonebook',
        name=name,
        phone_number=phone_number,
        email=email
        )
        return redirect('/')

@app.route('/update_entry')

def update():
    # id = request.args.get('id') gets the id from url (only works when clicking person from home page)
    id = request.args.get('id')

    query=db.query('''select * from myphonebook where id = %s''' % id)
    query_list = query.namedresult()
    entry = query_list[0]

    return render_template(
        'update.html',
        title = 'Phonebook',
        entry = entry
        )

@app.route('/submit_update', methods=['POST'])

def submit_update():
    myid = request.form.get('id')
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')
    action = request.form.get('update')
    if action == "submitupdates":
        db.update('myphonebook', {
        'id': myid,
        'name': name,
        'phone_number': phone_number,
        'email': email
        })

    return redirect('/') 


# @app.route('/submit_update_entry', methods=['POST'])




if __name__ == '__main__':
    app.run(debug=True)

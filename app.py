from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bloodbank'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = request.form
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""
                INSERT INTO donors (
                    name, phone, email, age, gender, blood_group,
                    city, state, pincode, weight
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                form['name'],
                form['phone'],
                form['email'],
                int(form['age']),
                form['gender'],
                form['blood_group'],
                form['city'],
                form['state'],
                form['pincode'],
                float(form['weight'])
            ))
            mysql.connection.commit()
            cursor.close()
            flash("Donor registered successfully!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('register'))
    return render_template('registration.html')


@app.route('/blood', methods=['GET', 'POST'])
def blood():
    if request.method == 'POST':
        form = request.form
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""
                INSERT INTO receivers (
                    receiver_name, receiver_age, gender, blood_group, hospital_name,
                    location, contact_number
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                form['receiver_name'],
                int(form['receiver_age']),
                form['gender'],
                form['blood_group'],
                form['hospital_name'],
                form['location'],
                form['contact_number']
            ))
            mysql.connection.commit()
            cursor.close()
            flash("Blood request submitted successfully!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('blood'))
    return render_template('blood.html')


if __name__ == '__main__':
    app.run(debug=True)

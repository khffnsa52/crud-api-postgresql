#app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
 
app = Flask(__name__)
app.secret_key = "zkvlvk"
 
DB_HOST = "localhost"
DB_NAME = "tstdb"
DB_USER = "postgres"
DB_PASS = "1234567890"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
 
@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM heart_failure"
    cur.execute(s) # Execute the SQL
    list_data = cur.fetchall()
    return render_template('index.html', list_data = list_data)

@app.route('/create', methods=['POST'])
def create():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        age             = request.form['age']
        sex             = request.form['sex']
        chest_pain_type = request.form['chest_pain_type']
        cholesterol     = request.form['cholesterol']
        max_hr          = request.form['max_hr']
        heart_disease   = request.form['heart_disease']
        cur.execute("ROLLBACK")
        cur.execute("INSERT INTO heart_failure (age, sex, chest_pain_type, cholesterol, max_hr, heart_disease) VALUES (%s,%s,%s,%s,%s,%s)", (age, sex, chest_pain_type, cholesterol, max_hr, heart_disease))
        conn.commit()
        flash('Data Added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def edit(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('SELECT * FROM heart_failure WHERE id = {0}'. format(id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', dt = data[0])

@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        age             = request.form['age']
        sex             = request.form['sex']
        chest_pain_type = request.form['chest_pain_type']
        cholesterol     = request.form['cholesterol']
        max_hr          = request.form['max_hr']
        heart_disease   = request.form['heart_disease']
         
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute("""
            UPDATE heart_failure
            SET age = %s,
                sex = %s,
                chest_pain_type = %s,
                cholesterol = %s,
                max_hr = %s,
                heart_disease = %s
            WHERE id = %s
        """, (age, sex, chest_pain_type, cholesterol, max_hr, heart_disease, id))
        flash('Data Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('DELETE FROM heart_failure WHERE id = {0}'.format(id))
    conn.commit()
    flash('Data Removed Successfully')
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)
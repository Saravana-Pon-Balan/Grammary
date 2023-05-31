from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from connection import connect_to_database
import ibm_db
import re
from grammar import grammar_check
from spelling import spellcheck
from summary import summarize
conn = connect_to_database()
print("connected")

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def home():
    #if not session.get("name"):
    #   return redirect("/login")
    return render_template('home.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    return render_template('login.html')

@app.route("/logout")
def logout():
    #session["name"] = None
    return redirect("/")

@app.route('/register')
def register():
    return render_template('Register.html')

@app.route('/save', methods=['GET', 'POST'])
def save():
    success = 0
    uname = request.form['name']
    email = request.form['email']
    psw = request.form['pass']
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, email)):
        success = 1
        insert_sql = "INSERT INTO REGISTER (USERNAME, EMAIL, PASSWORD) VALUES (?,?,?)"
        prepSql = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prepSql, 1, uname)
        ibm_db.bind_param(prepSql, 2, email)
        ibm_db.bind_param(prepSql, 3, psw)
        ibm_db.execute(prepSql)
        #session["name"] = email
        return render_template('home.html')
    else:
        session['name'] = None
        msg = "EMail is not valid"
        return render_template('Register.html',msg=msg)

@app.route('/check', methods=['GET', 'POST'])
def check():
    email = request.form['email']
    psw = request.form['pass']
    
    sql = "SELECT * FROM REGISTER WHERE EMAIL=?"
    smtp = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(smtp, 1, email)
    ibm_db.execute(smtp)
    account=ibm_db.fetch_assoc(smtp)
    print(account)
    if account:
        #session["name"] = account['EMAIL']
        return render_template('home.html')
    else:
        #session["name"] = None
        return render_template('login.html', error=True,failed=1)

@app.route('/grammar_checker',methods=['GET','POST'])
def grammar_checker():
    #if not session.get("name"):
    #    return redirect("/login")
    #else:
        if request.method == 'POST':
            sentence = request.form['text']
            corrected, sentiment, noun_phrases = grammar_check(sentence)
            noun_phrases = ' '.join(noun_phrases)
            context={"corrected":corrected,"sentiment":sentiment,"noun_phrases":noun_phrases}
            return render_template('grammar.html',context=context)
        else:
            return render_template('grammar.html')
        
@app.route('/spelling_checker',methods=['GET','POST'])
def spelling_checker():
    #if not session.get("name"):
    #    return redirect("/login")
    #else:
        if request.method == 'POST':
            sentence = request.form['text']
            corrected,misspelled_count,misspelled = spellcheck(sentence)
            print(corrected)
            misspelled = ' '.join(misspelled)
            context={"corrected_text":corrected,"misspelled_count":misspelled_count,"misspelled":misspelled}
            return render_template('spelling.html',context=context)
        else:
            return render_template('spelling.html')

@app.route('/summarizer',methods=['GET','POST'])
def summarizer():
    #if not session.get("name"):
     #   return redirect("/login")
    #else:
        if request.method == 'POST':
            story = request.form['text']
            count = request.form['count']
            summary = summarize(story,int(count))
            context={"summary":summary}
            print(summary)
            return render_template('summary.html',context=context)
        else:
            return render_template('summary.html')

if __name__ == '__main__':
    app.run(debug=1,host='0.0.0.0', port=5000)

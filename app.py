from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import numpy as np
import pickle
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Use pickle to load in the pre-trained model.
with open('hiv_rfc', 'rb') as f:
    model1 = pickle.load(f)

#model2 = pickle.load(open('hiv_rfc', 'rb'))

app.config['MYSQL_HOST'] = 'us-cdbr-east-04.cleardb.com'
app.config['MYSQL_USER'] = 'b0f9135aa66d86'
app.config['MYSQL_PASSWORD'] = '2e28f6a7'
app.config['MYSQL_DB'] = 'heroku_c703864e708562a'

mysql = MySQL(app)


@app.route('/')
def man():
    return render_template('basicpred.php')

@app.route('/basicpred')
def basicpred():
    return render_template('basicpred.php')
    
@app.route('/advancepred')
def advancepred():
    return render_template('advancepred.php')
    
@app.route('/basicpredadmin')
def basicpredadmin():
    return render_template('basicpredadmin.php')
    
@app.route('/advancepredadmin')
def advancepredadmin():
    return render_template('advancepredadmin.php')
    
@app.route('/basicpredenduser')
def basicpredenduser():
    return render_template('basicpredenduser.php')
    
@app.route('/advancepredenduser')
def advancepredenduser():
    return render_template('advancepredenduser.php')
    
    

@app.route('/basicpredict', methods=['POST'])
def basicpredict():
    data1 = request.form['smiles']
    data2 = request.form['disease']
    data3 = request.form['modelName']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO basic_prediction(Smiles, TargetDisease, ModelApply, Output) VALUES (%s, %s , %s , %s)", ("hi", "HIV", 1, "Active"))
    mysql.connection.commit()
    cur.close()
    
    #diseases = ["HIV", "Corona Virus"]
    #modelName = [model1, model2]
    
    #for disease in diseases:
        #if(data2 == disease):
            #position = diseases.index(disease)
            #model = modelName[position]
        
    
    #train_X = data1
    #scaler = StandardScaler()
    #X_train_norm = scaler.fit_transform(train_X)
    #pred = model1.predict(data1)
    return render_template('after.php')
    #return render_template('after.php', data=pred)
    
@app.route('/advancepredict', methods=['POST'])
def advancepredict():
    #data1 = request.form['smiles']
    #data2 = request.form['disease']
    #data3 = request.form['modelName']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO basic_prediction(Smiles, TargetDisease, ModelApply, Output) VALUES (%s, %s , %s , %s)", ("bye", "HIV", 1, "Active"))
    mysql.connection.commit()
    cur.close()
    
    #diseases = ["HIV", "Corona Virus"]
    #modelName = [model1, model2]
    
    #for disease in diseases:
        #if(data2 == disease):
            #position = diseases.index(disease)
            #model = modelName[position]
        
    
    #train_X = data1
    #scaler = StandardScaler()
    #X_train_norm = scaler.fit_transform(train_X)
    #pred = model1.predict(data1)
    return render_template('after.php')
    #return render_template('after.php', data=pred)

if __name__=="__main__":
    app.run(debug=True)
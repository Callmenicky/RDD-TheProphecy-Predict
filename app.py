from flask import Flask, render_template, jsonify, request, send_file, session, flash, redirect
from flask_mysqldb import MySQL,MySQLdb
import numpy as np
import pickle
import sklearn
import csv
import seaborn as sns
import psycopg2
import base64
import binascii

#Import RDKit
import kora.install.rdkit

#Import pandas
import pandas as pd
from rdkit.Chem import PandasTools

#Import matolib
import matplotlib.pyplot as plt

#Import padelpy
from padelpy import from_smiles
from padelpy import padeldescriptor
from tqdm import notebook
from rdkit import Chem
from rdkit.Chem import AllChem
from mordred import Calculator, descriptors, is_missing
from psycopg2.extras import RealDictCursor



#scalar
from sklearn.preprocessing import StandardScaler

#dimensional reduction
from sklearn.decomposition import PCA

from datetime import date

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

conn = psycopg2.connect(
    host="ec2-3-216-221-31.compute-1.amazonaws.com",
    database="ddji904cha3set",
    user="frzxfyklyoytbw",
    password="6be1eb7f38291fdde5be4fc7707a108f3db8f11542897ff6716b80cf9fe93c64")
    
print ("Opened database successfully")

#error handler
@app.errorhandler(404)
def invalid_route(e):
    return "404 Page Not Found"

@app.route('/logout')
def man():
    if session.get("email") is not None:
        session.pop('email')
    
    return redirect("https://reversedrugdiscovery.ml/index.php")

@app.route('/basicpred')
def basicpred():
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC");
    disease = cur.fetchall()
    session['email'] = None
    return render_template('basicpred.php', disease=disease)
    
@app.route('/advancepred')
def advancepred(): 
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC");
    disease = cur.fetchall()
    session['email'] = None
    return render_template('advancepred.php', disease=disease)
    
@app.route('/basicpredadmin')
def basicpredadmin():
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC");
    disease = cur.fetchall()
    if session.get("email") is None:
        url = request.args.get('email')
    if not session.get("email") is None:
        url = session['email']
    
    if (url != None):
        session['email'] = url
        
        myemail = session['email']
        sql = "SELECT is_admin FROM users WHERE email='" + myemail + "'"
        result = cur.execute(sql) 
        temp = cur.fetchall()
        if (temp[0][0] == 0):
            flash('Unable to access admin content')
    if (url == None):
        flash('Login is required to proceed')
    return render_template('basicpredadmin.php', disease=disease)
    
@app.route('/advancepredadmin')
def advancepredadmin():
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC");
    disease = cur.fetchall()
    if session.get("email") is None:
        url = request.args.get('email')
    if not session.get("email") is None:
        url = session['email']
            
    if (url != None):
        session['email'] = url
        
        myemail = session['email']
        sql = "SELECT is_admin FROM users WHERE email='" + myemail + "'"
        result = cur.execute(sql) 
        temp = cur.fetchall()
        if (temp[0][0] == 0):
            flash('Unable to access admin content')
    if (url == None):
        flash('Login is required to proceed')
    return render_template('advancepredadmin.php', disease=disease)
    
@app.route('/basicpredenduser')
def basicpredenduser():
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC");
    disease = cur.fetchall()
    if session.get("email") is None:
        url = request.args.get('email')
    if not session.get("email") is None:
        url = session['email']
            
    if (url != None):
        session['email'] = url
        
        myemail = session['email']
        sql = "SELECT is_admin FROM users WHERE email='" + myemail + "'"
        result = cur.execute(sql) 
        temp = cur.fetchall()
        if (temp[0][0] == 1):
            flash('Unable to access end user content')
    if (url == None):
        flash('Login is required to proceed')
    return render_template('basicpredenduser.php', disease=disease)
    
@app.route('/advancepredenduser')
def advancepredenduser():
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC");
    disease = cur.fetchall()
    if session.get("email") is None:
        url = request.args.get('email')
    if not session.get("email") is None:
        url = session['email']
            
    if (url != None):
        session['email'] = url
        
        myemail = session['email']
        sql = "SELECT is_admin FROM users WHERE email='" + myemail + "'"
        result = cur.execute(sql) 
        temp = cur.fetchall()
        if (temp[0][0] == 1):
            flash('Unable to access end user content')
    if (url == None):
        flash('Login is required to proceed')
    return render_template('advancepredenduser.php', disease=disease)
    
def loadmodel(modelname,targetdis):
    cur = conn.cursor()
    sql = "SELECT model_id FROM model WHERE model_name=%s and target_disease=%s"
    val = (modelname,targetdis)
    cur.execute(sql,val)
    model_id = cur.fetchone()[0]
    
    model_id_list = []
    model_id_list.append(model_id)
    
    sql = "SELECT model FROM modelfile WHERE model_id=%s"
    cur.execute(sql,model_id_list)
    model = cur.fetchone()[0] #Memoryview Object
     
    model1 = bytes(model)
    model2 = base64.b64decode(model1); #Decode
    model3 = model2.hex() #become hex
    model4 = binascii.unhexlify(model3) #hex to binary
    model5 = pickle.loads(model4)
   
    return model5;
    
def read_dataprocessing_codes(modelname,targetdis):
    cur = conn.cursor()
    sql = "SELECT model_id FROM model WHERE model_name=%s and target_disease=%s"
    val = (modelname,targetdis)
    cur.execute(sql,val)
    model_id = cur.fetchone()[0]
    
    model_id_list = []
    model_id_list.append(model_id)
    
    cur = conn.cursor()
    sql = "SELECT processing FROM modelfile WHERE model_id=%s"
    cur.execute(sql,model_id_list)
    model = cur.fetchone()[0] #Memoryview Object
     
    #Method 3
    model1 = bytes(model)
    model2 = base64.b64decode(model1); #Decode
    model5 = str(model2,'utf8') #become string
    
    #overwrite the file from database to MLScript.py
    with open('MLScript.py', 'w') as f:
        f.write(model5)
        
def read_dataprocessing_files(modelname,targetdis):
    cur = conn.cursor()
    sql = "SELECT model_id FROM model WHERE model_name=%s and target_disease=%s"
    val = (modelname,targetdis)
    cur.execute(sql,val)
    model_id = cur.fetchone()[0]
    
    model_id_list = []
    model_id_list.append(model_id)
    
    sql = "SELECT dataset FROM modelfile WHERE model_id=%s"
    cur.execute(sql,model_id_list)
    model = cur.fetchone()[0] #Memoryview Object
     
    #Method 3
    model1 = bytes(model)
    model2 = base64.b64decode(model1); #Decode
    model5 = str(model2,'utf8') #become string
    
    #overwrite the file from database to MLScript.py
    with open('temporary.txt', 'w') as f:
        f.write(model5)
    
    dataframe1 = pd.read_csv("temporary.txt")
  
    # storing this dataframe in a csv file
    dataframe1.to_csv('trainingfile.csv', 
                      index = None)

def basicpredmethod():
    data1 = request.form['smiles']
    data2 = request.form['disease']
    data3 = request.form['modelName']
    
    read_dataprocessing_codes(data3,data2) 
    read_dataprocessing_files(data3,data2)
    
    #RunDataProcessingCodesForML
    import MLScript
    
    X_test_norm = MLScript.process_data_basic(data1)
    predmodel = loadmodel(data3,data2)
    pred = predmodel.predict(X_test_norm)
    
    print(pred)
    
    if pred[0] == 1:
       pred = "Active" 
    
    else:
        pred = "Inactive"
        
    print(pred)
    
    today = date.today()
    
    cur = conn.cursor()  
    sql = "SELECT model_id FROM model WHERE model_name=%s and target_disease=%s"
    val = (data3,data2)
    cur.execute(sql,val)
    Modelid = cur.fetchall()
    print(Modelid[0][0])
    session['model'] = Modelid
    cur.close()
     
    email = session['email']
    
    if(email != None):
        cur = conn.cursor()  
        sql = "SELECT user_id FROM users WHERE email='" + email + "'"
        print(sql)
        cur.execute(sql)
        Userid = cur.fetchone()[0]
        print(Userid)
        cur.close()

        cur = conn.cursor()
        cur.execute("INSERT INTO basicprediction(user_id, smiles, target_disease, model_apply, output, date) VALUES (%s, %s , %s , %s, %s, %s)", (Userid, data1, data2, int(Modelid[0][0]), pred, today))
        conn.commit()
        cur.close()
   
    return pred
    
def advancepredmethod():
    data1 = request.files['smilescsv']
    data2 = request.form['disease']
    data3 = request.form['modelName']
    
    read_dataprocessing_codes(data3,data2)
    read_dataprocessing_files(data3,data2)
    import MLScript
    
    if data1.filename != '':
        data1.save("inputsmiles.txt")
    
    with open("inputsmiles.txt", newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    molecule_list = []
    for i in data:
        molecule_list.append(i[0])
        
    print(molecule_list)
        
    
    X_test_norm = MLScript.process_data_advance(molecule_list)
    predmodel = loadmodel(data3,data2)
    pred = predmodel.predict(X_test_norm)
    
    prediction = []
    
    for i in pred: 
        if i == 1:
           prediction.append("Active") 
        
        else:
           prediction.append("Inactive")
           
    
    print(prediction)

    path = "static/outcome.csv"
    count = 0
            
    header = ["Smiles", "Result"]
            
    with open(path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in pred: 
            #write a row to the csv file
            result = [molecule_list[count],prediction[count]]
            writer.writerow(result)
            count += 1
           
    today = date.today()
    print(today)
    
    cur = conn.cursor()  
    sql = "SELECT model_id FROM model WHERE model_name=%s and target_disease=%s"
    val = (data3,data2)
    cur.execute(sql,val)
    Modelid = cur.fetchall()
    print(Modelid[0][0])
    session['model'] = Modelid
    cur.close()
    
    email = session['email']
    
    if(email != None):
        emails = str(email)

        cur = conn.cursor()  
        sql = "SELECT user_id FROM users WHERE email='" + email + "'"
        print(sql)
        cur.execute(sql)
        Userid = cur.fetchone()[0]
        print(Userid)
        cur.close()
        
        file = open(path, 'rb').read()
        print("hi")
        
        cur = conn.cursor()
        cur.execute("INSERT INTO advanceprediction(user_id, target_disease, model_apply, output_csv, date) VALUES (%s, %s , %s , %s, %s)", (Userid, data2, int(Modelid[0][0]), psycopg2.Binary(file), today))
        conn.commit()
        cur.close()
   
    return prediction

@app.route('/basicpredict', methods=['POST'])
def basicpredict():
    
    pred = basicpredmethod()
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC")
    disease = cur.fetchall()
    
    modelid = session['model']
    modelid = modelid[0][0]
    sql = "SELECT model_id,model_name,target_disease,pic50 FROM model WHERE model_id='" + str(modelid) + "'"
    
    result = cur.execute(sql) 
    temp = cur.fetchall()
    return render_template('afterbasicpred.php', disease=disease, temp=temp, data = pred)

@app.route('/basicpredictadmin', methods=['POST'])
def basicpredictadmin():
    pred = basicpredmethod()
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC")
    disease = cur.fetchall()
    
    modelid = session['model']
    modelid = modelid[0][0]
    sql = "SELECT model_id,model_name,target_disease,pic50 FROM model WHERE model_id='" + str(modelid) + "'"
    
    result = cur.execute(sql) 
    temp = cur.fetchall()
    return render_template('basicpredadminafter.php', disease=disease, temp=temp, data = pred)

@app.route('/basicpredictenduser', methods=['POST'])
def basicpredictenduser():
    pred = basicpredmethod()
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC")
    disease = cur.fetchall()
    
    modelid = session['model']
    modelid = modelid[0][0]
    sql = "SELECT model_id,model_name,target_disease,pic50 FROM model WHERE model_id='" + str(modelid) + "'"
    
    result = cur.execute(sql) 
    temp = cur.fetchall()
    return render_template('basicpredenduserafter.php', disease=disease, temp=temp, data = pred)
    
@app.route('/advancepredict', methods=['POST'])
def advancepredict():
    #read_dataprocessing_codes(modelname,targetdis)
    pred = advancepredmethod()
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC")
    disease = cur.fetchall()
    
    modelid = session['model']
    modelid = modelid[0][0]
    sql = "SELECT model_id,model_name,target_disease,pic50 FROM model WHERE model_id='" + str(modelid) + "'"
    
    result = cur.execute(sql) 
    temp = cur.fetchall()
    return render_template('afteradvancepred.php', disease=disease, temp=temp, data = pred)

@app.route('/advancepredictadmin', methods=['POST'])
def advancepredictadmin():
    pred = advancepredmethod()
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC")
    disease = cur.fetchall()
    
    modelid = session['model']
    modelid = modelid[0][0]
    sql = "SELECT model_id,model_name,target_disease,pic50 FROM model WHERE model_id='" + str(modelid) + "'"
    
    result = cur.execute(sql) 
    temp = cur.fetchall()
    return render_template('advancepredadminafter.php', disease=disease, temp=temp, data = pred)

@app.route('/advancepredictenduser', methods=['POST'])
def advancepredictenduser():
    pred = advancepredmethod()
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC")
    disease = cur.fetchall()
    
    modelid = session['model']
    modelid = modelid[0][0]
    sql = "SELECT model_id,model_name,target_disease,pic50 FROM model WHERE model_id='" + str(modelid) + "'"
    
    result = cur.execute(sql) 
    temp = cur.fetchall()
    return render_template('advancepredenduserafter.php', disease=disease, temp=temp, data = pred)

@app.route("/mlmodel",methods=["POST","GET"])
def dropdownlist():  
    cur = conn.cursor()
    if request.method == 'POST':
        disease_name = request.form['disease_name'] 
        print(disease_name) 
        result = cur.execute("SELECT * FROM model WHERE is_enable=true AND target_disease = %s ORDER BY model_name ASC", [disease_name] )
        mlmodel = cur.fetchall()  
        OutputArray = []
        for row in mlmodel:
            outputObj = {
                'id': row[2],
                'name': row[1]}
            OutputArray.append(outputObj)
    return jsonify(OutputArray)

if __name__=="__main__":
    app.run(debug=True,host='reverse-drug-discovery.herokuapp.com')
    

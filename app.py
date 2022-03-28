from flask import Flask, render_template, jsonify, request, send_file, session
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

@app.route('/')
def man():
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC");
    disease = cur.fetchall()
    return render_template('basicpred.php', disease=disease)

@app.route('/basicpred')
def basicpred():
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC");
    disease = cur.fetchall()
    return render_template('basicpred.php', disease=disease)
    
@app.route('/advancepred')
def advancepred(): 
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC");
    url = request.args.get('email')
    session['email'] = url
    return render_template('advancepred.php', disease=disease)
    
@app.route('/basicpredadmin')
def basicpredadmin():
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC");
    disease = cur.fetchall()
    return render_template('basicpredadmin.php', disease=disease)
    
@app.route('/advancepredadmin')
def advancepredadmin():
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC");
    disease = cur.fetchall()
    url = request.args.get('email')
    session['email'] = url
    return render_template('advancepredadmin.php', disease=disease)
    
@app.route('/basicpredenduser')
def basicpredenduser():
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC");
    disease = cur.fetchall()
    return render_template('basicpredenduser.php', disease=disease)
    
@app.route('/advancepredenduser')
def advancepredenduser():
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC");
    disease = cur.fetchall()
    return render_template('advancepredenduser.php', disease=disease)
    
def loadmodel(modelname,targetdis):
    cur = conn.cursor()
    sql = "SELECT model FROM model WHERE model_name=%s and target_disease=%s"
    val = (modelname,targetdis)
    cur.execute(sql,val)
    model = cur.fetchone()[0] #Memoryview Object
     
    model1 = bytes(model)
    model2 = base64.b64decode(model1); #Decode
    model3 = model2.hex() #become hex
    model4 = binascii.unhexlify(model3) #hex to binary
    model5 = pickle.loads(model4)
   
    return model5;

def basicpredmethod():
    data1 = request.form['smiles']
    data2 = request.form['disease']
    data3 = request.form['modelName']
            
    # Convert SMILES into molecular descriptors
    molecule_list = [data1]#insert name of list containing only SMILES e.g. smiles_only_lst
    counter = 0
    
    descriptors_table = np.ndarray((len(molecule_list), 1826), dtype=object)
    print("Generating mordred descriptors:")
    for index in notebook.tqdm(range(descriptors_table.shape[0])):
        structure = molecule_list[index]
        mol = Chem.MolFromSmiles(structure)
    
    if mol is None:
        descriptors_table[index, :] = [None] * 1826
    else:
        AllChem.EmbedMolecule(mol, useExpTorsionAnglePrefs=True, useBasicKnowledge=True)
        descriptors_table[index, :] = Calculator(descriptors, ignore_3D=False)(mol).fill_missing()
        
    df =  pd.DataFrame(descriptors_table, columns=Calculator(descriptors, ignore_3D=False).descriptors)
      
    ##
    dataset_train = pd.read_csv('hiv integrase dataset (mordred_active_train).csv')
    
    dataset_train = dataset_train.dropna(axis='columns')
    df = df.dropna(axis='columns')
    
    df.to_csv('singlesmiles', index=False) 
    df = pd.read_csv('singlesmiles')
    
    for column1 in dataset_train.columns:
        if column1 not in df.columns : del dataset_train[column1]
    for column2 in df.columns:
        if column2 not in dataset_train.columns : del df[column2]

    #Training set remove columns that is not features
    #feature_train = [dataset_train.drop(['active'], axis=1, inplace=True)]
    feature_train = dataset_train.columns
    print('Training set updated columns:')
    dataset_train.columns
    
    feature_test = df.columns
    print('Testing set updated columns:')
    feature_test
    
    #identify x_train and y_train
    x_train = dataset_train.loc[:, feature_train].values

    ##
    dataset_train = pd.read_csv('hiv integrase dataset (mordred_active_train).csv')
    y_train = dataset_train.loc[:, ['active']].values
    
    feature_test
    x_test = df.loc[:,feature_test].values
    y_test = x_test
    
    #value standarization in x_train and x_test
    stdsc = StandardScaler()
    x_train_norm = stdsc.fit_transform(x_train)
    x_test_norm = stdsc.transform(x_test)
    
    #fit transform and transform in training and test PCA respectively (75.06% variance explained)
    pca = PCA(n_components = 10)
    x_train_pca = pca.fit_transform(x_train_norm)
    x_test_pca = pca.transform(x_test_norm)
    
    #Perform the principal component analysis at train set (10 PCA)
    df_train_pca = pd.DataFrame(data = x_train_pca, columns = ['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8', 'PC9', 'PC10'])
    df_train_target = dataset_train[['active']]
    #df_train_pca['active'] = df_train_target
    new_train_df = pd.concat([df_train_pca, df_train_target],axis = 1)
    
    #Perform the principal component analysis at test set (10 PCA)
    df_test_pca = pd.DataFrame(data = x_test_pca, columns = ['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8', 'PC9', 'PC10'])
    #df_test_target = dataset_test[['active']]
    new_test_df = pd.concat([df_test_pca],axis = 1)
    
    #save as csv
    ##
    new_train_df.to_csv('hiv integrase dataset (pca_train_descriptors).csv', index=True, header=True)
    new_test_df.to_csv('hiv integrase dataset (pca_test_descriptors).csv', index=True, header=True)
    
    dataset_train = new_train_df
    dataset_test = new_test_df 
    
    print('\n=====Testing======')
    print(dataset_test.shape)
    print(dataset_test.columns)
    
    X_train = dataset_train.iloc[:,0:10] #11 columns 
    y_train = dataset_train['active']
    X_test = dataset_test.iloc[:,0:10] #11 columns
    
    scaler = StandardScaler()
    X_train_norm = scaler.fit_transform(X_train)
    X_test_norm = scaler.transform(X_test)
    
    #load dataset
    ##
    dataset_train = pd.read_csv('hiv integrase dataset (pca_train_descriptors).csv')
    dataset_test = pd.read_csv('hiv integrase dataset (pca_test_descriptors).csv')
    
    # Remove columns
    dataset_train.drop(['Unnamed: 0'], axis=1, inplace=True)
    dataset_train.drop(['active'], axis=1, inplace=True)
    dataset_test.drop(['Unnamed: 0'], axis=1, inplace=True)
    
    #Add column with value train or test
    dataset_train['designation'] = "Train"
    dataset_test['designation'] = "Test"
    
    #complie dataset
    all = pd.concat([dataset_train,dataset_test], axis=0)
    
    all.reset_index(inplace=True)
    
    #set target value to y
    y = all['designation']
    
    #generate 2d pca
    pca_train = PCA(n_components=2)
    principalComponents_train = pca_train.fit_transform(all.iloc[:,:-1])
    principal_Df = pd.DataFrame(data = principalComponents_train, columns = ['PC1', 'PC2'])
    principal_Df['Designation'] = y
    principal_Df.head()
    
    #plot pca graph
    plt.figure(figsize=(7,7))
    sns.scatterplot(
        x="PC1", y="PC2",
        hue="Designation",
        size = "Designation",
        sizes=[20,100],
        palette=['red', 'green'],
        data=principal_Df,
        legend="full",
        alpha=0.7
    )
    
    plt.savefig('static/images/plots.PNG')
    
    predmodel = loadmodel(data3,data2)
    pred = predmodel.predict(X_test_norm)
    
    print(pred)
    
    if pred[0] == 1:
       pred = "Active" 
    
    else:
        pred = "Inactive"
        
    print(pred)
    
    today = date.today()
    
    cur = mysql.connection.cursor()
    sql = "SELECT ModelID FROM model WHERE ModelName=%s and TargetDisease=%s"
    val = (data3,data2)
    cur.execute(sql,val)
    Modelid = cur.fetchall()
    cur.execute("INSERT INTO basic_prediction(Smiles, TargetDisease, ModelApply, Output, PredictionDate) VALUES (%s, %s , %s , %s, %s)", (data1, data2, Modelid, pred, today))
    mysql.connection.commit()
    cur.close()
    return pred
    
def advancepredmethod():
    data1 = request.files['smilescsv']
    data2 = request.form['disease']
    data3 = request.form['modelName']
      
    if data1.filename != '':
        data1.save("inputsmiles.txt")
    
    with open("inputsmiles.txt", newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    molecule_list = []
    for i in data:
        molecule_list.append(i[0])

    # Convert SMILES into molecular descriptors
    counter = 0
    
    descriptors_table = np.ndarray((len(molecule_list), 1826), dtype=object)
    print("Generating mordred descriptors:")
    for index in notebook.tqdm(range(descriptors_table.shape[0])):
        structure = molecule_list[index]
        mol = Chem.MolFromSmiles(structure)
    
        if mol is None:
            descriptors_table[index, :] = [None] * 1826
        else:
            AllChem.EmbedMolecule(mol, useExpTorsionAnglePrefs=True, useBasicKnowledge=True)
            descriptors_table[index, :] = Calculator(descriptors, ignore_3D=False)(mol).fill_missing()
        
    df =  pd.DataFrame(descriptors_table, columns=Calculator(descriptors, ignore_3D=False).descriptors)
    
    df.to_csv('singlesmiles', index=False) 
    
    df = pd.read_csv('singlesmiles')     
    dataset_train = pd.read_csv('hiv integrase dataset (mordred_active_train).csv')
    
    dataset_train = dataset_train.dropna(axis='columns')
    df = df.dropna(axis='columns')
    
    for column1 in dataset_train.columns:
        if column1 not in df.columns : del dataset_train[column1]
    for column2 in df.columns:
        if column2 not in dataset_train.columns : del df[column2]

    #Training set remove columns that is not features
    #feature_train = [dataset_train.drop(['active'], axis=1, inplace=True)]
    feature_train = dataset_train.columns
    print('Training set updated columns:')
    dataset_train.columns
    
    feature_test = df.columns
    print('Testing set updated columns:')
    feature_test
    
    #identify x_train and y_train
    x_train = dataset_train.loc[:, feature_train].values

    dataset_train = pd.read_csv('hiv integrase dataset (mordred_active_train).csv')
    y_train = dataset_train.loc[:, ['active']].values
    
    feature_test
    x_test = df.loc[:,feature_test].values
    y_test = x_test
    
    #value standarization in x_train and x_test
    stdsc = StandardScaler()
    x_train_norm = stdsc.fit_transform(x_train)
    x_test_norm = stdsc.transform(x_test)
    
    #fit transform and transform in training and test PCA respectively (75.06% variance explained)
    pca = PCA(n_components = 10)
    x_train_pca = pca.fit_transform(x_train_norm)
    x_test_pca = pca.transform(x_test_norm)
    
    #Perform the principal component analysis at train set (10 PCA)
    df_train_pca = pd.DataFrame(data = x_train_pca, columns = ['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8', 'PC9', 'PC10'])
    df_train_target = dataset_train[['active']]
    #df_train_pca['active'] = df_train_target
    new_train_df = pd.concat([df_train_pca, df_train_target],axis = 1)
    
    #Perform the principal component analysis at test set (10 PCA)
    df_test_pca = pd.DataFrame(data = x_test_pca, columns = ['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8', 'PC9', 'PC10'])
    #df_test_target = dataset_test[['active']]
    new_test_df = pd.concat([df_test_pca],axis = 1)
    
    dataset_train = new_train_df
    dataset_test = new_test_df 
    
    X_train = dataset_train.iloc[:,0:10] #11 columns 
    y_train = dataset_train['active']
    X_test = dataset_test.iloc[:,0:10] #11 columns
    
    scaler = StandardScaler()
    X_train_norm = scaler.fit_transform(X_train)
    X_test_norm = scaler.transform(X_test)
    
    predmodel = loadmodel(data3,data2)
    pred = predmodel.predict(X_test_norm)
    
    prediction = []
    
    for i in pred: 
        if i == 1:
           prediction.append("Active") 
        
        else:
           prediction.append("Inactive")
           
    count = 0
    print(prediction)
    
    #save as csv
    new_train_df.to_csv('hiv integrase dataset (pca_train_descriptors).csv', index=True, header=True)
    new_test_df.to_csv('hiv integrase dataset (pca_test_descriptors_advance).csv', index=True, header=True)
    
    #load dataset
    dataset_train = pd.read_csv('hiv integrase dataset (pca_train_descriptors).csv')
    dataset_test = pd.read_csv('hiv integrase dataset (pca_test_descriptors_advance).csv')
    
    # Remove columns
    dataset_train.drop(['Unnamed: 0'], axis=1, inplace=True)
    dataset_train.drop(['active'], axis=1, inplace=True)
    dataset_test.drop(['Unnamed: 0'], axis=1, inplace=True)
    
    #Add column with value train or test
    dataset_train['designation'] = "Train"
    dataset_test['designation'] = "Test"
    
    #complie dataset
    all = pd.concat([dataset_train,dataset_test], axis=0)
    
    all.reset_index(inplace=True)
    
    #set target value to y
    y = all['designation']
    
    #generate 2d pca
    pca_train = PCA(n_components=2)
    principalComponents_train = pca_train.fit_transform(all.iloc[:,:-1])
    principal_Df = pd.DataFrame(data = principalComponents_train, columns = ['PC1', 'PC2'])
    principal_Df['Designation'] = y
    principal_Df.head()
    
    #plot pca graph
    plt.figure(figsize=(7,7))
    sns.scatterplot(
        x="PC1", y="PC2",
        hue="Designation",
        size = "Designation",
        sizes=[20,100],
        palette=['red', 'green'],
        data=principal_Df,
        legend="full",
        alpha=0.7
    )
    
    plt.savefig('static/images/plots1.PNG')

    path = "static/outcome.csv"
            
    with open(path, "w") as f:
        writer = csv.writer(f)
        for i in pred: 
            #write a row to the csv file
            f.write(molecule_list[count])
            f.write(": ")
            f.write(prediction[count] + "\n") 
            count += 1
           
    today = date.today()
    
    cur = conn.cursor()  
    sql = "SELECT model_id FROM model WHERE model_name=%s and target_disease=%s"
    val = (data3,data2)
    cur.execute(sql,val)
    Modelid = cur.fetchall()
    print(Modelid[0][0])
    cur.close()
     
    email = session['email']
    emails = str(email)

    cur = conn.cursor()  
    sql = "SELECT user_id FROM users WHERE email='" + email + "'"
    print(sql)
    cur.execute(sql)
    Userid = cur.fetchone()[0]
    print(Userid)
    cur.close()
     
    cur = conn.cursor()
    cur.execute("INSERT INTO advanceprediction(user_id, target_disease, model_apply, output_csv, date) VALUES (%s, %s , %s , %s, %s)", (Userid, data2, int(Modelid[0][0]), "static/outcome.csv", today))
    cur.close()
   
    return prediction

@app.route('/basicpredict', methods=['POST'])
def basicpredict():
    pred = basicpredmethod()
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC")
    disease = cur.fetchall()
    result = cur.execute("SELECT model_id,model_name,target_disease,pic50 FROM model WHERE model_id=97")
    temp = cur.fetchall()
    return render_template('afterbasicpred.php', disease=disease, temp=temp, data = pred)

@app.route('/basicpredictadmin', methods=['POST'])
def basicpredictadmin():
    pred = basicpredmethod()
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC")
    disease = cur.fetchall()
    result = cur.execute("SELECT model_id,model_name,target_disease,pic50 FROM model WHERE model_id=97")
    temp = cur.fetchall()
    return render_template('basicpredadminafter.php', disease=disease, temp=temp, data = pred)

@app.route('/basicpredictenduser', methods=['POST'])
def basicpredictenduser():
    pred = basicpredmethod()
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC")
    disease = cur.fetchall()
    result = cur.execute("SELECT model_id,model_name,target_disease,pic50 FROM model WHERE model_id=97")
    temp = cur.fetchall()
    return render_template('basicpredenduserafter.php', disease=disease, temp=temp, data = pred)
    
@app.route('/advancepredict', methods=['POST'])
def advancepredict():
    pred = advancepredmethod()
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC")
    disease = cur.fetchall()
    result = cur.execute("SELECT model_id,model_name,target_disease,pic50 FROM model WHERE model_id=97")
    temp = cur.fetchall()
    return render_template('afteradvancepred.php', disease=disease, temp=temp, data = pred)

@app.route('/advancepredictadmin', methods=['POST'])
def advancepredictadmin():
    pred = advancepredmethod()
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC")
    disease = cur.fetchall()
    result = cur.execute("SELECT model_id,model_name,target_disease,pic50 FROM model WHERE model_id=97")
    temp = cur.fetchall()
    return render_template('advancepredadminafter.php', disease=disease, temp=temp, data = pred)

@app.route('/advancepredictenduser', methods=['POST'])
def advancepredictenduser():
    pred = advancepredmethod()
    cur = conn.cursor()     
    cur.execute("SELECT DISTINCT target_disease FROM model ORDER BY target_disease ASC")
    disease = cur.fetchall()
    result = cur.execute("SELECT model_id,model_name,target_disease,pic50 FROM model WHERE model_id=97")
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
    app.run(debug=True)
    

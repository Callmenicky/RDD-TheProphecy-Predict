from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import numpy as np
import pickle
import sklearn


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
from mordred import Calculator, descriptors

#scalar
from sklearn.preprocessing import StandardScaler

#dimensional reduction
from sklearn.decomposition import PCA

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
    
def basicpredmethod():
    data1 = request.form['smiles']
    data2 = request.form['disease']
    data3 = request.form['modelName']

    #diseases = ["HIV", "Coronavirus"]
    #modelName = [model1, model2]
    
    #for disease in diseases:
        #if(data2 == disease):
            #position = diseases.index(disease)
            #model = modelName[position]
            
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

    dataset_train = pd.read_csv('hiv integrase dataset (mordred_active_train).csv')
    #dataset_train = pd.read_csv('hiv integrase dataset (padelpy_active_train).csv')
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
    
    #Perform the principal component analysis at test set (10 PCA)
    df_test_pca = pd.DataFrame(data = x_test_pca, columns = ['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8', 'PC9', 'PC10'])
    #df_test_target = dataset_test[['active']]
    new_test_df = pd.concat([df_test_pca],axis = 1)
        
    pred = model1.predict(new_test_df)
   
    print(pred)
    print(pred[0])
    print(new_test_df)
    
    if pred[0] == 1:
       pred = "Active" 
    
    else:
        pred = "Inactive"
        
    print(pred)
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO basic_prediction(Smiles, TargetDisease, ModelApply, Output) VALUES (%s, %s , %s , %s)", (data1, "HIV", 2, pred))
    mysql.connection.commit()
    cur.close()
    return pred
    
def advancepredmethod():
    data1 = request.form['smilescsv']
    data2 = request.form['disease']
    data3 = request.form['modelName']
    
    with open(data1, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    molecule_list = []
    for i in data:
        molecule_list.append(i[0])
    
    # Convert SMILES into molecular descriptors
    print(molecule_list)
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
            
    dataset_train = pd.read_csv('hiv integrase dataset (mordred_active_train).csv')
    
    md = df
    
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

    dataset_train = pd.read_csv('hiv integrase dataset (mordred_active_train).csv')
    #dataset_train = pd.read_csv('hiv integrase dataset (padelpy_active_train).csv')
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
    
    #Perform the principal component analysis at test set (10 PCA)
    df_test_pca = pd.DataFrame(data = x_test_pca, columns = ['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8', 'PC9', 'PC10'])
    #df_test_target = dataset_test[['active']]
    new_test_df = pd.concat([df_test_pca],axis = 1)
        
    pred = model1.predict(new_test_df)
   
    print(pred)
    print(pred[0])
    print(new_test_df)
    
    if pred[0] == 1:
       pred = "Active" 
    
    else:
        pred = "Inactive"
        
    print(pred)
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO basic_prediction(Smiles, TargetDisease, ModelApply, Output) VALUES (%s, %s , %s , %s)", ("bye", "HIV", 1, "Active"))
    mysql.connection.commit()
    cur.close()
   
    return pred

@app.route('/basicpredict', methods=['POST'])
def basicpredict():
    pred = basicpredmethod()
    return render_template('after.php', data = pred)
    #return render_template('after.php', data=pred)

@app.route('/basicpredictadmin', methods=['POST'])
def basicpredictadmin():
    pred = basicpredmethod()
    return render_template('basicpredadminafter.php', data = pred)
    #return render_template('after.php', data=pred)

@app.route('/basicpredictenduser', methods=['POST'])
def basicpredictenduser():
    pred = basicpredmethod()
    return render_template('basicpredenduserafter.php', data = pred)
    #return render_template('after.php', data=pred)
    
@app.route('/advancepredict', methods=['POST'])
def advancepredict():
    pred = advancepredmethod()
    return render_template('after.php')
    #return render_template('after.php', data=pred)

@app.route('/advancepredictadmin', methods=['POST'])
def advancepredictadmin():
    pred = advancepredmethod()
    return render_template('advancepredadminafter.php')
    #return render_template('after.php', data=pred)

@app.route('/advancepredictenduser', methods=['POST'])
def advancepredictenduser():
    pred = advancepredmethod()
    return render_template('advancepredenduserafter.php')
    #return render_template('after.php', data=pred)

if __name__=="__main__":
    app.run(debug=True)

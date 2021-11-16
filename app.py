from flask import Flask, render_template, request, send_file
from flask_mysqldb import MySQL
import numpy as np
import pickle
import sklearn
import csv
import seaborn as sns

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

#scalar
from sklearn.preprocessing import StandardScaler

#dimensional reduction
from sklearn.decomposition import PCA

from datetime import date

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

def loadselection():
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT TargetDisease FROM model")
    if resultValue > 0:
        disease = cur.fetchall()
        return render_template('basicpred.php', disease=disease)

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
    new_train_df.to_csv('hiv integrase dataset (pca_train_descriptors).csv', index=True, header=True)
    new_test_df.to_csv('hiv integrase dataset (pca_test_descriptors).csv', index=True, header=True)
    
    #load dataset
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
    
    pred = model1.predict(new_test_df)
    
    if pred[0] == 1:
       pred = "Active" 
    
    else:
        pred = "Inactive"
        
    print(pred)
    
    today = date.today()
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO basic_prediction(Smiles, TargetDisease, ModelApply, Output, PredictionDate) VALUES (%s, %s , %s , %s, %s)", (data1, "HIV", 2, pred, today))
    mysql.connection.commit()
    cur.close()
    return pred
    
def advancepredmethod():
    data1 = request.files['smilescsv']
    data2 = request.form['disease']
    data3 = request.form['modelName']
    
    #diseases = ["HIV", "Coronavirus"]
    #modelName = [model1, model2]
    
    #for disease in diseases:
        #if(data2 == disease):
            #position = diseases.index(disease)
            #model = modelName[position]
      
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
    
    #Perform the principal component analysis at test set (10 PCA)
    df_test_pca = pd.DataFrame(data = x_test_pca, columns = ['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8', 'PC9', 'PC10'])
    #df_test_target = dataset_test[['active']]
    new_test_df = pd.concat([df_test_pca],axis = 1)
        
    pred = model1.predict(new_test_df)
    
    prediction = []
    
    for i in pred: 
        if i == 1:
           prediction.append("Active") 
        
        else:
           prediction.append("Inactive")
           
    count = 0
    print(prediction)
    
    path = "static/outcome.txt"
    
    with open(path, "r") as f:
        print(f.read())
    
    with open(path, "w") as f:
        for i in pred: 
            f.write("Smile String ")
            f.write(str(count + 1))
            f.write(": ")
            f.write(prediction[count] + "\n") 
            count += 1
           
    today = date.today()
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO advance_prediction(InputCSV, TargetDisease, ModelApply, OutputCSV, Date) VALUES (%s, %s , %s , %s, %s)", (data1, "HIV", 1, "static\outcome.txt", today))
    mysql.connection.commit()
    cur.close()
   
    return prediction

@app.route('/basicpredict', methods=['POST'])
def basicpredict():
    pred = basicpredmethod()
    return render_template('afterbasicpred.php', data = pred)

@app.route('/basicpredictadmin', methods=['POST'])
def basicpredictadmin():
    pred = basicpredmethod()
    return render_template('basicpredadminafter.php', data = pred)

@app.route('/basicpredictenduser', methods=['POST'])
def basicpredictenduser():
    pred = basicpredmethod()
    return render_template('basicpredenduserafter.php', data = pred)
    
@app.route('/advancepredict', methods=['POST'])
def advancepredict():
    pred = advancepredmethod()
    return render_template('afteradvancepred.php', data = pred)

@app.route('/advancepredictadmin', methods=['POST'])
def advancepredictadmin():
    pred = advancepredmethod()
    return render_template('advancepredadminafter.php', data = pred)

@app.route('/advancepredictenduser', methods=['POST'])
def advancepredictenduser():
    pred = advancepredmethod()
    return render_template('advancepredenduserafter.php', data = pred)
    

if __name__=="__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import numpy as np
import pickle
import sklearn
from sklearn.preprocessing import StandardScaler

# Use pickle to load in the pre-trained model.
with open('hiv_rfc', 'rb') as f:
    model1 = pickle.load(f)

#model2 = pickle.load(open('hiv_rfc', 'rb'))

app = Flask(__name__)


@app.route('/')
def man():
    return render_template('basicpred.php')


@app.route('/predict', methods=['POST'])
def home():
    data1 = request.form['smiles']
    data2 = request.form['disease']
    data3 = request.form['modelName']
    
    #diseases = ["HIV", "Corona Virus"]
    #modelName = [model1, model2]
    
    #for disease in diseases:
        #if(data2 == disease):
            #position = diseases.index(disease)
            #model = modelName[position]
        
    
    #train_X = data1
    #scaler = StandardScaler()
    #X_train_norm = scaler.fit_transform(train_X)
    pred = model1.predict(data1)
    return render_template('after.php', data=pred)

if __name__=="__main__":
    app.run(debug=True)
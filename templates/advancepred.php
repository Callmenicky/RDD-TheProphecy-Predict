<!DOCTYPE html>
<html lang="en">

<head>
    <title>RDD</title>
    <meta charset="utf-8"/>
    <meta name="author" content="Chin Jing Jie"/>
    <meta name="description" content="RDD Web Portal"/>
    <meta name="keywords" content="drug, prediction, smiles"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='styles/style.css') }}"/>
    <link rel="icon" href="{{url_for('static', filename='images/logo_RDD.png')}}"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" >
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/js/bootstrap.min.js"></script>
    <script src="//code.jquery.com/jquery-1.11.1.min.js"></script>
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>
	<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.1/dist/umd/popper.min.js" integrity="sha384-SR1sx49pcuLnqZUnnPwx6FCym0wLsk5JZuNx2bPPENzswTNFaQU1RDvt3wT4gWFG" crossorigin="anonymous"></script>
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.min.js" integrity="sha384-j0CNLUeiqtyaRmlzUHCPZ+Gy5fQu0dQ6eZ/xAww941Ai1SxSY+0EQqNXNE6DZiVc" crossorigin="anonymous"></script>
</head>
<body>
  <header>
    <a href="https://rdd-theprophecy.herokuapp.com/"><img class="logo" src="{{url_for('static', filename='images/logo_RDD.png')}}" alt="logo"/></a>
    <h1>Machine Learning Reverse Drug Discovery</h1>
  </header>
  <section class="predict">
    <div class="predcontent">
        <h2>Advance Prediction</h2>
		<form id="AdvancePrediction" method="post" action="{{url_for('advancepredict')}}" enctype=multipart/form-data>
        <p>Upload a CSV file containing SMILES</p>
        <input type="file" id="smilescsv" name="smilescsv"/>
        <select name="disease" id="disease">
          <option value="default">Select Target Disease</option>
		  {% for d in disease %}
		      <option>{{d[0]}}</option>
          {% endfor %}
        </select>
        <p id="showmore"><a href="#" onclick="showMore()">more>></a></p>
        <div id="more">
          <select name="modelName" id="modelName">
            <option value="default">Select Specific Model</option>
            <option value="adac_corona">AdaBoost Classifier</option>
            <option value="rfc_hiv">Random Forest Classifier</option>
            <option value="xgbc_hiv">XBG CLassifier</option>
          </select>
          <p><a href="#" onclick="showLess()">hide>></a></p>
        </div>
        <button type="submit" name="predictadvance" class="btn btn-info">Predict</button>
        </form>
      </div>
      <div class="predimg">
        <img src="{{url_for('static', filename='images/icon_ml.JPG')}}" alt="identity icon">
      </div>
    </section>
  	<footer>
		<address>&#169; RDD 2021. All rights reserved</address> 
		<script src="{{ url_for('static', filename='js/script.js') }}"></script>
	</footer>
</body>
  
</html>

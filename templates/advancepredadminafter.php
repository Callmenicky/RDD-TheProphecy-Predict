<!DOCTYPE html>
<html lang="en">

{% extends 'adminheader.php' %}
{% block content %}
<body>
  <h1>Machine Learning Reverse Drug Discovery</h1>
  <section class="predict">
    <div class="predcontent">
        <h2>Advance Prediction</h2>
		<form id="AdvancePrediction" method="post" action="{{url_for('advancepredictadmin')}}">
        <p>upload a CSV file containing SMILES</p>
        <input type="file" id="smilescsv" name="smilescsv"/>
        <select name="disease" id="disease">
          <option value="default">Select Target Disease</option>
		  <option value="corona">Coronavirus</option>
          <option value="hiv">HIV</option>
        </select>
        <select name="modelName" id="modelName">
            <option value="default">Select Specific Model</option>
			<option value="adac_corona">AdaBoost Classifier</option>
            <option value="rfc_hiv">Random Forest Classifier</option>
            <option value="xgbc_hiv">XBG CLassifier</option>
        </select>
        <br/>
        <button type="submit" name="predictadvanceAdmin" class="btn btn-info">Predict</button>
        </form>
      </div>
      <div class="predimg">
		{%if data == "Active"%}
				<h1>Active</h1>  
				<img src="images/icon_ml.JPG" alt="identity icon"> 

				{%else%}
				<h1>InActive</h1>
				<img src="images/icon_ml.JPG" alt="identity icon">
				
				{%endif%}

					<br><br>
				<a href='/'>go back to home page</a>
      </div>
    </section>
  	<footer>
		<address>&#169; RDD 2021. All rights reserved</address> 
		<script src="{{ url_for('static', filename='js/script.js') }}"></script>
	</footer>
</body>
  {% endblock %}
</html>
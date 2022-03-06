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
        <h2>Basic Prediction</h2>
        <form id="BasicPrediction" method="post" action="{{url_for('basicpredict')}}">
        <input type="text" id="smiles" name="smiles" placeholder="Enter smiles string" maxlength="150"/>
        <select name="disease" id="disease"> 
            <option>Select Target Disease</option>
            {% for row in disease %}
            <option value="{{row.TargetDisease}}">{{row.TargetDisease}}</option>
            {% endfor %}
        </select>
        <select name="modelName" id="modelName"><option>Select ML Model</option></select>
	<br/>
        <button type="submit" name="predictadvance" class="btn btn-info">Predict</button>
    </form>
	</div>
        <div class="predimg predimgafter">
	  <!--Start of slideshow-->
	      <div class="slideshow-container">
		  <div class="mySlides">
		      <img src="{{url_for('static', filename='images/result_ml.jpg')}}" alt="result icon">
		      <div class="centered">Centered 1</div>
		  </div>
		  <div class="mySlides">
		      <img src="{{url_for('static', filename='images/plots.PNG')}}" alt="pca chart">
		      <div class="centered">Centered 2</div>
		  </div>
		  <div class="sliderButtons">
		      <span class="dot" onclick="currentSlide(1)"></span>
		      <span class="dot" onclick="currentSlide(2)"></span>
		  </div>
	      </div>
	<!--End of slideshow-->
				{%if data == "Active"%}
                <h2>Prediction Result: Active</h2>
                {% for row in temp %}
                <p>In <b>{{row.ModelName}}</b> model that target on <b>{{row.TargetDisease}}</b>, molecule that has pIC50 higher than <b>{{row.pIC50}}</b> is consider as active.</p>
                {% endfor %}
                <p>PCA Chart:</p> 
				<img src="{{url_for('static', filename='images/plots.PNG')}}" alt="pca chart">

				{%else%}
                <h2>Prediction Result: Inactive</h2>
                {% for row in temp %}
                <p>In <b>{{row.ModelName}}</b> model that target on <b>{{row.TargetDisease}}</b>, molecule that has pIC50 higher than <b>{{row.pIC50}}</b> is consider as active.</p>
                {% endfor %}
                <p>PCA Chart:</p> 
				<img src="{{url_for('static', filename='images/plots.PNG')}}" alt="pca chart">
				
				{%endif%}

					<br><br>
        </div>
    </section>	
  	<footer>
		<address>&#169; RDD 2021. All rights reserved</address> 
		<script src="{{ url_for('static', filename='js/script.js') }}"></script>
	</footer>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.12.2/js/bootstrap-select.min.js"></script>
        <script>
            $(document).ready(function () {
                $("#disease").selectpicker();
   
                $("#modelName").selectpicker();
   
                function load_data(type, disease_name) {
                    $.ajax({
                        url: "/mlmodel",
                        method: "POST",
                        data: { type: type, disease_name: disease_name },
                        dataType: "json",
                        success: function (data) {
                            var html = "";
                            for (var count = 0; count < data.length; count++) {
                                html += '<option value="' + data[count].name + '">' + data[count].name + "</option>";
                            }
                            if (type == "modelData") {
                                $("#disease").html(html);
                                $("#disease").selectpicker("refresh");
                            } else {
                                $("#modelName").html(html);
                                $("#modelName").selectpicker("refresh");
                            }
                        },
                    });
                }
   
                $(document).on("change", "#disease", function () {
                    var disease_name = $("#disease").val();
                    load_data("mlModeldata", disease_name);
                });
            });
        </script>
</body>
  
</html>








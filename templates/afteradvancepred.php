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
        <p>Upload a text file containing SMILES</p>
        <input type="file" id="smilescsv" name="smilescsv"/>
        <select name="disease" id="disease"> 
            <option>Select Target Disease</option>
            {% for row in disease %}
            <option value="{{row[0]}}">{{row[0]}}</option>
            {% endfor %}
        </select>
        <select name="modelName" id="modelName"><option>Select ML Model</option></select>
        <br/>
        <button type="submit" name="predictadvance" class="btn btn-primary long2">Predict</button>
    </form>
	</div>
        <div class="predimg predimgafter">
          <h2>Prediction Result</h2>
          <p>Have a look at the model analysis :</p>
          <button type="button" class="btn btn-info long2" data-bs-toggle="modal" data-bs-target="#ModelAnalysis" data-id ="<?php echo $row['user_id'];?>">Analyze</button>
          <h2>
              <a download href="outcome.txt">
                <a class="white" href=" {{url_for('static', filename='outcome.csv')}}" download>Download</a>
              </a>
          </h2>
      </div>
    </section>
  	<footer>
		<address>&#169; RDD 2021. All rights reserved</address> 
		<script src="{{ url_for('static', filename='js/script.js') }}"></script>
	</footer>
    <div class="modal fade design" id="ModelAnalysis" tabindex="-1" data-bs-backdrop="static" aria-labelledby="exampleModalLabel" aria-hidden="true">
		  <div class="modal-dialog modal-lg">
			<div class="modal-content">
			  <div class="modal-header">
				<h3 class="modal-title" id="exampleModalLabel">Model Analysis</h3>
				<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
			  </div>
              <div class="modal-body">
				    <!--Start of slideshow-->
                      <div class="slideshow-container">
                      <div class="mySlides">
                          <img src="{{url_for('static', filename='images/result_ml.jpg')}}" alt="result icon">
                          <div class="centered">
                          {% for row in temp %}
                            <p>In <b>{{row[1]}}</b> model that target on <b>{{row[2]}}</b>, molecule that has pIC50 higher than <b>{{row[3]}}</b> is consider as active.</p>
                          {% endfor %}
                          </div>
                      </div>
                      <div class="mySlides">
                          <img src="{{url_for('static', filename='images/plots.PNG')}}" alt="pca chart" class="pca">
                      </div>
                      <div class="mySlides">
                          <img src="{{url_for('static', filename='images/result_ml.jpg')}}" alt="result icon">
                          <div class="centered"><p>PCA chart is applied to visualize the accuacy of prediction. <b>If the SMILES(green) lays between the range of training sample(red), the prediction result is promising.</b></p></div>
                      </div>
                      <div class="sliderButtons">
                          <span class="dot" onclick="currentSlide(1)"></span>
                          <span class="dot" onclick="currentSlide(2)"></span>
                          <span class="dot" onclick="currentSlide(3)"></span>
                      </div>
                      </div>
                <!--End of slideshow-->
				 
				  <div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
				  </div>
			</div>
		  </div>
		</div>
    </div>
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








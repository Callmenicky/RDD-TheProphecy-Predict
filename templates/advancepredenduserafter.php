<!DOCTYPE html>
<html lang="en">

{% extends 'enduserheader.php' %}
{% block content %}
<body>
  <h1>Machine Learning Reverse Drug Discovery</h1>
  <section class="predict">
    <div class="predcontent">
        <h2>Advance Prediction</h2>
		<form id="AdvancePrediction" method="post" action="{{url_for('advancepredictenduser')}}" enctype=multipart/form-data>
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
        <button type="submit" name="predictadvanceEnduser" class="btn btn-primary long2">Predict</button>
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
        <br/><br/>
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
{% endblock %}
</html>

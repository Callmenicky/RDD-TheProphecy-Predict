<!DOCTYPE html>
<html lang="en">

{% extends 'enduserheader.php' %}
{% block content %}
<body>
  <h1>Machine Learning Reverse Drug Discovery</h1>
  <section class="predict">
        <div class="predcontent">
        <h2>Basic Prediction</h2>
        <form id="BasicPrediction" method="post" action="{{url_for('basicpredictenduser')}}">
        <input type="text" id="smiles" name="smiles" placeholder="Enter smiles string" maxlength="150"/>
        <select name="disease" id="disease"> 
            <option>Select Target Disease</option>
            {% for row in disease %}
            <option value="{{row[0]}}">{{row[0]}}</option>
            {% endfor %}
        </select>
        <select name="modelName" id="modelName"><option>Select ML Model</option></select>
        <br/>
        <button type="submit" name="predictbasicenduser" class="btn btn-primary long2" onclick="saveData();">Predict</button>
        </form>
        </div>
        <div class="predimg predimgafter">
            <h2 class="scrollmenu" id="mysmiles"></h2>
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
		      <div class="centered"><p>PCA chart is applied to visualize the accuacy of prediction. <b>If the SMILES(green) lays between the range of training sample(red), the prediction result is promising.</b></p>
              </div>
          </div>
		  </div>
		  <div class="sliderButtons">
		      <span class="dot" onclick="currentSlide(1)"></span>
		      <span class="dot" onclick="currentSlide(2)"></span>
		      <span class="dot" onclick="currentSlide(3)"></span>
		  </div>
	      </div>
	<!--End of slideshow-->
		{%if data == "Active"%}
                  <h2>Prediction Result: Active</h2>
		  {%else%}
                  <h2>Prediction Result: Inactive</h2>		
		{%endif%}
        </div>
    </section>
  	<footer>
		<address>&#169; RDD 2021. All rights reserved</address> 
		<script src="{{ url_for('static', filename='js/script.js') }}"></script>
	</footer>
    <script>
          let smilesName = sessionStorage.getItem("smiles");
          document.getElementById("mysmiles").innerHTML = smilesName;
       </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.12.2/js/bootstrap-select.min.js"></script>
        <script>
            function saveData(){
                var input = document.getElementById("smiles");
                sessionStorage.setItem("smiles", input.value);
            }
            
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

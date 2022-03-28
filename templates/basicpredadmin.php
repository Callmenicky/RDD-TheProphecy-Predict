<!DOCTYPE html>
<html lang="en">

{% extends 'adminheader.php' %}
{% block content %}
<body>
  <h1>Machine Learning Reverse Drug Discovery</h1>
  <button onclick="alertFunction()" name ="alert"> Create Alert</button>
    <script>
    function alertFunction() {
     alert("Hi!, I am a Simple Alert. Please Click on the 'OK' Button.");
    }
    </script>
  <section class="predict">
        <div class="predcontent">
        <h2>Basic Prediction</h2>
        <form id="BasicPrediction" method="post" action="{{url_for('basicpredictadmin')}}">
        <input type="text" id="smiles" name="smiles" placeholder="Enter smiles string" maxlength="150"/>
        <select name="disease" id="disease"> 
            <option>Select Target Disease</option>
            {% for row in disease %}
            <option value="{{row[0]}}">{{row[0]}}</option>
            {% endfor %}
        </select>
        <select name="modelName" id="modelName"><option>Select ML Model</option></select>
        <br/>
        <button type="submit" name="predictbasicadmin" class="btn btn-info" onclick="saveData();">Predict</button>
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

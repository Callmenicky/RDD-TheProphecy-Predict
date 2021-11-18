<!DOCTYPE html>
<html lang="en">

{% extends 'adminheader.php' %}
{% block content %}
<body>
  <h1>Machine Learning Reverse Drug Discovery</h1>
  <style>
    .bootstrap-select .dropdown-toggle{
        display:none;
    }
  </style>
  <section class="predict">
    <div class="predcontent">
        <h2>Advance Prediction</h2>
		<form id="AdvancePrediction" method="post" action="{{url_for('advancepredictadmin')}}" enctype=multipart/form-data>
        <p>upload a CSV file containing SMILES</p>
        <input type="file" id="smilescsv" name="smilescsv"/>
        <select name="disease" id="disease"> 
            <option>Select Target Disease</option>
            {% for row in disease %}
            <option value="{{row.TargetDisease}}">{{row.TargetDisease}}</option>
            {% endfor %}
        </select>
        <select name="modelName" id="modelName"><option>Select ML Model</option></select>
        <br/>
        <button type="submit" name="predictadvanceAdmin" class="btn btn-info">Predict</button>
        </form>
      </div>
      <div class="predimg">
				{%if data[0] == "Active"%}
				<a download href="outcome.txt">  
				<a href=" {{url_for('static', filename='outcome.txt')}}" download>Download Output Results</a>
				<img src="{{url_for('static', filename='images/plots1.PNG')}}" alt="identity icon"> 

				{%else%}
				<a href=" {{url_for('static', filename='outcome.txt')}}" download>Download Output Results</a>
				<img src="{{url_for('static', filename='images/plots1.PNG')}}" alt="identity icon"> 
				
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
  {% endblock %}
</html>

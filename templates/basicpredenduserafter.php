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
            <option value="{{row.TargetDisease}}">{{row.TargetDisease}}</option>
            {% endfor %}
        </select>
        <select name="modelName" id="modelName"><option>Select ML Model</option></select>
        <br/>
        <button type="submit" name="predictbasicenduser" class="btn btn-info">Predict</button>
        </form>
        </div>
        <div class="predimg">
		  {%if data == "Active"%}
				<h2>Output: Active</h2>  
				<img src="{{url_for('static', filename='images/plots.PNG')}}" alt="identity icon">

				{%else%}
				<h2>Output: Inactive</h2>
				<img src="{{url_for('static', filename='images/plots.PNG')}}" alt="identity icon">
				
				{%endif%}

					<br><br>
				<a href='/'>go back to home page</a>
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

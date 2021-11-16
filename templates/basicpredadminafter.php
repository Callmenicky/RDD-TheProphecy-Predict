<!DOCTYPE html>
<html lang="en">

{% extends 'adminheader.php' %}
{% block content %}
<body>
  <h1>Machine Learning Reverse Drug Discovery</h1>
  <section class="predict">
        <div class="predcontent">
        <h2>Basic Prediction</h2>
        <form id="BasicPrediction" method="post" action="{{url_for('basicpredictadmin')}}">
        <input type="text" id="smiles" name="smiles" placeholder="Enter smiles string" maxlength="150"/>
        <select name="disease" id="disease">
          <option value="default">Select Target Disease</option>
          <?php
                $conn = mysqli_connect('us-cdbr-east-04.cleardb.com', 'b0f9135aa66d86', '2e28f6a7', 'heroku_c703864e708562a');
                $db = mysqli_select_db($conn, 'b0f9135aa66d86');

                $query = " SELECT DISTINCT TargetDisease FROM model";
                $query_run = mysqli_query($conn,$query);

                while($row = mysqli_fetch_array($query_run)){
           ?>
                    <option><?php echo $row['TargetDisease']; ?></option>
           <?php
            }
           ?>
        </select>
        <select name="modelName" id="modelName">
            <option value="default">Select Specific Model</option>
        </select>
        <br/>
        <button type="submit" name="predictbasicadmin" class="btn btn-info">Predict</button>
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
    <script type="text/javascript">
    $("#disease").change(function(){
        var x = $("#disease").val();
        xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET","preddropdown.php?model="+x,false);
        xmlhttp.send(null);
        $("#modelName").html(xmlhttp.responseText)
    });
  </script>
</body>
  {% endblock %}
</html>

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
    <a href="index.php"><img class="logo" src="{{url_for('static', filename='images/logo_RDD.png')}}" alt="logo"/></a>
    <h1>Machine Learning Reverse Drug Discovery</h1>
  </header>
  <section class="predict">
        <div class="predcontent">
        <h2>Basic Prediction</h2>
        <form id="BasicPrediction" method="post" action="{{url_for('basicpredict')}}">
        <input type="text" id="smiles" name="smiles" placeholder="Enter smiles string" maxlength="50"/>
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
        <p id="showmore"><a href="#" onclick="showMore()">more>></a></p>
        <div id="more">
          <select name="modelName" id="modelName">
            <option value="default">Select Specific Model</option>
            <?php
                $conn = mysqli_connect('us-cdbr-east-04.cleardb.com', 'b0f9135aa66d86', '2e28f6a7', 'heroku_c703864e708562a');
                $db = mysqli_select_db($conn, 'b0f9135aa66d86');

                $query = " SELECT * FROM model";
                $query_run = mysqli_query($conn,$query);

                while($row = mysqli_fetch_array($query_run)){
             ?>
                    <option><?php echo $row['ModelName']; ?></option>
             <?php
                }
             ?>
          </select>
          <p><a href="#" onclick="showLess()">hide>></a></p>
        </div>
        <button type="submit" name="predictbasic" class="btn btn-info">Predict</button>
        </div>
        <div class="predimg">
				{%if data == "Active"%}
				<h1>Active</h1>  
				<img src="images/icon_ml.JPG" alt="identity icon"> 

				{%else%}
				<h1>Inactive</h1>
				<img src="images/icon_ml.JPG" alt="identity icon">
				
				{%endif%}

					<br><br>
				<a href='/'>go back to home page</a>
        </div>
        </form>
    </section>
  	<footer>
		<address>&#169; RDD 2021. All rights reserved</address> 
		<script src="{{ url_for('static', filename='js/script.js') }}"></script>
	</footer>
</body>
  
</html>








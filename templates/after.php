<!DOCTYPE html>
<html lang="en">

<?php include "header.php";?>
<body>
  <header>
    <a href="index.php"><img class="logo" src="images/logo_RDD.png" alt="logo"/></a>
    <h1>Machine Learning Reverse Drug Discovery</h1>
  </header>
  <section class="predict">
        <div class="predcontent">
        <h2>Basic Prediction</h2>
        <form id="BasicPrediction" method="post" action="{{url_for('home')}}">
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
				{%if data == 0%}
				<h1>Iris-setosa</h1>  
				<img src="images/icon_ml.JPG" alt="identity icon"> 

				{%else%}
				<h1>Iris-versicolor</h1>
				<img src="images/icon_ml.JPG" alt="identity icon">
				
				{%endif%}

					<br><br>
				<a href='/'>go back to home page</a>
        </div>
        </form>
    </section>
  <?php include "footer.php"; ?>
</body>
  
</html>








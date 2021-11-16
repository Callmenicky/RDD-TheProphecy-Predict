 <?php
$conn = mysqli_connect('us-cdbr-east-04.cleardb.com', 'b0f9135aa66d86', '2e28f6a7', 'heroku_c703864e708562a');
$db = mysqli_select_db($conn, 'b0f9135aa66d86');
if(isset($_GET['model'])){
    $query = " SELECT ModelName FROM model WHERE TargetDisease='".$_GET['model']."'";
    $query_run = mysqli_query($conn,$query);
    while($row = mysqli_fetch_array($query_run)){
    ?>
    <option value="<?php echo $row['ModelName']; ?>"><?php echo $row['ModelName']; ?></option>
<?php
    }
    }
?>
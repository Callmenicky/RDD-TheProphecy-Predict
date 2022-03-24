<?php
session_start();
if($_SESSION['Email']==""){
?>
    <script type="text/javascript">
        alert("Login is required to proceed");
        window.location.href = "login.php";
    </script>
<?php
} 

if($_SESSION['Admin']==0){
?>
    <script type="text/javascript">
        alert("Unable to access admin content");
        window.location.href = "https://rdd-theprophecy.herokuapp.com/dashboardenduser.php";
    </script>
<?php
} 

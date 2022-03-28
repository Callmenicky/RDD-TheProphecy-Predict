<?php
session_start();
$_SESSION['Email'] = "empty";
$_SESSION['Email'] = $_GET['email'];
if($_SESSION['Email']=="empty"){
?>
    <script type="text/javascript">
        alert("Login is required to proceed");
        window.location.href = "login.php";
    </script>
<?php
} else{
?>
    <script type="text/javascript">
        alert($_SESSION['Email']);
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

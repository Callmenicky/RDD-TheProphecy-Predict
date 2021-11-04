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

<header>
<nav>
	<!-- The logo is originally illustrated and designed -->
  <ul>
    <a href="dashboardadmin.php"><img src="{{url_for('static', filename='images/logo_RDD.png')}}" alt="logo"/></a>
    <li class="parent"><a href="#">Prediction</a>
      <ul class="child">
        <li><a href="https://rdd-theprophecy.herokuapp.com/basicpredadmin.php">Basic</a></li>
        <li><a href="https://rdd-theprophecy.herokuapp.com/advancepredadmin.php">Advance</a></li>
        <li><a href="https://rdd-theprophecy.herokuapp.com/modeldeploy.php">New Model</a></li>
      </ul>
    </li>
    <li class="parent"><a href="#">History</a>
      <ul class="child">
        <li><a href="https://rdd-theprophecy.herokuapp.com/basichistoryadmin.php">Basic</a></li>
        <li><a href="https://rdd-theprophecy.herokuapp.com/advancehistoryadmin.php">Advance</a></li>
      </ul>
    </li>
    <li class="parent"><a href="#">Profile</a>
      <ul class="child">
        <li><a href="https://rdd-theprophecy.herokuapp.com/profileadmin.php">Personal</a></li>
        <li><a href="https://rdd-theprophecy.herokuapp.com/profileall.php">All</a></li>
      </ul>
    </li>
    <li class="parent"><a href="#" onclick = "logout()">Logout</a></li>
  </ul>
</nav>
</header>

{% block content %}

{% endblock %}


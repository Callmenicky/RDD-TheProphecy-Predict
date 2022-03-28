/* Filename: script.js
   Target page: registrationclient.php
   Purpose : 
   author : Chin Jing Jie, Liew Woun Kai, Nicholas Lim Tun Yang
   Date written: 5/10/2021
   Revisions: 5/10/2021
*/

//Carousel by Chin Jing Jie
var slideIndex = 1;
showSlides(slideIndex);

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");

  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
 
}

//Show Password by Chin Jing Jie
function showPswd(){
	var show = document.getElementById("pswd");
	var hidepass1 = document.getElementById("hide1");
	var hidepass2 = document.getElementById("hide2");
	if (show.type == "password") {
		show.type = "text";
		hidepass1.style.display = "block";
		hidepass2.style.display = "none";
	} else {
		show.type = "password";
		hidepass1.style.display = "none";
		hidepass2.style.display = "block";
	}
}

function showPswd1(){
	var show = document.getElementById("pswd1");
	var hidepass1 = document.getElementById("hide3");
	var hidepass2 = document.getElementById("hide4");
	if (show.type == "password") {
		show.type = "text";
		hidepass1.style.display = "block";
		hidepass2.style.display = "none";
	} else {
		show.type = "password";
		hidepass1.style.display = "none";
		hidepass2.style.display = "block";
	}
}

function logout(){
	var logout;
	logout = confirm("Do you want to continue your action");
	if (logout == true)
	{
		location.href = "https://rdd-theprophecy.herokuapp.com/index.php";
	}
}

function windowClose() {
    window.open('','_parent','');
    window.close();
}

var gErrorMsg = "";

function validateForm(){
    "use strict";  
    var isAllOK = false;  
    gErrorMsg = "";
	var emailOK = chkEmail();
	var passwordOK = chkPswd();
	var recpasswordOK = chkReconfirmPassword();
	var termcondOK = chkTermCond();

	if( passwordOK &&  recpasswordOK && emailOK && termcondOK)
	{
		isAllOK = true;
	}
	
   else{
       alert(gErrorMsg); 
       gErrorMsg = "";  
       isAllOK = false;
   }
   
   return isAllOK;
}

function validateForm2(){
    "use strict";   
    var isAllOK = false;  
    gErrorMsg = ""; 
	var emailOK = chkEmail();
	var passwordOK = chkPswd();
	var recpasswordOK = chkReconfirmPassword();
	var termcondOK = chkTermCond();
	var secretkeyOK = chkSecretKey();
	
	if( passwordOK &&  recpasswordOK && emailOK && termcondOK && secretkeyOK)
	{
		isAllOK = true;
	}
	
   else{
       alert(gErrorMsg); 
       gErrorMsg = "";  
       isAllOK = false;
   }
   
   return isAllOK;
}

function validateForm3(){
    "use strict";   
    var isAllOK = false;  
    gErrorMsg = ""; 
	var ModelnameOK = chkModelName();
	var ModelDateOK = chkModelDate();
	var TargetdiseaseOK = chkTargetDisease();
	var ModelfileOK = chkModelFile();
	var ModelperformanceOK = chkModelPerformance();
	
	
	if( ModelnameOK && ModelDateOK && TargetdiseaseOK && ModelfileOK && ModelperformanceOK )
	{
		isAllOK = true;
	}
	
   else{
       alert(gErrorMsg); 
       gErrorMsg = "";  
       isAllOK = false;
   }
   
   return isAllOK;
}

function validateForm4(){
    "use strict";
    var isAllOK = false;  
    gErrorMsg = ""; 
	var usernameOK = chkUsername();
	var emailOK = chkEmail();
	var passwordOK = chkPswd();
	var recpasswordOK = chkReconfirmPassword();
	
	if(usernameOK && passwordOK && recpasswordOK && emailOK)
	{
		isAllOK = true;
	}
	
   else{
       alert(gErrorMsg); 
       gErrorMsg = "";  
       isAllOK = false;
   }
   
   return isAllOK;
}

function validateForm5(){
    "use strict";  
    var isAllOK = false;  
    gErrorMsg = "";
	var password2OK = chkPswd2();
	var recpassword2OK = chkReconfirmPassword2();

	if( password2OK &&  recpassword2OK)
	{
		isAllOK = true;
	}
	
   else{
       alert(gErrorMsg); 
       gErrorMsg = "";  
       isAllOK = false;
   }
   
   return isAllOK;
}

function validateForm6(){
    "use strict";  
    var isAllOK = false;  
    gErrorMsg = "";
	var SmilesOK = chkSmiles();
	var DiseaseOK = chkDisease();
	var ModelOK = chkModel();

	if( SmilesOK && DiseaseOK && ModelOK)
	{
		isAllOK = true;
	}
	
   else{
       alert(gErrorMsg); 
       gErrorMsg = "";  
       isAllOK = false;
   }
   
   return isAllOK;
}

function validateForm7(){
    "use strict";  
    var isAllOK = false;  
    gErrorMsg = "";
	var InputCSVOK = chkInputCSV();
	var DiseaseOK = chkDisease();

	if( InputCSVOK && DiseaseOK)
	{
		isAllOK = true;
	}
	
   else{
       alert(gErrorMsg); 
       gErrorMsg = "";  
       isAllOK = false;
   }
   
   return isAllOK;
}

function chkPswd(){
	var pwsd = document.getElementById("pswd").value;     
	var regex = /^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
	var pwsdOk = true;	
	if ((pwsd.length == 0)){       
		gErrorMsg = gErrorMsg + "Please enter a Password\n"
        pwsdOk = false; 
        document.getElementById("pswd").style.borderColor = "red";
	}
	if(pwsd.match(regex))
	{
		pwsdOk = true
		
	}
	else{
		gErrorMsg = gErrorMsg + "Password must contain at least one digit [0-9]\n"
		gErrorMsg = gErrorMsg + "Password must contain at least one lowercase [a-z]\n"
		gErrorMsg = gErrorMsg + "Password must contain at least one uppercase [A-Z]\n"
		gErrorMsg = gErrorMsg + "Password must contain a length of at least 8 characters\n"
		document.getElementById("pswd").style.borderColor = "red";
		pwsdOk = false;
	}
	
	return pwsdOk;
}

function chkReconfirmPassword(){
	var pwsd1 = document.getElementById("pswd1").value;
	var pwsd = document.getElementById("pswd").value;    
	var pwsd1Ok = true;	
	if ((pwsd1.length == 0)){        
		gErrorMsg = gErrorMsg + "Please enter reconfirmation Password\n" 
        pwsd1Ok = false; 
        document.getElementById("pswd1").style.borderColor = "red";
	}
	
	else {
		if(pwsd != pwsd1)
		{
			gErrorMsg = gErrorMsg + "Reconfirmation Password is not the same as Password\n"
			pwsd1Ok = false;
		}
		
	}
	
	return pwsd1Ok;
}

function chkPswd2(){
	var pwsd = document.getElementById("pswd").value;     
	var regex = /^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
	var pwsdOk = true;	
	if ((pwsd.length == 0)){       
		gErrorMsg = gErrorMsg + "Please enter a Password\n"
        pwsdOk = false; 
        document.getElementById("pswd").style.borderColor = "red";
	}
	if(pwsd.match(regex))
	{
		pwsdOk = true
		
	}
	else{
		gErrorMsg = gErrorMsg + "Password must contain at least one digit [0-9]\n"
		gErrorMsg = gErrorMsg + "Password must contain at least one lowercase [a-z]\n"
		gErrorMsg = gErrorMsg + "Password must contain at least one uppercase [A-Z]\n"
		gErrorMsg = gErrorMsg + "Password must contain a length of at least 8 characters\n"
		document.getElementById("pswd").style.borderColor = "red";
		pwsdOk = false;
	}
	
	return pwsdOk;
}

function chkReconfirmPassword2(){
	var pwsd1 = document.getElementById("pswd1").value;
	var pwsd = document.getElementById("pswd").value;    
	var pwsd1Ok = true;	
	if ((pwsd1.length == 0)){        
		gErrorMsg = gErrorMsg + "Please enter reconfirmation Password\n" 
        pwsd1Ok = false; 
        document.getElementById("pswd1").style.borderColor = "red";
	}
	
	else {
		if(pwsd != pwsd1)
		{
			gErrorMsg = gErrorMsg + "Reconfirmation Password is not the same as Password\n"
			pwsd1Ok = false;
		}
		
	}
	
	return pwsd1Ok;
}

function chkEmail() {  //Email
	var email = document.getElementById("email");
	var result = false; 
	var pattern = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-za-zA-Z0-9.-]{1,4}$/;
	if (pattern.test(email.value)){
		result = true;
	}
    else{  
       result = false;
       document.getElementById("email").style.borderColor = "red";
       gErrorMsg = gErrorMsg + "Please enter a valid Email Address\n"
	}
	return result;
}

function chkTermCond() {  // Terms and Condition
	var selected = false;
	
	if (document.getElementById("t&c").checked){
		selected = true;
	}
	else{
		gErrorMsg = gErrorMsg + "Please agree to the Terms and Condition\n"
		selected = false;
	}
	
	return selected;
}

function chkSecretKey(){
	var key = document.getElementById("key").value;
	var keystring = 1234567890
	var keyOk = true;	
	if ((key.length == 0)){        
		gErrorMsg = gErrorMsg + "Please enter the Secret Key\n" 
        keyOk = false; 
        document.getElementById("key").style.borderColor = "red";
	}
	
	if (key != keystring){
		gErrorMsg = gErrorMsg + "Please enter the given Secret Key\n" 
        keyOk = false; 
        document.getElementById("key").style.borderColor = "red";
	}
	
	return keyOk;
}

function chkModelName(){
	var Name = document.getElementById("ModelName").value;     
	var NameOk = true;	
	if ((Name.length == 0)){        
		gErrorMsg = gErrorMsg + "Please enter the Model Name\n" 
        NameOk = false; 
        document.getElementById("ModelName").style.borderColor = "red";
	}
	
	return NameOk;
}

function chkModelDate(){
	var selected = false;
	var UploadDate = document.getElementById("ModelUploadDate").value;

	if (UploadDate!=""){
		selected = true;
		document.getElementById("ModelUploadDate").style.borderColor = "black";
	}
	else{
		selected = false;
        document.getElementById("ModelUploadDate").style.borderColor = "red";
		gErrorMsg = gErrorMsg + "Please Choose a Model Upload Date\n"
	}
	return selected; 
}

function chkTargetDisease(){
	var TargetDisease = document.getElementById("TargetDisease").value;     
	var TargetDiseaseOk = true;	
	if ((TargetDisease.length == 0)){        
		gErrorMsg = gErrorMsg + "Please enter the Model's target disease\n" 
        TargetDiseaseOk = false; 
        document.getElementById("TargetDisease").style.borderColor = "red";
	}
	
	return TargetDiseaseOk;
}

function chkModelFile(){
	var File = document.getElementById("Model");
    var FileV;  
	var FileOk = true;
	if(File != null)
	{
		FileV = document.getElementById("Model").value;
	}
	
	else
	{
		File = document.getElementById("Model");
		FileV = document.getElementById("Model").value;
	}
	if(FileV == ""){ 
		gErrorMsg = gErrorMsg + "Please upload a ML Model file\n" 
        FileOk = false; 
        File.style.borderColor = "red";
	}
	return FileOk;
}

function chkModelPerformance(){
	var Performance = document.getElementById("Performance");
    var PerformanceV;  
	var PerformanceOk = true;
	if(Performance != null)
	{
		PerformanceV = document.getElementById("Performance").value;
	}
	
	else
	{
		Performance = document.getElementById("Performance");
		PerformanceV = document.getElementById("Performance").value;
	}
	if(PerformanceV == ""){ 
		gErrorMsg = gErrorMsg + "Please upload ML Model Performance Graph\n" 
        PerformanceOk = false; 
        Performance.style.borderColor = "red";
	}
	return PerformanceOk;
}

function chkUsername(){
	var Name = document.getElementById("Name").value;     
	var NameOk = true;	
	if ((Name.length == 0)){        
		gErrorMsg = gErrorMsg + "Please enter your Username\n" 
        NameOk = false; 
        document.getElementById("Name").style.borderColor = "red";
	}
	
	return NameOk;	
}

function chkSmiles(){
	var Smiles = document.getElementById("smiles").value;     
	var SmilesOk = true;	
	if ((Smiles.length == 0)){        
		gErrorMsg = gErrorMsg + "Please enter a Smiles String for prediction\n" 
        SmilesOk = false; 
        document.getElementById("smiles").style.borderColor = "red";
	}
	
	return SmilesOk;	
}

function chkDisease(){
	 var Disease = document.getElementById('disease');
	 var DiseaseOk = true;
	 var Model = document.getElementById('modelName');

    if(Disease.selectedIndex==0){
	gErrorMsg = gErrorMsg + "Please choose a specific targeted disease\n" 
	gErrorMsg = gErrorMsg + "Please choose a specific model\n"
        Disease.focus();
	Model.focus();
	DiseaseOk = false; 
        document.getElementById("disease").style.borderColor = "red";
	document.getElementById("modelName").style.borderColor = "red";
    }
	
	return DiseaseOk;	
}

function chkInputCSV(){
	var File = document.getElementById("smilescsv");
    var FileV;  
	var FileOk = true;
	if(File != null)
	{
		FileV = document.getElementById("smilescsv").value;
	}
	
	else
	{
		File = document.getElementById("smilescsv");
		FileV = document.getElementById("smilescsv").value;
	}
	if(FileV == ""){ 
		gErrorMsg = gErrorMsg + "Please attach a file of SMILES strings\n" 
        FileOk = false; 
        File.style.borderColor = "red";
	}
	return FileOk;
}

function validateInputOnBlur(){
	
	var objectLostFocus_id = this.id;
	var isOk = false;
	
	switch (objectLostFocus_id){
		case "pwsd": 
			isOk = chkPassword();
			break;
		case "pwsd1": 
			isOk = chkReconfirmPassword();
			break;
		case "email": 
			isOk = chkEmail();
			break;
		case "ModelName": 
			isOk = chkModelName();
			break;
		case "TargetDisease": 
			isOk = chkTargetDisease();
			break;
		case "email": 
			isOk = chkEmail();
			break;
		case "Name": 
			isOk = chkUsername();
			break;
		case "pwsd": 
			isOk = chkPassword2();
			break;
		case "pwsd1": 
			isOk = chkReconfirmPassword2();
			break;
		case "smiles": 
			isOk = chkSmiles();
			break;
		case "modelName": 
			isOk = chkModel();
			break;
		case "smilescsv": 
			isOk = chkInputCSV();
			break;
            }
	if (!isOk) {
        document.getElementById(objectLostFocus_id).style.borderColor = ""; 
        document.getElementById(objectLostFocus_id).style.backgroundColor = "lightgray";
		gErrorMsg = "";
	}
}

function resetFormat(){
	var clicked_id = this.id;    
	document.getElementById(clicked_id).style.backgroundColor = "white";
	document.getElementById(clicked_id).style.borderColor = "grey";
 }

 function registerInputsOnBlur(){  
	var myForm = document.getElementById("endUserRegistrationForm");
	if(myForm == null)
    { 
		myForm = document.getElementById("adminRegistrationForm");	
		if(myForm == null)
		{ 
			myForm = document.getElementById("UploadMachineModel");	
			
			if(myForm == null)
			{ 
				myForm = document.getElementById("EditPersonalProfile");	
				
				if(myForm == null)
				{ 
					myForm = document.getElementById("resetpswdForm");

					if(myForm == null)
					{ 
						myForm = document.getElementById("BasicPrediction");	
						
						if(myForm == null)
						{ 
							myForm = document.getElementById("AdvancePrediction");	
						}
					}					
				}
			}
		}
	}
	var inputElements = myForm.getElementsByTagName("input");
	for (var i = 0; i < inputElements.length; i++){
		inputElements[i].onblur = validateInputOnBlur;
	}
}


function registerInputsOnClick(){  
	var myForm = document.getElementById("endUserRegistrationForm");
	if(myForm == null)
    { 
		myForm = document.getElementById("adminRegistrationForm");
		if(myForm == null)
		{ 
			myForm = document.getElementById("UploadMachineModel");	
			
			if(myForm == null)
			{ 
				myForm = document.getElementById("EditPersonalProfile");

				if(myForm == null)
				{	

					myForm = document.getElementById("resetpswdForm");	
					
					if(myForm == null)
					{ 
						myForm = document.getElementById("BasicPrediction");	
						
						if(myForm == null)
						{ 
							myForm = document.getElementById("AdvancePrediction");	
						}
					}	
				}	
			}
		}
	}
	var inputElements = myForm.getElementsByTagName("input");
	for (var i = 0; i < inputElements.length; i++){
		inputElements[i].onclick = resetFormat;
	}
}


function init() {
	registerInputsOnBlur();
	registerInputsOnClick();
	
    var myForm = document.getElementById("endUserRegistrationForm");
	
	if(myForm != null)
	{	
		myForm.onsubmit = validateForm;
	}
	  
	else
	{
		myForm = document.getElementById("adminRegistrationForm");
		if(myForm != null)
		{	
			myForm.onsubmit = validateForm2;
		}	
		
		else
		{
			myForm = document.getElementById("UploadMachineModel");
			
			if(myForm != null)
			{	
				myForm.onsubmit = validateForm3;
			}
			
			else
			{
				myForm = document.getElementById("EditPersonalProfile");
				
				if(myForm != null)
				{	
					myForm.onsubmit = validateForm4;
				}
				
				else
				{
					myForm = document.getElementById("resetpswdForm");
				
					if(myForm != null)
					{	
						myForm.onsubmit = validateForm5;
					}
					
					else
					{
						myForm = document.getElementById("BasicPrediction");
					
						if(myForm != null)
						{	
							myForm.onsubmit = validateForm6;
						}
						
						else
						{
							myForm = document.getElementById("AdvancePrediction");
					
							if(myForm != null)
							{	
								myForm.onsubmit = validateForm7;
							}
						}
					}
				}
			}	
		}	
   	}
}

window.onload = init;

 $(document).ready(function () {


     $('#dp5').datetimepicker({
	 viewMode: "years",
         pickTime: false
     });     
     $(".dropdown-menu li a").click(function(){
	 
	 $(".btn:first-child").text($(this).text());
	 $(".btn:first-child").val($(this).text());
	 
     });

     $("#swipe").focus();
     // $("#swipe").change(function (){
     // 	 $("#swipe-button").click();
     // 	 $("#swipe").val("");
     // });
     $("#waiver-button").hide();
     $("#waiver").change(handleWaiverSelect);
     $("#file-button").hide();
     $("#file").hide();
     $("#kiosk-login").hide();
     $("#canvas").hide();
     $("#kiosk-login-button").click(function(){
	 $("#kiosk-login").show();
	 $("#kiosk-register-button").show();
	 $("#kiosk-register").hide();
     });
     
     function focusRegisterForm(){
 	 $("#kiosk-login").hide();
	 $("#kiosk-register-button").show();
	 $("#kiosk-register").show();
     }
     $("#kiosk-register-button").click(focusRegisterForm);
     $("#kiosk-no-email-button").click(focusRegisterForm);
     
     setTimeout(function(){ $('.flash').animo( 
	 { animation: "fadeOutRight", duration: 1, keep: true}, 
	     function() { $('.flash').hide(); })}, 5000);

     // Put event listeners into place
     window.addEventListener("DOMContentLoaded", function() {
       // Grab elements, create settings, etc.
       var canvas = document.getElementById("canvas"),
       context = canvas.getContext("2d"),
       video = document.getElementById("video"),
       videoObj = { "video": true },
       errBack = function(error) {
	 console.log("Video capture error: ", error.code); 
       };

       // Put video listeners into place
       if(navigator.getUserMedia) { // Standard
	 navigator.getUserMedia(videoObj, function(stream) {
	   video.src = stream;
	   video.play();
	 }, errBack);
       } else if(navigator.webkitGetUserMedia) { // WebKit-prefixed
	 navigator.webkitGetUserMedia(videoObj, function(stream){
	   video.src = window.webkitURL.createObjectURL(stream);
	   video.play();
	 }, errBack);
       } else if(navigator.mozGetUserMedia) { // WebKit-prefixed
	 navigator.mozGetUserMedia(videoObj, function(stream){
	   video.src = window.URL.createObjectURL(stream);
	   video.play();
	 }, errBack);
       }

       // Trigger photo take
       document.getElementById("snap").addEventListener("click", function() {
	 context.drawImage(video, 0, 0, 640, 480);
	 var dataURL = canvas.toDataURL("image/jpeg");
	 console.log(dataURL);
	 $("#file").val(dataURL);
	 $("#file-button").click();
       });
     }, false);


 });

function handleWaiverSelect(){
    console.log($("#waiver").find(":selected").text());
    if ($("#waiver").find(":selected").text() === "Yes"){		
	$("#waiver-button").show();
    } else {
	$("#waiver-button").hide();
    }
   
}


// var gui = require('nw.gui');
// var win = gui.Window.get();
// var exec = require('child_process').exec, child;
// var siteName;
// var exitPw;
// var timeO;
// var alertTo;
// var alertTo1;
// var alertTo2;
// var alertTo3;
// var alertTo4;
// var alertTo5;
// var qrTo;
// var needTakePhoto = true;
// var focusTo;
// var camError = false;
// var cardid;
// var custid;
// var codename;
// var cInfo;
// var defAreaCode;
// var optDob;
// var optPhone;
// var optSex;
// var hideDob;
// var hidePhone;
// var hideSex;
// var enablePhoto = true;
// var adminCard;
// var dataentrytimeout;
// var waivertimeout;
// var configExit = false;
// var disableBs;
// var sitecode;
// var enableUpload;
// var needRefresh = false;
// var email;
// var fname;
// var lname;
// var $errorCount = 0;
// var $maxRetry = 10;
// var $retryTime = 100;
// var procDialogTo;
// var lnameNext;
// var phoneNext;
// var dobNext;
// var dobPrev;
// var sexPrev;
// var codenamePrev;



// function ajaxStart(){
// 	clearTimeout(procDialogTo);
// 	procDialogTo = setTimeout( "$( '#loading' ).show();", 100);
// }

// function ajaxSuccess(){
// 	clearTimeout(procDialogTo);
// 	//console.log("success");
// 	$( "#loading" ).hide();
// 	$errorCount = 0;
// }

// function ajaxFailure(funct){
// 	if(funct == 0) $errorCount = 9999;
// 	$errorCount++;
// 	logFailure(funct, $errorCount);
// 	console.log("Error running: " + funct + " Error Count: " + $errorCount);
// 	if($errorCount > $maxRetry){
// 		console.log("Too Many Errors.... Let's show the error page");
// 		//window.location.href = 'app://pos/error.html';
// 	}else{
// 		console.log("Retrying ... Error Count: " + $errorCount);
// 		setTimeout(funct, $retryTime);
// 	}
// }

// function logFailure(funct, count){
// 	var url = '/log_ajax_failure.php?site=230&function=' + funct + '&count=' + count;
// 	$.get(url);
// }

// function scaleContents(){
// 	var hd = 1024;
// 	var wd = 1280;
// 	var h = window.innerHeight;
// 	var w = window.innerWidth;
// 	var scale = (h/hd);
// 	var trans = 'scale(' + scale + ')';
// 	var top = (h - hd) / 2;
// 	var top = top + 'px';
// 	var left = (w - wd) / 2;
// 	var left = left + 'px';
// 	$('body.kiosk').css({
// 		"transform": trans,
// 		"-webkit-transform": trans,
// 		"position": 'absolute',
// 		"left": left,
// 		"top": top
// 	});
// }

// function loadConfig(){
// 	var url = 'ajax/config.php';
// 	ajaxStart();
// 	jQuery.get(url, function( data ) {
// 		$errorCount = 0;
// 		console.log(data);
// 		siteName = data.sitename;
// 		defAreaCode = data.defaultareacode;
// 		optDob = data.custdoboptional;
// 		hideDob = data.custdobhide;
// 		optPhone = data.custphoneoptional;
// 		hidePhone = data.custphonehide;
// 		optSex = data.custsexoptional;
// 		hideSex = data.custsexhide;
// 		exitPw = data.exitPw;
// 		enablePhoto = data.cameraenabled;
// 		adminCard = data.admincard;
// 		waivertimeout = data.waivertimeout;
// 		dataentrytimeout = data.dataentrytimeout;
// 		sitecode = data.sitecode;
// 		enableUpload = data.enableUpload;
// 		$( "#emailPrompt" ).html( data.emailPrompt );
// 		document.getElementById("waiverinner").innerHTML = data.waivertext;
// 		document.getElementById("site").innerHTML = siteName;
// 		document.getElementById("areacode").value = defAreaCode;
// 		if(!enablePhoto){
// 			document.getElementById("camError").style.display = 'none';
// 		}
// 		if(hideDob){
// 			$( "#dobTr" ).hide();
// 		}
// 		if(hidePhone){
// 			$( "#phoneTr" ).hide();
// 		}
// 		if(hideSex){
// 			$( "#sexTr" ).hide();
// 		}
// 		setNavDests();
// 	}, 'json')
// 		.done(function() {
// 			ajaxSuccess();
// 		})
// 		.fail(function() {
//     		ajaxFailure("loadConfig();");
//   		});
// }

// function entsub(event) {
// 	if (event && event.which == 13){
//     	process_card();
//   		return false;
// 	}else{
//     	return true;
//     }
// };

// function process_card(){
// 	var swipe = document.getElementById('swipe').value;
// 	sw = swipe.toLowerCase()
// 	if(sw == "exitnow"){
// 		exitApp('exit');
// 	}else if(sw == "config"){
// 		exitApp('config');
// 	}else if(sw == "debug"){
// 		exitApp('dev');
// 	}else if(sw == "shutdownnow"){
// 		exitApp('shutdown');
// 	}else if(sw == "rebootnow"){
// 		exitApp('reboot');
// 	}else if(sw == "refresh"){;
// 		location.reload();
// 	}else if(sw == "fixcam"){;
// 		location.reload();
// 	}else{
// 		var url = "http://kiosk.centermanagerpro.com/230/ajax/validateswipe.php";
// 		ajaxStart();
// 		$.post( url, { "swipe": swipe }, function(d){
// 			document.getElementById('swipe').value = '';
// 			//console.log(d);
// 			ajaxSuccess();
// 			if(d.valid){
// 				if(d.cardid == adminCard){
// 					exitApp('shutdown');
// 				}else{
// 					if(d.reg){
// 						cardid = d.cardid;
// 						cInfo = d;
// 						document.getElementById("fname").value = d.firstname;
// 						document.getElementById("lname").value = d.lastname;
// 						document.getElementById("codename").value = d.codename;
// 						document.getElementById("email").value = d.email;
// 						document.getElementById("bm").value = d.bm;
// 						document.getElementById("bd").value = d.bd;
// 						document.getElementById("by").value = d.by;
// 						document.getElementById("sex").value = d.sex;
// 						if(d.areacode) document.getElementById("areacode").value = d.areacode;
// 						if(d.phone1){
// 							document.getElementById("p1").value = d.phone1;
// 						}else{
// 							document.getElementById("p1").value = '';
// 						}
// 						if(d.phone2){
// 							document.getElementById("p2").value = d.phone2;
// 						}else{
// 							document.getElementById("p2").value = '';
// 						}
// 						document.getElementById("step1").style.display = 'none';
// 						document.getElementById("step2").style.display = 'block';
// 						document.getElementById("fname").select();
// 						if(d.photo){
// 							document.getElementById("oldPhoto").src = d.photo;
// 							needTakePhoto = false;
// 						}else{
// 							needTakePhoto = true;
// 						}
// 						trigStartOver(dataentrytimeout);
// 					}else{
// 						alertMe("Card Not Registered - Please see an attendant");
// 						keepFocus();
// 					}
// 				}
// 			}else{
// 				alertMe("Card Read Error - Please Try Again");
// 			}
// 		},'json')
// 			.done(function() {
// 				//ajaxSuccess();
// 			})
// 			.fail(function() {
//     			ajaxFailure("process_card();");
//   			});
// 	}
// }

// function validateStep2(){
// 	fname = document.getElementById("fname").value;
// 	lname = document.getElementById("lname").value;
// 	codename = document.getElementById("codename").value;
// 	email = document.getElementById("email").value;
// 	var areacode = document.getElementById("areacode").value;
// 	var p1 = document.getElementById("p1").value;
// 	var p2 = document.getElementById("p2").value;
// 	var bm = document.getElementById("bm").value;
// 	var bd = document.getElementById("bd").value;
// 	var by = document.getElementById("by").value;
// 	var sex = document.getElementById("sex").value;
// 	sex = sex.toUpperCase();
// 	if(email != ''){
// 		if((email.indexOf("@") > 0) && (email.lastIndexOf(".") > email.indexOf("@")) && (email.lastIndexOf("@") == email.indexOf("@"))){
// 			var validEmail = true;
// 		}else{
// 			var validEmail = false;
// 		}
// 	}else{
// 		var validEmail = true;
// 	}
// 	if((sex == '') && (optSex)){
// 		var validSex = true;
// 	}else if((sex == 'M') || (sex == 'F') || (sex == 'B') || (sex == 'G') || (sex == 'H')){
// 		var validSex = true;
// 	}else{
// 		var validSex = false;
// 	}
// 	if((p1 == '') && (p2 == '') && (optPhone)){
// 		var validPhone = true;
// 	}else if((p1.length == 3) && (p2.length == 4) && (areacode.length == 3)){
// 		var validPhone = true;
// 	}else{
// 		var validPhone = false;
// 	}
// 	if((by == '') && (bm == '') && (bd == '') && (optDob)){
// 		var validDob = true;
// 	}else if(((bd > 0) && (bd < 32)) && ((bm > 0) && (bm < 13)) && ((by > 0) && (by < 100) || (((by > 1900) && (by < 2014))))){
// 		var validDob = true;
// 	}else{
// 		var validDob = false;
// 	}
// 	if(fname == ''){
// 		alertMeStep2("Please Enter Your First Name");
// 		document.getElementById("fname").select();
// 	}else if(lname == ''){
// 		alertMeStep2("Please Enter Your Last Name");
// 		document.getElementById("lname").select();
// 	}else if(codename == ''){
// 		alertMeStep2("Please Enter Your Code Name");
// 		document.getElementById("codename").select();
// 	}else if(!validSex){
// 		alertMeStep2("Please Enter Your Sex");
// 		document.getElementById("sex").select();
// 	}else if(!validPhone){
// 		alertMeStep2("Please Enter Your Phone Number");
// 		document.getElementById("p1").select();
// 	}else if(!validDob){
// 		alertMeStep2("Please Enter Your Date of Birth");
// 		document.getElementById("bm").select();
// 	}else if(!validEmail){
// 		alertMeStep2("Please Enter Your Email Address");
// 		document.getElementById("email").select();
// 	}else{
// 		var url = "ajax/savedata.php";
// 		ajaxStart();
// 		var postData = {
// 			"cardid":cardid,
// 			"FirstName":fname,
// 			"LastName":lname,
// 			"phone":p1,
// 			"phone2":p2,
// 			"areacode":areacode,
// 			"Sex":sex,
// 			"Address1":cInfo.addr1,
// 			"Address2":cInfo.addr2,
// 			"City":cInfo.town,
// 			"State":cInfo.state,
// 			"Zip":cInfo.zip,
// 			"Country":cInfo.country,
// 			"CodeName":codename,
// 			"GroupType":'',
// 			"email":email,
// 			"dob_y":by,
// 			"dob_m":bm,
// 			"dob_d":bd
// 		}
// 		$.post( url, postData, function(d){
// 			processStep2ret(d);
// 		}, 'json')
// 			.done(function() {
// 				ajaxSuccess();
// 			})
// 			.fail(function() {
//     			ajaxFailure("validateStep2();");
//   			});

// 	}
// }

// function processStep2ret(d){
// 	//console.log(d);
// 	if(d.success){
// 		custid = d.custId;
// 		//console.log(custid);
// 		document.getElementById("step2").style.display = 'none';
// 		document.getElementById("waiver").style.display = 'block';
// 		document.getElementById("waiverInput").focus();
// 		trigStartOver(waivertimeout);
// 	}
// }

// function waiverSub(event) {
// 	if (event && event.which == 13 || event == 'go'){
//     	var wEnt = document.getElementById("waiverInput").value;
//     	wEnt = wEnt.toLowerCase();
//     	//translate frech entries
//     	if(wEnt == 'oui'){
//     		wEnt = 'yes';
//     	}
//     	if(wEnt =='non'){
//     		wEnt = 'no';
//     	}
//     	//translate french
//     	if(wEnt == 'yes'){
//     		ajaxStart();
//     		var url = "ajax/savewaiver.php";
// 			var postData = {
// 				"cardid":cardid,
// 				"codename":codename,
// 				"custid":custid
// 			}
// 			$.post( url, postData, function(d){
// 				document.getElementById("waiverInput").value = '';
// 				document.getElementById("step4inner").innerHTML = d;
// 				if(needTakePhoto && !camError && enablePhoto){
// 					document.getElementById("step2").style.display = 'none';
// 					document.getElementById("waiver").style.display = 'none';
// 					document.getElementById("step3").style.display = 'block';
// 					document.getElementById("takePhoto").focus();
// 					trigStartOver(45);
// 				}else{
// 					takenPhoto();
// 				}
// 			})
// 			.done(function() {
// 				ajaxSuccess();
// 			})
// 			.fail(function() {
//     			ajaxFailure("waiverSub('go');");
//   			});
// 			disableBs = true;
// 		}else if(wEnt == 'no'){
// 			startOver();
// 		}else{
// 			alertMeWaiver("Please Type 'YES' or 'NO', Then press ENTER");
// 		}
//   		return false;
// 	}else{
//     	return true;
//     }
// };

// function takePhoto(){
// 	var c = document.getElementById('photo');
// 	var cc = document.getElementById('photoSave');
// 	var v = document.getElementById('camFeed');
// 	c.getContext('2d').drawImage(v, 0, 0, 800, 600);
// 	cc.getContext('2d').drawImage(v, 0, 0, 320, 240);

// 	document.getElementById("camFeed").style.display = 'none';
// 	document.getElementById("takeBtn").style.display = 'none';
// 	document.getElementById("photo").style.display = 'block';
// 	document.getElementById("saving").style.display = 'block';

// 	var imgData = cc.toDataURL("image/jpeg");
// 	$.post('ajax/uploadphoto.php',{ 'data' : imgData, 'cardid' : cardid }, function(d){
// 		takenPhoto();
// 	})
// 		.done(function() {
// 			ajaxSuccess();
// 		})
// 		.fail(function() {
//     		ajaxFailure("takePhoto()");
//   		});
// }

// function takenPhoto(){
// 	document.getElementById("step2").style.display = 'none';
// 	document.getElementById("step3").style.display = 'none';
// 	document.getElementById("step4").style.display = 'block';
// 	document.getElementById("camFeed").style.display = 'block';
// 	document.getElementById("takeBtn").style.display = 'block';
// 	document.getElementById("photo").style.display = 'none';
// 	document.getElementById("saving").style.display = 'none';
// 	document.getElementById("waiver").style.display = 'none';
// 	trigStartOver(10);
// }

// function onLaunch(){
// 	loadConfig();
// 	scaleContents();
// 	document.getElementById("swipe").focus();
// 	navigator.webkitGetUserMedia({video:true}, onSuccess, onFail);
// 	focusSwipe();
// 	keepFocus();
// 	setTimeout("triggerRefresh();", 360000);
// }

// function focusSwipe(){
// 	win.focus()
// 	document.getElementById("swipe").focus();
// }

// function keepFocus(){
// 	focusSwipe();
// 	clearInterval(focusTo);
// 	focusTo = setInterval("focusSwipe();", 1000);
// 	if(needRefresh){
// 		location.reload();
// 	}
// }

// function loseFocus(){
// 	clearInterval(focusTo);
// }

// function trigStartOver(t){
// 	window.clearTimeout(timeO);
// 	var time = t * 1000;
// 	timeO = setTimeout("startOver();", time)
// }

// function triggerRefresh(){
// 	needRefresh = true;
// }

// function startOver(){
// 	document.getElementById("waiver").style.display = 'none';
// 	document.getElementById("step4").style.display = 'none';
// 	document.getElementById("step3").style.display = 'none';
// 	document.getElementById("step2").style.display = 'none';
// 	document.getElementById("step1").style.display = 'block';
// 	session = 0;
// 	cardid = 0;
// 	custid = 0;
// 	codename = '';
// 	document.getElementById('swipe').value = '';
// 	document.getElementById("swipe").focus();
// 	document.getElementById("oldPhoto").src = 'images/noPhoto.jpg';
// 	document.getElementById("waiverInput").value = '';
// 	document.getElementById("areacode").value = defAreaCode;
// 	keepFocus();
// 	disableBs = false;
// }

// function alertMe(a){
// 	clearTimeout(alertTo);
// 	clearTimeout(alertTo1);
// 	document.getElementById('alertArea').style.visibility = 'visible';
// 	document.getElementById('alertArea').innerHTML = a;
// 	alertTo1 = setTimeout("document.getElementById('alertArea').style.visibility = 'hidden';", 4999);
// 	alertTo = setTimeout("document.getElementById('alertArea').innerHTML = '';", 5000);
// }

// function alertMeStep2(a){
// 	clearTimeout(alertTo2);
// 	clearTimeout(alertTo3);
// 	document.getElementById('alertAreaStep2').style.visibility = 'visible';
// 	document.getElementById('alertAreaStep2').innerHTML = a;
// 	alertTo2 = setTimeout("document.getElementById('alertAreaStep2').style.visibility = 'hidden';", 4999);
// 	alertTo3 = setTimeout("document.getElementById('alertAreaStep2').innerHTML = '';", 5000);
// }

// function alertMeWaiver(a){
// 	clearTimeout(alertTo4);
// 	clearTimeout(alertTo5);
// 	document.getElementById('alertAreaWaiver').style.visibility = 'visible';
// 	document.getElementById('alertAreaWaiver').innerHTML = a;
// 	alertTo4 = setTimeout("document.getElementById('alertAreaWaiver').style.visibility = 'hidden';", 4999);
// 	alertTo5 = setTimeout("document.getElementById('alertAreaWaiver').innerHTML = '';", 5000);
// }

// function exitApp(config){
// 	if(config == 'config'){
// 		configExit = 'c';
// 	}else if(config == 'dev'){
// 		configExit = 'd';
// 	}else if(config == 'shutdown'){
// 		configExit = 's';
// 	}else if(config == 'reboot'){
// 		configExit = 'r';
// 	}else{
// 		configExit = 'x';
// 	}
// 	document.getElementById("exitPw").style.display = 'block';
// 	loseFocus();
// 	document.getElementById("exitPwBox").focus();
// }

// function exitPwPress(event) {
// 	if (event && event.which == 13){
//     	exitPwCh();
//   		return false;
// 	}else{
//     	return true;
//     }
// };

// function exitPwCh(){
// 	var entry = document.getElementById('exitPwBox').value;
// 	document.getElementById('exitPwBox').value = '';
// 	if(entry == exitPw){
// 		document.getElementById("exitPw").style.display = 'none';
// 		keepFocus();
// 		if(configExit == 'c'){
// 			win.leaveKioskMode();
// 			window.location.href = 'app://pos/config.html';
// 		}else if(configExit == 'd'){
// 			loseFocus();
// 			document.getElementById('swipe').value = '';
// 			win.showDevTools();
// 		}else if(configExit == 's'){
// 			child = exec('shutdown /p');
// 			gui.App.quit();
// 		}else if(configExit == 'r'){
// 			child = exec('shutdown /r');
// 			gui.App.quit();
// 		}else{
// 			gui.App.quit();
// 		}
// 	}else{
// 		document.getElementById("exitPw").style.display = 'none';
// 		startOver();
// 	}
// }


// <!-- Camera Functions-->
// function onSuccess(stream){
// 	document.getElementById('camFeed').src = webkitURL.createObjectURL(stream);
// }

// function onFail(){
// 	if(enablePhoto){
// 		// document.getElementById("camError").style.display = 'block';
// 	}
// 	camError = true;
// 	startOver();
// }

// <!-- Data Entry Functions-->
// var badKey = new Array(27, 34, 37, 38, 39, 40, 41, 42, 47, 58, 59, 60, 61, 62, 91, 92, 93, 94, 96, 123, 125, 126);
// var backCount = 0;
// var enableSubmit = false;

// function keydown(k, ne, le){
// 	trigStartOver(dataentrytimeout);
// 	k = k.which;
// 	if(enableSubmit && k == 13){
// 		validateStep2();
// 	}else if(k == 13 || k == 93 || k == 40){
// 		event.preventDefault();
// 		document.getElementById(ne).focus();
// 		document.getElementById(ne).select();
// 		backCount = 0;
// 	}else if(k == 27 || k == 38){
// 		event.preventDefault();
// 		document.getElementById(le).select();
// 		backCount++;
// 		if(backCount > 20){
// 			startOver();
// 			backCount = 0;
// 		}
// 	}else{
// 		backCount = 0;
// 	}
// }

// function tabOnFull(key, self, next, size){
// 	var key = key.which;
// 	if(((key > 47) && (key < 58)) || ((key > 95) && (key < 106))){
// 		var i = document.getElementById(self).value;
// 		if(i.length == size){
// 			document.getElementById(next).select();
// 		}
// 	}
// }

// function keypress(k){
// 	k = k.which;
// 	if(badKey.indexOf(k) > -1){
// 		event.preventDefault();
// 	}
// }

// function upperCodename(){
// 	var codename = document.getElementById("codename").value;
// 	codename = codename.toUpperCase();
// 	document.getElementById("codename").value = codename.substring(0,11);
// }

// function fixSex(){
// 	var sex = document.getElementById("sex").value;
// 	//console.log(sex);
// 	sex = sex.toUpperCase();
// 	document.getElementById("sex").value = sex.substring(0,1);
// }

// function buttonFocus(){
// 	document.getElementById("submit").value = "Press Enter to Continue";
// 	enableSubmit = true;
// }

// function buttonBlur(){
// 	document.getElementById("submit").value = " ";
// 	enableSubmit = false;
// }

// function inputFocus(id){
// 	$( "#" + id ).addClass("selected");
// 	if(id == 'email'){
// 		$( "#email" ).tooltip({
// 			position: {
// 				my: "center bottom",
// 				at: "center top",
// 				of: "#email"
//         	},
//         	content: emailPrompt,
//         	items: "input"
//         });
// 	}
// }

// function inputBlur(id){
// 	$( "#" + id ).removeClass("selected");
// 	if(id =='codename'){
// 		upperCodename();
// 	}else if(id =='sex'){
// 		fixSex();
// 	}
// }



///////////////stop backspace from navigating/////////
// $(document).keydown(function(e){
// 	if ((e.keyCode == 8) && (disableBs)){
// 		e.preventDefault();
// 	}
// });
//////////////////////////////////////////////////

///////////fix navigation if options are hidden//////



// var dobPrev;
// var sexPrev;
// var codenamePrev;


// function setNavDests(){
// 	if(hidePhone){
// 		dobPrev = 'lname';
// 		if(hideDob){
// 			if(hideSex){
// 				lnameNext = 'codename';
// 			}else{
// 				lnameNext = 'sex';
// 			}
// 		}else{
// 			lnameNext = 'bm';
// 		}
// 	}else{
// 		lnameNext = 'p1';
// 		dobPrev = 'p2';
// 	}


// 	if(hideDob){
// 		if(hideSex){
// 			phoneNext = 'codename';
// 		}else{
// 			phoneNext = 'sex';
// 		}
// 	}else{
// 		phoneNext = 'bm';
// 	}


// 	if(hideDob){
// 		if(hidePhone){
// 			sexPrev = 'lname';
// 		}else{
// 			sexPrev = 'p2';
// 		}
// 	}else{
// 		sexPrev = 'by';
// 	}

// 	if(hideSex){
// 		dobNext = 'codename';
// 	}else{
// 		dobNext = 'sex';
// 	}

// 	if(hideSex){
// 		if(hideDob){
// 			if(hidePhone){
// 				codenamePrev = 'lname';
// 			}else{
// 				codenamePrev = 'p2';
// 			}
// 		}else{
// 			codenamePrev = 'by';
// 		}
// 	}else{
// 		codenamePrev = 'sex';
// 	}
// }


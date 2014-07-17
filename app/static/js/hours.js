
function storeHours(fm) {
    console.log(fm);
}
function setDate(){ 
    var currentTime = new Date();
    var currentYear = currentTime.getFullYear();  
    var currentMonth = currentTime.getMonth();
    document.getElementsByName('year')[0].setAttribute('value',currentYear);
    document.getElementsByName('month')[0].value = ((currentMonth+1) % 12);
}


function createTimeOptions(day,i){
    var optionBlock = "";
    var time = " AM";
    for (var val = 0; val < 24; val++){
    	if (val === 12){
    	    time = " PM";
    	}
	if (val % 12 === 0){
	    hour = 12;
	} else {
	    hour = val % 12;
	}
    	optionBlock += "<option value=\"" + val + "\">" + hour + time + "</option>";
    }
    return "<td>"+day+":</td><td>"     
    	+"<select name=\"start"+i+"\" onchange=\"updateHours(this)\">"
    	+ optionBlock
    	+"</select></td><td>"
    	+"<select name=\"end"+i+"\" onchange=\"updateHours(this)\">"
    	+ optionBlock
    	+"</select></td>";
}

function writeHours(){
    var days = ["sunday","monday","tuesday","wednesday","thursday","friday","saturday"];
    table = "<table name=\"hours-table\">"
	+"<thead>"
	+"<tr>"
	+"<th>Day<\/th>"
	+"<th>Start<\/th>"
	+"<th>End<\/th>"
	+"<\/tr>"
	+"<\/thead>"
        +"<tbody>"

    for (var i=0; i<7;i++){
	table += "<tr>" + createTimeOptions(days[i],i)+ "<\/tr>" ;
    }
    table += "\n</tbody>"
    document.getElementsByName('hours')[0].innerHTML = table;
}

function setDefaultHours(){ 
    document.getElementsByName('start0')[0].value = 10;
    document.getElementsByName('end0')[0].value = 18;
    document.getElementsByName('start1')[0].value = 15;
    document.getElementsByName('end1')[0].value = 21;
    document.getElementsByName('start2')[0].value = 12;
    document.getElementsByName('end2')[0].value = 21;
    document.getElementsByName('start3')[0].value = 12;
    document.getElementsByName('end3')[0].value = 21;
    document.getElementsByName('start4')[0].value = 12;
    document.getElementsByName('end4')[0].value = 21;
    document.getElementsByName('start5')[0].value = 12;
    document.getElementsByName('end5')[0].value = 23;
    document.getElementsByName('start6')[0].value = 10;
    document.getElementsByName('end6')[0].value = 0;
}

function updateHours(selector){
    var nameToDates
    selector.attributes["name"].value
    
}

function selectAllText(textBox){
    textBox.focus();
    textBox.select();
}

function loadCalendar() {
    if (localStorage.getItem('calendar')){
	sample.innerHTML = localStorage.getItem('calendar'); 
    }
}

$(document).ready(function() {
    writeHours();
    setDefaultHours();
    var sample = document.getElementById('sample');
    $("#saveAll").click(function(e) {
	e.preventDefault();
	localStorage.setItem('calendar', sample.innerHTML);
	alertify.success("You have saved your calendar.");
    });
    $("#clearAll").click(function(e) {
	e.preventDefault();
	localStorage.clear();
	location.reload();
    });   
    loadCalendar();

    $("#extract-html").click( function() {
	var sample = document.getElementById('sample');
	$("#calendar-html").val(sample.innerHTML);
	selectAllText($("#calendar-html"));
    });

    $( "#month" ).on('click','td', function() {
	$( this ).toggleClass( "day", 1000 );
	return false;
    });

    $(".tiptext").mouseover(function() {
	$(this).children(".description").show();
	$(this).css({"border-color": "#000", 
		     "border-width":"1px", 
		     "border-style":"solid"});
    }).mouseout(function() {
	$(this).children(".description").hide();     
	$(this).css({"border":"none"});
    });

    $("#hours-submit").click(function() {
    	storeHours(this.form);
    });
});

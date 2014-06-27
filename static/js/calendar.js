var dow = ['&nbsp;Sunday&nbsp;&nbsp;','&nbsp;Monday&nbsp;&nbsp;','&nbsp;Tuesday&nbsp;','Wednesday','Thursday&nbsp;','&nbsp;Friday&nbsp;&nbsp;','Saturday&nbsp;'];
function valButton(btn) {var cnt = -1;for (var i=btn.length-1; i > -1; i--) {if (btn[i].checked) {cnt = i; i = -1;}}if (cnt > -1) return btn[cnt].value;else return null;}
function monthLength(month,year) {var dd = new Date(year, month, 0);return dd.getDate();}
function setCell(f,day,col,hours) {
    var valueToTime = [];
    valueToTime[0] = "12 AM"
    valueToTime[1] = "1 AM"
    valueToTime[2] = "2 AM"
    valueToTime[3] = "3 AM"
    valueToTime[4] = "4 AM"
    valueToTime[5] = "5 AM"
    valueToTime[6] = "6 AM"
    valueToTime[7] = "7 AM"
    valueToTime[8] = "8 AM"
    valueToTime[9] = "9 AM"
    valueToTime[10] = "10 AM"
    valueToTime[11] = "11 AM"
    valueToTime[12] = "12 PM"
    valueToTime[13] = "1 PM"
    valueToTime[14] = "2 PM"
    valueToTime[15] = "3 PM"
    valueToTime[16] = "4 PM"
    valueToTime[17] = "5 PM"
    valueToTime[18] = "6 PM"
    valueToTime[19] = "7 PM"
    valueToTime[20] = "8 PM"
    valueToTime[21] = "9 PM"
    valueToTime[22] = "10 PM"
    valueToTime[23] = "11 PM"

    var c = [];
    var t = '<td';
    if (f==0) c.push('previous');
    if (col==0 || col==6) c.push('weekend');
    if (f==9) c.push('next');
    if (c.length>0) t+=' class="'+c.join(' ')+'"';
    t += '><span class="date">'+day+'<\/span><div class="day" contenteditable="true">\n'+ valueToTime[hours[2*col]]+'-<br>'+valueToTime[hours[(2*col)+1]]+'<\/div><\/td>\n';
    return t;
}

function setCal(fm) {
    console.log(fm);
    var m = parseInt(fm.month.value,10);
    var y = parseInt(fm.year.value,10);
    var hours = [];
    hours.push(parseInt(fm.start0.value,10))
    hours.push(parseInt(fm.end0.value,10))
    hours.push(parseInt(fm.start1.value,10))
    hours.push(parseInt(fm.end1.value,10))
    hours.push(parseInt(fm.start2.value,10))
    hours.push(parseInt(fm.end2.value,10))
    hours.push(parseInt(fm.start3.value,10))
    hours.push(parseInt(fm.end3.value,10))
    hours.push(parseInt(fm.start4.value,10))
    hours.push(parseInt(fm.end4.value,10))
    hours.push(parseInt(fm.start5.value,10))
    hours.push(parseInt(fm.end5.value,10))
    hours.push(parseInt(fm.start6.value,10))
    hours.push(parseInt(fm.end6.value,10))
    if (y < 1901 || y > 2100) {alert('year must be after 1900 and before 2101'); return false;}
    var c = new Date();
    c.setDate(1);
    c.setMonth(m);
    c.setFullYear(y);
    var x = parseInt(valButton(fm.day),10);
    var s = (c.getDay()-x)%7; if (s<0) s+=7;
    var dm = monthLength(m,y);
    var h = '<table id="month" class="flat-table flat-table-1">\n<thead>\n<tr>\n';
    for (var i=0;i<7;i++) {
	h+= '<th';
	if ((i+x)%7==0 || (i+x)%7==6) h+= ' class="weekend"';
	h+= '>'+dow[(i+x)%7]+'<\/th>\n';}
    h += '<\/tr>\n<\/thead>\n<tbody>\n<tr>\n';
    for (var i=s;i>0;i--) {
	h += setCell(0,dm-i+1,(s-i+x)%7,hours);
    }
    dm = monthLength(m+1,y);
    for(var i=1; i <= dm; i++) {
	if((s%7)==0) {h += '<\/tr><tr>\n'; s = 0;}
	h += setCell(1,i,(s+x)%7,hours);
	s++;
    }
    var j=1;
    for (var i=s;i<7;i++) {
	h += setCell(9,j,(i+x)%7,hours);
	j++;
    }
    h += '<\/tr>\n<\/tbody>\n<\/table>';

    style="<style>.flat-table {    margin-bottom: 20px;    border-collapse:collapse;    font-family: 'Lato', Calibri, Arial, sans-serif;    border: none;    border-radius: 3px;    -webkit-border-radius: 3px;    -moz-border-radius: 3px;}.flat-table th, .flat-table td {    border-bottom: 2px solid #26517c;    border-right: 2px solid #26517c;}.flat-table th {    font-weight: normal;    -webkit-font-smoothing: antialiased;    padding: 1em;    color: rgba(0,0,0,0.45);    text-shadow: 0 0 1px rgba(0,0,0,0.1);    font-size: 1.5em;}.flat-table td {    color: #f7f7f7;    padding: 0.7em 1em 0.7em 1.15em;    text-shadow: 0 0 1px rgba(255,255,255,0.1);    font-size: 1.4em;}.flat-table tr {    -webkit-transition: background 0.3s, box-shadow 0.3s;    -moz-transition: background 0.3s, box-shadow 0.3s;    transition: background 0.3s, box-shadow 0.3s;}.flat-table-1 {    background: #336ca6;}.flat-table-1 td:hover {    background: rgba(0,0,0,0.19);}.flat-table-2 tr:hover {    background: rgba(0,0,0,0.1);}.flat-table-2 {    background: #f06060;}.flat-table-3 {    background: #52be7f;}.flat-table-3 tr:hover {    background: rgba(0,0,0,0.1);</style>" 

    
    fm.html.value = style + h;
    document.getElementById('sample').innerHTML = style + h;
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
    setDate();
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

    $("#month").on("click", "td", function() {
	alert($( this ).text());
    });
    
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

    $("#calendar-submit").click(function() {
    	setCal(this.form);
    });
});

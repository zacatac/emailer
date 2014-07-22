if(typeof(String.prototype.trim) === "undefined")
{
    String.prototype.trim = function() 
    {
	return String(this).replace(/^\s+|\s+$/g, '');
    };
}

function validateListForm(){
    var criteriaTextInputs = $('[name^=criteria]');  
    for (var box = 0; box < criteriaTextInputs.length; box++){
	var parentStyle = criteriaTextInputs[box].parentNode.style.display;
	if ((criteriaTextInputs[box].value.trim() === '') && (parentStyle !== "none")){      
	    alertify.error("Text forms can't be empty");
	    return false;
	}
    }
    localStorage.setItem('search', document.getElementById('email-search-container').innerHTML);
    alertify.success("You have saved your search.");
    return true;
}

function handleBase(num){
    var baseDropdown = document.getElementById('email-base'+num);
    var currentValue = baseDropdown.options[baseDropdown.selectedIndex].value; 
    var activityDropdown = document.getElementById('activity'+num);
    var criteriaText = document.getElementById('criteria'+num);
    var relationDropdown = document.getElementById('email-relation'+num);
    var monthDropdown = document.getElementById('month'+num);
    function alterOptions(selectElement,setTo){
	for (var i = 0; i < selectElement.options.length; i++){
	    selectElement.options[i].disabled = setTo;
	}
    }
    relationDropdown.value = 0;
    alterOptions(relationDropdown,false);
    activityDropdown.style.display = "none";
    criteriaText.style.display = "inline-block";
    monthDropdown.style.display = "none";
    relationDropdown.options[8].disabled = true;
    switch(currentValue){
    case "0":
    case "1":
    case "2":
    case "4":
	relationDropdown.options[2].disabled = true;
	relationDropdown.options[3].disabled = true;
	break;
    case "3":
	relationDropdown.value = 8;
	relationDropdown.options[8].disabled = false;
	handleRelation(num);
	break;
    case "7":
	alterOptions(relationDropdown,true);
	relationDropdown.options[6].disabled = false;
	/* relationDropdown.options[7].disabled = false; */ // ***ALERT*** Will implement later
	relationDropdown.value = 6;
	activityDropdown.style.display = "inline-block";
	criteriaText.style.display = "none";	 
	criteriaText.value = "";
	break;
    default:
	alterOptions(relationDropdown,false);
	activityDropdown.style.display = "none";
	criteriaText.style.display = "inline-block";
	break;
    }
    handleRelation(num);
}

function handleRelation(num){
    var relationDropdown = document.getElementById('email-relation'+num);
    var relationValue = relationDropdown.options[relationDropdown.selectedIndex].value;
    var monthDropdown = document.getElementById('month'+num);
    var criteriaText = document.getElementById('criteria'+num);
    var activityDropdown =  document.getElementById('activity'+num);
    if (relationValue == "8"){
	monthDropdown.style.display = "inline-block";
	criteriaText.style.display = "none";
    } else if  (activityDropdown.style.display === "none"){
	criteriaText.style.display = "inline-block";
	monthDropdown.style.display = "none";     
    } else {
	monthDropdown.style.display = "none"; 
    }     
}

function deleteSearchRow(num){
    console.log("deleted row: " + num);  
    var rowContainer = document.getElementById("email-search-container");  
    var numRows = document.getElementsByName("search-row").length;
    var row = document.getElementById("search-row"+num);
    console.log("numRows"+numRows);
    if (numRows > 1){
	$('#search-row'+num).animo( {animation: "fadeOutRight", duration: 0.25, keep: true}, 
				    function() { 
					$('#search-row'+num).remove();
				    });
    } else {    
	alertify.error("You must have at least one search criteria");
    }    
}
function deleteParentListElement(el){
    parent = el.parentNode.parentNode;
    numElements = parent.parentNode.getElementsByTagName("li").length;
    if (numElements > 1){
	parent.parentNode.removeChild(parent);
    } else {
	alertify.error("You can't delete the last person. Use Clear All");
    }
    return false;
} 

function makeEditable(el){
    var leftDiv = $(el).parents().prev('.left-li');
    var rightDiv= $(el).closest('.right-li');
    var editButton = rightDiv.children('input');
    var change_to_edit = true;
    $(el).parents().prev('.left-li').children('[class^=customer]').each(function (index) {
	console.log("caller: " + index);
	var this_span = $(this).children('span');
	if (this_span.attr("contenteditable") === "false" || this_span.attr("contenteditable") === undefined){
	    this_span.attr("contenteditable",true);
	    change_to_edit = false;
	}
	else {
	    this_span.attr("contenteditable",false);
	}
    });
    if (change_to_edit === true){
	$(editButton).attr("value","edit");     
    } else {
	$(editButton).attr("value","save");     
    }
}

function loadToDo() {  
    if (localStorage.getItem('customerList')){
	$('#list').prepend(localStorage.getItem('customerList'));
    };
    var numCustomersTotal = document.getElementsByName('customer-li').length
    alertify.success( numCustomersTotal + " "+pluralizer(numCustomersTotal,'customer') +" matched");
}
var pluralizer = function(num,word){ if (parseInt(num) < 2){return word;}else{ return word + "s";}}

var rowNumber = 0;
function addSearchRow(){
    var searchRow = "<div class=\"search-row\" name=\"search-row\" id=\"search-row"+rowNumber+"\">"
	+" <div  class=\"form-group form-group-inline\">"
	+ " <select name=\"base"+rowNumber+"\" class=\"form-control\" id=\"email-base"+rowNumber+"\" onchange=handleBase("+rowNumber+")>"
	+ " <option value=\"0\">Email Address</option>"
	+ " <option value=\"1\">First Name</option>"
	+ " <option value=\"2\">Last Name</option>"
	+ " <option value=\"3\">Birthdate</option>"
	+ " <option value=\"4\">Code name</option>"
	+ " <option value=\"5\">Entered</option>"
	+ " <option value=\"6\">Last played</option>"
	+ " <option value=\"7\">Activity</option>"
	+ " </select>"
	+ " </div>"
	+ " <div class=\"form-group form-group-inline\">"
	+ " <select name=\"relation"+rowNumber+"\" class=\"form-control\" id=\"email-relation"+rowNumber+"\" onchange=handleRelation("+rowNumber+")>"
	+ " <option value=\"0\">contains</option>"
	+ " <option value=\"1\">does not contain</option>"
	+ " <option value=\"2\">before</option>"
	+ " <option value=\"3\">after</option>"
	+ " <option value=\"4\">starts with</option>"
	+ " <option value=\"5\">ends with</option>"
	+ " <option value=\"6\">is</option>"
	+ " <option value=\"7\">is not</option>"
	+ " <option value=\"8\">month</option>"
	+ " </select>"
	+ " </div>	"
	+ " <div style=\"display:none;\" class=\"form-group form-group-inline\" id=\"activity"+rowNumber+"\">"
	+ " <select name=\"activity"+rowNumber+"\" class=\"form-control\">"
	+ " <option value=\"0\">Laserstrike</option>"
	+ " <option value=\"1\">Learn to Skate</option>"
	+ " <option value=\"2\">Youth Hockey</option>"
	+ " <option value=\"3\">Adult Hockey</option>"
	+ " <option value=\"4\">Figure Skating</option>"
	+ " </select>"
	+ " </div>	"
	+ " <div style=\"display:none;\" class=\"form-group form-group-inline\" id=\"month"+rowNumber+"\">"
	+ " <select name=\"month"+rowNumber+"\" class=\"form-control\">"
	+ " <option value=\"1\">January</option>"
	+ " <option value=\"2\">February</option>"
	+ " <option value=\"3\">March</option>"
	+ " <option value=\"4\">April</option>"
	+ " <option value=\"5\">May</option>"
	+ " <option value=\"6\">June</option>"
	+ " <option value=\"7\">July</option>"
	+ " <option value=\"8\">August</option>"
	+ " <option value=\"9\">September</option>"
	+ " <option value=\"10\">October</option>"
	+ " <option value=\"11\">November</option>"
	+ " <option value=\"12\">December</option>"
	+ " </select>"
	+ " </div>"
	+ " <div class=\"form-group form-group-inline\" id=\"criteria"+rowNumber+"\">"
	+ " <input type=\"text\" size=20 name=\"criteria"+rowNumber+"\" class=\"form-control form-control-inline\">"
	+ " </div>" 
	+"<div class=\"form-group form-control-inline\">"
	+ "<button type=button onclick=\"deleteSearchRow("+rowNumber+");\" class=\"btn btn-block btn-lg btn-danger btn-remove-row btn-bar\" id=\"delete-row"+rowNumber+"\"><span class=\"fui-cross\"></span></button>"
	+"</div>"
	+ " </div>"

    $('#email-search-container').append(searchRow);
    newBase = document.getElementById("email-base" + rowNumber);
    newRelation = document.getElementById("email-relation" + rowNumber);
    handleBase(rowNumber);
    if (rowNumber > 0){
	$('#add-search-boxes').unbind('click');
	$('#search-row'+rowNumber).animo( { animation: 'bounceInRight', duration: 1 }, function() {
	    $('#add-search-boxes').bind('click',addSearchRow); console.log("called rebind");
	});    
    }  
    rowNumber += 1;  
}

function exportData(list){
    exportList = "First Name, Last Name, Email, Codename, Birthdate \n"
    list.children($('li')).each(
	function (index) {
	    $(this).children('.left-li').children('[class^=customer]').each(
		function (index) {
		    exportList += $(this).children('span').text().trim() + ",";
		});
	    exportList = exportList.slice(0,-1);
	    exportList += "\n";	
	});
    var a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";
    function saveData(data, fileName) {
	blob = new Blob([data], {type: "octet/stream"});
	url = window.URL.createObjectURL(blob);
	a.href = url;
	a.download = fileName;
	a.click();
	window.URL.revokeObjectURL(url);
    }
    saveData(exportList,"example.csv")  
}

$(document).ready(function() {
    var list = document.getElementById('list');
    $("#saveAll").click(function(e) {
	e.preventDefault();
	localStorage.setItem('customerList', list.innerHTML);
	alertify.success("You have saved your list.");
    });
    /* $('#ema
il-base').change(handleBase);
       /* REMOVE LATER ***ALERT*** */
    /* $('#email-base option[value=\"6\"]').prop('disabled',true); */
    /****************************/     
    /* $('#email-relation').change(handleRelation); */ 
    $("#clearAll").click(function(e) {
	e.preventDefault();
	localStorage.clear();
	window.location.href = "/email";
    });   
    $("#exportAll").click(function(e) {
	exportData($("#list"));
    });
    
    
    loadToDo();  
    $('#add-search-boxes').click(addSearchRow);  
    addSearchRow();
    $('#email-search-form').submit(validateListForm);
}); 

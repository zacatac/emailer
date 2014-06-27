if(typeof(String.prototype.trim) === "undefined")
{
    String.prototype.trim = function() 
    {
	return String(this).replace(/^\s+|\s+$/g, '');
    };
}

function validateListForm(){
  console.log("CALLINg");
    var criteriaTextBoxDiv = document.getElementById('criteria');
    var criteriaText = criteriaTextBoxDiv.children[0].value;       
    if (criteriaTextBoxDiv.style.display !== "none" && (criteriaText.trim() === '')) {
	return false;
    }
    return true; 
}

function handleBase(num){
  console.log("clicked handle base and num = " + num);
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
      relationDropdown.options[7].disabled = false;
      relationDropdown.value = 6;
      activityDropdown.style.display = "inline-block";
      criteriaText.style.display = "none";	 
      criteriaText.value = "";
      break;
    default:
      alterOptions(relationDropdown,false);
      activityDropdown.style.display = "none";
      criteriaText.style.display = "inline-block";
  }
}
function handleRelation(num){
  console.log("clicked handle relation and num = " + num);
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

function deleteParentListElement(el){
    parent = el.parentNode.parentNode;
    numElements = parent.parentNode.getElementsByTagName("li").length;
    if (numElements > 1){
	parent.parentNode.removeChild(parent);
    } else {
	alertify.error("You can't delete the last person. Use Clear All");
    }
} 

function makeEditable(el){
    var divs = el.parentNode.parentNode.getElementsByTagName('div');
    var leftDiv = divs[0];
    var rightDiv = divs[1];
    var editButton = rightDiv.getElementsByTagName('input')[0] 
    if ($(leftDiv).attr("contenteditable") === "false" || $(leftDiv).attr("contenteditable") === undefined) {
	$(leftDiv).attr("contenteditable",true);
	$(editButton).attr("value","save");     
    } else {
	$(leftDiv).attr("contenteditable",false);
	$(editButton).attr("value","edit");     
    }
}

function loadToDo() {    
    if (localStorage.getItem('todoList')){
	list.innerHTML = localStorage.getItem('todoList'); 
    };
}

var rowNumber = 0;
function addSearchRow(){
  rowContainer = document.getElementById('email-search-container');  
  var searchRow = "<div class=\"search-row\" name=\"search-row\" id=\"search-row"+rowNumber+"\">"
  +" <div  class=\"form-group form-group-inline\">"
  + " <select name=\"base\" class=\"form-control\" id=\"email-base"+rowNumber+"\" onchange=handleBase("+rowNumber+")>"
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
  + " <select name=\"relation\" class=\"form-control\" id=\"email-relation"+rowNumber+"\" onchange=handleRelation("+rowNumber+")>"
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
  + " <select name=\"activity\" class=\"form-control\">"
  + " <option value=\"0\">Laserstrike</option>"
  + " <option value=\"1\">Learn to Skate</option>"
  + " <option value=\"2\">Youth Hockey</option>"
  + " <option value=\"3\">Adult Hockey</option>"
  + " <option value=\"4\">Figure Skating</option>"
  + " </select>"
  + " </div>	"
  + " <div style=\"display:none;\" class=\"form-group form-group-inline\" id=\"month"+rowNumber+"\">"
  + " <select name=\"month\" class=\"form-control\">"
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
  + " <input type=\"text\" size=20 name=\"criteria\" class=\"form-control form-control-inline\">"
  + " </div>" 
  +"<div class=\"form-group form-control-inline\">"
  + "<button class=\"btn btn-block btn-lg btn-danger btn-remove-row btn-bar\"><span class=\"fui-cross\"></span></button>"
  +"</div>"
  + " </div>"

  rowContainer.innerHTML = rowContainer.innerHTML + searchRow;
  newBase = document.getElementById("email-base" + rowNumber);
  newRelation = document.getElementById("email-relation" + rowNumber);
  rowNumber += 1;  
}

$(document).ready(function() {
    var list = document.getElementById('list');
    $("#saveAll").click(function(e) {
	e.preventDefault();
	localStorage.setItem('todoList', list.innerHTML);
	alertify.success("You have saved your list.");
    });
  /* $('#email-base').change(handleBase);
  /* REMOVE LATER ***ALERT*** */
  /* $('#email-base option[value=\"6\"]').prop('disabled',true); */
  /****************************/     
  /* $('#email-relation').change(handleRelation); */ 
    $("#clearAll").click(function(e) {
	e.preventDefault();
	localStorage.clear();
	window.location.href = "/email";
    });   
    loadToDo();  
  $('#add-search-boxes').click(addSearchRow);  
  addSearchRow();
  /* $('#email-add-constraint').submit(validateListForm); */
});

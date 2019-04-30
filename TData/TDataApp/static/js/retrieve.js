var dbList = [];
var relList = [];
var attrList = [];
var x = 1;
var selectedDB;
var selectedRel;
var compiled_list = [];

function UpdateDBList(){
  console.log(dbList.length);
  var str = '<option value="-1" disabled selected>---Select DB---</option>';
  var i=0;
  for(i=0; i<dbList.length; i++){
    str+='<option value="'+i+'">'+dbList[i]+"</option>";
  }
  console.log(str);
  $('#select_db').html(str);
}

function GetDBList(){
  $.ajax({
    type: "POST",
    url: "get_dbList/",
    async: false,
    success: function(response) {
      dbList = JSON.parse(response);
      console.log(dbList);
      UpdateDBList();
    },
    error: function(response){
      // alert(response.status);
      console.log(response.status);
    },
  })
}

function UpdateRelList(id){
  console.log(relList.length);
  var str = '<option value="-1" disabled selected>---Select Table---</option>';
  var i=0;
  for(i=0; i<relList.length; i++){
    str+='<option value="'+i+'">'+relList[i]+"</option>";
  }
  console.log(str);
  document.getElementById(id).innerHTML = str;
}

function GetRelList(selectedDB, id){
  $.ajax({
    type: "POST",
    url: "get_relList/",
    async: false,
    data:{
      'dbName': JSON.stringify(selectedDB)
    },
    success: function(response) {
      relList = JSON.parse(response);
      UpdateRelList(id);
    },
    error: function(response){
      console.log(response.status);
    },
  })
}

function UpdateAttrList(){
  console.log(attrList);
  str=''
  val = 0
  for(var attr in attrList){
    str+='<tr><td><input type="checkbox" class="temp" val="'+val+'"></td>';
    str+='<td class="colName">'+attrList[attr][0]+'</td>';
    str+='<td class="colType">'+attrList[attr][1]+'</td></tr>';
  }
  
  console.log(str);
  $("#addAttr").html(str);
  $("#attributesTable").show();
}

function GetAttr(selectedDB, selectedRel){
  $.ajax({
    type: "POST",
    url: "get_attrList/",
    async: false,
    data: {
      'dbName': JSON.stringify(selectedDB),
      'relName': JSON.stringify(selectedRel)
    },
    success:function(response){
      attrList = JSON.parse(response);
      UpdateAttrList();
    }
  })
}

$(document).ready(function() {
  $("#FromWrapper").hide();
  x = 1;
  $("#attributesTable").hide();
  GetDBList();
  $("#select_db").change(function(){
    selectedDB = $(this).find("option:selected").text();
    GetRelList(selectedDB, 1);
  })
  $("#select_rel").change(function(){
    selectedDB = $("#select_db").find("option:selected").text();
    selectedRel = $(this).find("option:selected").text();
    GetAttr(selectedDB, selectedRel);
  })
})

function EmptyAll(){
  $('#select_rel').html('');
  $("#attributesTable").hide();
  GetDBList();
}



function AddRel(){
  x = x + 1;
  
  var SelRel = document.createElement('div');
  SelRel.className = "form-group";
  SelRel.id = x + 1000;

  var dropDown = document.createElement('select');
  dropDown.className = 'form-control';
  dropDown.id = x;
  dropDown.innerHTML = '<br>'  

  var attrForm = document.createElement('form');
  attrForm.id = "form" + x;
  strAttrWaala = '<br> Attributes: ' 
  attrForm.innerHTML = strAttrWaala;

  var inp = document.createElement('input');
  inp.setAttribute('type', 'text');
  inp.setAttribute('id', 'attrList'+x);

  document.getElementById('AllRelContainer').appendChild(SelRel);
  document.getElementById(x+1000).appendChild(dropDown);
  document.getElementById(x+1000).appendChild(attrForm);
  document.getElementById('form'+x).appendChild(inp);
  
  UpdateRelList(x);
}


function getAttrList(){
  var y = x;
  var i = 1;
  
  compiled_list = []; 
  for (i=1; i<=y; i++){
    var a_list = document.getElementById("attrList"+i).value;
    alert(a_list);
  
    a_list = a_list.replace(/\s/g, ""); //This regex removes whitespaces, if any in attrlist.  
    
    a_list = a_list.split(",");
    var e = document.getElementById(i)
    var chosen_rel = e.options[e.selectedIndex].text;
    
    var list_attr = [];
    var size = a_list.length;
    var j = 0;
    for(j=0; j<size; j++){
      list_attr[j] = chosen_rel + "." + a_list[j];

    }
      compiled_list = compiled_list.concat(list_attr);
      
  }
  console.log(compiled_list);
}


function Retrieve(){
  getAttrList();
  checkedRel = [];
  $('#FromWrapper tr').each(function(){
    var isTemp = ($(this).find(".FromList:checked").val());
    var isTemp2 = ($(this).find(".relNameCheckBox").html());

    console.log("---------");

    if(isTemp=="1"){
      checkedRel.push(isTemp2);
    }
  })
  
  var whereVal = $("#whereClause").val();
  // var additionalQueryVal  = $("#additionalQuery").val();

  data = {}
  data.dbName = selectedDB;
  data.relName = checkedRel;
  data.selAttr = compiled_list;
  data.where = whereVal;
  // data.additionalQuery = additionalQueryVal;

  console.log(data);


  $.ajax({
    type: "POST",
    url: "retrieveData/",
    data: {
      'data': JSON.stringify(data)
    },
    async: false,
    // dataType:'text',
    success: function(response) {
      console.log(response, typeof(response));
      if (response == "1") {
        swal('Done', 'Table created.', 'success');
      } else if (response == "-1") {
        swal('Duplication detected for this relations', 'Contact admin for further queries', 'error');
      } else if(response == "0") {
        swal('Given attribute(s) already temporalized', 'Duplication detected for this attribute', 'success');
      } else {
        swal('Something went wrong', 'we will get back to you later', 'error');
      }
      EmptyAll();
    }
  })
}

function FromCondition(){
 for (var i = 0; i < relList.length; i++) {
      var isTemp = '<td><input type="checkbox" class="FromList" value="' + 1 + '"></td><td class="relNameCheckBox">' + relList[i] + '</td>';
    $('#FromWrapper').append("<tr>" + isTemp + "</tr>");  
  }
  $("#FromWrapper").show();
}
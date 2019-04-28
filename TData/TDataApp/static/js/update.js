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
      // alert(response.status);
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

  var attrForm = document.createElement('form');
  attrForm.id = "form" + x;
  var inp = document.createElement('input');
  inp.setAttribute('type', 'text');
  inp.setAttribute('id', 'attrList'+x);

  // SelRel.innerHTML = dropDown;
  document.getElementById('AllRelContainer').appendChild(SelRel);
  document.getElementById(x+1000).appendChild(dropDown);
  document.getElementById(x+1000).appendChild(attrForm);
  document.getElementById('form'+x).appendChild(inp);
  
  UpdateRelList(x);
}


function getAttrList(){
  var y = x;
  var i = 1;
  // alert(y);
  compiled_list = []; 
  for (i=1; i<=y; i++){
    var a_list = document.getElementById("attrList"+i).value;
    alert(a_list);
    //This regex removes whitespaces, if any in attrlist.  
    a_list = a_list.replace(/\s/g, "");      
    
    // Gives a list of attributes
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


function Submit(){
  getAttrList();
  alert(compiled_list.length);
  $('#FromWrapper tr').each(function(){
    var isTemp = ($(this).find(".FromList:checked").val());
    // console.log(isTemp());
      
  })
}

function FromCondition(){
 for (var i = 0; i < relList.length; i++) {
      var isTemp = '<td><input type="checkbox" class="FromList" value="' + relList[i] + '"></td><td>' + relList[i] + '</td>';
    $('#FromWrapper').append("<tr>" + isTemp + "</tr>");  
  }
  $("#FromWrapper").show();
}

function Temporalize(){
  var tempo = 0;
  var table_data = []; //list of list containing isTemp and colName
  $('#addAttr tr').each(function() {
    var isTemp = ($(this).find(".temp:checked").val());
    console.log(isTemp, typeof(isTemp));
    if(isTemp=="on"){
      isTemp=1;
      tempo+=1;
    }
    else{
      isTemp=0;
    }
    
    var attrName = ($(this).find(".colName").html())//.toString();
    var attrType = ($(this).find(".colType").html());
    if(attrName!="")
      table_data.push([isTemp, attrName, attrType]);
  })
  
  console.log(table_data);
  if(tempo==0){
    swal('', 'No col selected for temporalizing', 'error');
    return;
  }
  
  data = {};
  data.dbName = selectedDB;
  data.relName = selectedRel;
  data.attributes = table_data;
  console.log(data);
  
  $.ajax({
    type: "POST",
    url: "temp_rel/",
    // contentType: "application/json",
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


var dbList = [];
var relList = [];
var attrList = [];

var selectedDB;
var selectedRel;

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

function UpdateRelList(){
  console.log(relList.length);
  var str = '<option value="-1" disabled selected>---Select Table---</option>';
  var i=0;
  for(i=0; i<relList.length; i++){
    str+='<option value="'+i+'">'+relList[i]+"</option>";
  }
  console.log(str);
  $('#select_rel').html(str);
}

function GetRelList(selectedDB){
  $.ajax({
    type: "POST",
    url: "get_relList/",
    async: false,
    data:{
      'dbName': JSON.stringify(selectedDB)
    },
    success: function(response) {
      relList = JSON.parse(response);
      UpdateRelList();
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
  $("#attributesTable").hide();
  GetDBList();
  $("#select_db").change(function(){
    selectedDB = $(this).find("option:selected").text();
    GetRelList(selectedDB);
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


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
  for(var i=0; i<relList.length; i++){
    str+='<option value="'+i+'">'+relList[i]+"</option>";
  }
  console.log(str);
  $("#select_rel").html(str);
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

function UpdateAttrList(attrList){
  str=''
  val = 0
  for(var attr in attrList){
    console.log(attrList[attr]);
    str += '<tr><td class="colName">'+attrList[attr][0]+'</td>';
    str += '<td class="colType">'+attrList[attr][1]+'</td>';
    str += '<td class="value"><input type="text" class="colVal"></td></tr>';
  }

  console.log(str);
  $("#addAttr").html(str);
  $("#attrTableDiv").show();
  
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
      UpdateAttrList(attrList);
    }
  })
}

$(document).ready(function(){
  $("#attrTableDiv").hide();
  
  GetDBList();
  
  $("#select_db").change(function(){
    selectedDB = $(this).find("option:selected").text();
    GetRelList(selectedDB);
    // HideAttrTable();
  })
  
  $("#select_rel").change(function(){
    selectedDB = $("#select_db").find("option:selected").text();
    selectedRel = $(this).find("option:selected").text();
    GetAttr(selectedDB, selectedRel);
  })
  
})

function Insert(){
  
  var attr = [];
  
  $('#addAttr tr').each(function(){
    var colName = ($(this).find(".colName")).html();
    var colType = ($(this).find(".colType")).html();
    var colVal = ($(this).find(".colVal")).val();
    
    if(colVal!='')
      attr.push([colName, colType, colVal]);
  })
  
  var data = {};
  data.dbName = selectedDB;
  data.relName = selectedRel;
  data.attrVal = attr;
  
  $.ajax({
    type: "POST",
    async: false,
    data: {
      'data': JSON.stringify(data)
    },
    url: "insertQuery/",
    success: function(response){
      if(response==1){
        swal({ title: "Insertion Successful", icon: "success"}).then(function(){
          location.reload();
        });
      }else{
        swal("Something went wrong", "please look for the constraints", "error");
      }
    },
    error: function(err){
      swal("Something went wrong", "please look for the constraints", "error");
      console.log(err.status);
    }
  })
}
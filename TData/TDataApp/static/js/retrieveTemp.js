var dbList = [];
var relList = [];
var attrList = [];

var selectedDB;
var selectedRel;
var selectedQuery;

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
    str+='<td class="colName">'+attrList[attr]+'</td></tr>';
  }
  
  console.log(str);
  $("#addAttr").html(str);
  $("#attributesTable").show();
}
function GetAttr(selectedDB, selectedRel){
  $.ajax({
    type: "POST",
    url: "get_tempAttrList/",
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
  $("#select_temp_query").change(function(){
    selectedQuery = $(this).find("option:selected").val();
  })
})

function Retrieve(){
  var tempo = 0;
  var table_data = []; //list of list containing isTemp and colName
  $('#addAttr tr').each(function() {
    var isTemp = ($(this).find(".temp:checked").val());
    if(isTemp=="on"){
      isTemp=1;
      tempo+=1;
    }
    else{
      isTemp=0;
    }
    
    var attrName = ($(this).find(".colName").html())//.toString();
    if(isTemp==1)
      table_data.push(attrName);
  })
  
  console.log("----");
  console.log(table_data);
  if(tempo==0){
    swal('', 'No col selected for retrieval', 'error');
    return;
  }
  
  var tempQueryVal = $("#tempQueryVal").val();
  
  data = {};
  data.dbName = selectedDB;
  data.relName = selectedRel;
  data.attributes = table_data;
  data.query = selectedQuery;
  data.val = tempQueryVal;
  console.log(data);
  
  $.ajax({
    type: "POST",
    url: "ret_temp/",
    // contentType: "application/json",
    data: {
      'data': JSON.stringify(data)
    },
    async: false,
    // dataType:'text',
    success: function(response) {
      console.log(response, typeof(response));
      data = JSON.parse(response);
      
      var head = data.head;
      var body = data.body;
      console.log(head);
      console.log(body);
      
      var populateTableHead = "<tr>";
      var populateTableBody = "";
      
      for(var i in head){
        if(i!=0){
          populateTableHead+="<td colspan='3' style='text-align:center;'>"+head[i]+"</td>";
        }
        else {
          populateTableHead+="<td>"+head[i]+"</td>";
        }
      }
      populateTableHead+="</tr>";
      console.log(populateTableHead);
      
      for(var i in body){
        populateTableBody+="<tr>";
        console.log(i, body[i]);
        for(var j in body[i]){
          populateTableBody += "<td>"+body[i][j]+"</td>"
        }
        populateTableBody+="</tr>";
      }
      
      console.log(populateTableBody);
      
      $("#outputTableHead").html(populateTableHead);
      $("#outputTableBody").html(populateTableBody);
      $("#outputDiv").show();
      if (response == "0") {
        swal('Something went wrong', 'we will get back to you later', 'error');
      } else {
        swal("done", "", "success");
      }
    }
  })
  
}
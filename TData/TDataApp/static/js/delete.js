var dbList = [];
var relList = [];
var epochCount = 1;

var dbSelected = "";
var relSelected = {};

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
  for(var i=0; i<epochCount; i++){
    var id = "#select_rel"+i;
    $(id).html(str);
  }
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
      console.log(response.status);
    },
  })
}

$(document).ready(function(){
  $("#attrTableDiv0").hide();
  
  GetDBList();
  
  $("#select_db").change(function(){
    selectedDB = $(this).find("option:selected").text();
    GetRelList(selectedDB);
  })
})

function AddAttr(){
  var html = '<hr><div class="form-group relDiv"><label for="select rel">Select Relation</label><select class="form-control select_rel" id="select_rel'+epochCount+'"></div>';
  $('#repDiv').append(html);
  epochCount++;
  
}
function Delete(){
  var dbSelected = $("#select_db").find("option:selected").text();
  
  var relSelected = [];
  for(var i=0; i<epochCount; i++){
    var relId = "#select_rel"+i;
    var relVal = $(".repetitiveDiv .relDiv").find(relId+" option:selected").val();
    var relName = $(".repetitiveDiv .relDiv").find(relId+" option:selected").text();
    if(relVal!=-1)
      relSelected.push(relName);
  }
  
  // var additionalRelVal = $("#additionalRel").val();
  var whereVal = $("#whereClause").val();
  var additionalQueryVal  = $("#additionalQuery").val();
  
  var data = {};
  data.dbName = dbSelected;
  data.relNames = relSelected;
  // data.additionalRel = additionalRelVal;
  data.where = whereVal;
  data.additionalQuery = additionalQueryVal;
  
  console.log(data);
  
  $.ajax({
    type: "POST",
    url: "deleteQuery/",
    async: false,
    data: {
      'data': JSON.stringify(data)
    },
    success: function(resp){
      console.log(resp, typeof(resp));
      if(resp=="1"){
        swal({ title: "Deletion Successful", icon: "success"}).then(function(){
          location.reload();
        });
      } else if(resp=="0"){
        swal("Something went wrong", "Please check the query again", "error");
      } else {
        swal("Something went wrong", "We will get back to you later", "error");
      }
    },
    error(err){
      alert(err);
    }
  })
  
  console.log(relSelected);
}
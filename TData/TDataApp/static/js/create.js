// relName not required as of now

var dataTypes = ['int', 'string'];
var dbName = "";
// var relName = "";
var table_data = [];

$(document).ready(function() {
  EmptyAll();
  // document.write('<script type="text/javascript" src="global.js"></script>');
  // $.ajax({
  // 	type:"POST",
  // 	url:"get_data_types",
  // 	success:function(response){
  // 		dataTypes=JSON.parse(response);
  // 	}
  // })
})

function EmptyAll(){
  $('#rel_table').hide();
  $('#db_name').val('');
  // $('#rel_name').val('');
  $('#rel_table').html('');
}
function UpdateDBName() {
  dbName = $('#db_name').val();
}

// function UpdateRelName() {
//   relName = $('#rel_name').val();
// }

function EmptyDBError() {
  UpdateDBName();
  console.log(dbName);
  if (dbName == "") {
    swal('', 'Please Insert DB Name', 'error');
    return 0;
  }
  return 1;
}

// function EmptyRelError() {
//   if (EmptyDBError() == 0)
//     return 0;
//   UpdateRelName();
//   if (relName == "") {
//     swal('', 'Please Insert Relation Name', 'error');
//     return 0;
//   }
//   return 1;
// }

function Display(response) {
  alert(response);
}

function GetRel() {
  if (EmptyDBError() == 0)
    return 0;
  $.ajax({
    type: 'POST',
    url: "get_rel/",
    data: {
      'dbName': JSON.stringify(dbName)
    },
    async: false,
    success: function(response) {
      console.log(response, typeof(response));
      if (response == "" || response == undefined || response == null) {
        swal('', 'Database does not exist', 'error');
        return (-1);
      } else {
        Display(response);
        console.log(response);
        return response;
      }
    },
    error: function(err) {
      swal('something went wrong', 'Cant get to respective Database', 'error');
    }
  })
}

// function CheckRel() {
//   if (EmptyRelError() == 0)
//     return 0;
//   $.ajax({
//     type: 'POST',
//     url: 'check_duplicate/',
//     data: {
//       'dbName': JSON.stringify(dbName),
//       'relName': JSON.stringify(relName)
//     },
//     async: false,
//     success: function(response) {
//       console.log(response, typeof(response));
//       if (response == '-1') {
//         swal('Wait!!', 'Even the db does not exist.\nBut we can create it for you.', 'error');
//       } else if (response == '0') {
//         swal('Wait!!', 'Relation already exists in the db.', 'error');
//       } else if (response == '1') {
//         swal('Go Ahead.', 'No such relation exists in the db.', 'success');
//       } else {
//         swal('Something went wrong.', 'We will get back to you later.', 'error');
//       }
//       return response;
//     },
//     error: function(response) {
//       swal('Something went wrong.', 'We will get back to you later', 'error');
//       return 0;
//     },
//   })
// }

function AddAttr() {
  $('#rel_table').show();

  var isTemp = '<td><input type="checkbox" name="temp" class="temp"></td>';
  
  var name = '<td><input type="text" class="colName"></td>';

  var type = '<td><select class="form-group colType">';
  for (var i = 0; i < dataTypes.length; i++) {
    type += '<option value="' + i + '">' + dataTypes[i] + '</option>';
  }
  type += '</select></td>';
  
  var isNotNull = '<td><input type="checkbox" name="notNull" class="notNull"></td>';
  
  var isUnique = '<td><input type="checkbox" name="unique" class="unique"></td>';

  $('#rel_table').append("<tr>" + isTemp + name + type + isNotNull + isUnique + "</tr>");
}

function AddRel() {
  // if (EmptyRelError() == 0)
    // return 0;
  if(EmptyDBError()==0)
    return 0;
  
  console.log(dbName);
  table_data=[];
  $('#rel_table tr').each(function() {
    var isTemp = ($(this).find(".temp:checked").val());
    if(isTemp==undefined) isTemp=0;
    else isTemp=1;
    
    var isNotNull = ($(this).find(".notNull:checked").val());
    if(isNotNull==undefined) isNotNull=0;
    else isNotNull=1;
    
    var isUnique = ($(this).find(".unique:checked").val());
    if(isUnique==undefined) isUnique=0;
    else isUnique=1;
      
    var attrName = ($(this).find(".colName").val()).toString();
    var attrType = ($(this).find(".colType").val()).toString();
    if(attrName!="")
      table_data.push([isTemp, attrName, attrType, isNotNull, isUnique]);
  })
  
  console.log(table_data);
  if(table_data.length==0){
    swal('', 'Schema cant be empty', 'error');
    return;
  }
  
  data = {};
  data.dbName = dbName;
  // data.relName = relName;
  data.attributes = table_data;
  console.log(data);

  $.ajax({
    type: "POST",
    url: "create_rel/",
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
        swal('Duplication detected', 'One or more of the attributes already exists', 'error');
      } else {
        swal('Something went wrong', 'we will get back to you later', 'error');
      }
      EmptyAll();
    }
  })
}
var dbList=[];
var dbName="";
var relList=[];

$(document).ready(function(){
  $('#showDbDiv').hide();
  GetDBList();
})

function EmptyAll(){
  // <!-- works on db.change() as well -->
  
}

function GetDBList(){
  $.ajax({
    type:'POST',
    url:"get_db/",
    async: false,
    success: function(response){
      console.log(response, typeof(response));
      if(response=="" || response==null || response.length==0){
        alert("empty");
      //   swal("Looks like we have no db currently\nWould you like to create one?",{
      //     buttons: {
      //       cancel: "No, I like it here!!",
      //       catch: {
      //         text: "Obviously!!",
      //         value: "catch",
      //       },
      //     },
      //   }).then((value)=>{
      //     switch(value){
      //       case "catch": 
      //         document.location.href="../create/";
      //     }
      //   });
      }
      else{
        // dbList=JSON.parse(response);
        dbList=response;
        console.log(dbList, typeof(response));
        console.log(dbList, typeof(dbList));
        // PopulateDB();
      }
    },
    error:function(err){
      alert(err.status);
      // swal('Something went wrong', '', 'error');
    }
  });
  console.log("get db list here");
}

function PopulateDB(){
  var str = "";
  console.log(dbList, typeof(dbList));
  for(i=0; i<dbList.length; i++){
    str+='<option value="'+dbList[i]+'">'+dbList[i]+'</option>';
  }
  $('#select_db').append(str);
}

function GetRel(){
  console.log("This function is already done in create.html");
}

function poplulateRel(){
  var i=0;
  var st = '';
  for(i=1; i<=relList.length; i++){
    st+='<option value="' + str(i) + '">' + relList[i-1] + '</option>'
  }
  return st;
}

function AddRel(){
  var sel = '<br><label for="join_rel">Join:</label><select class="form-control join_rel"></select>'
  var getOptions = poplulateRel();
  var btn = '<br><input type="button" class="btn btn-default" onClick="AddRel()" value="Join" style="float: right">'
  sel+=getOptions+btn;
  console.log(sel);
  $('#joinRelDiv').append(sel);
  
}
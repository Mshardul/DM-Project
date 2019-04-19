$(document).ready(function() {
  $("#sqlTable").hide();
  GetSql();
  
  $('.accept').click(function(){
    var id = $(this).closest('tr').find('td:nth-child(1)').text();
    var db = $(this).closest('tr').find('td:nth-child(2)').text();
    var rel = $(this).closest('tr').find('td:nth-child(3)').text();
    var sql = $(this).closest('tr').find('td:nth-child(4)').text();
    var attr = $(this).closest('tr').find('td:nth-child(5)').text();
    
    var data = {};
    data.dbName = db;
    data.relName = rel;
    data.query = sql;
    data.queryId = id;
    data.attr = attr;
    console.log(data);
    
    $.ajax({
      type: "POST",
      url: "exec_query/",
      async: false,
      data: {'data': JSON.stringify(data)},
      success: function(response){
        if(response==1){
          swal('', 'Query Executed Successfully', 'success');
        }else if(response==-1){
          swal('', 'Query could not be executed', 'error');
        }else{
          swal('', 'Something went wrong', 'error');
        }
        location.reload();
      },
      error: function(resp){
        alert(resp.status);
      }
    })
  });
  
  $('.reject').click(function(){
    var id = $(this).closest('tr').find('td:nth-child(1)').text();
    var db = $(this).closest('tr').find('td:nth-child(2)').text();
    var rel = $(this).closest('tr').find('td:nth-child(3)').text();
    var sql = $(this).closest('tr').find('td:nth-child(4)').text();
    var data = {};
    
    data.dbName = db;
    data.relName = rel;
    data.query = sql;
    data.queryId = id;
    console.log(data);
    
    $.ajax({
      type: "POST",
      url: "del_query/",
      async: false,
      data: {'data': JSON.stringify(data)},
      success: function(response){
        if(response==1){
          swal('', 'Query Deleted Successfully', 'success');
        }else if(response==-1){
          swal('', 'Query could not be deleted', 'error');
        }else{
          swal('', 'Something went wrong', 'error');
        }
        location.reload();
      },
      error: function(resp){
        alert(resp.status);
      }
    })
  });
  
})

function GetSql(){
  $.ajax({
    type: "POST",
    url: "get_sql/",
    async: false,
    success: function(response) {
      resp = JSON.parse(response)
      console.log(resp);
      if(resp.length==0){
        swal('Nothing to show here', 'Looks like your work is done', 'success');
        // setTimeout(function(){
        //   window.location.href="/app/makeTemp/";
        // }, 700);
        return;
      }
      table = "";
      for(var ind in resp){
        console.log(resp[ind]);
        table += "<tr><td class='id'>"+resp[ind][0]+"</td>";
        table += "<td class='db'>"+resp[ind][1]+"</td>";
        table += "<td class='rel'>"+resp[ind][2]+"</td>";
        table += "<td class='sql'>"+resp[ind][3]+"</td>";
        table += "<td class='attr'>"+resp[ind][4]+"</td>";
        table += "<td><input type='button' class='accept' value='execute'></td>";
        table += "<td><input type='button' class='reject' value='delete'></td></tr>";
      }
      $("#sqlStatements").html(table);
      $("#sqlTable").show();
    },
  })
}
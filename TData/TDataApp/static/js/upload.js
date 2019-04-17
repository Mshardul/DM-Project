function Upload(){
  var data = new FormData($('#fileForm').get(0));
  $.ajax({
    type: 'POST',
    url: "upload_file/",
    data: data,
    async: false,
    success: function(response) {
      alert(response.len);
    },
    error: function(response) {
      alert(response.status);
    },
  })
}
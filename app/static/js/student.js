$(document).ready(function() {

  function getData() {

    return {
      "year": $("#學年度").val(),
      "school": $("#學校名稱").val(),
      "div": $("#進修別").val(),
      "level": $("#等級別").val(),
      "grade": $("#年級").val(),
      "gender": $("#性別").val(),
      "loc": $("#縣市").val(),
    }
  }

  var table = $("#table").DataTable({
    "ajax": {//http://127.0.0.1:5000
      "url": "https://big-data-www.herokuapp.com/api/student",
      "type": "POST",
      "data": getData
    }
  });
  $(".dataTables_length").addClass("bs-select");

  $("#btn-filter").click(function() {

    table.ajax.reload();
  });
});
$(function () {
  $("#content_index").load(`${get_root_url()}/admin/posts` + " #content");
  $("#views a").click(function (event) {
    event.preventDefault();
    var url = $(this).attr("href");
    console.log(url);
    $("#content_index").load(url + " #content");
  });
});

function get_root_url() {
  return window.location.origin;
}

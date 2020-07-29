$(function () {
  $("#follow").click(function (event) {
    event.preventDefault();
    const url_follow = $("#follow").data("url");
    $.getJSON(url_follow, function (data) {
      if (data == "following") {
        $("#follow").attr("class", "btn-sm btn btn-secondary");
        $("#follow").text("Dejar de seguir");
        $("#follow").attr("id", "unfollow");
      }
    }).fail(function (err) {
      console.log(err);
    });
  });

  $("#unfollow").click(function (event) {
    event.preventDefault();
    const url_unfollow = $("#unfollow").data("url");
    $.getJSON(url_unfollow, function (data) {
      if (data == "unfollowing") {
        console.log(data, $(this));
        $("#unfollow").attr("class", "btn-sm btn btn-success");
        $("#unfollow").text("Seguir");
        $("#unfollow").attr("id", "follow");
      }
    }).fail(function (err) {
      console.log(err);
    });
  });
});

function getUrlRoot() {
  return window.location.origin;
}

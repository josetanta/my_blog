$(function () {
	$('button').click(function (event) {
		event.preventDefault();
		console.log(event.target.value);
		$.getJSON("{{ url_for('admin.ban', id = post.id) }}", function (data) {
			if (data.status === false) {
				let e = `<button id="ban_post_{{ post.id }}" type="submit" class="btn-sm btn btn-success">Dar Alta</button>`;
				let flag = `<td class="post-flags text-danger" id="flag">Suspendido</td>`;

				$('#ban_post_{{ post.id }}').replaceWith(e);

				$('#flag-{{ post.id }}').replaceWith(flag);
			}
			else if (data.status === true) {
				let e = `<button id="ban_post_{{ post.id }}" type="submit" class="btn-sm btn btn-danger">Suspender</button>`;
				let flag = `<td class="post-flags text-success" id="flag">Publicado</td>`;

				$('#ban_post_{{ post.id }}').replaceWith(e);

				$('#flag-{{ post.id }}').replaceWith(flag);
			}
		});
	});
})

// $(function () {
// 	$('#ban_post_{{ post.id }}').click(function(event) {
// 		event.preventDefault();
// 		$.getJSON("{{ url_for('admin.ban', id = post.id) }}", function(data) {
// 			if(data.status === false){
// 				let e =`<button id="ban_post_{{ post.id }}" type="submit" class="btn-sm btn btn-success">Dar Alta</button>`;
// 				let flag =`<td class="post-flags text-danger" id="flag">Suspendido</td>`;

// 				$('#ban_post_{{ post.id }}').replaceWith(e);

// 				$('#flag-{{ post.id }}').replaceWith(flag);
// 			}
// 			else if (data.status === true){
// 				let e =`<button id="ban_post_{{ post.id }}" type="submit" class="btn-sm btn btn-danger">Suspender</button>`;
// 				let flag =`<td class="post-flags text-success" id="flag">Publicado</td>`;

// 				$('#ban_post_{{ post.id }}').replaceWith(e);

// 				$('#flag-{{ post.id }}').replaceWith(flag);
// 			}
// 		});
// 	});
// });

export default function Post({ post }) {
  return (
    <div className="shadow post-show my-2">
      <legend>
        <h3>
          <a className="text-info text-decoration-none" href="/">
            {post.title}
          </a>
        </h3>
      </legend>
      <div id="post-public">
        <img className="post-img" alt="Imagen del Post" src={post.image} />
        <div className="post-content">
          <p className="text-justify text-break">{post.content}</p>
          <a className="text-primary" href="/">
            Más informacion aquí <i className="fad fa-external-link" />
          </a>
          <p className="text-muted">Publicado: {post.created} </p>
        </div>
        <div className="meta-data">
          <a className="text-success text-decoration-none" href="/">
            <img
              className="image-account-post"
              src={post.author.image}
              alt="Foto de mi perfil"
            />
            <b>{post.author.username}</b>
          </a>
        </div>
      </div>
    </div>
  );
}

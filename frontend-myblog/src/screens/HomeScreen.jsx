import { useEffect } from "react";

// Redux
import { postListAction } from "../actions/postsActions";
import { useDispatch, useSelector } from "react-redux";
import Post from "../components/Post";
import Fade from "react-reveal/Fade";

export default function HomeScreen() {
  const dispatch = useDispatch();
  const { loading, posts, error } = useSelector((state) => state.postList);

  useEffect(() => {
    dispatch(postListAction());
  }, [dispatch]);
  return (
    <>
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary navbar-sticky">
        <a className="navbar-brand" href="/">
          Blog
        </a>
        <button
          className="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#basePost"
          aria-controls="basePost"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon" />
        </button>

        <div className="collapse navbar-collapse" id="basePost">
          <ul className="navbar-nav mr-auto">
            <li className="nav-item">
              <a href="/" className="nav-link">
                <i className="fas fa-home-lg-alt" />
              </a>
            </li>
            <li className="nav-item">
              <a href="/" className="nav-link">
                <i className="far fa-plus-circle" /> Post
              </a>
            </li>
            <li className="nav-item">
              <a href="/" className="nav-link">
                Sobre nosotros
              </a>
            </li>
            <li className="nav-item">
              <a href="/" target="_blank" className="nav-link">
                <i className="fab fa-github" /> GitHub
              </a>
            </li>
          </ul>
          <ul className="navbar-nav mr-0">
            <li className="nav-item">
              <a href="/" className="nav-link">
                <i className="far fa-user-plus"> </i> Registrarse
              </a>
            </li>
            <li className="nav-item">
              <a href="/" className="nav-link">
                <i className="fas fa-sign-in-alt" /> Iniciar Sesión
              </a>
            </li>
          </ul>
          <ul className="navbar-nav mr-0">
            <div className="nav-item btn-group dropleft ml-5">
              <button className="btn btn-outline-light">
                <i className="fas fa-caret-down" />
                <img className="account-img-profile" src="#" alt="product" />
                <i className="fas fa-user" />
              </button>
              <div
                className="dropdown-menu"
                aria-labelledby="dropdownOptionsAccount"
              >
                <a href="/" className="dropdown-item">
                  <i className="fas fa-columns" /> Administrar
                </a>
                <a href="/" className="dropdown-item">
                  <i className="fas fa-user-circle" /> Mi Perfil
                </a>
                <a href="/" className="dropdown-item">
                  <i className="fas fa-user-edit" /> Editar Mi Perfil
                </a>
                <a href="/" className="dropdown-item text-danger">
                  <i className="fas fa-sign-out-alt" /> Cerrar Sesión
                </a>
              </div>
            </div>
          </ul>
        </div>
      </nav>
      <main role="main" className="py-4 container">
        {loading ? (
          <div className="alert alert-info">Cargando ... </div>
        ) : error ? (
          <div className="alert alert-danger">Error de Página</div>
        ) : (
          <Fade right cascade>
            <div>
              {posts &&
                posts.map((post, index) => (
                  <div key={index}>
                    <Post post={post} />
                  </div>
                ))}
            </div>
          </Fade>
        )}
      </main>
      <footer className="text-center border-top mt-3">
        <p>
          <a href="/">jose.tanta.27@unsch.edu.pe</a>
        </p>
      </footer>
    </>
  );
}

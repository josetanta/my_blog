import { useEffect } from "react";
import { BrowserRouter, Link, Route } from "react-router-dom";
import HomeView from "./views/HomeView";
import PostDetailsView from "./views/PostDetailsView";
import { useDispatch, useSelector } from "react-redux";
import { postListAction } from "./actions/postActions";

function App() {
  const { loading, data, error } = useSelector((state) => state.postList);
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(postListAction());
  }, [dispatch]);
  return (
    <BrowserRouter>
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary navbar-sticky">
        <Link to={"/"} className="navbar-brand">
          Blog
        </Link>
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
              <Link to="/" className="nav-link">
                <i className="fas fa-home-lg-alt" />
              </Link>
            </li>
            <li className="nav-item">
              <Link to="/" className="nav-link">
                <i className="far fa-plus-circle" /> Post
              </Link>
            </li>
            <li className="nav-item">
              <Link to="/" className="nav-link">
                Sobre nosotros
              </Link>
            </li>
            <li className="nav-item">
              <Link to="/" target="_blank" className="nav-link">
                <i className="fab fa-github" /> GitHub
              </Link>
            </li>
          </ul>
          <ul className="navbar-nav mr-0">
            <li className="nav-item">
              <Link to="/" className="nav-link">
                <i className="far fa-user-plus"> </i> Registrarse
              </Link>
            </li>
            <li className="nav-item">
              <Link to="/" className="nav-link">
                <i className="fas fa-sign-in-alt" /> Iniciar Sesión
              </Link>
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
                <Link to="/" className="dropdown-item">
                  <i className="fas fa-columns" /> Administrar
                </Link>
                <Link to="/" className="dropdown-item">
                  <i className="fas fa-user-circle" /> Mi Perfil
                </Link>
                <Link to="/" className="dropdown-item">
                  <i className="fas fa-user-edit" /> Editar Mi Perfil
                </Link>
                <Link to="/" className="dropdown-item text-danger">
                  <i className="fas fa-sign-out-alt" /> Cerrar Sesión
                </Link>
              </div>
            </div>
          </ul>
        </div>
      </nav>
      <main role="main" className="py-4 container">
        <Route path="/post/:slug" component={PostDetailsView} />
        <Route path="/" exact={true}>
          <HomeView loading={loading} data={data} error={error} />
        </Route>
      </main>
      <footer className="text-center border-top mt-3">
        <p>
          <a href="/">jose.tanta.27@unsch.edu.pe</a>
        </p>
      </footer>
    </BrowserRouter>
  );
}

export default App;

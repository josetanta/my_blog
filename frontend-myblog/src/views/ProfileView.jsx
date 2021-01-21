import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { userDetailsSlugAction } from "../actions/userActions";

// Components
import ImageUser from "../components/ImageUser";
import Fade from "react-reveal/Fade";

export default function ProfileView(props) {
  const slug = props.match.params.slug_user;

  const userDetails = useSelector((state) => state.userDetails);
  const { loading, error, user } = userDetails;
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(userDetailsSlugAction({ slug }));
    return () => {};
  }, [dispatch, slug]);

  return (
    <>
      {loading ? (
        <div className="alert alert-info">Cargando el Perfil 😄😄</div>
      ) : error ? (
        <div className="alert alert-danger">Error...</div>
      ) : (
        <>
          {user && (
            <>
              <div className="row">
                <div className="col-md-4">
                  <Fade left>
                    <div className="card">
                      <ImageUser
                        classes={"card-img-top image-account"}
                        alt="ImageUser"
                        userData={user.data}
                      />
                      <div className="card-body">
                        <h2 className="card-title">{user.data.username}</h2>
                        <p className="card-text">{user.data.email}</p>
                        <div className="mx-center d-flex justify-content-between">
                          <button type="button" className="btn btn-info">
                            Seguidores{" "}
                            <span className="badge badge-light">
                              {user.data.followers}
                            </span>
                          </button>
                          <div className="my-2" />
                          <button type="button" className="btn btn-secondary">
                            Siguiendo{" "}
                            <span className="badge badge-light">
                              {user.data.followeds}
                            </span>
                          </button>
                        </div>
                      </div>
                    </div>
                  </Fade>
                </div>
                <div className="col-md-8">
                  <Fade right>
                    <h3 className="text-teal">
                      Post publicados por{" "}
                      <b>
                        <em>{user.data.username}</em>
                      </b>
                    </h3>
                    <fieldset className="shadow col-lg-10 col-sm-4 my-3">
                      <legend>
                        <h4 className="text-primary">
                          <a href="/">post title</a>
                        </h4>
                      </legend>

                      <p className="text-muted">Created Date</p>
                    </fieldset>
                    <fieldset className="shadow col-lg-10 col-sm-4 post-ban my-3">
                      <legend>
                        <h4 className="post-title-ban">post title baned</h4>
                      </legend>
                      <p className="text-break post-ban-body">
                        Este post fue baneado. Comunicate con el Staff
                      </p>
                    </fieldset>
                  </Fade>
                </div>
              </div>
            </>
          )}
        </>
      )}
    </>
  );
}

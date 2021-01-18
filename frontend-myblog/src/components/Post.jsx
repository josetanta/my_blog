import { useEffect } from "react";
import { Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { userDetailsAction } from "../actions/userActions";
import ImageUser from "./ImageUser";

export default function Post({ post: { data, paths } }) {
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.userDetails);
  useEffect(() => {
    dispatch(userDetailsAction(paths.user));
  }, [dispatch, data, paths]);

  return (
    <div className="post-show my-2">
      <legend>
        <h3>
          <Link
            className="text-info text-decoration-none"
            to={"/post/" + data.slug}
          >
            {data.title}
          </Link>
        </h3>
      </legend>
      <div id="post-public">
        <img className="post-img" alt="Imagen del Post" src={data.image} />
        <div className="post-content">
          <p className="text-justify text-break">{data.content}</p>
          <a className="text-primary" href="/">
            Más informacion aquí <i className="fad fa-external-link" />
          </a>
          <p className="text-muted">Publicado: {data.created} </p>
        </div>

        <div className="meta-data">
          <Link to={"/user"} className="text-success text-decoration-none">
            {user && (
              <ImageUser
                classes={"image-account-post"}
                image={user.data.image}
              />
            )}
            {"  "}
            <b>{user && user.data.username}</b>
          </Link>
        </div>
      </div>
    </div>
  );
}

import { useEffect } from "react";
import { Link } from "react-router-dom";

// Redux
import { useDispatch, useSelector } from "react-redux";
import { userDetailsWithPathAction } from "../actions/userActions";

// Components
import ImageUser from "./ImageUser";
import ImagePost from "./ImagePost";

export default function Post({
  post: { data, paths },
  linkMoreInfoStatus,
  truncateText,
}) {
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.userDetails);
  useEffect(() => {
    dispatch(userDetailsWithPathAction(paths.user));
  }, [dispatch, data, paths]);

  return (
    <div className="post-show my-2">
      <div className="post-content">
        <Link
          className="text-info text-decoration-none"
          to={"/post/" + data.slug}
        >
          <h3>{data.title}</h3>

          <ImagePost classes="post-img" alt="Imagen del Post" postData={data} />
        </Link>
        {(!truncateText && (
          <p className="my-2 text-justify text-break">{data.content}</p>
        )) || (
          <p className="my-2 text-justify text-break">
            {data.content.slice(0, data.content.length / 4)} ...
          </p>
        )}

        {linkMoreInfoStatus && (
          <Link className="text-primary" to={"/post/" + data.slug}>
            Más informacion aquí <i className="fad fa-external-link" />
          </Link>
        )}

        <p className="text-muted">Publicado: {data.created} </p>
      </div>
      <div className="meta-data">
        {user && (
          <ImageUser
            classes={"mr-3 image-account-post"}
            userData={user.data}
            showLink={true}
          />
        )}
      </div>
    </div>
  );
}

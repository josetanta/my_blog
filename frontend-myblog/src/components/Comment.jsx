import { Fragment, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { commentListAction } from "../actions/commentActions";
import { Link } from "react-router-dom";

import Fade from "react-reveal/Fade";
import { userDetailsAction } from "../actions/userActions";
import ImageUser from "./ImageUser";

export default function Comment(props) {
  const { loading, data, error } = useSelector((state) => state.commentList);
  const { user } = useSelector((state) => state.userDetails);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(commentListAction(props.paths.comments));
    dispatch(userDetailsAction(props.paths.user));
  }, [dispatch, props.paths.comments, props.paths.user]);

  return (
    <div>
      {loading ? (
        <div>Loading</div>
      ) : error ? (
        <div>Error</div>
      ) : (
        data.comments && (
          <Fragment>
            <Fade cascade right>
              <div>
                {data.comments.map((comment, index) => (
                  <div className="my-2" key={index}>
                    <ImageUser
                      image={user.data.image}
                      classes={"mr-3 comment-img-author"}
                    />
                    <div className="media-body">
                      <Link className="text-decoration-none" to={"#"}>
                        <b>{user.data.username}</b>
                      </Link>{" "}
                      <br />{" "}
                      <b className="small text-secondary">
                        Publicado:
                        <em className="small text-secondary">
                          {comment.data.created}
                        </em>
                      </b>
                      <div className="text-break text-justify">
                        {comment.data.content}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </Fade>
          </Fragment>
        )
      )}
    </div>
  );
}

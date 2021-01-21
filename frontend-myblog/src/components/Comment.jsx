import { Fragment, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { commentListWithPathAction } from "../actions/commentActions";

import Fade from "react-reveal/Fade";
import { userDetailsWithPathAction } from "../actions/userActions";
import ImageUser from "./ImageUser";

export default function Comment(props) {
  const { loading, data, error } = useSelector((state) => state.commentList);
  const { user } = useSelector((state) => state.userDetails);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(commentListWithPathAction(props.paths.comments));
    dispatch(userDetailsWithPathAction(props.paths.user));
  }, [dispatch, props.paths.comments, props.paths.user]);

  return (
    <>
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
                  <div key={index} className="my-4 media-body">
                    {user && (
                      <ImageUser
                        userData={user.data}
                        classes={"mr-3 comment-img-author"}
                        showLink={true}
                      />
                    )}
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
                ))}
              </div>
            </Fade>
          </Fragment>
        )
      )}
    </>
  );
}

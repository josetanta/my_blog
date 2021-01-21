import { Fragment, useEffect } from "react";

// Redux
import { useDispatch, useSelector } from "react-redux";
import { postDetailsAction } from "../actions/postActions";

// Components
import Comment from "../components/Comment";
import Post from "../components/Post";
import Fade from "react-reveal/Fade";

export default function PostDetailsView(props) {
  const slug = props.match.params.slug;
  const { loading, post, error } = useSelector((state) => state.postDetails);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(postDetailsAction({ slug }));
  }, [dispatch, slug]);

  return (
    <Fragment>
      <div className="row">
        {loading ? (
          <div className="alert alert-info">Cargando... 😀😊😊</div>
        ) : error ? (
          <div className="alert alert-danger">Sucedio algo mal... 😯😯</div>
        ) : (
          post && (
            <Fragment>
              <Fade left>
                <div className="col-md-7">
                  <Post post={{ data: post.data, paths: post.paths }} />
                </div>
              </Fade>
              <div className="col-md-5">
                <div className="ml-4">
                  <h4 className="text-info">Comentarios</h4>
                  <button className="btn text-secondary">
                    <i className="fal fa-comments" />
                  </button>
                </div>
                <div className="ml-4">
                  <div className="row my-3 py-2 pr-1">
                    <Comment paths={post.paths} />
                  </div>
                </div>
              </div>
            </Fragment>
          )
        )}
      </div>
    </Fragment>
  );
}

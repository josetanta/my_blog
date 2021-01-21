// Components
import Post from "../components/Post";

// React-Reveal
import Fade from "react-reveal/Fade";
import { Fragment } from "react";
import Page from "../components/Page";

export default function HomeView({ loading, error, data }) {
  return (
    <Fragment>
      {loading ? (
        <div className="alert alert-info">Cargando ... </div>
      ) : error ? (
        <div className="alert alert-danger">Error de Página</div>
      ) : (
        <Fade right cascade>
          <div>
            {data.posts &&
              data.posts.map((post, index) => (
                <div key={index}>
                  <Post post={post} linkMoreInfoStatus={true} truncateText />
                </div>
              ))}
          </div>
          <Page />
        </Fade>
      )}
    </Fragment>
  );
}

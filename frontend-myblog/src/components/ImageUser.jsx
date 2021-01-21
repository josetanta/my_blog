import { Link } from "react-router-dom";

export default function ImageUser({ userData, classes, alt, showLink }) {
  return (
    <div className="d-flex align-items-center">
      {userData && <img className={classes} src={userData.image} alt={alt} />}
      {showLink && (
        <Link className="text-decoration-none" to={"/profile/" + userData.slug}>
          <b>{userData.username}</b>
        </Link>
      )}
    </div>
  );
}

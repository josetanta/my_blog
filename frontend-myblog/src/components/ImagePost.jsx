export default function ImagePost({ postData, classes, alt }) {
  // + "post-img"
  return <img className={classes} src={postData.image} alt={alt} />;
}

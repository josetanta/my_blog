import * as typeAction from "../typeActions/postTypeActions";

export function postListReducer(state = { posts: [] }, action) {
  switch (action.type) {
    case typeAction.POSTS_LIST_REQUEST:
      return { loading: true };
    case typeAction.POSTS_LIST_SUCCESS:
      return { loading: false, posts: action.payload };
    case typeAction.POSTS_LIST_FAIL:
      return { loading: false, error: action.payload };
    default:
      return state;
  }
}

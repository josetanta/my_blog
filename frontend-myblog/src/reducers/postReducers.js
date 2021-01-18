import * as typeAction from "../typeActions/postTypeActions";

export function postListReducer(state = { data: {} }, action) {
  switch (action.type) {
    case typeAction.POSTS_LIST_REQUEST:
      return { loading: true };
    case typeAction.POSTS_LIST_SUCCESS:
      return {
        loading: false,
        data: { posts: action.payload.posts },
      };
    case typeAction.POSTS_LIST_FAIL:
      return { loading: false, error: action.payload };
    default:
      return state;
  }
}

export function postDetailsReducer(state = {}, action) {
  switch (action.type) {
    case typeAction.POST_DETAILS_REQUEST:
      return { loading: true };
    case typeAction.POST_DETAILS_SUCCESS:
      return { loading: false, post: action.payload.post };
    case typeAction.POST_DETAILS_FAIL:
      return { loading: false, error: action.payload };
    default:
      return state;
  }
}

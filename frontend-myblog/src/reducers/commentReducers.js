import * as typeAction from "../typeActions/commentTypeActions";

export function commentListReducer(state = { data: {} }, action) {
  switch (action.type) {
    case typeAction.COMMENT_LIST_POST_REQUEST:
      return { loading: true };

    case typeAction.COMMENT_LIST_POST_SUCCESS:
      return { loading: false, data: { comments: action.payload.comments } };

    case typeAction.COMMENT_LIST_POST_FAIL:
      return { loading: false, error: action.payload };

    default:
      return state;
  }
}

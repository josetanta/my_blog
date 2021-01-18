import * as typeAction from "../typeActions/userTypeActions";

export function userDetailsReducer(state = {}, action) {
  switch (action.type) {
    case typeAction.USER_DETAILS_REQUEST:
      return { loading: true };
    case typeAction.USER_DETAILS_SUCCESS:
      return { loading: false, user: action.payload.user };
    case typeAction.USER_DETAILS_FAIL:
      return { loading: false, error: action.payload };
    default:
      return state;
  }
}

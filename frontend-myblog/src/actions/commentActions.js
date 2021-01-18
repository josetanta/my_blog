import * as typeAction from "../typeActions/commentTypeActions";
import axios from "axios";

export const commentListAction = (path) => async (dispatch) => {
  try {
    dispatch({ type: typeAction.COMMENT_LIST_POST_REQUEST });
    const data = await (await axios.get(path)).data;
    dispatch({ type: typeAction.COMMENT_LIST_POST_SUCCESS, payload: data });
  } catch (error) {
    dispatch({
      type: typeAction.COMMENT_LIST_POST_FAIL,
      payload: error.message,
    });
  }
};

import * as typeAction from "../typeActions/postTypeActions";
import axios from "axios";

export const postListAction = () => async (dispatch) => {
  try {
    dispatch({ type: typeAction.POSTS_LIST_REQUEST });
    const data = await (await axios.get("/api/v1/posts")).data;
    dispatch({ type: typeAction.POSTS_LIST_SUCCESS, payload: data });
  } catch (error) {
    dispatch({ type: typeAction.POSTS_LIST_FAIL, payload: error.message });
  }
};

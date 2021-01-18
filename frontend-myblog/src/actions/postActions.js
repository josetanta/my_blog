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

export const postDetailsAction = (post) => async (dispatch) => {
  try {
    dispatch({ type: typeAction.POST_DETAILS_REQUEST });
    const slug = post.slug;
    if (slug) {
      const data = await (await axios.get("/api/v1/posts/" + slug)).data;
      dispatch({ type: typeAction.POST_DETAILS_SUCCESS, payload: data });
    } else {
      dispatch({
        type: typeAction.POST_DETAILS_FAIL,
        payload: { message: "Este post no existe" },
      });
    }
  } catch (error) {
    dispatch({ type: typeAction.POST_DETAILS_FAIL, payload: error.message });
  }
};

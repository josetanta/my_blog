import * as typeAction from "../typeActions/userTypeActions";
import axios from "axios";

export const userDetailsAction = (path) => async (dispatch) => {
  try {
    dispatch({ type: typeAction.USER_DETAILS_REQUEST });
    const data = await (await axios.get(path)).data;
    dispatch({ type: typeAction.USER_DETAILS_SUCCESS, payload: data });
  } catch (error) {
    dispatch({ type: typeAction.USER_DETAILS_FAIL, payload: error.message });
  }
};

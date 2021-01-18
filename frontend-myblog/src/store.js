import { applyMiddleware, combineReducers, compose, createStore } from "redux";
import thunk from "redux-thunk";

// Reducers
import * as postReducers from "./reducers/postReducers";
import * as userReducers from "./reducers/userReducers";
import * as commentReducers from "./reducers/commentReducers";

const initialState = {};

const reducers = combineReducers({
  postList: postReducers.postListReducer,
  postDetails: postReducers.postDetailsReducer,
  userDetails: userReducers.userDetailsReducer,
  commentList: commentReducers.commentListReducer,
});

const composeRedux = window["__REDUX_DEVTOOLS_EXTENSION_COMPOSE__"] || compose;

const store = createStore(
  reducers,
  initialState,
  composeRedux(applyMiddleware(thunk))
);

export default store;

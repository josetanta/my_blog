import { applyMiddleware, combineReducers, compose, createStore } from "redux";
import thunk from "redux-thunk";

import * as postReducers from "./reducers/postReducers";

const initialState = {};

const reducers = combineReducers({
  postList: postReducers.postListReducer,
});

const composeRedux = window["__REDUX_DEVTOOLS_EXTENSION_COMPOSE__"] || compose;

const store = createStore(
  reducers,
  initialState,
  composeRedux(applyMiddleware(thunk))
);

export default store;

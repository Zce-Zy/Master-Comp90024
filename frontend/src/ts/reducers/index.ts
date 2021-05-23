import { combineReducers } from "redux";
import { IMapState, mapReducer as map } from "./mapReducer";
import { IXHRState, xhrReducer as xhr } from "./xhrReducer";
import { ILoadingState, loadingReducer as loading } from "./loadingReducer";

export interface IState {
  map: IMapState;
  xhr: IXHRState;
  loading: ILoadingState;
}

export default combineReducers({ map, xhr, loading });

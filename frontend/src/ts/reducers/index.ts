import { combineReducers } from "redux";
import { IMapState, mapReducer as map } from "./mapReducer";
import { IXHRState, xhrReducer as xhr } from "./xhrReducer";

export interface IState {
  map: IMapState;
  xhr: IXHRState;
}

export default combineReducers({ map, xhr });

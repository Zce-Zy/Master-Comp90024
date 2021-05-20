import { INITIAL_CENTER, ZOOM_BOUNDARY } from "../constants/map";
import { IClickedInfo, ICoordinate } from "../interfaces/Map";
import { IAction } from "../interfaces/action";
import {
  UPDATE_MAP_CENTER_AND_ZOOM,
  UPDATE_LAST_CLICKED_INFO,
} from "../actions/map";

export interface IMapState {
  center: ICoordinate;
  zoom: number;
  lastClickedInfo: IClickedInfo | null;
}

const INIT_STATE: IMapState = {
  center: INITIAL_CENTER,
  zoom: ZOOM_BOUNDARY.min,
  lastClickedInfo: null,
};

export const mapReducer = (
  state: IMapState = INIT_STATE,
  action: IAction
): IMapState => {
  switch (action.type) {
    case UPDATE_MAP_CENTER_AND_ZOOM:
      return { ...state, ...action.payload };
    case UPDATE_LAST_CLICKED_INFO:
      return { ...state, lastClickedInfo: action.payload };
    default:
      return state;
  }
};

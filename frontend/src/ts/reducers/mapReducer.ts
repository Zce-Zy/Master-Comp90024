import { INITIAL_CENTER, ZOOM_BOUNDARY } from "../constants/map";
import { ICoordinate } from "../interfaces/Map";
import { IAction } from "../interfaces/action";
import { UPDATE_MAP_CENTER_AND_ZOOM } from "../actions/map";

export interface IMapState {
  center: ICoordinate;
  zoom: number;
  lastClickedInfo: any | null;
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
    default:
      return state;
  }
};

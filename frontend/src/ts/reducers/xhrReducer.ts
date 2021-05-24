import {
  CLEAR_LGA_DATA,
  LGA_DATA_RECEIVED,
  OVERVIEW_DATA_RECEIVED,
} from "../actions/actionTypes";
import { IAction } from "../interfaces/action";
import { IOverview } from "../interfaces/overview";

export interface IXHRState {
  tweetCount: number;
  overview: IOverview | null;
  lgaData: IOverview | null;
}

const INIT_STATE: IXHRState = {
  tweetCount: 0,
  overview: null,
  lgaData: null,
};

export function xhrReducer(state = INIT_STATE, action: IAction) {
  switch (action.type) {
    case OVERVIEW_DATA_RECEIVED:
      return { ...state, overview: action.payload };
    case LGA_DATA_RECEIVED:
      return { ...state, lgaData: action.payload };
    case CLEAR_LGA_DATA:
      return { ...state, lgaData: null };
    default:
      return state;
  }
}

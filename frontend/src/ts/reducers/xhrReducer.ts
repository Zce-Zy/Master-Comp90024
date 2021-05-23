import { OVERVIEW_DATA_RECEIVED } from "../actions/actionTypes";
import { IAction } from "../interfaces/action";
import { IOverview } from "../interfaces/overview";

export interface IXHRState {
  tweetCount: number;
  overview: IOverview | null;
}

const INIT_STATE: IXHRState = {
  tweetCount: 0,
  overview: null,
};

export function xhrReducer(state = INIT_STATE, action: IAction) {
  switch (action.type) {
    case OVERVIEW_DATA_RECEIVED:
      return { ...state, overview: action.payload };
    default:
      return state;
  }
}

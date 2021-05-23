import { IAction } from "../interfaces/action";
import { IOverview } from "../interfaces/overview";

export interface IXHRState {
  tweetCount: number;
  overview: IOverview | null;
}

const INIT_STATE: IXHRState = {
  tweetCount: 0,
  overview: {
    sentiment: {
      neutral: 26607,
      positive: 19401,
      negative: 7440,
    },
  },
};

export function xhrReducer(state = INIT_STATE, action: IAction) {
  switch (action.type) {
    default:
      return state;
  }
}

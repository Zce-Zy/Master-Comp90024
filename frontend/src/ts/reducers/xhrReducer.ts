import { IAction } from "../interfaces/action";

export interface IXHRState {
  tweetCount: number;
}

const INIT_STATE: IXHRState = {
  tweetCount: 0,
};

export function xhrReducer(state = INIT_STATE, action: IAction) {
  switch (action.type) {
    default:
      return state;
  }
}

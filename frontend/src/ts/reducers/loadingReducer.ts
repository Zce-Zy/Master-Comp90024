import { UPDATE_LOADING_STATUS } from "../actions/actionTypes";
import { IAction } from "../interfaces/action";

export interface ILoadingState {
  isLoading: boolean;
}

const LOADING_REDUCER_DEFAULT_VALUE: ILoadingState = {
  isLoading: false,
};

export function loadingReducer(
  state = LOADING_REDUCER_DEFAULT_VALUE,
  action: IAction
) {
  switch (action.type) {
    case UPDATE_LOADING_STATUS:
      return { ...state, ...action.payload };
    default:
      return state;
  }
}

import { UPDATE_LOADING_STATUS } from "./actionTypes";
import { IAction } from "../interfaces/action";

function updateLoadingStatus(isLoading = false): IAction<boolean> {
  return {
    type: UPDATE_LOADING_STATUS,
    payload: isLoading,
  };
}

export const startLoading = () => updateLoadingStatus(true);
export const stopLoading = () => updateLoadingStatus();

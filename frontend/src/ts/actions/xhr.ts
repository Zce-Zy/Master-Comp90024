import { startLoading, stopLoading } from "./loading";
import { API__GET_OVERALL_INFO } from "../constants/api";
import { Dispatch } from "redux";
import { OVERVIEW_DATA_RECEIVED } from "./actionTypes";
import { IOverview } from "../interfaces/overview";

export function getOverviewData() {
  return (dispatch: Dispatch) => {
    dispatch(startLoading());

    return fetch(API__GET_OVERALL_INFO)
      .then((res) => {
        if (res.ok) {
          return res.json();
        }

        throw res.statusText;
      })
      .then((overviewData: IOverview) => {
        console.log("overviewData =", overviewData);
        dispatch({ type: OVERVIEW_DATA_RECEIVED, payload: overviewData });
      })
      .finally(() => dispatch(stopLoading()));
  };
}

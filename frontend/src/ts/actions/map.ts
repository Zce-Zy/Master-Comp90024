import { IClickedInfo, ICoordinate, IMapInfo } from "../interfaces/Map";
import { IAction } from "../interfaces/action";
import { Dispatch } from "redux";
import {
  builtReverseGeocodingUrl,
  getCityAddressObject,
  getCityName,
  getStateShortName,
} from "../utils/googleMap";
import { getDataOfLGA } from "./xhr";

export const UPDATE_MAP_CENTER_AND_ZOOM: string = "UPDATE_MAP_CENTER_AND_ZOOM";
export const UPDATE_LAST_CLICKED_INFO: string = "UPDATE_LAST_CLICKED_INFO";

export function updateMapCenterAndZoom(
  center: ICoordinate,
  zoom: number
): IAction<IMapInfo> {
  return {
    type: UPDATE_MAP_CENTER_AND_ZOOM,
    payload: { center, zoom },
  };
}

export function updateLastClickedInfo(
  lastClickedInfo: IClickedInfo | null = null
): IAction<IClickedInfo | null> {
  return {
    type: UPDATE_LAST_CLICKED_INFO,
    payload: lastClickedInfo,
  };
}

export const reverseGeocoding =
  ({ lat, lng, x, y }: IClickedInfo) =>
  (dispatch: Dispatch) => {
    dispatch(updateLastClickedInfo());

    return fetch(builtReverseGeocodingUrl(lat, lng))
      .then((res) => {
        if (res.ok) {
          return res.json();
        }

        throw res.statusText;
      })
      .then((address) => {
        console.log("In reverseGeocoding, address =", address);
        console.log(
          "In reverseGeocoding, cityName =",
          getCityAddressObject(address)
        );
        dispatch(updateLastClickedInfo({ lat, lng, x, y, address }));

        const cityName = getCityName(address, false);
        if (address && getStateShortName(address) === "VIC") {
          getDataOfLGA(cityName)(dispatch);
        }
      });
  };

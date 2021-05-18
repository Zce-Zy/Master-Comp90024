import { ICoordinate, IMapInfo } from "../interfaces/Map";
import { IAction } from "../interfaces/action";

export const UPDATE_MAP_CENTER_AND_ZOOM: string = "UPDATE_MAP_CENTER_AND_ZOOM";

export function updateMapCenterAndZoom(
  center: ICoordinate,
  zoom: number
): IAction<IMapInfo> {
  return {
    type: UPDATE_MAP_CENTER_AND_ZOOM,
    payload: { center, zoom },
  };
}

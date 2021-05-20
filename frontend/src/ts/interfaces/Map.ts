export interface ICoordinate {
  lng: number;
  lat: number;
}

export interface IZoomBoundary {
  min: number;
  max: number;
}

export interface IMapInfo {
  center: ICoordinate;
  zoom: number;
}

export interface IClickedInfo extends ICoordinate {
  x: number;
  y: number;
  address?: any;
}

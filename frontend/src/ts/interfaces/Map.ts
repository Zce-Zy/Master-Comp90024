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

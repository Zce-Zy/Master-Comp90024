import { ICoordinate, IZoomBoundary } from "../interfaces/Map";

export const ZOOM_BOUNDARY: IZoomBoundary = { min: 7, max: 12 };
export const INITIAL_CENTER: ICoordinate = {
  lng: 145.3327648384119,
  lat: -36.45378603127134,
};

export const GEOJSON_URL: string =
  "https://elasticbeanstalk-ap-southeast-2-144912544139.s3-ap-southeast-2.amazonaws.com/vic_sa4.geojson";

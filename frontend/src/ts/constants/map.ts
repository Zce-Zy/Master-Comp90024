import { ICoordinate, IZoomBoundary } from "../interfaces/Map";

export const DEFAULT_ZOOM: number = 7;
export const ZOOM_BOUNDARY: IZoomBoundary = { min: DEFAULT_ZOOM, max: 14 };
export const INITIAL_CENTER: ICoordinate = {
  lng: 145.3327648384119,
  lat: -36.45378603127134,
};

export const GEOJSON_URL: string =
  "https://data.gov.au/geoserver/vic-local-government-areas-psma-administrative-boundaries/wfs?request=GetFeature&typeName=ckan_bdf92691_c6fe_42b9_a0e2_a4cd716fa811&outputFormat=json";
// "https://elasticbeanstalk-ap-southeast-2-144912544139.s3-ap-southeast-2.amazonaws.com/vic_sa4.geojson";

import React, { Component } from "react";
import GoogleMapReact from "google-map-react";
import { GOOGLE_MAP_API_KEY } from "../configurations/google";
import { connect } from "react-redux";
import { inspect } from "util";
import { Dispatch } from "redux";

import { ICoordinate } from "../interfaces/Map";
import { GEOJSON_URL, ZOOM_BOUNDARY } from "../constants/map";
import mapStyle from "../constants/mapStyle";
import { IState } from "../reducers";
import { updateMapCenterAndZoom } from "../actions/map";
import { capitalizeString } from "../utils/string";

interface IMapOwnProps {}

interface IMapStateProps {
  center: ICoordinate;
  zoom: number;
}

interface IMapDispatchProps {
  updateMapCenterAndZoom: (center: ICoordinate, zoom: number) => void;
}

interface IMapProps extends IMapOwnProps, IMapStateProps, IMapDispatchProps {}

class MapComponent extends Component<IMapProps> {
  private map: any;
  private maps: any;
  private dataLayer: any;

  constructor(props: IMapProps) {
    super(props);
  }

  handleMapApiLoad = (map: any, maps: any) => {
    this.map = map;
    this.maps = maps;
    this.initDataLayer();
    // this.setDataStyle();
  };

  initDataLayer() {
    console.log("this.map =", this.map);
    console.log("this.maps =", this.maps);

    if (this.maps) {
      this.dataLayer = new this.maps.Data({ map: this.map });
      this.dataLayer.loadGeoJson(GEOJSON_URL);
    }
  }

  // setDataStyle = () => {
  //   if (this.dataLayer) {
  //     this.dataLayer.setStyle((feature: any) => {
  //       const { minValue, maxValue, extractedMapData } = this.props;
  //       const name = capitalizeString(feature.getProperty("vic_lga__3"));

  //       // console.log("in setDataStyle, name =", name);
  //       let colors = gradient("#be9283", "#621b47", 7);

  //       const valueOfThisLGA = extractedMapData.get(name);
  //       // console.log("valueOfThisLGA =", valueOfThisLGA);

  //       const step = (maxValue - minValue) / 7;
  //       let i = 0;
  //       for (i = 0; i <= 6; i++) {
  //         if (
  //           valueOfThisLGA >= minValue + i * step &&
  //           valueOfThisLGA <= minValue + (i + 1) * step
  //         ) {
  //           break;
  //         }
  //       }

  //       // let fillColor = colors[i];

  //       let fillColor = valueOfThisLGA === undefined ? "#c7b79e" : colors[i];

  //       // console.log(
  //       //   `valueOfThisLGA =${valueOfThisLGA}, LGA = ${name}, color = ${fillColor} colors = ${colors}, i = ${i}`
  //       // );

  //       return {
  //         fillColor: fillColor,
  //         strokeWeight: 0.25,
  //         strokeColor: "#ffffff",
  //         zIndex: 0,
  //         fillOpacity: 0.7,
  //       };
  //     });
  //   }
  // };

  render() {
    const { center, zoom, updateMapCenterAndZoom } = this.props;
    return (
      <GoogleMapReact
        yesIWantToUseGoogleMapApiInternals
        bootstrapURLKeys={{ key: GOOGLE_MAP_API_KEY }}
        defaultCenter={center}
        defaultZoom={zoom}
        options={{
          gestureHandling: "greedy",
          zoomControl: true,
          fullscreenControl: false,
          maxZoom: ZOOM_BOUNDARY.max,
          minZoom: ZOOM_BOUNDARY.min,
          styles: mapStyle,
        }}
        onChange={({ zoom, center }) => {
          console.log(
            `onChange trigerred, zoom = ${zoom}, center = ${inspect(center)}`
          );
          updateMapCenterAndZoom(center, zoom);
        }}
        onClick={(value) => {
          console.log("onClick trigerred, value =", value);
          // this.getLocationInfo(value);
          // if (hideComparisonPanel) {
          //   hideComparisonPanel();
          // }
        }}
        onGoogleApiLoaded={({ map, maps }) => this.handleMapApiLoad(map, maps)}
      ></GoogleMapReact>
    );
  }
}

const mapStateToProps = (state: IState): IMapStateProps => {
  const { center, zoom } = state.map;

  return { center, zoom };
};

const mapDispatchToProps = (dispatch: Dispatch): IMapDispatchProps => {
  return {
    updateMapCenterAndZoom: (center, zoom) =>
      dispatch(updateMapCenterAndZoom(center, zoom)),
  };
};

const Map = connect(mapStateToProps, mapDispatchToProps)(MapComponent);

export { Map };

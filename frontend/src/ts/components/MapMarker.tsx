import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMapPin } from "@fortawesome/free-solid-svg-icons";

interface MapMarkerOwnProps {
  lat: number;
  lng: number;
}

interface MapMarkerProps extends MapMarkerOwnProps {}

export const MapMarker = (prop: MapMarkerProps) => {
  return (
    <FontAwesomeIcon
      icon={faMapPin}
      style={{
        color: "red",
        fontSize: "1rem",
      }}
    />
  );
};

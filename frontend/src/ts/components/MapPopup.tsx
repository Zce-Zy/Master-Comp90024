import React, { useState } from "react";
import { connect } from "react-redux";
import { Popover, Row, Col } from "antd";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMapPin } from "@fortawesome/free-solid-svg-icons";
import { IState } from "../reducers/index";
import { getCityName } from "../utils/googleMap";

interface IMapPopupOwnProps {}

interface IMapPopupStateProps {
  cityName: string;
  lastClickedInfo: any;
  mostRecentDate: any;
  data: any;
}

interface IMapPopupDispatchProps {}

interface IMapPopupProps
  extends IMapPopupOwnProps,
    IMapPopupStateProps,
    IMapPopupDispatchProps {}

const MapPopupComponent = ({
  cityName,
  lastClickedInfo,
  mostRecentDate,
  data,
}: IMapPopupProps) => {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <Popover
      visible={isVisible}
      placement={"bottom"}
      onVisibleChange={setIsVisible}
      title={
        <header>
          {cityName && (
            <span>
              {cityName} ""
              {` (${data || 0} Confirmed${
                mostRecentDate ? ` By ${mostRecentDate}` : ""
              })`}
            </span>
          )}
        </header>
      }
      content={
        <Row>
          <Col span={12}>
            <p>Hello world</p>
          </Col>
        </Row>
      }
    >
      <FontAwesomeIcon
        icon={faMapPin}
        style={{
          left: lastClickedInfo.x,
          top: lastClickedInfo.y,
          position: "absolute",
          color: "red",
        }}
      />
    </Popover>
  );
};

const mapStateToProps = (state: IState) => {
  const { lastClickedInfo } = state.map;

  let cityName = "";
  let cityShortName = "";

  if (lastClickedInfo && lastClickedInfo.address) {
    const address = lastClickedInfo.address;

    cityName = getCityName(address);
    cityShortName = getCityName(address, false);
  }

  return {
    cityName,
    lastClickedInfo,
  };
};

const MapPopup = connect(mapStateToProps)(MapPopupComponent);

export { MapPopup };

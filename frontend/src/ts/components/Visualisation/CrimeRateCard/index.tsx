import React, { useState } from "react";
import { connect } from "react-redux";
import { Card } from "antd";
import {
  CartesianGrid,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  LineChart as RechartLine,
} from "recharts";

import {
  getCityName,
  getStateName,
  getStateShortName,
} from "../../../utils/googleMap";
import { IState } from "../../../reducers";
import { ICrimeRate } from "../../../interfaces/overview";
import { DataTypeSelector } from "./DataTypeSelector";
import {
  CRIME_RATE_LABEL_DETAILS,
  TOTAL_COUNT_VALUE,
} from "../../../constants/crimeRates";
import { composeTitle } from "../../../utils/titleHelper";

interface ICrimeRateCardOwnProps {}

interface ICrimeRateCardStateProps {
  cityName: string;
  stateName: string;
  stateShortName: string;
  data: ICrimeRate[];
}

interface ICrimeRateCardProps
  extends ICrimeRateCardOwnProps,
    ICrimeRateCardStateProps {}

const CrimeRateCardComponent = ({
  cityName,
  stateName,
  stateShortName,
  data,
}: ICrimeRateCardProps) => {
  const title = composeTitle(
    "Crime Rates from 2011 to 2020",
    stateName,
    cityName,
    stateShortName
  );

  const [dataType, setDataType] = useState(TOTAL_COUNT_VALUE);

  return (
    <Card hoverable className="col-6 crime-rate-card" title={title}>
      <div className="visualisation-container">
        <DataTypeSelector handleChange={setDataType} />

        <ResponsiveContainer>
          <RechartLine
            data={data}
            width={730}
            height={220}
            margin={{ top: 5, right: 10, left: 10, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="year" />
            <YAxis type="number" />
            <Tooltip
              formatter={(value: string, name: string) => {
                return [value, CRIME_RATE_LABEL_DETAILS.get(dataType)!.label];
              }}
            />

            <Line
              type="monotone"
              dataKey={dataType}
              stroke={CRIME_RATE_LABEL_DETAILS.get(dataType)!.color}
              animationDuration={4000}
            />
          </RechartLine>
        </ResponsiveContainer>
      </div>
      {data.length === 0 && (
        <div className={"empty-data-cover"}>
          <h2>Oops, there are no data available...</h2>
        </div>
      )}
    </Card>
  );
};

const mapStateToProps = (state: IState): ICrimeRateCardStateProps => {
  const { lastClickedInfo } = state.map;

  let unsortedData = state.xhr?.lgaData?.crimeRates ?? [];
  if (!unsortedData.length) {
    unsortedData = state.xhr?.overview?.crimeRates ?? [];
  }

  let cityName = "";
  let stateName = "";
  let stateShortName = "";

  if (lastClickedInfo && lastClickedInfo.address) {
    const { address } = lastClickedInfo;
    cityName = getCityName(address);
    stateName = getStateName(address);
    stateShortName = getStateShortName(address);
  }

  const data = unsortedData.sort((a, b) => a.year - b.year);

  return { cityName, stateName, data, stateShortName };
};

const CrimeRateCard = connect(mapStateToProps)(CrimeRateCardComponent);

export { CrimeRateCard };

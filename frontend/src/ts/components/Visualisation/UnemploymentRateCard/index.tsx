import React, { useState } from "react";
import { connect } from "react-redux";
import { Card } from "antd";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Tooltip,
  XAxis,
  YAxis,
  Cell,
  ResponsiveContainer,
} from "recharts";

// import { COLOR_MAPPING } from "../../constants/covid19ColorMapping";
// import { STATE_MAPPING } from "../../constants/states";
import {
  IUnemploymentQuarterRate,
  IUnemploymentRate,
} from "../../../interfaces/overview";
import { IState } from "../../../reducers/index";
import { getCityName, getStateName } from "../../../utils/googleMap";
import { composeTitle } from "../../../utils/titleHelper";
import { YearSelector } from "./YearSelector";
import {
  AVERAGE_VALUE,
  BAR_COLOR_MAPPING,
} from "../../../constants/unemploymentRates";
import {
  getAverageUnemploymentQuarterRate,
  getQuarterLabel,
} from "../../../utils/unemploymentRates";

interface IUnemploymentRateCardOwnProps {}

interface IUnemploymentRateCardStateProps {
  cityName: string;
  stateName: string;
  data: IUnemploymentRate[];
}

interface IUnemploymentRateCardProps
  extends IUnemploymentRateCardOwnProps,
    IUnemploymentRateCardStateProps {}

const UnemploymentRateCardComponent = ({
  cityName,
  stateName,
  data,
}: IUnemploymentRateCardProps) => {
  const [selectedYear, setSelectedYear] = useState(AVERAGE_VALUE);
  const years: number[] = Array.from(new Set(data.map((rate) => rate.year)));

  let title =
    "Unemployment Rates Per Quarter" +
    (selectedYear === AVERAGE_VALUE
      ? " from 2011 - 2020"
      : ` in ${selectedYear}`);

  title = composeTitle(title, stateName, cityName);

  let dataOfYear: IUnemploymentQuarterRate[];

  if (selectedYear === AVERAGE_VALUE) {
    const aggregatedData = data.map((d) => d.data);

    dataOfYear = [
      getAverageUnemploymentQuarterRate(aggregatedData, 1),
      getAverageUnemploymentQuarterRate(aggregatedData, 2),
      getAverageUnemploymentQuarterRate(aggregatedData, 3),
      getAverageUnemploymentQuarterRate(aggregatedData, 4),
    ];
  } else {
    dataOfYear = data
      .filter((dataOfTheYear) => `${dataOfTheYear.year}` === selectedYear)
      .map((dataOfTheYear) => dataOfTheYear.data);
  }

  return (
    <Card hoverable className="col-6" title={title}>
      <div className="visualisation-container">
        <YearSelector years={years} handleChange={setSelectedYear} />
        <ResponsiveContainer>
          <BarChart
            width={700}
            height={250}
            data={dataOfYear}
            layout="vertical"
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis dataKey="quarter" type="category" width={80} />
            <Tooltip
              formatter={(value: number, name: string, props: any) => [
                value.toFixed(2),
                getQuarterLabel(props.payload.quarter),
              ]}
            />
            <Bar
              dataKey={"rate"}
              barSize={40}
              animationDuration={4000}
              name={"Number"}
            >
              {dataOfYear.map((barData, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={BAR_COLOR_MAPPING.get(barData.quarter)}
                />
              ))}
            </Bar>
          </BarChart>
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

const mapStateToProps = (state: IState) => {
  const { lastClickedInfo } = state.map;
  let unsortedData = state.xhr.overview?.unemploymentRates ?? [];

  let cityName = "";
  let stateName = "";

  if (lastClickedInfo && lastClickedInfo.address) {
    cityName = getCityName(lastClickedInfo.address);
    stateName = getStateName(lastClickedInfo.address);
  }

  const data = unsortedData.sort((a, b) => a.year - b.year);

  return { cityName, stateName, data };
};

const UnemploymentRateCard = connect(mapStateToProps)(
  UnemploymentRateCardComponent
);

export { UnemploymentRateCard };

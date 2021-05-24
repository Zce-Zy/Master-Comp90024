import React, { useState } from "react";
import { connect } from "react-redux";
import { Card } from "antd";
import {
  Pie,
  Cell,
  ResponsiveContainer,
  Sector,
  PieChart as RechartPie,
} from "recharts";

import { getCityName, getStateName } from "../../utils/googleMap";
import { capitalizeString } from "../../utils/string";
import { IState } from "../../reducers/index";
import { ISentiment } from "../../interfaces/overview";
import { composeTitle } from "../../utils/titleHelper";

interface ISentimentCardOwnProps {}

interface ISentimentCardStateProps {
  cityName: string;
  stateName: string;
  sentiment: ISentiment | null;
}

interface ISentimentCardProps
  extends ISentimentCardOwnProps,
    ISentimentCardStateProps {}

const SENTIMENT_COLOR_MAPPING = new Map([
  ["Negative", "#a52a2a"],
  ["Positive", "#11c299"],
  ["Neutral", "#ffbf00"],
]);

const renderActiveShape = (props: any) => {
  const RADIAN = Math.PI / 180;
  const {
    cx,
    cy,
    midAngle,
    innerRadius,
    outerRadius,
    startAngle,
    endAngle,
    fill,
    payload,
    percent,
  } = props;
  const sin = Math.sin(-RADIAN * midAngle);
  const cos = Math.cos(-RADIAN * midAngle);
  const sx = cx + (outerRadius + 10) * cos;
  const sy = cy + (outerRadius + 10) * sin;
  const mx = cx + (outerRadius + 30) * cos;
  const my = cy + (outerRadius + 30) * sin;
  const ex = mx + (cos >= 0 ? 1 : -1) * 22;
  const ey = my;
  const textAnchor = cos >= 0 ? "start" : "end";

  return (
    <g>
      <Sector
        cx={cx}
        cy={cy}
        innerRadius={innerRadius}
        outerRadius={outerRadius}
        startAngle={startAngle}
        endAngle={endAngle}
        fill={fill}
      />
      <Sector
        cx={cx}
        cy={cy}
        startAngle={startAngle}
        endAngle={endAngle}
        innerRadius={outerRadius + 6}
        outerRadius={outerRadius + 10}
        fill={fill}
      />
      <path
        d={`M${sx},${sy}L${mx},${my}L${ex},${ey}`}
        stroke={fill}
        fill="none"
      />
      <circle cx={ex} cy={ey} r={2} fill={fill} stroke="none" />
      <text
        x={ex + (cos >= 0 ? 1 : -1) * 12}
        y={ey}
        textAnchor={textAnchor}
        fill={fill}
      >
        {payload.name}
      </text>
      <text
        x={ex + (cos >= 0 ? 1 : -1) * 12}
        y={ey}
        dy={20}
        textAnchor={textAnchor}
        fill="#333"
      >
        {`Count: ${payload.value}`}
      </text>
      <text
        x={ex + (cos >= 0 ? 1 : -1) * 12}
        y={ey}
        dy={40}
        textAnchor={textAnchor}
        fill="#333"
      >
        {`${(percent * 100).toFixed(2)}%`}
      </text>
    </g>
  );
};

const SentimentCardComponent = ({
  cityName,
  stateName,
  sentiment,
}: ISentimentCardProps) => {
  // console.log("In SentimentCard, sentiment =", sentiment);

  const [activeIndex, setActiveIndex] = useState(0);
  const title = composeTitle("Tweet Sentiment Data", stateName, cityName);

  if (!sentiment || !Object.keys(sentiment).length) {
    return (
      <Card hoverable className="col-6 tweet-card xhr-data-card" title={title}>
        <div className={"empty-data-cover"}>
          <h2>Oops, there are no Tweet sentiment data available...</h2>
        </div>
      </Card>
    );
  }

  const data = [];
  let sum = 0;
  for (let type in sentiment) {
    const name = capitalizeString(type);
    console.log(`name = ${name}`);
    if (SENTIMENT_COLOR_MAPPING.has(name)) {
      const currentCount = sentiment[type];
      data.push({ name, value: currentCount });
      sum += currentCount;
    }
  }

  return (
    <Card hoverable className="col-6 tweet-card xhr-data-card" title={title}>
      <div className={"data-presentation"}>
        <p>
          <span>
            <b>Number of tweets analysed: </b>
          </span>
          {sum}
        </p>
      </div>
      <ResponsiveContainer height={"100%"} width={"70%"}>
        <RechartPie width={400} height={150} margin={{ left: 50, right: 50 }}>
          <Pie
            data={data}
            dataKey="value"
            startAngle={90}
            endAngle={-270}
            outerRadius={100}
            activeIndex={activeIndex}
            activeShape={renderActiveShape}
            isAnimationActive={false}
            onMouseEnter={(_: any, index: number) => setActiveIndex(index)}
          >
            {data.map((entry, index) => (
              <Cell
                key={`slice-${index}`}
                fill={entry ? SENTIMENT_COLOR_MAPPING.get(entry.name) : ""}
              />
            ))}
          </Pie>
        </RechartPie>
      </ResponsiveContainer>
      {!Object.keys(sentiment).length && (
        <div className={"empty-data-cover"}>
          <h2>Oops, there are no Tweet sentiment data available...</h2>
        </div>
      )}
    </Card>
  );
};

const mapStateToProps = (state: IState) => {
  let sentiment = state.xhr?.lgaData?.sentiment ?? null;
  if (!sentiment) {
    sentiment = state.xhr?.overview?.sentiment ?? null;
  }

  const { lastClickedInfo } = state.map;

  let cityName = "";
  let stateName = "";

  if (lastClickedInfo && lastClickedInfo.address) {
    cityName = getCityName(lastClickedInfo.address);
    stateName = getStateName(lastClickedInfo.address);
  }

  return { sentiment, cityName, stateName };
};

const SentimentCard = connect(mapStateToProps)(SentimentCardComponent);

export { SentimentCard };

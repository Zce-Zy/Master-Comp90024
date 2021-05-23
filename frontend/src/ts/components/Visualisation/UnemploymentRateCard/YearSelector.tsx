import React from "react";
import { Select } from "antd";
import {
  CRIME_RATE_LABEL_DETAILS,
  RATE_PER_100000,
  TOTAL_COUNT_VALUE,
} from "../../../constants/crimeRates";
import { connect } from "react-redux";
import { IState } from "../../../reducers/index";
import { Dispatch } from "redux";
import {
  AVERAGE_LABEL,
  AVERAGE_VALUE,
} from "../../../constants/unemploymentRates";
const { Option } = Select;

interface IYearSelectorProps {
  years: number[];
  handleChange: (value: string) => void;
}

const YearSelector = ({ years, handleChange }: IYearSelectorProps) => {
  const descendingYears = years.sort((a, b) => b - a);
  return (
    <div className="visualisation-selector">
      <span>Year: </span>
      <Select
        defaultValue={AVERAGE_VALUE}
        style={{ width: 250 }}
        onChange={handleChange}
      >
        <Option value={AVERAGE_VALUE}>{AVERAGE_LABEL}</Option>
        {descendingYears.map((year) => (
          <Option key={year} value={`${year}`}>
            {year}
          </Option>
        ))}
      </Select>
    </div>
  );
};

export { YearSelector };

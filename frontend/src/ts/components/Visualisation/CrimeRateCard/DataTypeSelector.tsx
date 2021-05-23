import React from "react";
import { Select } from "antd";
import {
  CRIME_RATE_LABEL_DETAILS,
  RATE_PER_100000,
  TOTAL_COUNT_VALUE,
} from "../../../constants/crimeRates";
const { Option } = Select;

interface IDataTypeSelectorProps {
  handleChange: (value: string) => void;
}

export const DataTypeSelector = ({ handleChange }: IDataTypeSelectorProps) => {
  return (
    <div className="visualisation-selector">
      <span>Data Type: </span>
      <Select
        defaultValue={TOTAL_COUNT_VALUE}
        style={{ width: 250 }}
        onChange={handleChange}
      >
        <Option value={TOTAL_COUNT_VALUE}>
          {CRIME_RATE_LABEL_DETAILS.get(TOTAL_COUNT_VALUE)!.label}
        </Option>
        <Option value={RATE_PER_100000}>
          {CRIME_RATE_LABEL_DETAILS.get(RATE_PER_100000)!.label}
        </Option>
      </Select>
    </div>
  );
};

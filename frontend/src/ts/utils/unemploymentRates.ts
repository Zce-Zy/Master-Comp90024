import { BAR_LABEL_MAPPING } from "../constants/unemploymentRates";
import { IUnemploymentQuarterRate } from "../interfaces/overview";

export const getQuarterLabel = (quarter: number): string => {
  const season: string = BAR_LABEL_MAPPING.get(quarter)!;
  switch (quarter) {
    case 1:
      return `1st Quarter (${season})`;
    case 2:
      return `2nd Quarter (${season})`;
    case 2:
      return `3rd Quarter (${season})`;
    default:
      return `4th Quarter (${season})`;
  }
};

export const getQuarterAverageRate = (
  data: IUnemploymentQuarterRate[],
  quarter: number
): number => {
  const rates = data.filter((d) => d.quarter === quarter).map((d) => d.rate);
  const sum = rates.reduce((a, b) => a + b, 0);
  const average = sum / rates.length || 0;
  return average;
};

export const getAverageUnemploymentQuarterRate = (
  data: IUnemploymentQuarterRate[],
  quarter: number
): IUnemploymentQuarterRate => {
  const average = getQuarterAverageRate(data, quarter);
  return { quarter, rate: average };
};

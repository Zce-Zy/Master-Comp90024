import { ILabelDetails } from "../interfaces/visualisation";

export const TOTAL_COUNT_VALUE: string = "totalCount";
export const RATE_PER_100000: string = "ratePer100000population";

export const CRIME_RATE_LABEL_DETAILS = new Map<string, ILabelDetails>([
  [TOTAL_COUNT_VALUE, { label: "Total Count", color: "#318ce7" }],
  [RATE_PER_100000, { label: "Rate Per 100000 Population", color: "#008000" }],
]);

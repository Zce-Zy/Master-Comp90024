export interface IOverview {
  sentiment: ISentiment;
}

export interface ISentiment {
  [key: string]: number;
  positive: number;
  negative: number;
  neutral: number;
}

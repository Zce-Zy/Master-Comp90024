export interface IOverview {
  sentiment: ISentiment;
  crimeRates: ICrimeRate[];
}

export interface ISentiment {
  [key: string]: number;
  positive: number;
  negative: number;
  neutral: number;
}

export interface ICrimeRate {
  [key: string]: number;
  year: number;
  totalCount: number;
  ratePer100000population: number;
}

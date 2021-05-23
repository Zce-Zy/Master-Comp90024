export interface IOverview {
  sentiment: ISentiment;
  crimeRates: ICrimeRate[];
  unemploymentRates: IUnemploymentRate[];
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

export interface IUnemploymentQuarterRate {
  quarter: number;
  rate: number;
}

export interface IUnemploymentRate {
  [key: string]: any;
  year: number;
  data: IUnemploymentQuarterRate;
}

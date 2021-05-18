import { capitalizeString } from "./string";
var moment = require("moment");

export function extractStartAndEndDateFromArray(
  datesRange: any,
  exportString = false
): [string | null, string | null] {
  try {
    const startDate: string | null =
      datesRange.length === 2
        ? exportString
          ? datesRange[0].format("YYYY-MM-DD")
          : new Date(datesRange[0].format("YYYY-MM-DD"))
        : null;
    const endDate: string | null =
      datesRange.length === 2
        ? exportString
          ? datesRange[1].format("YYYY-MM-DD")
          : new Date(datesRange[1].format("YYYY-MM-DD"))
        : null;
    return [startDate, endDate];
  } catch {
    return [null, null];
  }
}

function getMostRecentDateObjectFromArray(
  datesStringArray: string[],
  datesRange: any
) {
  const [startDate, endDate] = extractStartAndEndDateFromArray(datesRange);
  
  // todo: work on this.
  //   const mostRecentDateObject = new Date(
  //     Math.max.apply(
  //       null,
  //       datesStringArray
  //         .map((dateString) => new Date(dateString))
  //         .filter(
  //           (dateObj) =>
  //             (startDate === null || dateObj >= new Date(startDate)) &&
  //             (endDate === null || dateObj <= new Date(endDate))
  //         )
  //     )
  //   );

  const mostRecentDateObject = Date.now;

  return mostRecentDateObject;
}

export function extractDataByTypeFromOverview(
  overviewData: any,
  targetState = "",
  datesRange = [],
  absoluteData = true,
  skipTested = true
) {
  const dataIndex = absoluteData ? 0 : 1;
  const extractedMapData = new Map();

  const mostRecentDateObject = getMostRecentDateObjectFromArray(
    Object.keys(overviewData),
    datesRange
  );

  const mostRecentDate = mostRecentDateObject
    ? moment(mostRecentDateObject.toString()).format("YYYY-MM-DD")
    : "";

  if (mostRecentDate) {
    for (let state in overviewData[mostRecentDate]) {
      if (targetState === "" || targetState === state) {
        for (let dataType in overviewData[mostRecentDate][state]) {
          if (skipTested && dataType === "Tested") {
            continue;
          }

          let dataOfTheType = 0;
          if (extractedMapData.has(dataType)) {
            dataOfTheType = extractedMapData.get(dataType);
          }

          if (dataType === "Tested") {
            dataOfTheType += overviewData[mostRecentDate][state][dataType];
          } else {
            dataOfTheType +=
              overviewData[mostRecentDate][state][dataType][dataIndex];
          }

          extractedMapData.set(dataType, dataOfTheType);
        }
      }
    }
  }

  const aggregatedData: any[] = [];
  extractedMapData.forEach((value, name) =>
    aggregatedData.push({ value, name })
  );

  // console.log("aggregatedData", aggregatedData);

  return [aggregatedData, mostRecentDate];
}

export function extractAllDataByDateFromOverview(
  overviewData: any,
  targetState = "",
  datesRange = [],
  absoluteData = true,
  skipTested = true
) {
  const dataIndex = absoluteData ? 0 : 1;
  let flattenData: any[] = [];

  const [startDate, endDate] = extractStartAndEndDateFromArray(datesRange);

  for (let date in overviewData) {
    const dateObj = new Date(date);
    if (startDate && dateObj < new Date(startDate)) {
      continue;
    }
    if (endDate && dateObj > new Date(endDate)) {
      continue;
    }

    for (let state in overviewData[date]) {
      if (targetState === "" || targetState === state) {
        for (let type in overviewData[date][state]) {
          if (skipTested && type === "Tested") {
            continue;
          }

          const recordedObject = flattenData.find(
            (recordedData) => recordedData.date === date
          );

          const unchangedRecords = flattenData.filter(
            (recordedData) => recordedData.date !== date
          );

          let number = recordedObject ? recordedObject[type] || 0 : 0;
          if (type === "Tested") {
            number += overviewData[date][state][type];
          } else {
            number += overviewData[date][state][type][dataIndex];
          }

          flattenData = [
            ...unchangedRecords,
            { ...recordedObject, date, [type]: number },
          ];
        }
      }
    }
  }

  // console.log("flattenData =", flattenData);

  return flattenData;
}

export function extractMostRecentDataOfStateByCategory(
  overviewData: any,
  targetingCategory: any,
  absoluteData = true,
  datesRange = []
) {
  const dataIndex = absoluteData ? 0 : 1;
  const extractedMapData = new Map();

  const mostRecentDateObject = getMostRecentDateObjectFromArray(
    Object.keys(overviewData),
    datesRange
  );

  const mostRecentDate = mostRecentDateObject
    ? moment(mostRecentDateObject.toString()).format("YYYY-MM-DD")
    : "";

  if (mostRecentDate) {
    for (let state in overviewData[mostRecentDate]) {
      for (let dataCategory in overviewData[mostRecentDate][state]) {
        if (dataCategory !== targetingCategory) {
          continue;
        }

        let dataOfTheState = 0;
        if (extractedMapData.has(state)) {
          dataOfTheState = extractedMapData.get(state);
        }

        if (dataCategory === "Tested") {
          dataOfTheState += overviewData[mostRecentDate][state][dataCategory];
        } else {
          dataOfTheState +=
            overviewData[mostRecentDate][state][dataCategory][dataIndex];
        }

        extractedMapData.set(state, dataOfTheState);
      }
    }
  }

  const aggregatedData: any[] = [];
  extractedMapData.forEach((value, name) =>
    aggregatedData.push({ value, name })
  );

  return [aggregatedData, mostRecentDate];
}

export function extractMostRecentDataOfVicLGA(
  vicOverviewData: any,
  absoluteData = true,
  datesRange = []
) {
  const dataIndex = absoluteData ? 0 : 1;
  const extractedMapData = new Map();

  const mostRecentDateObject = getMostRecentDateObjectFromArray(
    Object.keys(vicOverviewData),
    datesRange
  );

  let minValue = 0;
  let maxValue = 0;

  const mostRecentDate = mostRecentDateObject
    ? moment(mostRecentDateObject.toString()).format("YYYY-MM-DD")
    : "";

  if (mostRecentDate) {
    for (let lga in vicOverviewData[mostRecentDate]) {
      const data = vicOverviewData[mostRecentDate][lga][dataIndex];

      minValue = Math.min(data, minValue);
      maxValue = Math.max(data, maxValue);

      extractedMapData.set(capitalizeString(lga), data);
    }
  }

  // console.log(
  //   "In extractMostRecentDataOfVicLGA, extractedMapData =",
  //   extractedMapData
  // );
  // console.log("In extractMostRecentDataOfVicLGA, minValue =", minValue);
  // console.log("In extractMostRecentDataOfVicLGA, maxValue =", maxValue);

  return [extractedMapData, mostRecentDate, maxValue, minValue];
}

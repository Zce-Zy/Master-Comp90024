export const composeTitle = (
  title: string,
  state: string,
  city: string,
  stateShortName: string
): string => {
  if (
    city &&
    state &&
    stateShortName &&
    stateShortName.toUpperCase() === "VIC"
  ) {
    title = `${title} - ${city}, ${state}`;
  } else {
    title = `${title} - Victoria`;
  }

  return title;
};

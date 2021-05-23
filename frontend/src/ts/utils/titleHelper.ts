export const composeTitle = (
  title: string,
  state: string,
  city: string
): string => {
  if (city && state) {
    title = `${title} - ${city}, ${state}`;
  }

  return title;
};

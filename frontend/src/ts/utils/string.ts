export const capitalizeString = (targetingString: string): string => {
  return targetingString
    .split(" ")
    .map(
      (string) => string.charAt(0).toUpperCase() + string.slice(1).toLowerCase()
    )
    .join(" ");
};

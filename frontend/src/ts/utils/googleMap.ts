import {
  API__GOOGLE_REVERSE_GEOCODING_FIRST_HALF,
  API__GOOGLE_REVERSE_GEOCODING_SECOND_HALF,
} from "../constants/api";
import { GOOGLE_MAP_API_KEY } from "../configurations/google";
import { inspect } from "util";

export function builtReverseGeocodingUrl(lat: number, lng: number): string {
  return `${API__GOOGLE_REVERSE_GEOCODING_FIRST_HALF}${lat},${lng}${API__GOOGLE_REVERSE_GEOCODING_SECOND_HALF}${GOOGLE_MAP_API_KEY}`;
}

export function getFormattedAddress(address: any) {
  console.log(`In getFormattedAddress, address = ${inspect(address)}`);

  try {
    return address.results[0].formatted_address;
  } catch {
    return "";
  }
}

function getAddressWithType(address: any, targetType: string) {
  console.log(
    `In getAddressWithType, address = ${inspect(
      address
    )}, targetType = ${targetType}`
  );

  try {
    return address.results.find((result: any) =>
      result.types.find((type: any) => type === targetType)
    );
  } catch {
    return null;
  }
}

export function getCityAddressObject(address: any) {
  return getAddressWithType(address, "administrative_area_level_2");
}

export function getCityName(address: any, getLongName = true) {
  const cityAddressObject = getCityAddressObject(address);
  if (cityAddressObject) {
    const components = cityAddressObject.address_components[0];

    return getLongName ? components.long_name : components.short_name;
  }

  return "";
}

export function getStateAddressObject(address: any) {
  return getAddressWithType(address, "administrative_area_level_1");
}

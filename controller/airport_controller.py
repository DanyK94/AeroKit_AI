from fastapi import APIRouter, HTTPException
from services.airport_service import getAirportInformation, getWeatherReport, getListAirportByKeyword
from dataclasses import asdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

#GET /airport/{icao_code} - info completo aeroporto (nome, città, paese, coordinate, runway, elevation)
@router.get("/airport/{icao_code}")
def getAirportInfo(icao_code: str):
    logger.info(f"Fetching airport info for {icao_code}")
    data = getAirportInformation(icao_code)
    if not data:
        logger.error(f"No Data for {icao_code}")
        raise HTTPException(status_code=404, detail="Airport not found")
    return asdict(data)


@router.get("/airport/{icao_code}/weather")
def getAiportWeather(icao_code : str):
    logger.info(f"Fetching weather info for {icao_code}")
    data = getWeatherReport(icao_code)
    if not data:
        logger.error(f"No Data for {icao_code}")
        raise HTTPException(status_code=404, detail="Weather not found")
    return data

#GET /airports/search?query={term} - lista aeroporti che matchano il search term
@router.get("/airports/search")
def getAirportsByKey(query : str):
    logger.info(f"Fetching airports list for key {query}")
    data = getListAirportByKeyword(query)
    if not data:
        logger.error(f"No Data for {query}")
        raise HTTPException(status_code=404, detail="Weather not found")
    return data

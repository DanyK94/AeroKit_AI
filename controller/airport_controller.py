from fastapi import APIRouter
from services.airport_service import getAirportInformation, getWeatherReport, getListAirportByKeyword
from dataclasses import asdict

router = APIRouter()

#GET /airport/{icao_code} - info completo aeroporto (nome, città, paese, coordinate, runway, elevation)
@router.get("/airport/{icao_code}")
def getAirportInfo(icao_code: str):
    return asdict(getAirportInformation(icao_code))


@router.get("/airport/{icao_code}/weather")
def getAiportWeather(icao_code : str):
    return getWeatherReport(icao_code)

#GET /airports/search?query={term} - lista aeroporti che matchano il search term
@router.get("/airports/search")
def getAirportsByKey(query : str):
    return getListAirportByKeyword(query)


#GET /airport/{icao_code}/flights - voli in arrivo/partenza dall'aeroporto (se disponibile via API) [NON DISPONIBILE VIA API]


#GET /health (opzionale ma consigliato) ??

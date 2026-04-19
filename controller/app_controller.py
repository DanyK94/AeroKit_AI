from fastapi import APIRouter
import time

router = APIRouter()

start_timte = time.time()

@router.get("/health")
def health_check():
    uptime = int(time.time() - start_timte)  
    avwx_status = check_avwx()
    airlabs_status = check_airlabs()
    if avwx_status == "connected" and  airlabs_status == "connected":
        status = "healthy"
    else:
        status = "degraded"

    return {
        "status": status,
        "version": "a1",
        "uptime_seconds": uptime,
        "dependencies": {
            "avwx_api": avwx_status,
            "airlabs_api": airlabs_status
        }
    } # 

#MOCK CHECK APIs
def check_avwx():
    return "connected"

def check_airlabs():
    return "connected"
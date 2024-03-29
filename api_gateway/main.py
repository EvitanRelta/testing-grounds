from fastapi import FastAPI, HTTPException, Request, WebSocket
import httpx
import json
from fastapi.middleware.cors import CORSMiddleware

from utils.api_gateway_util import check_permission, map_path_microservice_url, connect_matching_service_websocket, attach_cookie, delete_cookie

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        # Receive message from client
        message = await websocket.receive_text()

        request =  json.loads(message)
        service = request["service"]

        # Send message to microservice
        if service == "matching-service":
            connect_matching_service_websocket(websocket, request)
        else:
            raise HTTPException(status_code=400, detail=f"Invalid service requested: {service}")

    except HTTPException as http_exc:
        await websocket.send_text(http_exc.detail)

async def route_request(method: str, path: str, request: Request):
    # Determine the microservice URL based on the path
    service, microservice_url = map_path_microservice_url(path)

    if not service:
        raise HTTPException(status_code=404, detail="Endpoint not found")

    cookies = request.cookies
    session_id = cookies.get('session_id')

    await check_permission(session_id, path, method)

    data = await request.body()

    # Forward the request to the microservice
    async with httpx.AsyncClient() as client:
        if method == "GET":
            if service == "sessions":
                path += f"/{session_id}"
            response = await client.get(f"{microservice_url}{path}")
        elif method == "POST":
            response = await client.post(f"{microservice_url}{path}", data=data)
        elif method == "PUT":
            response = await client.put(f"{microservice_url}{path}", data=data)
        elif method == "DELETE":
             if service == "sessions":
                path += f"/{session_id}"
             response = await client.delete(f"{microservice_url}{path}")

        return response

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def handle_request(request: Request):
    path = request.url.path
    method = request.method

    response = await route_request(method, path, request)
    response = response.json()

    if 'status_code' in response: # status code will not be there if there is no error
        raise HTTPException(status_code=response['status_code'], detail=response['message'])
    if path == "/sessions" and method == "POST":
        return attach_cookie(response)
    if path == "/sessions" and method == "DELETE":
        return delete_cookie(response)

    return response


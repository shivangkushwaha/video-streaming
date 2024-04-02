from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import os

app = FastAPI()
current_working_directory = os.getcwd()

VIDEO_FILE_PATH = current_working_directory+'\example.mp4'
print('VIDEO_FILE_PATH',VIDEO_FILE_PATH)
def stream_video(video_path: str):
    with open(video_path, 'rb') as video_file:
        while chunk := video_file.read(1024 * 1024):  # Read 1MB at a time
            yield chunk

@app.get("/video")
def video():
    return StreamingResponse(stream_video(VIDEO_FILE_PATH), media_type="video/mp4")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

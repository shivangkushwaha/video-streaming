from fastapi import FastAPI, File, UploadFile, HTTPException
import boto3
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, String

# DATABASE_URL = "sqlite:///./test.db"
# database = Database(DATABASE_URL)
# metadata = MetaData()

# files = Table(
#     "files",
#     metadata,
#     Column("filename", String, primary_key=True),
#     Column("url", String),
# )

# engine = create_engine(DATABASE_URL)
# metadata.create_all(engine)

app = FastAPI(
        title="My Awesome API",
        description="This is a very fancy project for the user login and video streaming.",
        version="0.0.1",
)

s3_client = boto3.client('s3', aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')

# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # Validate MIME type
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a video file.")
    
    # You can also check the file size here if necessary, but it's a bit more complex as you need to read the file.
    
    try:
        s3_client.upload_fileobj(file.file, "your-bucket-name", file.filename)
        file_url = f"https://{s3_client.meta.endpoint_url}/your-bucket-name/{file.filename}"
        # query = files.insert().values(filename=file.filename, url=file_url)
        # await database.execute(query)
        return {"message": f"Successfully uploaded {file.filename} to S3 and saved the location in the database."}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

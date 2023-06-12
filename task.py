#!/usr/bin/python


from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
import platform
import html as safe
from pathlib import Path
import tempfile
import tarfile
app = FastAPI()

@app.get("/") 
async def root():
return {"message": "Hello from Snyk Hunter Team"}

# Get Location of Temporary folder in the file system
# If the file system is not one of: Windows,Linux or Darwin, show an error

def get_tmp_path():
	system = platform.system() 
	if system == "Windows":
		return "C:\\Temp\\unpack" 
	elif system == "Linux":
		return "/tmp/unpack/" 
	elif system == "Darwin":
		return "/tmp/unpack/" 
	else:
		raise NotImplementedError(f"Unsupported system: {system}") 

# Create a new temporary file, with the same name as the archive, extract all the contents of the archive and read them
def process_file(filename):
	with tempfile.NamedTemporaryFile(delete=True) as tmpfile:
		tmpfile.write(filename.read())
		tmpfile.seek(0)
		with tarfile.open(tmpfile.name, "r:gz") as untar:
			untar.extractall(path=get_tmp_path()) 
		untar.close()		

@app.get("/hello/{name}")
async def hello_name(name: str):
	escaped_name = safe.escape(name)
	return {"message": f"Hello, {escaped_name}!"}


# Upload feature: We can upload only tar.gz files. If the file is accepted, then it is processed

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
	ext = file.filename.split(".")[-1]	

	if ext.lower() != "gz":
		return {"filename": file.filename, "message": "File must be a Tar GZ file"} 
	else:
		process_file(file.file)
		return {"filename": file.filename, "message": "File uploaded and processed"}

@app.delete("/delete")
async def delete_file(file_path: str):
	path = Path(file_path) #todo
	return {"message": f"{file_path} deleted successfully."}


if __name__ == "__main__":
uvicorn.run(app, host="127.0.0.1", port=8000,reload=False)



#1) Explain in a brief paragraph what the code snippet is doing?
#2) What type of vulnerability is occurring in the code snippet?
#3) How can this vulnerability be exploited and what is its impact on a target system?
#4) Explain how user input from a user (source) is flowing into the dangerous function(sink) resulting in the vulnerability. Whenever possible, include the method/function name and a short description of what is taking place, how data is flowing from one function to another, whether tainted data is being manipulated, checks that are taking place etc. Whenever possible add code snippets to the relevant answer along with a brief explanation of what that code snippet is doing.
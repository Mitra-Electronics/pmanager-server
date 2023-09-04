FROM python:3.10
#It creates a working directory(app) for the Docker image and container
WORKDIR /
#It will copy all files and the source code from the host `fast-api` folder to the `app` container working directory
COPY . .
#It will install the framework and the dependencies in the `requirements.txt` file.
RUN pip3 install --upgrade pip poetry
RUN python3 -m poetry install
RUN python3 -m poetry add uvicorn[standard]
#It will expose the FastAPI application on port `8000` inside the container
EXPOSE 8000
#It is the command that will start and run the FastAPI application container
CMD ["python3", "-m","poetry", "run","uvicorn", "src.main:app", "--host", "0.0.0.0","--port","80"]
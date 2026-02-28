FROM python:3.11-slim
WORKDIR /app
COPY src/api .
RUN pip install -r requirements.txt
COPY models/*.pkl models/
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
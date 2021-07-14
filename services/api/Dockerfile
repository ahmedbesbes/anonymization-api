FROM python:3.7

RUN pip install fastapi uvicorn spacy

COPY . /api/api

ENV PYTHONPATH=/api
WORKDIR /api

EXPOSE 5000

ENTRYPOINT ["uvicorn"]
CMD ["api.main:app", "--host", "0.0.0.0:5000"]
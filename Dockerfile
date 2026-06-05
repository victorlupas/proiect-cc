#imagine oficiala Pyhton
FROM python:3.11-slim

#directorul de lucru in container
WORKDIR /app

#dependintele instalate in container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#se copiaza restul de cod sursa
COPY . .

#portul pe care va rula aplicatia
EXPOSE 8080

#se ruleaza aplicatia folosind gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]


# Use an official Python image
FROM python:3.9-slim

WORKDIR /final_project

RUN apt-get update && apt-get install -y sqlite3 && apt-get clean
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["sh", "-c", \
    "sqlite3 /final_project/addresses_list/addresses.db < \
    /final_project/addresses_list/addresses_db_cmd.sql && \
    python /final_project/init_db.py && \
    streamlit run /final_project/__main__.py"]

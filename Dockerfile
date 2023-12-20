FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
	build-essential \
	curl \
	software-properties-common \
	git \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE $PORT
# expose port used by trulens
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:$PORT/_stcore/health

# Use the shell form of ENTRYPOINT to use the environment variable
ENTRYPOINT streamlit run chatbot.py --server.port=$PORT --server.address=0.0.0.0 --browser.gatherUsageStats=False

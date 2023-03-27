FROM python:3.10.10-bullseye

WORKDIR /app
ADD src/ .
ADD requirements.txt .
RUN pip install -r requirements.txt

ENV OPENAI_API_KEY unknown
ENV DISCORD_BOT_TOKEN unknown
ENV GUILD_ID unknown

CMD ["python", "main.py"]

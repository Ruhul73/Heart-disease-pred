FROM python:3.11-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system deps needed for tkinter and building wheels
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
     && apt-get install -y --no-install-recommends \
         ca-certificates wget git \
         python3-tk tk-dev tcl-dev libx11-6 libxext6 libxrender1 \
         build-essential gfortran libatlas-base-dev libopenblas-dev liblapack-dev \
         libffi-dev libssl-dev python3-dev \
     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt ./
# Upgrade pip/setuptools/wheel and prefer binary wheels when installing heavy packages
ENV PIP_NO_CACHE_DIR=1
RUN pip install --upgrade pip setuptools wheel

# Install core binary packages first with --prefer-binary to avoid compilation
RUN pip install --prefer-binary numpy pandas scikit-learn

# Install remaining requirements (if any)
RUN pip install -r requirements.txt || pip install --prefer-binary -r requirements.txt

# Copy app
COPY . .

# Use python as ENTRYPOINT so users can choose to run GUI or CLI:
# e.g. (default) `docker run ... heart-predict:latest` will run GUI
# or override: `docker run ... heart-predict:latest python cli.py --values ...`
ENTRYPOINT ["python"]
CMD ["./heart_disease_gui.py"]

# Run this from PowerShell. Requires Docker Desktop and an X server (VcXsrv) running on Windows.
# This script uses host.docker.internal to forward X connections to the Windows host.

$image = "heart-predict:latest"

Write-Host "Building image..."
docker build -t $image .

Write-Host "Running container (GUI) using host.docker.internal:0.0 as DISPLAY"
docker run --rm -e DISPLAY=host.docker.internal:0.0 -e LIBGL_ALWAYS_INDIRECT=1 -v ${PWD}:/app $image

# For headless CLI usage inside container (example values):
# docker run --rm -v ${PWD}:/app $image python cli.py --values 52,1,0,125,212,0,1,168,0,1,2,2,3

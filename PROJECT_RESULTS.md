# Project Results

## Day 8 — Docker Baseline

### Application containerisation

- Successfully built the FastAPI application as the `secure-api` Docker image.
- Successfully started FastAPI inside a Docker container.
- Published host port 8000 to container port 8000.
- Verified `GET /health` returned HTTP 200 from the containerised application.

### Baseline measurements

- Docker image local disk usage: 273 MB
- Docker image content size: 65.3 MB
- Python dependency installation layer: 65.8 MB
- Application COPY layer: 49.2 kB
- Docker build context: 6.27 kB
- Container runtime user: `root` (`uid=0`)
- Uvicorn listener inside container: `0.0.0.0:8000`

### Security improvement targets

Future container-hardening work should aim to:

- Run the application as a non-root user.
- Reduce unnecessary image size where practical.
- Scan the image for vulnerabilities.
- Remove or remediate high-severity vulnerabilities.
- Keep secrets outside the image.
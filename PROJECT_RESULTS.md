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

## Day 9 — Docker Compose and Persistence

### Multi-container architecture

- Ran FastAPI and PostgreSQL as separate Docker Compose services.
- Connected the API to PostgreSQL using Docker DNS through the `db` service hostname.
- Published only the API service to the host while keeping PostgreSQL unexposed to the host network.
- Successfully performed API reads and writes across the Docker network.

### Persistence validation

- Stored PostgreSQL data in a Docker named volume.
- Inserted users through both PostgreSQL and the FastAPI API.
- Destroyed and recreated the API container, PostgreSQL container, and Compose network.
- Verified all database records persisted after complete stack recreation.

### Build caching

- Rebuilt the API image using Docker layer caching.
- Reused the dependency-installation layer instead of rerunning `pip install`.
- Previously measured dependency installation time: approximately 9.5 seconds.
- Cached dependency installation during rebuild: 0.0 seconds.

### Reliability observation

- Observed that a Docker container reporting `Up` does not guarantee that the application inside it is ready to receive traffic.
- An immediate request after stack startup received a connection reset, while a subsequent request succeeded after Uvicorn completed startup.
- This establishes a future improvement target for container health checks and readiness validation.

## Day 10 — Container Security

### Baseline

- API container initially ran as `root` (`uid=0`).
- Initial Trivy vulnerability scan detected 56 HIGH/CRITICAL OS-package findings:
  - 53 HIGH
  - 3 CRITICAL
- Python dependencies had 0 detected HIGH/CRITICAL findings.
- Initial image content size: 65.3 MB.

### Hardening

- Created a dedicated `appuser` and configured the API to run as non-root.
- Upgraded Debian packages during the image build.
- Separated production dependencies from development/test dependencies.
- Removed test-only packages such as pytest and HTTPX from the production container.
- Replaced broad `COPY . .` behavior with explicit copying of runtime application files.
- Excluded `.env` and non-runtime project files from the Docker build context.
- Kept database credentials out of the image and injected `DATABASE_URL` at container runtime.

### Results

- Runtime identity changed from `root` (`uid=0`) to `appuser` (`uid=1000`).
- HIGH/CRITICAL vulnerability findings reduced from 56 to 44 — a 21.4% reduction.
- CRITICAL findings reduced from 3 to 0.
- Final vulnerability count: 44 HIGH, 0 CRITICAL.
- `/health` and database-backed `/users` remained functional after hardening.
- Test-only packages were absent from the final production container.
- Final image content size: 71.6 MB.
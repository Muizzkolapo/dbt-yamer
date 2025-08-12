# Use Python 3.9 slim image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DBT_PROFILES_DIR=/workspace/profiles

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create workspace directory
WORKDIR /workspace

# Install dbt and dependencies
RUN pip install --no-cache-dir \
    dbt-core==1.7.* \
    dbt-postgres==1.7.*

# Copy requirements for dbt-yamer dependencies
COPY requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt

# Create a non-root user
RUN useradd --create-home --shell /bin/bash dbt
RUN chown -R dbt:dbt /workspace
USER dbt

# Set the default command
CMD ["/bin/bash"]
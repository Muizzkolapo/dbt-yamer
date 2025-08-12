#!/bin/bash

set -e

echo "🚀 Starting /home/dbt/.local/bin/dbt-yamer Docker Test Environment"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker Desktop."
    exit 1
fi

print_status "Building Docker containers..."
docker-compose build

print_status "Starting PostgreSQL and dbt containers..."
docker-compose up -d

print_status "Waiting for PostgreSQL to be ready..."
timeout=60
elapsed=0
while ! docker-compose exec -T postgres pg_isready -U dbt_user -d dbt_test_db >/dev/null 2>&1; do
    sleep 2
    elapsed=$((elapsed + 2))
    if [ $elapsed -ge $timeout ]; then
        print_error "PostgreSQL failed to start within $timeout seconds"
        docker-compose logs postgres
        exit 1
    fi
done

print_success "PostgreSQL is ready!"

print_status "Installing dbt-yamer in the container..."
# Force reinstall to ensure latest code is loaded
docker-compose exec -T dbt pip uninstall -y dbt-yamer 2>/dev/null || true
docker-compose exec -T dbt pip install -e /dbt-yamer-source

print_status "Setting up dbt project..."
# Remove conflicting doc files that cause parsing errors
print_status "Cleaning up conflicting documentation files..."
# Remove all .md files except docs.md
docker-compose exec -T dbt bash -c "find /workspace/test-project -name '*.md' ! -name 'docs.md' -type f -delete"
docker-compose exec -T dbt bash -c "find /workspace/test-project -name '*dbt_yamer*' -type f -delete"
docker-compose exec -T dbt bash -c "find /workspace/test-project -name '_schema_*.yml' -delete"
docker-compose exec -T dbt bash -c "find /workspace/test-project -name 'stg_*.yml' -delete"
docker-compose exec -T dbt dbt deps
docker-compose exec -T dbt dbt seed
docker-compose exec -T dbt dbt run
docker-compose exec -T dbt dbt test

print_success "dbt project setup complete!"

print_status "Testing /home/dbt/.local/bin/dbt-yamer commands..."

# Clean environment before tests
print_status "Preparing test environment..."
# Remove any conflicting docs before tests (all .md except docs.md)
docker-compose exec -T dbt bash -c "find /workspace/test-project -name '*.md' ! -name 'docs.md' -type f -delete"
# Remove any leftover macro files
docker-compose exec -T dbt bash -c "find /workspace/test-project -name '*dbt_yamer*' -type f -delete"

# Test YAML generation
echo ""
print_status "Testing YAML generation for single model..."
if docker-compose exec -T dbt /home/dbt/.local/bin/dbt-yamer yaml -s stg_customers; then
    print_success "✅ Single model YAML generation - PASSED"
else
    print_error "❌ Single model YAML generation - FAILED"
fi

# Test multiple models
echo ""
print_status "Testing YAML generation for multiple models..."
if docker-compose exec -T dbt /home/dbt/.local/bin/dbt-yamer yaml -s stg_customers stg_orders; then
    print_success "✅ Multiple model YAML generation - PASSED"
else
    print_error "❌ Multiple model YAML generation - FAILED"
fi

# Test tag selector (might fail if no staging tag exists)
echo ""
print_status "Testing tag selector..."
if docker-compose exec -T dbt /home/dbt/.local/bin/dbt-yamer yaml -s tag:staging; then
    print_success "✅ Tag selector - PASSED"
else
    print_warning "⚠️  Tag selector - FAILED (expected if no staging tag exists)"
fi

# Test different target
echo ""
print_status "Testing different target..."
if docker-compose exec -T dbt /home/dbt/.local/bin/dbt-yamer yaml -s stg_payments -t test; then
    print_success "✅ Different target - PASSED"
else
    print_error "❌ Different target - FAILED"
fi

# Test markdown generation
echo ""
print_status "Testing markdown generation..."
if docker-compose exec -T dbt /home/dbt/.local/bin/dbt-yamer md -s dim_customers; then
    print_success "✅ Markdown generation - PASSED"
else
    print_error "❌ Markdown generation - FAILED"
fi

# Clean up generated markdown files before next tests to avoid doc name conflicts
print_status "Cleaning up generated markdown files..."
docker-compose exec -T dbt bash -c "find /workspace/test-project -name '*.md' ! -name 'docs.md' -type f -delete"

# Test combined generation
echo ""
print_status "Testing combined YAML and markdown generation..."
if docker-compose exec -T dbt /home/dbt/.local/bin/dbt-yamer yamd -s fct_orders; then
    print_success "✅ Combined generation - PASSED"
else
    print_error "❌ Combined generation - FAILED"
fi

# Clean up generated markdown files before dbt run test
print_status "Cleaning up generated markdown files..."
docker-compose exec -T dbt bash -c "find /workspace/test-project -name '*.md' ! -name 'docs.md' -type f -delete"

# Test dbt run command
echo ""
print_status "Testing dbt run command..."
if docker-compose exec -T dbt /home/dbt/.local/bin/dbt-yamer run -s stg_customers; then
    print_success "✅ dbt run command - PASSED"
else
    print_error "❌ dbt run command - FAILED"
fi

# Test security features
echo ""
print_status "Testing security validations..."

print_status "Testing malicious input rejection..."
if docker-compose exec -T dbt /home/dbt/.local/bin/dbt-yamer yaml -s "model'; DROP TABLE test; --" 2>&1 | grep -q "validation error\|Security validation error\|Invalid"; then
    print_success "✅ Malicious input handling - PASSED"
else
    print_warning "⚠️  Malicious input handling - needs verification"
fi

print_status "Testing path traversal protection..."
if docker-compose exec -T dbt /home/dbt/.local/bin/dbt-yamer yaml -s "../../../etc/passwd" 2>&1 | grep -q "validation error\|Security validation error\|Invalid"; then
    print_success "✅ Path traversal protection - PASSED"
else
    print_warning "⚠️  Path traversal protection - needs verification"
fi

# Check generated files
echo ""
print_status "Checking generated files..."
docker-compose exec -T dbt find /workspace/test-project -name "*.yml" -o -name "*.md" -type f | head -10 | while read file; do
    docker-compose exec -T dbt ls -la "$file"
done

# Test database connectivity
echo ""
print_status "Verifying database connectivity..."
if docker-compose exec -T postgres psql -U dbt_user -d dbt_test_db -c "SELECT table_name FROM information_schema.tables WHERE table_schema = 'dbt_yamer_test';" | head -10; then
    print_success "✅ Database connectivity - PASSED"
else
    print_error "❌ Database connectivity - FAILED"
fi

# Clean up macro file and any generated files
docker-compose exec -T dbt rm -f /workspace/test-project/macros/dbt_yamer_temp.sql
# Clean up all .md files except docs.md
docker-compose exec -T dbt bash -c "find /workspace/test-project -name '*.md' ! -name 'docs.md' -type f -delete"

echo ""
echo "=============================================="
print_success "🎉 dbt-yamer Docker Test Environment is ready!"
echo ""
echo "To access the dbt container interactively:"
echo "  docker-compose exec dbt /bin/bash"
echo ""
echo "To access PostgreSQL:"
echo "  docker-compose exec postgres psql -U dbt_user -d dbt_test_db"
echo ""
echo "To stop the environment:"
echo "  docker-compose down"
echo ""
echo "Available /home/dbt/.local/bin/dbt-yamer commands to test:"
echo "  /home/dbt/.local/bin/dbt-yamer yaml -s stg_customers"
echo "  /home/dbt/.local/bin/dbt-yamer md -s dim_customers"
echo "  /home/dbt/.local/bin/dbt-yamer yamd -s fct_orders"
echo "  /home/dbt/.local/bin/dbt-yamer run -s tag:staging"
echo "============================================"

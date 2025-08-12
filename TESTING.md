# 🧪 Testing dbt-yamer

This guide shows you how to test dbt-yamer using our comprehensive Docker-based test environment.

## 🚀 Quick Start (5 minutes)

### Prerequisites
- **Docker Desktop** installed and running
- **Git** to clone the repository

### One-Command Test

```bash
# Clone and test
git clone https://github.com/Muizzkolapo/dbt-yamer.git
cd dbt-yamer/docker-test
./test_dbt_yamer.sh
```

**That's it!** The script will automatically:

1. 🏗️ **Build Docker containers** with PostgreSQL + dbt
2. 📊 **Create sample data** (customers, orders, payments)
3. 🔧 **Install dbt-yamer** from your source code
4. ⚡ **Run comprehensive tests** covering all functionality
5. 🎯 **Show results** with clear PASS/FAIL status

## 📋 What Gets Tested

### ✅ Core Functionality
- YAML schema generation for single/multiple models
- Tag-based model selection (`tag:staging`, `tag:mart`)
- Markdown documentation generation
- Combined YAML + Markdown generation
- dbt model execution via `dbt-yamer run`
- Custom targets and manifest paths

### 🔒 Security Features
- Input validation and sanitization
- Command injection prevention
- Path traversal protection
- Malicious input rejection
- Timeout handling

### 🐛 Bug Fixes Validation
- Fixed column documentation extraction
- Race condition prevention
- Proper exception handling
- Tag selector expansion
- Temporary file cleanup

## 📊 Expected Output

When you run `./test_dbt_yamer.sh`, you should see:

```bash
🚀 Starting dbt-yamer Docker Test Environment
==============================================
[INFO] Building Docker containers...
[INFO] Starting PostgreSQL and dbt containers...
[SUCCESS] PostgreSQL is ready!
[INFO] Installing dbt-yamer in the container...
[INFO] Setting up dbt project...
[SUCCESS] dbt project setup complete!

[INFO] Testing YAML generation for single model...
✅ Single model YAML generation - PASSED

[INFO] Testing YAML generation for multiple models...
✅ Multiple model YAML generation - PASSED

[INFO] Testing tag selector...
✅ Tag selector - PASSED

[INFO] Testing different target...
✅ Different target - PASSED

[INFO] Testing markdown generation...
✅ Markdown generation - PASSED

[INFO] Testing combined YAML and markdown generation...
✅ Combined generation - PASSED

[INFO] Testing dbt run command...
✅ dbt run command - PASSED

[INFO] Testing security validations...
✅ Malicious input rejected - PASSED
✅ Path traversal protection - PASSED

[SUCCESS] 🎉 dbt-yamer Docker Test Environment is ready!
```

## 🔍 Manual Testing

If you want to test specific scenarios manually:

### 1. Start the Environment
```bash
cd docker-test
docker-compose up -d
```

### 2. Access the dbt Container
```bash
docker-compose exec dbt /bin/bash
```

### 3. Test dbt-yamer Commands
```bash
# Basic YAML generation
dbt-yamer yaml -s stg_customers

# Multiple models
dbt-yamer yaml -s stg_customers stg_orders stg_payments

# Tag selectors
dbt-yamer yaml -s tag:staging

# Different targets
dbt-yamer yaml -s dim_customers -t test

# Markdown documentation
dbt-yamer md -s fct_orders

# Combined YAML + Markdown
dbt-yamer yamd -s dim_customers

# Run dbt models
dbt-yamer run -s tag:mart

# Custom manifest path
dbt-yamer yaml -s stg_customers --manifest target/manifest.json
```

### 4. Verify Results
```bash
# Check generated YAML files
find . -name "*.yml" -exec ls -la {} \;

# View YAML content
cat models/staging/stg_customers.yml

# Check generated markdown
find . -name "*.md" -exec ls -la {} \;
```

### 5. Test Database
```bash
# Access PostgreSQL
docker-compose exec postgres psql -U dbt_user -d dbt_test_db

# Check created tables
\dt dbt_yamer_test.*

# Query sample data
SELECT * FROM dbt_yamer_test.dim_customers LIMIT 5;
```

## 🗂️ Test Data Structure

The test environment includes realistic e-commerce data:

### Seeds (Raw Data)
- **customers.csv**: 8 customers with various statuses
- **orders.csv**: 10 orders with different statuses  
- **payments.csv**: 7 payment records

### dbt Models
- **Staging**: `stg_customers`, `stg_orders`, `stg_payments` (tagged: `staging`)
- **Intermediate**: `int_customer_orders` (tagged: `intermediate`)
- **Marts**: `dim_customers`, `fct_orders` (tagged: `mart`, `production`)

### Documentation
- Full doc blocks for testing fuzzy matching
- Multiple matching strategies (exact, model-specific, generic)

## ❌ Troubleshooting

### Docker Issues
```bash
# Check if Docker is running
docker info

# Check container status
docker-compose ps

# View logs
docker-compose logs dbt
docker-compose logs postgres

# Restart services
docker-compose restart
```

### Test Failures
```bash
# Check dbt logs
docker-compose exec dbt cat logs/dbt.log

# Verify database connectivity
docker-compose exec postgres pg_isready -U dbt_user -d dbt_test_db

# Clean restart
docker-compose down -v
docker-compose up -d
```

### Permission Issues (Linux/Mac)
```bash
# Make script executable
chmod +x test_dbt_yamer.sh

# Fix Docker permissions
sudo usermod -aG docker $USER
# Then logout and login again
```

## 🧹 Cleanup

When you're done testing:

```bash
# Stop containers
docker-compose down

# Remove volumes (optional - deletes database data)
docker-compose down -v

# Remove images (optional - saves disk space)
docker system prune
```

## 🎯 Testing Specific Features

### Security Testing
```bash
# Test malicious input (should be rejected)
dbt-yamer yaml -s "model'; DROP TABLE test; --"

# Test path traversal (should be rejected)
dbt-yamer yaml -s "../../../etc/passwd"

# Test empty input (should show helpful error)
dbt-yamer yaml -s ""
```

### Performance Testing
```bash
# Test concurrent execution (race conditions)
for i in {1..5}; do
  dbt-yamer yaml -s stg_customers &
done
wait

# Check for leftover temp files (should be none)
find . -name "tmp_dbt_yamer*"
```

### Error Handling
```bash
# Test nonexistent model
dbt-yamer yaml -s nonexistent_model

# Test invalid target
dbt-yamer yaml -s stg_customers -t invalid_target

# Test missing manifest
dbt-yamer yaml -s stg_customers --manifest /nonexistent/path.json
```

## 📈 Success Criteria

A successful test run should show:

✅ All basic functionality tests passing  
✅ Security validations rejecting malicious inputs  
✅ Generated YAML files with proper doc block references  
✅ Generated markdown files with templates  
✅ Database tables/views created successfully  
✅ No leftover temporary files  
✅ Clear, helpful error messages for invalid inputs  
✅ Fast execution with timeout protection  

## 💡 Tips

- **First time setup**: Allow ~2-3 minutes for Docker images to download
- **Iterative testing**: Leave containers running between tests with `docker-compose up -d`
- **Development workflow**: Mount your code changes with volumes for fast iteration
- **CI/CD integration**: The test script returns proper exit codes for automation

---

**Need help?** Open an issue at [dbt-yamer Issues](https://github.com/Muizzkolapo/dbt-yamer/issues) 🐛
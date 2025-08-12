# dbt-yamer Docker Test Environment

This Docker-based test environment provides a complete setup for testing the improved dbt-yamer tool with a PostgreSQL database and sample dbt project.

## 🚀 How to Run Tests

### ⚡ One-Command Test (Recommended)

```bash
# From the project root directory
cd docker-test
./test_dbt_yamer.sh
```

**That's it!** This single command will:
- ✅ Build Docker containers with PostgreSQL + dbt
- ✅ Install dbt-yamer from your source code  
- ✅ Create realistic sample data (customers, orders, payments)
- ✅ Set up complete dbt project with models and docs
- ✅ Test all dbt-yamer commands and security features
- ✅ Show clear PASS/FAIL results for each test

### Expected Output
```bash
🚀 Starting dbt-yamer Docker Test Environment
==============================================
[SUCCESS] PostgreSQL is ready!
[INFO] Testing YAML generation for single model...
✅ Single model YAML generation - PASSED
[INFO] Testing security validations...  
✅ Malicious input rejected - PASSED
[SUCCESS] 🎉 dbt-yamer Docker Test Environment is ready!
```

### Prerequisites
- **Docker Desktop** installed and running
- **Git** (if cloning the repository)

### Alternative: Manual Testing

If you prefer to test interactively:

```bash
# Start containers
docker-compose up -d

# Access dbt environment
docker-compose exec dbt /bin/bash

# Test commands manually
dbt-yamer yaml -s stg_customers
dbt-yamer md -s dim_customers
```

## 🏗️ Architecture

### Docker Services

- **postgres**: PostgreSQL 15 database with sample e-commerce data
- **dbt**: dbt-core environment with dbt-yamer installed

### Sample Data

The test environment includes realistic e-commerce data:

- **customers**: Customer information with status tracking
- **orders**: Order data with various statuses
- **payments**: Payment records with different methods

### dbt Models

**Staging Layer (`tag:staging`):**
- `stg_customers` - Customer data with derived fields
- `stg_orders` - Order data with categorization  
- `stg_payments` - Payment data with type classification

**Intermediate Layer (`tag:intermediate`):**
- `int_customer_orders` - Customer order aggregations

**Mart Layer (`tag:mart`):**
- `dim_customers` - Customer dimension with segmentation
- `fct_orders` - Orders fact table with enriched data

## 🧪 Testing Scenarios

The test environment validates:

### Core Functionality
- ✅ YAML schema generation for single models
- ✅ YAML schema generation for multiple models  
- ✅ Tag selector expansion (`tag:staging`, `tag:mart`)
- ✅ Markdown documentation generation
- ✅ Combined YAML + Markdown generation
- ✅ dbt model execution via dbt-yamer run

### Security Features
- ✅ Input validation and sanitization
- ✅ Command injection prevention
- ✅ Path traversal protection
- ✅ Malicious input rejection
- ✅ Timeout handling

### Error Handling
- ✅ Graceful error messages
- ✅ Missing model handling
- ✅ Invalid target handling
- ✅ Database connectivity issues

### Doc Block Matching
- ✅ Exact match: `col_{model}_{column}`
- ✅ Model-specific: `{model}_{column}`
- ✅ Generic: `col_{column}`
- ✅ Fuzzy matching with 80%+ confidence
- ✅ Fallback to empty descriptions

## 🔧 Manual Testing Commands

Access the dbt container for interactive testing:

```bash
docker-compose exec dbt /bin/bash
```

Inside the container, you can run:

```bash
# Test basic YAML generation
dbt-yamer yaml -s stg_customers

# Test multiple models
dbt-yamer yaml -s stg_customers stg_orders stg_payments

# Test tag selectors  
dbt-yamer yaml -s tag:staging

# Test different targets
dbt-yamer yaml -s dim_customers -t test

# Test markdown generation
dbt-yamer md -s fct_orders

# Test combined generation
dbt-yamer yamd -s dim_customers

# Test dbt run functionality
dbt-yamer run -s tag:mart

# Test with custom manifest
dbt-yamer yaml -s stg_customers --manifest target/manifest.json
```

## 🔍 Verify Results

### Check Generated Files
```bash
# Find generated YAML files
find . -name "*.yml" -newer /tmp/start_time

# Check file contents
cat models/staging/stg_customers.yml

# Find generated markdown files  
find . -name "*.md" -newer /tmp/start_time
```

### Database Verification
```bash
# Access PostgreSQL
docker-compose exec postgres psql -U dbt_user -d dbt_test_db

# Check created tables/views
\dt dbt_yamer_test.*
\dv dbt_yamer_test.*

# Query sample data
SELECT * FROM dbt_yamer_test.dim_customers LIMIT 5;
```

## 🐛 Debugging

### View Logs
```bash
# Container logs
docker-compose logs dbt
docker-compose logs postgres

# dbt logs (inside container)
docker-compose exec dbt cat logs/dbt.log
```

### Check Container Status
```bash
docker-compose ps
```

### Restart Services
```bash
docker-compose restart
```

## 🧹 Cleanup

Stop and remove containers:
```bash
docker-compose down

# Remove volumes (optional - deletes database data)
docker-compose down -v
```

## 📊 Expected Test Results

When running `./test_dbt_yamer.sh`, you should see:

- ✅ All basic functionality tests passing
- ✅ Security validation rejecting malicious inputs
- ✅ Generated YAML files with proper doc block references
- ✅ Generated markdown files with dbt documentation templates
- ✅ Database tables/views created successfully
- ✅ No temporary files left behind (race condition fixes working)

Any failures indicate bugs that need to be addressed in the dbt-yamer implementation.

## 🎯 Testing Focus Areas

This environment specifically validates the major bug fixes:

1. **Security Issues Fixed**: Command injection, path traversal, input validation
2. **Race Conditions Fixed**: Unique temporary file naming, proper cleanup
3. **Error Handling Fixed**: No more `sys.exit()`, proper exception handling
4. **Performance Issues Fixed**: Thread pool limits, timeout handling
5. **Functionality Fixed**: Correct column doc extraction, tag expansion
6. **Code Quality**: Consolidated duplicate code, consistent interfaces
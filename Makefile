# Variables
PACKAGE := dbt_yamer
DIST_DIR := dist
BUILD_DIR := build

# Uninstall the package
uninstall: 
	pip uninstall -y $(PACKAGE) || echo "WARNING: Skipping $(PACKAGE) as it is not installed."

# Clean build artifacts
clean:
	rm -rf dist build *.egg-info

# Build the package
build: 
	pip install .

# Restart by uninstalling, cleaning, and rebuilding
restart: uninstall clean build

.PHONY: all install uninstall clean build restart

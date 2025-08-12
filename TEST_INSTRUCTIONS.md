# 🧪 How to Test dbt-yamer

## Quick Test (5 minutes)

```bash
# 1. Make sure Docker Desktop is running

# 2. Run the test
cd docker-test
./test_dbt_yamer.sh
```

That's it! The script will automatically test everything and show PASS/FAIL results.

## What Gets Tested

✅ YAML schema generation  
✅ Markdown documentation  
✅ Tag selectors (`tag:staging`)  
✅ Security features (input validation)  
✅ Bug fixes (race conditions, error handling)  
✅ All improved functionality  

## Expected Results

You should see output like:
```
✅ Single model YAML generation - PASSED
✅ Multiple model YAML generation - PASSED  
✅ Tag selector - PASSED
✅ Security validation working - PASSED
🎉 dbt-yamer Docker Test Environment is ready!
```

## Need Help?

- **Docker not installed?** → [Install Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Test failing?** → Check [TESTING.md](TESTING.md) for troubleshooting
- **Found a bug?** → [Report it here](https://github.com/Muizzkolapo/dbt-yamer/issues)

**Full testing guide:** See [TESTING.md](TESTING.md) for detailed instructions.
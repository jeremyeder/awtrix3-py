# CI Test Plan

This document outlines the testing strategy for the awtrix3-py project's Continuous Integration pipeline.

## Runtime Requirement

**All tests must complete within 1 minute maximum.**

## Test Categories

### 1. Core Library Testing (awtrix3.py)

**Scope**: Unit tests for the core `Awtrix3` class and its methods
**Duration**: 15-20 seconds

#### Test Cases:
- Constructor initialization with host and optional auth
- HTTP request validation for all 5 endpoints (notify, stats, power, custom_app, play_sound)
- JSON response parsing
- Error handling for HTTP failures
- Mock HTTP responses to avoid external dependencies

#### Implementation:
```bash
# Setup
pip install pytest pytest-mock requests-mock

# Run tests
pytest tests/test_awtrix3.py -v --tb=short
```

### 2. CLI Testing (trixctl)

**Scope**: Command-line interface argument parsing and functionality
**Duration**: 10-15 seconds

#### Test Cases:
- Argument parsing for all subcommands (notify, stats, power, app, sound)
- Global options (--host, --username, --password)
- Input validation and error messages
- Help text generation
- Command execution without real device interaction

#### Implementation:
```bash
# Run CLI tests
pytest tests/test_trixctl.py -v --tb=short
```

### 3. Bash Completion Testing

**Scope**: Validate bash completion scripts (if present)
**Duration**: 5 seconds

#### Test Cases:
- Syntax validation of completion scripts
- Subcommand completion logic
- Option completion behavior

#### Implementation:
```bash
# Check for completion scripts and validate syntax
bash -n completion/trixctl.bash 2>/dev/null || echo "No completion script found"
```

### 4. Documentation Testing

**Scope**: Verify README examples and documentation accuracy
**Duration**: 10-15 seconds

#### Test Cases:
- Validate Python code examples in README.md
- Check CLI usage examples
- Ensure all documented features exist in code
- Link validation (internal references)

#### Implementation:
```bash
# Extract and validate code examples
python scripts/validate_readme_examples.py
```

### 5. Cross-Platform Testing (Python 3.12 Only)

**Scope**: Ensure compatibility with Python 3.12
**Duration**: 10-15 seconds

#### Test Cases:
- Import validation
- Basic functionality verification
- Dependency compatibility check

#### Implementation:
```bash
# Verify Python 3.12 compatibility
python3.12 -c "import awtrix3; print('Import successful')"
python3.12 -m py_compile awtrix3.py
python3.12 -m py_compile trixctl
```

### 8. Integration Testing

**Scope**: End-to-end testing with mocked external dependencies
**Duration**: 15-20 seconds

#### Test Cases:
- Complete workflow: CLI -> Library -> Mock HTTP Response
- Configuration file handling
- Error propagation through the stack
- Real-world usage scenarios with mocked responses

#### Implementation:
```bash
# Run integration tests with mocked Awtrix3 device
pytest tests/test_integration.py -v --tb=short
```

## CI Pipeline Configuration

### Prerequisites
```bash
pip install pytest pytest-mock requests-mock
```

### Test Execution Order
1. Core Library Testing
2. CLI Testing  
3. Cross-Platform Testing
4. Documentation Testing
5. Bash Completion Testing
6. Integration Testing

### Success Criteria
- All tests pass
- Total runtime < 60 seconds
- Code coverage > 80% (if implemented)

### Failure Handling
- Stop on first category failure
- Provide clear error messages
- Log detailed output for debugging

## Test Data and Mocking

### Mock HTTP Responses
```json
{
  "stats": {"version": "0.96", "uptime": 12345},
  "notify": {"success": true},
  "power": {"state": "on"},
  "app": {"status": "active"},
  "sound": {"playing": true}
}
```

### Test Configuration
```python
TEST_HOST = "192.168.1.100"
TEST_USERNAME = "testuser"
TEST_PASSWORD = "testpass"
```

## Future Enhancements

This test plan focuses on core functionality and fast execution. Additional testing categories have been moved to separate backlog issues for future implementation:

- Security Testing (Issue TBD)
- Performance Testing (Issue TBD)

## Notes

- Tests use mocked HTTP responses to avoid requiring real hardware
- All external dependencies are mocked or stubbed
- Tests are designed for speed while maintaining coverage
- Real device testing should be done manually before releases
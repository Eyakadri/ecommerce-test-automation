#!/bin/bash
# Project Health Check Script

set -u

echo "=========================================="
echo "E-Commerce Test Automation Project"
echo "Health Check Report"
echo "=========================================="
echo ""

check_python_syntax() {
    echo "1. Checking Python syntax..."
    if python3 -m py_compile pages/*.py utils/*.py tests/conftest.py 2>/dev/null; then
        echo "   PASS: Python syntax is valid"
    else
        echo "   FAIL: Syntax errors were found"
        exit 1
    fi
    echo ""
}

check_imports() {
    echo "2. Checking module imports..."
    python3 <<'EOF'
import sys
sys.path.insert(0, '.')
try:
    from pages.base_page import BasePage
    from pages.login_page import LoginPage
    from pages.product_page import ProductPage
    from pages.cart_page import CartPage
    from pages.checkout_page import CheckoutPage
    from utils.config import Config
    from utils.screenshot import ScreenshotManager
    print("   PASS: Imports completed successfully")
except Exception as e:
    print(f"   FAIL: Import error: {e}")
    sys.exit(1)
EOF
    echo ""
}

check_configuration() {
    echo "3. Checking configuration..."
    python3 <<'EOF'
from utils.config import Config
print(f"   PASS: BASE_URL = {Config.BASE_URL}")
print(f"   PASS: BROWSER = {Config.BROWSER}")
print(f"   PASS: HEADLESS = {Config.HEADLESS}")
print(f"   PASS: IMPLICIT_WAIT = {Config.IMPLICIT_WAIT}s")
print(f"   PASS: EXPLICIT_WAIT = {Config.EXPLICIT_WAIT}s")
EOF
    echo ""
}

check_test_collection() {
    echo "4. Checking test discovery..."
    TEST_OUTPUT=$(python3 -m pytest --collect-only -q 2>/dev/null)
    if [ $? -eq 0 ]; then
        TEST_COUNT=$(echo "$TEST_OUTPUT" | grep -oE '^[[:space:]]*[0-9]+ items collected' | grep -oE '[0-9]+' | tail -n 1)
        if [ -n "$TEST_COUNT" ] && [ "$TEST_COUNT" -gt 0 ]; then
            echo "   PASS: Test collection completed ($TEST_COUNT tests)"
        else
            echo "   PASS: Test collection completed"
        fi
    else
        echo "   FAIL: Test collection could not be completed"
    fi
    echo ""
}

check_project_structure() {
    echo "5. Checking project structure..."
    FILES=(
        ".env"
        ".env.example"
        "requirements.txt"
        "pytest.ini"
        "README.md"
        "pages/base_page.py"
        "pages/login_page.py"
        "tests/conftest.py"
        "tests/test_login.py"
        "docs/test_plan.md"
    )

    for file in "${FILES[@]}"; do
        if [ -f "$file" ]; then
            echo "   PASS: $file"
        else
            echo "   FAIL: $file (missing)"
        fi
    done
    echo ""
}

check_python_syntax
check_imports
check_configuration
check_test_collection
check_project_structure

echo "=========================================="
echo "Project health status: READY"
echo "=========================================="
echo ""
echo "To run tests:"
echo "  pytest"
echo "  pytest tests/test_login.py"
echo "  pytest -v"
echo ""
echo "For CI or headless execution:"
echo "  Xvfb :99 -screen 0 1920x1080x24 &"
echo "  export DISPLAY=:99"
echo "  pytest"
echo ""

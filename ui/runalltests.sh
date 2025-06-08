#!/bin/bash

# Don't stop on first error
set +e

# Define test files
TEST_FILES=("test_login.py" "test_stored_credentials.py" "test_forgot_password.py")  # Replace with your files

# Browsers
BROWSERS=("chromium" "firefox" "webkit")

# Mobile devices
DEVICES=("iPhone 12" "Pixel 5")

# Pytest output options
PYTEST_OPTS="-q --tb=short"

# Output folders
LOG_DIR="logs"
REPORT_FILE="test_run_report.html"

# Setup log directory and HTML file
mkdir -p "$LOG_DIR"
> "$REPORT_FILE"

# HTML Header
echo "<html><head><title>Test Report</title></head><body><h1>Playwright Test Report</h1><ul>" >> "$REPORT_FILE"

run_and_log() {
  local TEST_FILE=$1
  local BROWSER=$2
  local DEVICE=$3

  local LABEL="$TEST_FILE on $BROWSER"
  local LOGFILE="$LOG_DIR/$(echo $LABEL | tr ' /' '__')"
  [ -n "$DEVICE" ] && {
    LABEL="$LABEL with $DEVICE"
    LOGFILE="$LOGFILE-$(echo $DEVICE | tr ' /' '__')"
  }
  LOGFILE="$LOGFILE.log"

  echo "$LABEL"
  
  if [ -n "$DEVICE" ]; then
    pytest "$TEST_FILE" --browser "$BROWSER" --device "$DEVICE" $PYTEST_OPTS &> "$LOGFILE"
  else
    pytest "$TEST_FILE" --browser "$BROWSER" $PYTEST_OPTS &> "$LOGFILE"
  fi

  if [ $? -eq 0 ]; then
    echo " $LABEL" >> "$REPORT_FILE"
    echo "<li style='color:green'> $LABEL</li>" >> "$REPORT_FILE"
  else
    echo "$LABEL (see $LOGFILE)" >> "$REPORT_FILE"
    echo "<li style='color:red'>$LABEL - <a href=\"$LOGFILE\">log</a></li>" >> "$REPORT_FILE"
  fi
}

# Run desktop tests
echo "Running desktop tests..."
for TEST_FILE in "${TEST_FILES[@]}"; do
  for BROWSER in "${BROWSERS[@]}"; do
    run_and_log "$TEST_FILE" "$BROWSER"
  done
done

# Run mobile tests
echo ""
echo " Running mobile tests..."
for TEST_FILE in "${TEST_FILES[@]}"; do
  for DEVICE in "${DEVICES[@]}"; do
    for BROWSER in "${BROWSERS[@]}"; do
      run_and_log "$TEST_FILE" "$BROWSER" "$DEVICE"
    done
  done
done

# Finish HTML
echo "</ul><p>Generated on $(date)</p></body></html>" >> "$REPORT_FILE"

echo ""
echo "All tests completed. Open $REPORT_FILE to view the summary."

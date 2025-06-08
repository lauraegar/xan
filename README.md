

# Description

A test suite to test an API and a UI

## Prerequisite packages for python

`pip install pytest requests freezegun locust json`

### Test Execution

running the script `runalltests.sh` will excute a bash script that runs the test cases against all browsers available in playwright webkit
and it also runs the tests against the playwright webkit mobile device emulators.
a log file is created from the test output to capture failures, and a report is also generated in html.

#### performance testing
the api could have performance tests excuted againt it using locust, but all attempts to carry out performance testing were rejected with a 429.

### <a href="https://playwright.dev/python/docs/intro#installing-playwright-pytest">Playwright</a>

it is necessary to install playwright to excute the tests, the command is:
`pip install pytest-playwright`

and then install the browsers
`playwright install`








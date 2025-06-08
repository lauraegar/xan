### Performance

the performance tests run using locust.

install locust with `python -m pip install locust`

<a href="https://locust.io">Locust</a> is an open source load testing tool. 

running tests from a command line: 
`locust --headless --users 10 --spawn-rate 1 -H http://your-server.com`

web interface is at `localhost:8089`

command to run with web interface is for example : `locust -f locusttests.py --host=https://api.matchbook.com`

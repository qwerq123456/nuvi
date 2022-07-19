# Report

## with no multiprocess

``` 
Traceback (most recent call last):
  File "/usr/local/lib/python3.9/site-packages/urllib3/connection.py", line 169, in _new_conn
    conn = connection.create_connection(
  File "/usr/local/lib/python3.9/site-packages/urllib3/util/connection.py", line 96, in create_connection
    raise err
  File "/usr/local/lib/python3.9/site-packages/urllib3/util/connection.py", line 86, in create_connection
    sock.connect(sa)
TimeoutError: [Errno 60] Operation timed out

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.9/site-packages/urllib3/connectionpool.py", line 699, in urlopen
    httplib_response = self._make_request(
  File "/usr/local/lib/python3.9/site-packages/urllib3/connectionpool.py", line 382, in _make_request
    self._validate_conn(conn)
  File "/usr/local/lib/python3.9/site-packages/urllib3/connectionpool.py", line 1010, in _validate_conn
    conn.connect()
  File "/usr/local/lib/python3.9/site-packages/urllib3/connection.py", line 353, in connect
    conn = self._new_conn()
  File "/usr/local/lib/python3.9/site-packages/urllib3/connection.py", line 181, in _new_conn
    raise NewConnectionError(
urllib3.exceptions.NewConnectionError: <urllib3.connection.HTTPSConnection object at 0x11b8174c0>: Failed to establish a new connection: [Errno 60] Operation timed out

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.9/site-packages/requests/adapters.py", line 439, in send
    resp = conn.urlopen(
  File "/usr/local/lib/python3.9/site-packages/urllib3/connectionpool.py", line 755, in urlopen
    retries = retries.increment(
  File "/usr/local/lib/python3.9/site-packages/urllib3/util/retry.py", line 574, in increment
    raise MaxRetryError(_pool, url, error or ResponseError(cause))
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='open.neis.go.kr', port=443): Max retries exceeded with url: /hub/mealServiceDietInfo?Type=json&Key=1475950391944d1c8831b761ade19ff6&ATPT_OFCDC_SC_CODE=B10&pIndex=1&pSize=1000&SD_SCHUL_CODE=7010254 (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x11b8174c0>: Failed to establish a new connection: [Errno 60] Operation timed out'))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/kyeonghwankim/Documents/nuvi/nuvi.py", line 85, in <module>
    main()
  File "/Users/kyeonghwankim/Documents/nuvi/nuvi.py", line 74, in main
    tempList.append(getMealDataWithSchoolCode(SD_SCHUL_CODE))
  File "/Users/kyeonghwankim/Documents/nuvi/nuvi.py", line 44, in getMealDataWithSchoolCode
    res = requests.get(url).json()
  File "/usr/local/lib/python3.9/site-packages/requests/api.py", line 75, in get
    return request('get', url, params=params, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/requests/api.py", line 61, in request
    return session.request(method=method, url=url, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/requests/sessions.py", line 542, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/local/lib/python3.9/site-packages/requests/sessions.py", line 655, in send
    r = adapter.send(request, **kwargs)
  File "/usr/local/lib/python3.9/site-packages/requests/adapters.py", line 516, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='open.neis.go.kr', port=443): Max retries exceeded with url: /hub/mealServiceDietInfo?Type=json&Key=1475950391944d1c8831b761ade19ff6&ATPT_OFCDC_SC_CODE=B10&pIndex=1&pSize=1000&SD_SCHUL_CODE=7010254 (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x11b8174c0>: Failed to establish a new connection: [Errno 60] Operation timed out'))
```

## with multiprocess

just stop 


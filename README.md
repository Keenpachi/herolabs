## Api handles parking data

Get parking data:
`/parking/{parking_id}`

`parking_id` - integer value

Put - update scheduler:
`/crawl/{parking_id}/{refresh_period}`

`refresh_period` - integer value in minutes

# install and run
```
pip install -r requirements.txt
uvicorn main:app --reload
```

# Run examples
get
```
curl -X 'GET' \
  'http://127.0.0.1:8000/parking/534013' \
  -H 'accept: application/json'
```
put
```
curl -X 'PUT' \
  'http://127.0.0.1:8000/crawl/534013/3' \
  -H 'accept: application/json'
```

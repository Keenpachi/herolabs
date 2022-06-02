## Api handles parking data

Get parking data:
`/parking/{parking_id}`

`parking_id` - integer value

Put - update scheduler:
`/crawl/{parking_id}/{refresh_period}`

`refresh_period` - integer value in minutes

# Run examples
get
```
http://127.0.0.1:8000/parking/534013
```
put
```
http://127.0.0.1:8000/crawl/534013/1
```

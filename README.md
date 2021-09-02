# pepserver
## Running
Build container:
```sh
docker build -t pepserver .      
```
Spin up server on port 8000:
```sh
docker run -e PORT="8000" -p 8000:8000 pepserver      
```
Run tests:
```sh
pytest tests -v
```

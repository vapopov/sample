# Sample search words

## Run application
    python app.py

## Run tests
    python -m tornado.test.runtests tests.search_test

## Request Examples

### Add sample documents to the storage
```bash
curl --request POST \
  --url http://localhost:8080/document/05e1b243-f5a1-4abe-bd59-d909fd225edd \
  --data 'Test text search1'
```

```bash
curl --request POST \
  --url http://localhost:8080/document/0c28d903-3fd5-437e-adf4-65b844e60c54 \
  --data 'Test text search2'
```

### Search them by terms

 With many terms and one
```bash
curl --request GET \
  --url 'http://localhost:8080/search?q=search1,search2' \
  --header 'postman-token: 06091cb5-d00a-7639-9596-a484a63cfdfd'
```

```bash
curl --request GET \
  --url 'http://localhost:8080/search?q=test' \
  --header 'postman-token: 06091cb5-d00a-7639-9596-a484a63cfdfd'
```
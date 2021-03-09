# Hail Query test

```bash
gcloud builds submit --tag australia-southeast1-docker.pkg.dev/leo-dev-290304/ar-sydney/query-test:latest .
```

```bash
python3 main.py
```

For Dataproc cluster creation to work, the corresponding service account in Hail Batch needs the following roles:

- Dataproc Administrator (at the project level)
- Dataproc Worker (at the project level)
- Service Account User (on itself...!)

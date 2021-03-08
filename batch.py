import hailtop.batch as hb

backend = hb.ServiceBackend(
    billing_project='leonhardgruenschloss-trial',
    bucket='gs://leo-tmp-au',
)

batch = hb.Batch(backend=backend, name='query test')

job = batch.new_job(name='main')
job.image(
    'australia-southeast1-docker.pkg.dev/leo-dev-290304/ar-sydney/query-test:latest'
)
job.command('python3 main.py')

batch.run()

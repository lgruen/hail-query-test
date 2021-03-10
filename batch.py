import uuid
import hailtop.batch as hb

IMAGE = 'australia-southeast1-docker.pkg.dev/leo-dev-290304/ar-sydney/query-test:latest'
REGION = 'australia-southeast1'
GCLOUD_AUTH = 'gcloud -q auth activate-service-account --key-file=/gsa-key/key.json'
GCLOUD_PROJECT = 'gcloud config set project hail-295901'


def add_query_script(batch, script, *, use_dataproc=False, depends_on=None):
    if use_dataproc:
        cluster_name = f'dataproc-{uuid.uuid4().hex}'

        start_job = batch.new_job(name='start Dataproc cluster')
        if depends_on:
            start_job.depends_on(start_job)
        start_job.image(IMAGE)
        start_job.command(GCLOUD_AUTH)
        start_job.command(GCLOUD_PROJECT)
        start_job.command(
            f'hailctl dataproc start --max-age 8h --region {REGION} --service-account='
            f'$(gcloud config list account --format "value(core.account)") '
            f'--num-preemptible-workers 20 '
            f'{cluster_name}'
        )

        main_job = batch.new_job(name='main')
        main_job.depends_on(start_job)
        main_job.image(IMAGE)
        main_job.command(GCLOUD_AUTH)
        main_job.command(GCLOUD_PROJECT)
        main_job.command(
            f'hailctl dataproc submit --region {REGION} {cluster_name} {script}'
        )

        stop_job = batch.new_job(name='stop Dataproc cluster')
        stop_job.depends_on(main_job)
        stop_job.always_run()  # Always clean up.
        stop_job.image(IMAGE)
        stop_job.command(GCLOUD_AUTH)
        stop_job.command(GCLOUD_PROJECT)
        stop_job.command(f'hailctl dataproc stop --region {REGION} {cluster_name}')

        return stop_job

    job = batch.new_job(name='main')
    if depends_on:
        job.depends_on(depends_on)
    job.image(IMAGE)
    job.command(f'python3 {script}')
    return job


if __name__ == '__main__':
    backend = hb.ServiceBackend(
        billing_project='leonhardgruenschloss-trial',
        bucket='leo-tmp-au',
    )

    batch = hb.Batch(backend=backend, name='query test')
    sample_qc_job = add_query_script(batch, 'sample_qc.py', use_dataproc=True)
    add_query_script(batch, 'plot.py', depends_on=sample_qc_job)
    batch.run()

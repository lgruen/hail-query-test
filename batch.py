import uuid
import hailtop.batch as hb
import click

IMAGE = 'australia-southeast1-docker.pkg.dev/leo-dev-290304/ar-sydney/query-test:latest'
REGION = 'australia-southeast1'
GCLOUD_AUTH = 'gcloud -q auth activate-service-account --key-file=/gsa-key/key.json'
GCLOUD_PROJECT = 'gcloud config set project hail-295901'


@click.command(help='Hail Query test')
@click.option(
    '--use-dataproc/--no-use-dataproc',
    help='Whether to use a Dataproc cluster instead of the Query backend',
)
def main(use_dataproc=False):
    backend = hb.ServiceBackend(
        billing_project='leonhardgruenschloss-trial',
        bucket='gs://leo-tmp-au',
    )

    run_query_script(backend, 'main.py', use_dataproc)


def run_query_script(backend, filename, use_dataproc):
    batch = hb.Batch(backend=backend, name=filename)

    if use_dataproc:
        cluster_name = f'dataproc-{uuid.uuid4().hex}'

        start_job = batch.new_job(name='start Dataproc cluster')
        start_job.image(IMAGE)
        start_job.command(GCLOUD_AUTH)
        start_job.command(GCLOUD_PROJECT)
        start_job.command(
            f'hailctl dataproc start --max-age 8h --region {REGION} --service-account='
            f'$(gcloud config list account --format "value(core.account)") '
            f'--packages selenium --num-preemptible-workers 20 '
            f'{cluster_name}'
        )

        main_job = batch.new_job(name='main')
        main_job.depends_on(start_job)
        main_job.image(IMAGE)
        main_job.command(GCLOUD_AUTH)
        main_job.command(GCLOUD_PROJECT)
        main_job.command(
            f'hailctl dataproc submit --region {REGION} {cluster_name} {filename}'
        )

        stop_job = batch.new_job(name='stop Dataproc cluster')
        stop_job.depends_on(main_job)
        stop_job.always_run()  # Always clean up.
        stop_job.image(IMAGE)
        stop_job.command(GCLOUD_AUTH)
        stop_job.command(GCLOUD_PROJECT)
        stop_job.command(f'hailctl dataproc stop --region {REGION} {cluster_name}')
    else:
        job = batch.new_job(name='main')
        job.image(IMAGE)
        job.command('python3 {filename}')

    batch.run()


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter

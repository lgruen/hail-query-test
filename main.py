import hail as hl
from bokeh.io import export_svgs

GNOMAD_HGDP_1KG = 'gs://gcp-public-data--gnomad/release/3.1/mt/genomes/gnomad.genomes.v3.1.hgdp_1kg_subset_dense.mt'
OUTPUT_BUCKET = 'gs://leo-tmp-au/hail-query-test'
CALL_RATE_PLOT = 'call_rate.svg'
MEAN_SAMPLE_GQ_PLOT = 'mean_sample_gq.svg'

# Results in "hail.utils.java.FatalError: IOException: No FileSystem for scheme: gs".
# hl.init()

hl.context.init_service(
    billing_project='leonhardgruenschloss-trial',
    bucket='gs://leo-tmp-au',
    default_reference='GRCh38',
)

mt = hl.read_matrix_table(GNOMAD_HGDP_1KG)
mt_qc = hl.sample_qc(mt)


def plot_svg_to_gcs(plot, filename):
    export_svgs(call_rate_plot, filename)
    hl.hadoop_copy(filename, f'{OUTPUT_BUCKET}/{filename}')


call_rate_plot = hl.plot.histogram(
    mt_qc.sample_qc.call_rate, range=(0.88, 1), legend='Call Rate'
)
plot_svg_to_gcs(call_rate_plot, CALL_RATE_PLOT)

mean_sample_gq_plot = hl.plot.histogram(
    mt_qc.sample_qc.gq_stats.mean, legend='Mean Sample GQ'
)
plot_svg_to_gcs(mean_sample_gq_plot, MEAN_SAMPLE_GQ_PLOT)

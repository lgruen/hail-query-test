import hail as hl
from bokeh.io import export_svgs

OUTPUT_BUCKET = 'gs://leo-tmp-au/hail-query-test'
SAMPLE_QC_MT = 'f{OUTPUT_BUCKET}/gnomad_hgdp_sample_qc.mt'
CALL_RATE_PLOT = 'call_rate.svg'
MEAN_SAMPLE_GQ_PLOT = 'mean_sample_gq.svg'

hl.init()

mt = hl.read_matrix_table(SAMPLE_QC_MT)


def plot_svg_to_gcs(plot, filename):
    export_svgs(call_rate_plot, filename)
    hl.hadoop_copy(filename, f'{OUTPUT_BUCKET}/{filename}')


call_rate_plot = hl.plot.histogram(
    mt.sample_qc.call_rate, range=(0.88, 1), legend='Call Rate'
)
plot_svg_to_gcs(call_rate_plot, CALL_RATE_PLOT)

mean_sample_gq_plot = hl.plot.histogram(
    mt.sample_qc.gq_stats.mean, legend='Mean Sample GQ'
)
plot_svg_to_gcs(mean_sample_gq_plot, MEAN_SAMPLE_GQ_PLOT)

import hail as hl

GNOMAD_HGDP_1KG = 'gs://gcp-public-data--gnomad/release/3.1/mt/genomes/gnomad.genomes.v3.1.hgdp_1kg_subset_dense.mt'
OUTPUT_BUCKET = 'gs://leo-tmp-au/hail-query-test'
SAMPLE_QC_MT = f'{OUTPUT_BUCKET}/gnomad_hgdp_sample_qc.mt'

hl.init(default_reference='GRCh38')

if not hl.hadoop_exists(SAMPLE_QC_MT):
    mt = hl.read_matrix_table(GNOMAD_HGDP_1KG)
    mt_qc = hl.sample_qc(mt)
    mt_qc.write(SAMPLE_QC_MT)
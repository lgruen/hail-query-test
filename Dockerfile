FROM australia-southeast1-docker.pkg.dev/analysis-runner/images/driver:7f1a676f0b1e734981878576f6f091689e7d71c1-hail-0.2.64.dev201e81ff56c5

COPY sample_qc.py plot.py ./

FROM australia-southeast1-docker.pkg.dev/analysis-runner/images/driver:c84579d581ea5be372d9d3673346d347f381a1be-hail-0.2.63.dev47eefe392051

# hailctl dataproc invokes gcloud beta dataproc, which isn't default-installed.
RUN gcloud -q components install beta

# Enable bokeh image exports.
RUN conda install -c bokeh selenium

ENV HAIL_QUERY_BACKEND service

COPY main.py .

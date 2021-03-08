FROM australia-southeast1-docker.pkg.dev/analysis-runner/images/driver:5e5fc1116836e996244b364ee291ca472b8b1938-hail-0.2.63.devaf814aa68ce8

ENV HAIL_QUERY_BACKEND service

COPY main.py .

FROM texlive/texlive:TL2023-historic
LABEL maintainer="Patrick Baus <patrick.baus@physik.tu-darmstadt.de>"
LABEL description="PhD thesis figure compilation environment."

ENV VIRTUAL_ENV=/opt/venv
ENV DEBIAN_FRONTEND=noninteractive

RUN \
    apt update && \
    apt install -y python3.12-venv && \
    python3 -m venv --upgrade-deps $VIRTUAL_ENV && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt gen_matplotlib_cache.py /

RUN \
    pip install -r /requirements.txt && \
    mktexfmt xelatex.fmt && \
    python /gen_matplotlib_cache.py

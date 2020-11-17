FROM lambci/lambda:build-provided.al2

RUN yum install -q -y wget \
    readline-devel curl-devel \
    xorg-x11-server-devel libX11-devel libXt-devel \
    gcc-c++ gcc-gfortran \
    zlib-devel libbz2-devel bzip2 bzip2-libs

ARG VERSION=4.0.3
ARG R_DIR=/opt/R/

RUN wget -q https://cran.r-project.org/src/base/R-4/R-${VERSION}.tar.gz && \
  mkdir ${R_DIR} && \
  tar -xf R-${VERSION}.tar.gz && \
  mv R-${VERSION}/* ${R_DIR} && \
  rm R-${VERSION}.tar.gz

WORKDIR ${R_DIR}

RUN ./configure --prefix=${R_DIR} --exec-prefix=${R_DIR} --with-libpth-prefix=/opt/ --enable-R-shlib && \
   make && \
   cp /usr/lib64/libgfortran.so.3 lib/ && \
   cp /usr/lib64/libgomp.so.1 lib/ && \
   cp /usr/lib64/libquadmath.so.0 lib/ && \
   cp /usr/lib64/libstdc++.so.6 lib/
RUN yum install -q -y openssl-devel libxml2-devel && \
   ./bin/Rscript -e 'install.packages(c("httr", "logging", "yaml", "jsonlite", "aws.s3"), repos="http://cran.r-project.org")'
CMD mkdir -p /var/r/ && \
   cp -r bin/ lib/ etc/ library/ doc/ modules/ share/ /var/r/

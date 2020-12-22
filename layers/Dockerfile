FROM lambci/lambda:build-provided.al2

RUN amazon-linux-extras enable R4 && \
  yum install -q -y wget curl-devel openssl-devel libxml2-devel R && \
  Rscript -e 'install.packages(c("httr", "logging", "yaml", "jsonlite", "aws.s3"), repos="http://cran.r-project.org")' && \
  Rscript -e 'install.packages(c("Matrix", "survival", "gridExtra", "lattice", "gbm"), repos="http://cran.r-project.org")' && \
  mkdir -p /opt/R

WORKDIR /opt/R

RUN cp -R /usr/lib64/R/* . && \
  cp /usr/lib64/libgomp.so.1 lib/ && \
  cp /usr/lib64/libquadmath.so.0 lib/ && \
  cp /usr/lib64/libstdc++.so.6 lib/

CMD mkdir -p /var/r/ && \
  mkdir -p /var/r-gbm/R/library/ && \
  cp -R bin/ etc/ lib/ library/ modules/ /var/r/ && \
  cp -R library/Matrix library/survival library/gridExtra library/gtable library/lattice library/gbm /var/r-gbm/R/library/

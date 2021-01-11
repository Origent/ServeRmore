FROM lambci/lambda:build-provided.al2

RUN amazon-linux-extras enable R4 && \
 yum install -q -y wget R readline-devel libXt-devel curl-devel && \ 
 #yum install -q -y wget curl-devel openssl-devel libxml2-devel R && \
 # Rscript -e 'install.packages(c("httr", "logging", "yaml", "jsonlite", "aws.s3"), repos="http://cran.r-project.org")' && \
  #Rscript -e 'install.packages(c("Matrix", "survival", "gridExtra", "lattice", "gbm"), repos="http://cran.r-project.org")' && \
  mkdir -p /opt/R

ARG VERSION=4.0.2
ARG R_DIR=/opt/R/

RUN cd ~ && \
  wget -q https://cran.r-project.org/src/base/R-4/R-${VERSION}.tar.gz && \
  # mkdir ${R_DIR} && \
  tar -xf R-${VERSION}.tar.gz && \ 
  mv R-${VERSION}/* ${R_DIR} && \
  rm R-${VERSION}.tar.gz

WORKDIR /opt/R/

RUN ./configure --prefix=${R_DIR} --enable-R-shlib && \
  make && \
  cp /usr/lib64/libgomp.so.1 lib/ && \
  cp /usr/lib64/libgfortran.so.4 lib/ && \   
  cp /usr/lib64/libquadmath.so.0 lib/ && \
  cp /usr/lib64/libpcre2-8.so.0 lib/
  # cp /usr/lib64/libstdc++.so.6 lib/

CMD mkdir -p /var/r/ && \
  cp -r bin/ lib/ etc/ library/ doc/ modules/ share/ /var/r/ 

# CMD mkdir -p /var/r/ && \
# mkdir -p /var/r-gbm/R/library/ && \
# cp -R bin/ etc/ lib/ library/ modules/ /var/r/ && \
# cp -R library/Matrix library/survival library/gridExtra library/gtable library/lattice library/gbm /var/r-gbm/R/library/

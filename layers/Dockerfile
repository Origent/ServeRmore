FROM lambci/lambda:build-provided.al2

RUN amazon-linux-extras enable R4 && \
    yum clean metadata && \
    yum install -q -y R wget readline-devel curl-devel xorg-x11-server-devel libXt-devel

ARG VERSION=4.0.2
ARG R_DIR=/opt/R/

RUN cd ~ && \
  wget -q https://cran.r-project.org/src/base/R-4/R-${VERSION}.tar.gz && \
  mkdir ${R_DIR} && \
  tar -xf R-${VERSION}.tar.gz && \
  mv R-${VERSION}/* ${R_DIR} && \
  rm R-${VERSION}.tar.gz

WORKDIR ${R_DIR}

RUN ./configure --prefix=${R_DIR} --exec-prefix=${R_DIR} --with-libpth-prefix=/opt/ --enable-R-shlib && \
   make && \
   sed -i '122s/.*/SED=\/bin\/sed/' bin/R && \
   cp /usr/lib64/libgfortran.so.4 lib/ && \
   cp /usr/lib64/libgomp.so.1 lib/ && \
   cp /usr/lib64/libquadmath.so.0 lib/ && \
   cp /usr/lib64/libstdc++.so.6 lib/ && \
   cp /usr/lib64/libpcre2-8.so.0 lib/ && \ 
   cp /usr/lib64/libm.so.6 lib/ && \
   cp /usr/lib64/libc.so.6 lib/ 

RUN yum install -q -y openssl-devel libxml2-devel && \
   ./bin/Rscript -e 'install.packages(c("httr", "logging", "yaml", "jsonlite", "aws.s3"), repos="http://cran.r-project.org")'

CMD mkdir -p /var/r/ && \
   cp -r bin/ lib/ etc/ library/ doc/ modules/ share/ /var/r/

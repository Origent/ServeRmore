FROM lambci/lambda:build-provided.al2

RUN amazon-linux-extras enable R4 && \
 yum install -q -y wget readline-devel libXt-devel curl-devel bzip2-devel xz-devel pcre2-devel java-1.8.0-openjdk-devel openssl-devel libxml2-devel which && \ 
 mkdir -p /opt/R/bin && \
 mv /usr/bin/which /opt/R/bin

ARG VERSION
ARG PACKAGES
ARG R_DIR=/opt/R/
ENV PATH="/opt/R/bin:${PATH}"

RUN cd ~ && \
  wget -q https://cran.r-project.org/src/base/R-4/R-${VERSION}.tar.gz && \
  tar -xf R-${VERSION}.tar.gz && \ 
  mv R-${VERSION}/* ${R_DIR} && \
  rm R-${VERSION}.tar.gz

WORKDIR /opt/R/

RUN ./configure --prefix=${R_DIR} --exec-prefix=${R_DIR} --with-libpth-prefix=/opt/ --enable-R-shlib  && \
  make && \ 
  cp /usr/lib64/libgomp.so.1 lib/ && \
  cp /usr/lib64/libgfortran.so.4 lib/ && \
  cp /usr/lib64/libquadmath.so.0 lib/ && \
  cp /usr/lib64/libpcre2-8.so.0 lib/

RUN for i in ${PACKAGES}; do ./bin/Rscript -e "install.packages(\"$i\", repos=\"https://cran.r-project.org\")"; done;

CMD mkdir -p /var/r/ && \
  cp -r bin/ lib/ etc/ library/ doc/ modules/ share/ /var/r/

#!/bin/bash

set -euo pipefail

BUILD_DIR=/var/r-gbm/
R_DIR=/opt/R/

export R_LIBS=${BUILD_DIR}/R/library
mkdir -p ${R_LIBS}
${R_DIR}/bin/Rscript -e 'install.packages("Matrix", repos="http://cran.r-project.org")'
${R_DIR}/bin/Rscript -e 'install.packages("survival", repos="http://cran.r-project.org")'
${R_DIR}/bin/Rscript -e 'install.packages("gridExtra", repos="http://cran.r-project.org")'
${R_DIR}/bin/Rscript -e 'install.packages("lattice", repos="http://cran.r-project.org")'
${R_DIR}/bin/Rscript -e 'install.packages("gbm", repos="http://cran.r-project.org")'

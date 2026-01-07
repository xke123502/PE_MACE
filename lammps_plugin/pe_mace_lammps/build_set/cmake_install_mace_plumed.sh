cmake \
    -D CMAKE_BUILD_TYPE=Release \
    -D CMAKE_INSTALL_PREFIX=$(pwd) \
    -D CMAKE_CXX_STANDARD=17 \
    -D CMAKE_CXX_STANDARD_REQUIRED=ON \
    -D BUILD_MPI=ON \
    -D BUILD_SHARED_LIBS=ON \
    -D PKG_KOKKOS=ON \
    -D Kokkos_ENABLE_CUDA=ON \
    -D CMAKE_CXX_COMPILER=$(pwd)/../lib/kokkos/bin/nvcc_wrapper \
    -D Kokkos_ARCH_HOSTARCH=yes \
    -D Kokkos_ARCH_GPUARCH=yes \
    -D Kokkos_ENABLE_CUDA=yes \
    -D Kokkos_ENABLE_OPENMP=yes \
    -D CMAKE_PREFIX_PATH=$(pwd)/../../libtorch-gpu \
    -D PKG_ML-MACE=ON \
    -D PKG_PLUMED=yes \
    -D PLUMED_INCLUDE_DIR=/home/jwzhou/bin/plumed6/include \
    -D PLUMED_LIBRARY=/home/jwzhou/bin/plumed6/lib/libplumed.so \
    -D DOWNLOAD_PLUMED=no \
    -D BUILD_PLUMED=no \
    -D PLUMED_MODE=shared \
    -D CMAKE_CXX_FLAGS="-I/home/jwzhou/bin/plumed6/include" \
    -D GSL_INCLUDE_DIR=/home/jwzhou/bin/gsl/include \
    -D GSL_LIBRARY=/home/jwzhou/bin/gsl/lib \
    -D GSL_CBLAS_LIBRARY=/home/jwzhou/bin/gsl/lib \
    ../cmake
make -j 128
make install

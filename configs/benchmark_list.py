import os
import subprocess

POLYBENCH_ROOT = "/home/jerry/projects/gem5/workloads/PolyBenchC-4.2.1"

POLYBENCH_BENCHMARKS = {
    "correlation":      os.path.join(POLYBENCH_ROOT, "datamining/correlation/correlation"),
    "covariance":       os.path.join(POLYBENCH_ROOT, "datamining/covariance/covariance"),
    "2mm":              os.path.join(POLYBENCH_ROOT, "linear-algebra/kernels/2mm/2mm"),
    "3mm":              os.path.join(POLYBENCH_ROOT, "linear-algebra/kernels/3mm/3mm"),
    "atax":             os.path.join(POLYBENCH_ROOT, "linear-algebra/kernels/atax/atax"),
    "bicg":             os.path.join(POLYBENCH_ROOT, "linear-algebra/kernels/bicg/bicg"),
    "doitgen":          os.path.join(POLYBENCH_ROOT, "linear-algebra/kernels/doitgen/doitgen"),
    "mvt":              os.path.join(POLYBENCH_ROOT, "linear-algebra/kernels/mvt/mvt"),
    "gemm":             os.path.join(POLYBENCH_ROOT, "linear-algebra/blas/gemm/gemm"),
    "gemver":           os.path.join(POLYBENCH_ROOT, "linear-algebra/blas/gemver/gemver"),
    "gesummv":          os.path.join(POLYBENCH_ROOT, "linear-algebra/blas/gesummv/gesummv"),
    "symm":             os.path.join(POLYBENCH_ROOT, "linear-algebra/blas/symm/symm"),
    "syr2k":            os.path.join(POLYBENCH_ROOT, "linear-algebra/blas/syr2k/syr2k"),
    "syrk":             os.path.join(POLYBENCH_ROOT, "linear-algebra/blas/syrk/syrk"),
    "trmm":             os.path.join(POLYBENCH_ROOT, "linear-algebra/blas/trmm/trmm"),
    "cholesky":         os.path.join(POLYBENCH_ROOT, "linear-algebra/solvers/cholesky/cholesky"),
    "durbin":           os.path.join(POLYBENCH_ROOT, "linear-algebra/solvers/durbin/durbin"),
    "gramschmidt":      os.path.join(POLYBENCH_ROOT, "linear-algebra/solvers/gramschmidt/gramschmidt"),
    "lu":               os.path.join(POLYBENCH_ROOT, "linear-algebra/solvers/lu/lu"),
    "ludcmp":           os.path.join(POLYBENCH_ROOT, "linear-algebra/solvers/ludcmp/ludcmp"),
    "trisolv":          os.path.join(POLYBENCH_ROOT, "linear-algebra/solvers/trisolv/trisolv"),
    "deriche":          os.path.join(POLYBENCH_ROOT, "medley/deriche/deriche"),
    "floyd-warshall":   os.path.join(POLYBENCH_ROOT, "medley/floyd-warshall/floyd-warshall"),
    "nussinov":         os.path.join(POLYBENCH_ROOT, "medley/nussinov/nussinov"),
    "adi":              os.path.join(POLYBENCH_ROOT, "stencils/adi/adi"),
    "fdtd-2d":          os.path.join(POLYBENCH_ROOT, "stencils/fdtd-2d/fdtd-2d"),
    "heat-3d":          os.path.join(POLYBENCH_ROOT, "stencils/heat-3d/heat-3d"),
    "jacobi-1d":        os.path.join(POLYBENCH_ROOT, "stencils/jacobi-1d/jacobi-1d"),
    "jacobi-2d":        os.path.join(POLYBENCH_ROOT, "stencils/jacobi-2d/jacobi-2d"),
    "seidel-2d":        os.path.join(POLYBENCH_ROOT, "stencils/seidel-2d/seidel-2d"),
}


def prepare_benchmark(benchmark_name):
    """Recompile the given benchmark: make clean && make"""
    if benchmark_name not in POLYBENCH_BENCHMARKS:
        print(f"Error: Unknown benchmark '{benchmark_name}'")
        return

    benchmark_path = POLYBENCH_BENCHMARKS[benchmark_name]
    benchmark_dir = os.path.dirname(benchmark_path)

    try:
        print(f"Recompiling {benchmark_name} in {benchmark_dir}...")
        subprocess.run(["make", "clean"], cwd=benchmark_dir, check=True)
        subprocess.run(["make"], cwd=benchmark_dir, check=True)
        print(f"{benchmark_name} recompiled successfully!")
        return benchmark_path
    except subprocess.CalledProcessError as e:
        print(f"Failed to compile {benchmark_name}: {e}")

# X-DRL: Explainable Deep Reinforcement Learning for Sensor Placement in Water Distribution Networks

X-DRL is a Python research-software framework for investigating sensor-placement strategies in water distribution networks using deep reinforcement learning (DQN) and genetic algorithms (GA). It brings together network loading, graph-based coverage calculations, optimisation, benchmark execution, and supporting analysis utilities, with an emphasis on transparent experimental protocols and reproducibility.

**Repository status:** Corrected research-software working revision 1.0.0; release preparation is in progress. Regression tests, clean Linux and Windows CPU environment checks, and reduced-size integration smoke tests have passed. The full historical benchmark and independent full-scale reproduction have not been completed. Do not describe this working revision as a fully independently reproduced release.

## Scope and contents

- `src/`: DQN and GA engines, configuration, and analysis utilities.
- `benchmarks/`: Historical and safer benchmark drivers, plus instructions for obtaining network input files.
- `tests/`: Regression tests.
- `AUTHORS.md`: Author information and CRediT contributions.
- `CITATION.cff`: Software citation metadata.
- `RELEASE_NOTES.md`: Summary of corrections and validation evidence.

## Experimental protocols

The default DQN configuration uses coverage weight 0.70 and centrality weight 0.30. The historical 60-run benchmark driver explicitly uses the historical coverage-only weights (1.0 / 0.0); these protocols must not be conflated.

The GA configuration records the effective historical settings: population 100, generations 1000, mutation 0.10, crossover 0.80, and tournament size 5. Network sensor budgets are defined in `src/config.py`.

## Installation

### Linux / WSL2: pinned CPU environment (Python 3.12)

A hash-locked environment is provided for Linux x86-64 with Python 3.12 and CPU-only PyTorch. This is the clean environment configuration that was installed and tested during release preparation. It is platform-specific; do not use it as a Windows, macOS, or CUDA-enabled installation specification.

Install [uv](https://docs.astral.sh/uv/) first, then run from the repository root:

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python --require-hashes -r requirements-linux-cpu-py312.lock.txt
```

The Linux lock file includes the PyPI index and the official PyTorch CPU wheel index. It pins direct and transitive dependencies and includes hashes. The corresponding direct-dependency input is `requirements-linux-cpu-py312.in`; the lock was generated with uv for Python 3.12 on `x86_64-unknown-linux-gnu`.

Verify the installation:

```bash
.venv/bin/python -m pip check
.venv/bin/python -m compileall -q src benchmarks tests
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
```

### Windows 10/11: pinned CPU environment (Python 3.12)

A hash-locked environment is provided for 64-bit Windows with Python 3.12 and CPU-only PyTorch. This platform-specific configuration was installed and tested during release preparation. It should not be used as a Linux, macOS, or CUDA installation specification.

Install [uv](https://docs.astral.sh/uv/) first, then run from the repository root:

```powershell
uv venv .venv --python 3.12
uv pip install --python .\.venv\Scripts\python.exe --index-strategy unsafe-best-match --require-hashes -r requirements-windows-cpu-py312.lock.txt
```

The Windows lock file includes PyPI and the official PyTorch CPU wheel index. It pins direct and transitive dependencies and includes package hashes. The corresponding direct-dependency input is `requirements-windows-cpu-py312.in`; the lock was generated with uv for Python 3.12 on `x86_64-pc-windows-msvc`.

The `--index-strategy unsafe-best-match` option allows uv to resolve packages across both declared indexes. Hash verification remains enabled through `--require-hashes`.

Verify the installation:

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m compileall -q src benchmarks tests
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Virtual-environment activation is not required. Running the environment's Python executable directly avoids changing the machine's PowerShell execution policy.

### macOS / other environments

For macOS and other environments not covered by a platform-specific lock, use a clean Python 3.12 environment and the provisional declarations in `requirements.txt`. The general requirements file remains unpinned. No macOS validation or cross-platform dependency matrix is currently claimed.

The Linux and Windows CPU locks improve reproducibility for their respective tested platforms. They do not establish a tested macOS or CUDA dependency matrix.

## Tests

From the repository root:

```bash
python -m compileall -q src benchmarks tests
python -m unittest discover -s tests -v
```

**Recorded clean Linux validation** used WSL2, Ubuntu 26.04.1 LTS, and Python 3.12.16:

- Python compilation completed successfully.
- All 15 regression tests passed.
- `pip check` reported no broken requirements.
- Principal dependencies, including PyTorch, WNTR, NumPy, pandas, NetworkX, SciPy, Matplotlib, and SHAP, imported successfully.
- The Linux CPU lock resolved and installed 33 packages in a clean isolated environment with hash verification.

**Recorded clean Windows validation** used Windows 10/11, Python 3.12.10, and a CPU-only PyTorch environment:

- The Windows hash-locked environment installed all 34 resolved packages.
- `pip check` reported no broken requirements.
- PyTorch, WNTR, NumPy, pandas, NetworkX, SciPy, Matplotlib, and SHAP imported successfully.
- Python compilation completed successfully.
- All 15 regression tests passed.
- A WNTR-bundled Net3 EPANET smoke test completed successfully, producing pressure and flow results.

These checks establish installation, dependency consistency, regression-test execution, and limited integration evidence. They do not constitute a full benchmark reproduction.

## Integration and hydraulic simulation validation

Controlled, reduced-size DQN and GA integration smoke tests completed successfully on Hanoi, Net3, and C-Town. Selected sensor counts respected the configured budgets. DQN output artifacts were checked for internal consistency, including checkpoints, metadata, evaluation states, and reward histories. GA sensor selections were checked against the corresponding network graphs.

Separate WNTR/EPANET hydraulic simulation smoke tests successfully loaded and simulated all three network inputs in the Linux validation environment.

A separate Windows EPANET smoke test used WNTR's bundled Net3 network. The one-hour simulation completed successfully, producing pressure and flow results. This Windows check was an integration smoke test, not a full benchmark or a leak/contamination detection experiment.

**C-Town qualification:** WNTR reported that some C-Town curves were not assigned explicit curve types. Inspection established that curves 8–11 are referenced by the eleven pumps and identified as HEAD curves; curves 1–7 were imported with type=None. The original input was retained without modification. This warning does not directly affect the graph-based DQN and GA placement objectives, which use network topology, shortest-path coverage, and node centrality. However, successful loading and simulation alone do not establish complete hydraulic model fidelity.

The integration tests used reduced episode and generation counts. They establish execution of the software components on the three networks; they do not reproduce the historical 1000-episode DQN and 1000-generation GA experiments. They do not independently establish validated leak-detection or contamination-detection performance.

## Benchmark network inputs and execution

The Hanoi, Net3, and C-Town `.inp` files are intentionally **not included** in this public repository because their individual redistribution terms and attribution requirements have not all been established. See [benchmarks/README.md](benchmarks/README.md) for the input-file policy and local setup instructions. Do not assume that the MIT licence for X-DRL also applies to third-party benchmark data.

The historical driver, `benchmarks/42_final_benchmark_1000.py`, is retained in the research workspace for provenance and is not the recommended public execution entry point. It writes fixed result filenames and lacks the output-directory safeguards of the safer driver.

For a future full benchmark, use `benchmarks/run_historical_benchmark.py`. It checks required input files, creates a new UTC-timestamped output directory under `results/benchmark_runs/` by default, refuses to reuse an existing output directory, and records input hashes and protocol settings in a run manifest. Inspect options with:

```bash
python benchmarks/run_historical_benchmark.py --help
```

The full experiment comprises three networks, ten seeds, and two methods (60 method runs). It was not executed during this validation phase. Do not launch a full run until configuration, input provenance, computational requirements, and output location have been reviewed.

## SHAP workflow

The SHAP utility is a preliminary, checkpoint- and state-driven analysis tool. It explains a selected action value for supplied observed evaluation states; it does not establish causal effects, explain all policy behaviour, or validate explanations across all networks. The selected action index must be justified by the research question.

## Statistical analysis

The statistical utility rejects the historical `BestReward` CSV as a cross-method outcome because GA coverage fitness and DQN cumulative episode reward are not a common metric. It expects a separately generated `evaluation_metrics.csv` with columns:

`Network,Method,Seed,Metric,Value`

The same independently defined metric and evaluation procedure must be applied to both algorithms before matched-seed inference is attempted.

## Reproducibility and limitations

- Regression tests, reduced-size integration smoke tests, and hydraulic simulation smoke tests are distinct levels of evidence and must be reported separately.
- Historical results have not been overwritten or regenerated as part of the correction work.
- Runtime provenance differences and distinct DQN reward protocols remain documented limitations.
- The SHAP workflow is preliminary.
- Do not claim complete independent reproduction or validated leak/contamination detection from the current tests alone.
- Linux and Windows CPU-specific Python 3.12 hashed lock files are provided and have passed clean installation checks.
- The generic `requirements.txt` remains unpinned. No macOS or CUDA dependency validation is claimed.

## Licence

The original X-DRL software code and documentation in this repository are released under the MIT License, approved by all three copyright holders. Third-party benchmark network inputs are excluded and may be subject to separate terms. See [LICENSE](LICENSE) and [benchmarks/README.md](benchmarks/README.md).

## Authors and citation

See [AUTHORS.md](AUTHORS.md) for author affiliations, ORCID identifiers, and approved CRediT contributions. Cite the software using [CITATION.cff](CITATION.cff). An archival DOI will be added after a versioned release is deposited in a repository such as Zenodo.
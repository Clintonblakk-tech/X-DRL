# Corrected working revision — 2026-10-30

- Centralised GA and DQN hyperparameters and passed configuration explicitly.
- Preserved effective historical GA settings and explicit historical DQN coverage-only weights.
- Corrected DQN best-episode sensor/checkpoint tracking and exported actual visited states.
- Masked already-selected actions in DQN next-state bootstrapping.
- Replaced synthetic-state SHAP workflow with a checkpoint/state-driven CLI.
- Replaced raw reward significance testing with validation of common evaluation metrics.
- Added regression tests for configuration, chromosome repair, DQN masking, replay-buffer copying, and statistical input validation.
- No full benchmark was executed; historical results were not modified.
- This is a corrected working revision, not yet a fully validated independent-reproduction release.

## Linux validation and release-preparation update — 2026-10-31

### Environment and installation
- Created an isolated Linux validation environment using WSL2, Ubuntu 26.04.1 LTS, and Python 3.12.16.
- Installed the declared dependencies successfully.
- Verified principal package imports, including PyTorch, WNTR, NumPy, pandas, NetworkX, SciPy, Matplotlib, and SHAP.
- Confirmed that `pip check` reported no broken requirements.

### Pinned Linux CPU environment — Python 3.12
- Added `requirements-linux-cpu-py312.in` as the direct-dependency input and `requirements-linux-cpu-py312.lock.txt` as the generated, hash-locked environment.
- The lock targets Linux x86-64 / `x86_64-unknown-linux-gnu` with CPU-only PyTorch and includes both the PyPI index and the official PyTorch CPU wheel index.
- Resolved and locked 33 packages, including transitive dependencies. The direct dependency pins are NumPy 2.5.4, pandas 3.1.0, PyTorch 2.15.0+cpu, NetworkX 3.7, WNTR 1.5.0, Matplotlib 3.11.2, SciPy 1.18.1, and SHAP 0.54.1.
- Installed the hash-locked requirements into a fresh, isolated Python 3.12.16 environment; the existing validated development environment was not replaced.
- The clean-environment verification is scoped to this Linux CPU platform. The general `requirements.txt` remains unpinned for other platforms and CUDA configurations; a universal cross-platform dependency matrix has not been established.

### Windows validation and pinned CPU environment — Python 3.12
- Added `requirements-windows-cpu-py312.in` as the direct-dependency input and `requirements-windows-cpu-py312.lock.txt` as the generated, hash-locked environment.
- The lock targets Windows x86-64 / `x86_64-pc-windows-msvc`, uses CPU-only PyTorch, and includes the PyPI index and official PyTorch CPU wheel index.
- Resolved and locked 34 packages, including transitive dependencies. The lock file SHA-256 is `FCB352686C4E99AA7FC2EDEA55AD2498922A76D8909C2DD6A83831DC885DCA38`.
- Installed the lock into a fresh isolated Windows Python 3.12.10 environment using hash verification (`--require-hashes`) and `--index-strategy unsafe-best-match`. The install completed successfully.
- `pip check` reported no broken requirements; principal imports (including PyTorch, WNTR, NumPy, pandas, NetworkX, SciPy, Matplotlib, and SHAP) passed; Python compilation passed; all 15 regression tests passed.
- A separate one-hour WNTR-bundled Net3 EPANET hydraulic smoke test passed, producing pressure and flow result arrays. This is a smoke test, not a full benchmark.
- An earlier Windows WNTR compiled-extension import restriction did not recur in the final clean Python 3.12.10 environment. Smart App Control was not disabled.
- Windows validation is scoped to this CPU environment; it does not establish macOS, CUDA, or universal cross-platform compatibility.

### Software verification
- Linux: Python compilation completed successfully; all 15 regression tests passed; controlled DQN and GA integration smoke tests completed on Hanoi, Net3, and C-Town; DQN output artifacts and GA sensor selections passed the recorded consistency checks; separate WNTR/EPANET hydraulic simulation smoke tests completed on all three networks.
- Windows: Python compilation, all 15 regression tests, principal package imports, `pip check`, and the one-hour Net3 EPANET smoke test passed.
- Verified the safer benchmark driver's command-line interface and existing-output-directory protection.

### C-Town diagnostic
- Inspected all eleven pump definitions and their referenced curves.
- Confirmed that curves 8–11 are referenced by the pumps and identified by WNTR as HEAD curves.
- Curves 1–7 were imported with type=None.
- Retained the original benchmark input without modification.
- Hydraulic model fidelity remains qualified by this warning.

### Repository integrity
- Recovered and verified the safer benchmark driver against its GitHub blob.
- Added the driver to the local checksum manifest.
- Removed generated Python cache directories and temporary EPANET files.
- Verified all 18 entries in the local SHA256SUMS.txt manifest.
- Confirmed that all three software copyright holders approved the MIT licence already published in the repository.
- Added the Linux and Windows CPU dependency inputs and lock files to the release-validation branch.

### Outstanding release requirements
- Final benchmark-input redistribution and attribution decisions.
- Final repository and citation metadata review.
- Versioned archival release and persistent DOI.
- Final manuscript-to-software consistency review.
- macOS and CUDA environments have not been validated; the general `requirements.txt` remains unpinned.

### Experimental scope
No full 60-run benchmark was executed during this validation phase. Historical experimental results were preserved. Reduced-size integration smoke tests and the Windows Net3 EPANET smoke test must not be represented as full experimental reproduction or independent validation of leak-detection and contamination-detection performance.

The workspace remains a corrected research-software working revision and is not yet a finalized public release.

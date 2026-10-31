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
- Recorded a separate Windows WNTR import restriction associated with Windows Code Integrity Application Control. Smart App Control was not disabled.

### Pinned Linux CPU environment — Python 3.12

- Added `requirements-linux-cpu-py312.in` as the direct-dependency input and `requirements-linux-cpu-py312.lock.txt` as the generated, hash-locked environment.
- The lock targets Linux x86-64 / `x86_64-unknown-linux-gnu` with CPU-only PyTorch and includes both the PyPI index and the official PyTorch CPU wheel index.
- Resolved and locked 33 packages, including transitive dependencies. The direct dependency pins are NumPy 2.5.4, pandas 3.1.0, PyTorch 2.15.0+cpu, NetworkX 3.7, WNTR 1.5.0, Matplotlib 3.11.2, SciPy 1.18.1, and SHAP 0.54.1.
- Installed the hash-locked requirements into a fresh, isolated Python 3.12.16 environment; the existing validated development environment was not replaced.
- The clean-environment verification is scoped to this Linux CPU platform. The general `requirements.txt` remains unpinned for other platforms and CUDA configurations; a cross-platform dependency matrix has not been established.

### Software verification
- Python compilation completed successfully.
- All 15 regression tests passed.
- Controlled DQN and GA integration smoke tests completed on Hanoi, Net3, and C-Town.
- DQN output artifacts and GA sensor selections passed the recorded consistency checks.
- Separate WNTR/EPANET hydraulic simulation smoke tests completed on all three networks.
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
- Updated the local README to document validation evidence and remaining limitations.
- Confirmed that all three software copyright holders approved the MIT licence already published in the repository.

### Outstanding release requirements
- Windows Python 3.12 support remains under validation. Added `requirements-windows-cpu-py312.in` as a candidate direct-dependency input; no Windows lock has been generated or validated yet. The earlier Windows WNTR compiled-extension import restriction remains unresolved, and Smart App Control was retained.
- Validation of additional platform-specific environments (including Windows and CUDA configurations); the general `requirements.txt` remains unpinned.
- Final benchmark-input redistribution and attribution decisions.
- Final repository and citation metadata review.
- Versioned archival release and persistent DOI.
- Final manuscript-to-software consistency review.

### Experimental scope
No full 60-run benchmark was executed during this validation phase. Historical experimental results were preserved. Reduced-size integration smoke tests must not be represented as full experimental reproduction or independent validation of leak-detection and contamination-detection performance.

The workspace remains a corrected research-software working revision and is not yet a finalized public release.

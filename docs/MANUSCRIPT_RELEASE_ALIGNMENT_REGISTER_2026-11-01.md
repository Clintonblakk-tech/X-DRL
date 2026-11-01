# Manuscript-to-Release Alignment Register

**Project:** X-DRL  
**Manuscript reviewed:** `XDRL_JORS_Manuscript_Revision_2026-10-31.docx`  
**Public repository baseline inspected:** `main`, tag `v1.0.1`  
**Baseline commit:** `f09c0435535c09a21644d1dc5504bc5a897eb214`  
**Working branch:** `manuscript-alignment-v1.0.1-2026-11-01`  
**Review date:** 2026-11-01

## Purpose and scope

This register aligns the manuscript with the software that an independent researcher can actually obtain from the public GitHub repository. It does not attempt to publish the complete development history. Historical results and audit evidence remain preserved; only evidence relevant to claims made about the public software and the manuscript is used to define the publication package.

The inspected public baseline is tag `v1.0.1` on the repository's `main` branch. The repository describes v1.0.1 as a metadata/archive-integrity maintenance release based on v1.0.0. No claim is made here that the full historical benchmark has been independently reproduced.

## Initial alignment findings

| ID | Manuscript statement / location | Public release evidence | Status | Required manuscript action |
|---|---|---|---|---|
| A01 | Abstract, pp. 1–2: corrected package passed regression and clean-environment checks; full historical benchmark not reproduced. | Tagged README documents 15 tests, compilation, imports, pip checks, Linux and Windows Python 3.12 CPU lock-file installations, and reduced-size integration tests. | PARTIALLY ALIGNED | Expand the abstract only to accurately reflect both platform-specific validations; retain explicit statement that the full historical benchmark was not rerun. |
| A02 | §3.1, p. 4 and §6.2, pp. 11–12: current working revision has an 18-file checksum manifest. | Tagged `SHA256SUMS.txt` contains 21 payload-file entries (the manifest itself is not one of the payload entries). | MISALIGNED | Replace the 18-file count with the verified v1.0.1 manifest scope. State that the manifest establishes file integrity, not experimental provenance. |
| A03 | §§4.1, 5.1, 6.4, 8 and 10: requirements are unpinned / dependency pinning remains outstanding. | Tagged README provides separate hash-locked Linux x86-64 CPU Python 3.12 and Windows x86-64 CPU Python 3.12 environments. The generic `requirements.txt` remains unpinned; macOS/CUDA are not validated. | PARTIALLY MISALIGNED | Distinguish the two tested, pinned CPU environments from the still-unpinned generic requirements file and unsupported macOS/CUDA configurations. Do not say all dependencies remain unpinned. |
| A04 | Abstract, §§5–6 and conclusion: clean-environment validation is reported mainly as Linux/WSL2 evidence. | Tagged README records Linux and Windows clean CPU environment checks, 15 tests on both, and a Windows Net3 hydraulic smoke test. | INCOMPLETE | Add Windows evidence with exact scope. Do not imply the Windows smoke test covers Hanoi/C-Town or full benchmarks. |
| A05 | §§3.3–3.5: DQN reward protocols and repeated-run workflows. | Tagged `src/config.py` defines default DQN weights 0.70/0.30 and historical benchmark weights 1.00/0.00; tagged README and benchmark README identify the historical 60-method-run protocol as coverage-only. | REQUIRES SCRIPT-LEVEL CROSSWALK | Identify each manuscript-reported result by the exact tagged script and its effective configuration. Do not pool or interchange 0.70/0.30 and 1.00/0.00 results. |
| A06 | §3.4 and §6.2: corrected GA implementation and historical GA hash discussion. | Tagged `src/ga_engine.py` imports centralized `GA_PARAMS`, repairs chromosomes to enforce exact unique budgets, and returns best-so-far fitness, final-generation fitness, runtime and sensor nodes. | PARTIALLY ALIGNED | Describe the public v1.0.1 GA implementation from the tagged source. Clearly distinguish corrected release implementation from the engine that generated archived historical outputs where the hashes differ. |
| A07 | §6.2: checksum and source identity statements mix historical, RC2 and corrected working-copy terminology. | Public tag v1.0.1 has its own source blobs and checksum manifest. | AMBIGUOUS | Use one named reference baseline (v1.0.1) for all public implementation claims; retain historical comparisons only in a separate provenance paragraph/table. |
| A08 | §6.4, §8, §9 and conclusion: licence, archive DOI and release metadata are described as pending. | Public tag contains an MIT `LICENSE`, version 1.0.1 `CITATION.cff`, and a public v1.0.1 tag. The CFF inspected at the tag does not contain a DOI. | PARTIALLY MISALIGNED / DOI UNVERIFIED | Update the software licence and version statements to match the tag. Verify the live Zenodo record and its exact version/concept DOI before inserting or removing any DOI claim. Do not infer DOI validity from repository metadata. |
| A09 | §§2–3 and limitations: topological coverage is distinguished from hydraulic detection. | Tagged README states graph-based coverage does not establish hydraulic leak/contamination detection; separate WNTR/EPANET smoke tests are identified as smoke tests only. | ALIGNED | Preserve this limitation consistently. Do not claim validated leak detection, contamination detection, hydraulic observability or detection time. |
| A10 | §§4.3, 6.4 and limitations: SHAP and statistical comparisons are qualified. | Tagged README describes SHAP as preliminary selected-action-value attribution and rejects direct inference from incompatible GA coverage counts and DQN reward values. | ALIGNED SUBJECT TO EXACT TEXT CHECK | Keep SHAP as preliminary; do not claim causal explanation or validated policy-wide explanation. Do not report inferential GA–DQN superiority without common-metric run-level data. |
| A11 | §5 and §7: user-facing installation and benchmark execution instructions are described as needing finalisation. | Tagged README and `benchmarks/README.md` provide platform-specific installation, tests, input acquisition policy and a safer timestamped benchmark driver. | INCOMPLETE | Replace generic/proposed instructions with exact commands and paths from the public tag. Explicitly state that third-party network input files are not bundled and must be obtained separately under their source terms. |
| A12 | §9: availability describes a corrected local working revision, with public release identity pending. | Public repository has a v1.0.1 tag and MIT code licence. The inspected tag's CFF identifies version 1.0.1 but does not specify a DOI. | MISALIGNED | Rewrite availability around the actual public repository and tag. Add a version DOI only after the live archive record, version, files and checksums are verified. |

## Public-release facts confirmed by source inspection

- Repository: `Clintonblakk-tech/X-DRL`; default branch: `main`.
- Public baseline tag: `v1.0.1`.
- Main branch commit inspected: `f09c0435535c09a21644d1dc5504bc5a897eb214`.
- DQN configuration in `src/config.py`: 1,000 episodes, batch size 64, replay buffer 50,000, gamma 0.99, learning rate 0.0005, target update 100, epsilon 1.0 / 0.01 / 0.995, default reward weights 0.70 / 0.30.
- Historical benchmark DQN weights in `src/config.py`: coverage 1.00, centrality 0.00.
- Network budgets in `src/config.py`: Hanoi 3, Net3 5, C-Town 10; coverage radius 2.
- GA configuration in `src/config.py`: population 100, generations 1,000, mutation 0.10, crossover 0.80, tournament size 5.
- Tagged tests: 7 DQN, 6 GA and 2 statistical-analysis tests (15 total).
- Tagged README documents clean Linux and Windows CPU Python 3.12 environments, each with 15 tests passed; Linux integration smoke tests on all three networks; Windows EPANET smoke test on WNTR-bundled Net3.
- Benchmark network inputs are not included in the public repository. The code MIT licence does not automatically license third-party input files.
- The full historical 60-method-run benchmark was not rerun during release validation.

## Mandatory next verification before manuscript editing is finalised

1. Inspect every benchmark script in tag v1.0.1 and map each manuscript table/figure/result to one exact script, configuration, input identity, seed set and output file.
2. Confirm whether the manuscript's 30-run DQN result tables are retained historical evidence or outputs reproducible from a script present in v1.0.1. Do not label them as newly generated v1.0.1 results unless proven.
3. Verify the live Zenodo version record, concept DOI, archive filename, file list, checksums and GitHub tag relation.
4. Resolve all manuscript references, DOI citations, author metadata and JORS formatting after technical alignment.
5. Only then prepare a revised manuscript and, if needed, a new release candidate. Do not modify tag v1.0.1 or historical result files.

## Publication rule

The manuscript must describe the exact public software version and the evidence actually demonstrated by that version. Historical outputs may be reported as historical results only when their provenance and limitations are stated. Smoke tests are not full benchmark reproduction. File hashes are not proof that a given historical experiment used those files. A successful clean installation is not proof of scientific reproduction.

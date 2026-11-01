# X-DRL Experiment-to-Manuscript Traceability Crosswalk

**Baseline:** public GitHub tag `v1.0.1`  
**Repository commit inspected:** `f09c0435535c09a21644d1dc5504bc5a897eb214` (main)  
**Manuscript:** `XDRL_JORS_Manuscript_Revision_2026-10-31.docx`  
**Review date:** 2026-11-01

## 1. Executive determination

The public v1.0.1 release contains one full benchmark orchestration script, `benchmarks/run_historical_benchmark.py`. It runs 3 networks × 10 seeds × 2 methods = 60 method-runs, with 1,000 DQN episodes per run. It explicitly applies DQN reward weights 1.00/0.00 (coverage-only) and the centralized GA settings (population 100, generations 1,000, mutation 0.10, crossover 0.80, tournament 5).

The release does **not** contain the historical DQN-only ten-seed driver `run_10_seeds.py`, the historical 30-row DQN-only CSVs, the reward-history CSV collection, or the historical GA–DQN benchmark result CSVs. It also does not contain a figure-generation script for historical reward-convergence curves. The benchmark inputs are intentionally excluded.

Consequently, the v1.0.1 public release is a documented route for a future 60-method-run experiment, not a self-contained package of the historical result data reported in the manuscript audit. The manuscript must distinguish (a) source-verified software behaviour, (b) historical results audited from the preserved research workspace, and (c) future experiments executable from v1.0.1 after users obtain the required network inputs.

## 2. Script-to-claim crosswalk

| Manuscript section / claim | Relevant public script or source | Effective configuration / output | Evidence status | Editorial treatment |
|---|---|---|---|---|
| §3.3 DQN architecture and training parameters | `src/dqn_engine_real.py`; `src/config.py` | MLP  N–128–64–32–N; replay buffer; target network; 1,000 episode default; batch 64; buffer 50,000; gamma 0.99; learning rate 0.0005; target update 100; epsilon schedule 1.0 / 0.01 / 0.995. | VERIFIED against tagged source | Retain, explicitly label 0.70/0.30 as the default corrected protocol and not the historical coverage-only benchmark. |
| §3.3 default DQN reward | `src/config.py`; `src/dqn_engine_real.py` | Coverage 0.70; degree-centrality 0.30. | VERIFIED against tagged source | Describe as default configuration, not automatically as the setting used for every archived DQN result. |
| §3.3 historical benchmark reward | `src/config.py`; `benchmarks/run_historical_benchmark.py` | Coverage 1.00; centrality 0.00. | VERIFIED against tagged source | Label the public historical benchmark driver as coverage-only. Do not combine its results with the 0.70/0.30 DQN-only ten-seed protocol. |
| §3.4 GA algorithm and parameters | `src/ga_engine.py`; `src/config.py` | Population 100; generations 1,000; mutation 0.10; crossover 0.80; tournament 5; coverage radius 2. Returns best-so-far fitness, final-generation fitness, runtime, selected nodes. | VERIFIED for v1.0.1 implementation | Report as the corrected public release implementation. Do not claim that the corrected GA engine necessarily generated archived historical GA outputs. |
| §3.5 60-run GA–DQN benchmark | `benchmarks/run_historical_benchmark.py` | 3 networks × 10 seeds × 2 methods; 1,000 DQN episodes; coverage-only DQN reward; output `final_benchmark_results_1000.csv`, summary `final_benchmark_summary_1000.csv`, DQN artifacts, and `run_manifest.json`. | VERIFIED as executable protocol; NOT executed in release validation | Describe as the reproducible benchmark workflow available in v1.0.1. State explicitly that no new 60-run output was generated in the validation phase. |
| Historical DQN-only 30-run results | Historical `run_10_seeds.py` and historical `dqn_10_seed_results.csv` / summary, retained outside public tag | Hanoi/Net3/C-Town; 10 seeds each; 1,000 episodes; default 0.70/0.30 weights; best/final reward, runtime, sensor list. | PARTIALLY VERIFIED in research workspace; script/results are not present in v1.0.1 public tree | Treat as historical audit evidence only. Do not say the public release reproduces these 30 rows. Identify the exact historical script and source revision in supplementary provenance materials if retained in the paper. |
| Historical 30-row current-vs-archive comparison | Historical current and archived CSVs in research workspace | 30 matched network-seed pairs; best reward, final reward and sensor selections agree; runtime differs in all 30 pairs. | VERIFIED as a comparison of the two retained files; execution provenance not fully resolved | Report as file-to-file consistency, not independent rerun or reproducibility proof. Exclude runtime as a comparative performance finding. |
| Historical GA–DQN 60-row results | Historical archived CSVs and legacy benchmark driver in research workspace | DQN and GA result rows; separate historical protocol. | UNVERIFIED as a reproducible result from v1.0.1; archived driver/interface/configuration mismatch previously identified | Do not use for new comparative inference unless provenance is closed and common evaluation metrics are available. |
| Reward-convergence figures | No historical plotting script or raw convergence series included in v1.0.1 public tree | The tagged DQN engine can export per-episode histories for a run; no matching historical convergence dataset is included in the public release. | UNVERIFIED for historical manuscript curves | Do not recreate historical curves from unrelated or mismatched history files. Include a curve only if its exact run, checkpoint, history and configuration can be linked. |
| Statistical GA–DQN comparison | `src/60_statistical_analysis.py` | Requires `Network,Method,Seed,Metric,Value`; paired Wilcoxon for common seeds, Mann–Whitney only for non-overlapping seed sets; raw BestReward columns intentionally rejected by schema. | VERIFIED as software safeguard; no empirical common-metric dataset verified | Report the utility and safeguard, not a claim of empirical algorithmic superiority. A future analysis requires independently evaluated common metrics for both methods. |
| SHAP explanation | `src/50_shap_analysis.py`; DQN checkpoint and exported state artefacts from `run_dqn` | Explains one selected action-value output for supplied visited states and matching checkpoint; default background size 20; exports NPZ and plots. | VERIFIED as implemented workflow; comprehensive validity/stability not established | Describe as preliminary selected-action-value attribution. Do not call it causal, hydraulic or a complete explanation of the policy. |
| Hydraulic / water-quality detection claims | No leak/contamination event-evaluation pipeline in the public v1.0.1 benchmark driver | Benchmark objective is graph-distance coverage; smoke tests are not event-detection experiments. | NOT SUPPORTED by public benchmark workflow | Remove or qualify claims of validated leak-detection accuracy, contamination-detection accuracy, detection time or hydraulic observability. |

## 3. Key protocol separation

Two DQN workflows must remain separate:

1. **Default / ten-seed historical DQN-only workflow:** the historical script called `run_dqn()` without explicit reward-weight overrides. The inspected historical engine default was coverage 0.70 and centrality 0.30. The ten-seed raw CSVs and summary files are retained in the research workspace, not in public tag v1.0.1.
2. **Public v1.0.1 historical 60-run GA–DQN driver:** `benchmarks/run_historical_benchmark.py` explicitly passes coverage 1.00 and centrality 0.00 to DQN, alongside GA. This driver is present in the public release but was not executed during release validation.

These protocols are not interchangeable. Any manuscript statement that simply says “the 1,000-episode DQN benchmark” without naming its reward weights and driver is ambiguous.

## 4. GA result semantics

The v1.0.1 GA engine returns:
- best-so-far fitness over the evolutionary run;
- best fitness in the final generation;
- runtime;
- the selected sensor nodes associated with the best-so-far solution.

Do not label both reward fields as independent estimates of final performance. The historical GA engine and corrected v1.0.1 GA engine must be kept distinct where source hashes differ. The corrected public engine can support implementation and software-test claims, but does not retroactively establish the provenance of older GA outputs.

## 5. Runtime reporting decision

The historical ten-seed DQN current and archived CSVs have identical best rewards, final rewards and sensor selections across 30 matched rows, but runtime differs in every row. The runtime boundary in the inspected DQN engine includes environment/model setup and training, and excludes checkpoint/history file writing. However, the surviving historical CSVs do not carry sufficient run-level environment and source-revision metadata to identify which runtime series is the authoritative execution record.

**Decision:** do not report the historical runtime means as a robust algorithm-performance result, do not select one series because it is faster, and do not infer runtime from file timestamps. A future run should use the tagged driver and manifest, record machine/software metadata and raw per-run outputs, and use a monotonic timer for new timing measurements.

## 6. What is and is not reproducible from the public tag

### Reproducible workflow supplied by v1.0.1
- DQN and GA implementation code.
- Centralized parameter configuration.
- 60-method-run orchestration script.
- New run manifest with network-input SHA-256 values, seeds, budgets, DQN episode count, reward weights and GA parameters.
- Safe new output directory creation and refusal to overwrite existing output.
- Regression tests and documented platform-specific CPU installation paths.

### Not supplied as historical evidence in v1.0.1
- Historical DQN-only ten-seed script and 30-row results.
- Archived reward-history files and historical convergence figure data.
- Historical 60-row GA–DQN output files.
- Network input files themselves (users must obtain them separately).
- Complete historical execution environment records linking each output to exact code, data, hardware and package versions.

## 7. Manuscript corrections required before submission

1. In §3.1, describe the **public v1.0.1 repository layout**, not local working-tree contents. The public tree does not include local network input files or the historical DQN-only driver.
2. In §3.5, distinguish the public 60-run coverage-only GA–DQN driver from the historical 30-run DQN-only 0.70/0.30 results.
3. In §6.2, explain that source/checksum verification applies to the exact tagged files and does not prove historical execution provenance.
4. In §6.3 and the conclusion, identify the 30-row comparison as historical file consistency only; runtime provenance remains unresolved.
5. In §6.4 and §8, state that v1.0.1 supplies the safe benchmark workflow but no full benchmark was run as part of release validation.
6. In §9, cite the exact public tag and verified archival DOI only after Zenodo has been checked independently.
7. Ensure all plots, figures and numerical claims in the submitted manuscript can be traced to a named output file, source script, configuration, network input hash and seed set. If a trace cannot be supplied, remove the claim/figure or label it explicitly as an unverified historical artefact.

## 8. Evidence boundary

This crosswalk is based on the manuscript revision dated 2026-10-31, the public v1.0.1 Git tree and tagged source files, and the historical audit facts recorded in the project verification register. It does not assert that the historical runs were reproduced. No experiment was launched and no historical result file was modified during this crosswalk.

# X-DRL: Explainable Deep Reinforcement Learning for Sensor Placement in Water Distribution Networks

X-DRL is a Python research-software framework for investigating sensor-placement strategies in water distribution networks using deep reinforcement learning (DQN) and genetic algorithms (GA). It brings together network loading, graph-based coverage calculations, optimisation, benchmark execution, and supporting analysis utilities, with an emphasis on transparent experimental protocols and reproducibility.

**Repository status:** public development repository; corrected working revision 1.0.0. The software has passed its current regression-test suite, but clean-environment installation and full network-level reproduction remain outstanding. It should not yet be described as a fully independently reproduced release.

## Scope and contents

- `src/`: DQN and GA engines, configuration, and analysis utilities.
- `benchmarks/`: benchmark driver and instructions for obtaining network input files.
- `tests/`: lightweight regression tests.
- `AUTHORS.md`: author information and CRediT contributions.
- `CITATION.cff`: software citation metadata.
- `RELEASE_NOTES.md`: summary of the corrected working revision.

## Experimental protocols

The default DQN configuration uses coverage weight 0.70 and centrality weight 0.30. The historical 60-run benchmark driver explicitly uses the historical coverage-only weights (1.0 / 0.0); these protocols must not be conflated.

The GA configuration records the effective historical settings: population 100, generations 1000, mutation 0.10, crossover 0.80, and tournament size 5.

## Installation

Use a clean Python 3.12 environment. Install the declared dependencies:

```bash
python -m pip install -r requirements.txt
```

Dependency versions are currently provisional and will be pinned after a clean-environment compatibility test.

## Tests

From the repository root:

```bash
python -m unittest discover -s tests -v
python -m compileall -q src benchmarks tests
```

The current regression tests exercise selected engine and analysis behaviours. They do not train a full model or constitute a full integration reproduction on Hanoi, Net3, or C-Town.

## Benchmark network inputs

The Hanoi, Net3, and C-Town `.inp` files are intentionally **not included** in this public repository because their individual redistribution terms and attribution requirements have not yet been established. See [benchmarks/README.md](benchmarks/README.md) for the input-file policy and local setup instructions. Do not assume that the MIT licence for X-DRL also applies to third-party benchmark data.

## SHAP workflow

The SHAP utility is a preliminary, checkpoint- and state-driven analysis tool. It explains a selected action value for supplied observed states; it does not establish causal effects or explain all policy behaviour. See the script help and manuscript limitations before interpreting outputs.

## Statistical analysis

The statistical utility rejects the historical `BestReward` CSV as a cross-method outcome because GA coverage fitness and DQN cumulative episode reward are not a common metric. It expects a separately generated `evaluation_metrics.csv` with columns:

`Network,Method,Seed,Metric,Value`

The same independently defined metric and evaluation procedure must be applied to both algorithms before matched-seed inference is attempted.

## Reproducibility and limitations

- The regression tests passed in the recorded development environment; a clean installation test remains outstanding.
- Full network-level smoke tests and independent reruns across all benchmark networks have not yet been completed.
- Historical results have not been overwritten or regenerated as part of the correction work.
- Runtime provenance differences and distinct DQN reward protocols remain documented limitations.
- The SHAP workflow is preliminary.
- Do not claim complete independent reproduction or validated leak/contamination detection from the current tests alone.

## Licence

The original X-DRL software code and documentation in this repository are released under the MIT License. Third-party benchmark network inputs are excluded and may be subject to separate terms. See [LICENSE](LICENSE) and [benchmarks/README.md](benchmarks/README.md).

## Authors and citation

See [AUTHORS.md](AUTHORS.md) for author affiliations, ORCID identifiers, and approved CRediT contributions. Cite the software using [CITATION.cff](CITATION.cff). An archival DOI will be added after a versioned release is deposited in a repository such as Zenodo.

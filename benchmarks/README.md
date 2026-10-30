# Benchmark execution and network-input provenance

## Historical benchmark driver

`run_historical_benchmark.py` executes the historical protocol: Hanoi, Net3 and C-Town; seeds 1–10; GA and DQN; 1,000 DQN episodes. The historical DQN reward weights are coverage-only (1.0 / 0.0). GA settings are population 100, generations 1,000, mutation 0.10, crossover 0.80 and tournament size 5. These are distinct from the separate 0.70 / 0.30 DQN configuration described in the root README.

From the repository root, after installing dependencies and placing the three network files in this directory:

```bash
python benchmarks/run_historical_benchmark.py
```

The script checks all inputs before training starts. It creates a new UTC-timestamped output directory under `results/benchmark_runs/`, records input SHA-256 hashes and protocol settings in `run_manifest.json`, and refuses to overwrite an existing output directory. This is a full 60-run experiment, not a quick test.

## Redistribution audit

No benchmark `.inp` files are included in this repository. The MIT licence for X-DRL code does not automatically apply to third-party network inputs.

| Input | Source and permission evidence | Repository decision |
|---|---|---|
| `Net3.inp` | The exact 30,063-byte file in the prepared release matches the Git blob for `OpenWaterAnalytics/EPANET/example-networks/Net3.inp` (Git blob SHA-1 `3be1e96731612b1612b3f4e2143d2e1505310293`). The upstream EPANET repository is MIT-licensed. | Redistribution permission verified for this exact file under MIT, subject to retaining the upstream copyright and licence notice. It remains external for now; do not imply the X-DRL MIT notice replaces upstream attribution. |
| `Hanoi.inp` | The University of Exeter Centre for Water Systems describes the Hanoi network and offers an EPANET-format input, but its benchmark resource page does not state a redistribution licence. The exact historical file source/version has not been established. | Do not redistribute. Obtain it from the source and check its terms. |
| `C-Town.inp` | The University of Kentucky Libraries record for Avi Ostfeld's “04 Calibration Networks” identifies the C-town model and states CC BY-NC 4.0, requiring attribution and indication of changes. The historical file could not be byte-compared with the repository download endpoint, so exact identity/version is not established. | Do not redistribute at this stage. Obtain the file from the record and confirm exact identity before considering separate CC BY-NC 4.0 distribution. It must not be represented as MIT-licensed. |

## Authoritative references

- Net3 input: https://github.com/OpenWaterAnalytics/EPANET/blob/dev/example-networks/Net3.inp
- EPANET repository and MIT licence: https://github.com/OpenWaterAnalytics/EPANET
- Hanoi benchmark information: https://www.exeter.ac.uk/research/centres/cws/resources/benchmarks/
- University of Kentucky C-Town record and CC BY-NC 4.0 terms: https://uknowledge.uky.edu/wdst_models/2/

For each locally obtained input, record the source URL, access date, exact SHA-256, licence and any modifications. Do not silently modify historical network files.

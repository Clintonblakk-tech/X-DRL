# Corrected working revision — 2026-10-30

- Centralised GA and DQN hyperparameters and passed configuration explicitly.
- Preserved effective historical GA settings and explicit historical DQN coverage-only weights.
- Corrected DQN best-episode sensor/checkpoint tracking and exported actual visited states.
- Masked already-selected actions in DQN next-state bootstrapping.
- Replaced synthetic-state SHAP workflow with a checkpoint/state-driven CLI.
- Replaced raw reward significance testing with validation of common evaluation metrics.
- Added regression tests for configuration, chromosome repair, DQN masking, replay-buffer copying, and statistical input validation.
- The current regression suite passed (15 tests); a clean-environment installation and full network-level integration tests remain outstanding.
- No full benchmark was executed; historical results were not modified.
- This is a corrected working revision, not yet a fully validated independent-reproduction release.

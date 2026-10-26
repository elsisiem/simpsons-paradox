<h1 align="center">Simpson's paradox</h1>
<p align="center">Two Monte Carlo simulations of treatment effects: one where a treatment wins in every subgroup and loses overall, and one where the same pattern has the opposite explanation.</p>
<p align="center">
  <a href="#the-paradox-in-one-table">The paradox</a> ·
  <a href="#how-the-simulation-is-set-up">Setup</a> ·
  <a href="#the-beta-blocker-example">Beta-blocker</a> ·
  <a href="#run">Run</a>
</p>
<p align="center">
  <a href="https://github.com/elsisiem/simpsons-paradox/actions/workflows/ci.yml"><img src="https://github.com/elsisiem/simpsons-paradox/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/license-MIT-111318?style=flat-square" alt="MIT license">
  <img src="https://img.shields.io/badge/Python-stdlib%20only-111318?style=flat-square&logo=python&logoColor=white" alt="Python, standard library only">
</p>

## The paradox in one table

`python simpsons_paradox.py` simulates 10,000 kidney stone patients and prints the improvement rate by treatment, within each stone size and overall:

```text
Improvement rate by treatment (10,000 patients, seed 42)

              Surgery               Medication            Better
Large stones  49.7% (n=3,181)       30.9% (n=783)         surgery
Small stones  88.9% (n=651)         70.2% (n=5,385)       surgery
Overall       56.4% (n=3,832)       65.2% (n=6,168)       medication

Simpson's paradox: surgery is better within every stone size, but medication is better overall.
```

Surgery has the higher rate for large stones and for small stones. Medication has the higher rate when you pool everyone. Both statements are true of the same 10,000 patients.

The cause is who gets which treatment. 83% of surgery patients (3,181 of 3,832) have large stones, which improve less often whatever you do. 87% of medication patients (5,385 of 6,168) have small stones, which improve more often. Pooling mixes the treatment effect with the stone size effect.

Stone size is a confounder here: it affects both the treatment a patient gets and the outcome. The within-stone-size rows are the fair comparison, and they say surgery is better by about 20 points (exactly 20 in the model).

## How the simulation is set up

Each patient is simulated in order: stone size, then treatment, then outcome. The parameters are constants at the top of `simpsons_paradox.py`.

| Step | Rule |
| --- | --- |
| Stone size | Large with probability 0.4, otherwise small |
| Treatment | Surgery with probability 0.8 for large stones and 0.1 for small stones, otherwise medication |
| Improvement | Baseline 0.3. Large stone -0.2, small stone +0.2. Surgery +0.4, medication +0.2 |

That gives these true improvement probabilities:

| | Surgery | Medication |
| --- | --- | --- |
| Large stones | 0.5 | 0.3 |
| Small stones | 0.9 | 0.7 |
| Overall | 0.563 | 0.648 |

The simulated table matches within sampling noise. At 200,000 patients every cell is within a point of these values.

## The beta-blocker example

`python beta_blocker.py` runs a second model with the same shape of result and a different causal structure:

```text
Improvement rate by treatment (10,000 patients, seed 42)

              Pill                  No pill               Better
High BP       49.9% (n=3,160)       28.9% (n=856)         pill
Low BP        90.9% (n=583)         70.0% (n=5,401)       pill
All patients  56.3% (n=3,743)       64.3% (n=6,257)       no pill

The pill has the higher rate within each blood pressure group, but the lower rate for all patients.
Blood pressure sits between the pill and the outcome, so the all-patient row is the total effect of the pill.
```

Within each blood pressure group the pill has the higher improvement rate. For all patients it has the lower one. Here the correct row is the last one.

Blood pressure is a mediator, not a confounder. The pill changes it (high blood pressure in 84% of pill patients, 13% of the rest), and it changes the outcome. The pill is assigned at random, so nothing confounds pill and outcome, and the all-patient row is the total effect of the pill: the pill lowers the improvement rate by about 8 points (8.4 in the model).

Comparing within blood pressure groups holds the mediator fixed. That removes the path through blood pressure, so the within-group rows measure only the direct effect of the pill (20 points better in each group in the model). The pill does help directly, but it also pushes blood pressure up, and that second path costs more. Conditioning on the mediator answers a different question from "what happens to a patient who takes the pill".

| Model | Variable in the middle | Right comparison for the total effect |
| --- | --- | --- |
| Kidney stones | Stone size causes both treatment and outcome (confounder) | Within stone size |
| Beta-blocker | The pill causes blood pressure, which causes the outcome (mediator) | All patients |

The tables look alike. Only the causal graph tells you which comparison to trust.

## Run

Python 3 with the standard library only. CI runs both scripts on Python 3.11.

```bash
git clone https://github.com/elsisiem/simpsons-paradox.git
cd simpsons-paradox
python simpsons_paradox.py
python beta_blocker.py
```

Both scripts take `--seed` (default 42) and `--patients` (default 10000). The same seed gives the same output.

```bash
python simpsons_paradox.py --seed 7 --patients 200000
```

## Credits

Started as a class exercise on causal graphs.

## License

MIT. See [LICENSE](LICENSE).

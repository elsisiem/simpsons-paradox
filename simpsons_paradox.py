"""Simpson's paradox with kidney stone treatments, by Monte Carlo simulation.

Surgery beats medication within every stone size, yet medication beats surgery
overall, because surgery is given mostly to patients with large stones, who
improve less often whatever the treatment.

Usage: python simpsons_paradox.py [--seed 42] [--patients 10000]
"""
import argparse
import random

# 40% of patients present with large kidney stones (60% with small)
P_LARGE = 0.4

# 80% of large-stone patients are assigned to surgery (20% to medication)
P_SURGERY_IF_LARGE = 0.8

# 10% of small-stone patients are assigned to surgery (90% to medication)
P_SURGERY_IF_SMALL = 0.1

# At baseline, 30% of patients improve
IMPROVE_RATE = 0.3

# Absolute 20% fewer patients improve if the stone is large
IMPROVE_RATE_IF_LARGE = -0.2

# Absolute 20% more patients improve if the stone is small
IMPROVE_RATE_IF_SMALL = 0.2

# Absolute 40% more patients improve with surgery
IMPROVE_RATE_IF_SURGERY = 0.4

# Absolute 20% more patients improve with medication
IMPROVE_RATE_IF_MEDICATION = 0.2


def simulate_kidney_stone(rng):
    """Simulates one patient. Returns (stone_size, treatment, improved)."""
    # Stone size comes first, and it decides which treatment the patient gets.
    if rng.random() < P_LARGE:
        stone_size = 'large'
        p_surgery = P_SURGERY_IF_LARGE
    else:
        stone_size = 'small'
        p_surgery = P_SURGERY_IF_SMALL
    treatment = 'surgery' if rng.random() < p_surgery else 'medication'

    # Stone size and treatment both shift the probability of improvement.
    p_improve = IMPROVE_RATE
    p_improve += IMPROVE_RATE_IF_LARGE if stone_size == 'large' else IMPROVE_RATE_IF_SMALL
    p_improve += IMPROVE_RATE_IF_SURGERY if treatment == 'surgery' else IMPROVE_RATE_IF_MEDICATION

    improved = rng.random() < p_improve
    return stone_size, treatment, improved


def rate(improved, total):
    return improved / total if total else None


def format_cell(improved, total):
    if total == 0:
        return 'n/a'
    return f"{improved / total:.1%} (n={total:,})"


def summarize_results(results):
    """Prints the improvement rate by treatment within each stone size and overall."""
    groups = [('Large stones', 'large'), ('Small stones', 'small'), ('Overall', None)]
    print(f"{'':<14}{'Surgery':<22}{'Medication':<22}Better")

    better_in = {}
    for label, size in groups:
        cells = {}
        for treatment in ('surgery', 'medication'):
            outcomes = [improved for s, t, improved in results
                        if t == treatment and size in (None, s)]
            cells[treatment] = (sum(outcomes), len(outcomes))

        surgery_rate = rate(*cells['surgery'])
        medication_rate = rate(*cells['medication'])
        if surgery_rate is None or medication_rate is None:
            better_in[label] = 'n/a'
        else:
            better_in[label] = 'surgery' if surgery_rate > medication_rate else 'medication'
        print(f"{label:<14}{format_cell(*cells['surgery']):<22}"
              f"{format_cell(*cells['medication']):<22}{better_in[label]}")

    within = {better_in['Large stones'], better_in['Small stones']}
    overall = better_in['Overall']
    if len(within) == 1 and 'n/a' not in within | {overall} and overall not in within:
        print(f"\nSimpson's paradox: {within.pop()} is better within every stone size, "
              f"but {overall} is better overall.")


def main():
    parser = argparse.ArgumentParser(description="Simpson's paradox: kidney stone simulation")
    parser.add_argument('--seed', type=int, default=42, help='random seed (default: 42)')
    parser.add_argument('--patients', type=int, default=10000, help='number of simulated patients (default: 10000)')
    args = parser.parse_args()

    rng = random.Random(args.seed)
    results = [simulate_kidney_stone(rng) for _ in range(args.patients)]

    print(f"Improvement rate by treatment ({args.patients:,} patients, seed {args.seed})\n")
    summarize_results(results)


if __name__ == '__main__':
    main()

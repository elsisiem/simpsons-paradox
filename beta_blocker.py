"""Beta-blocker example: blood pressure is a mediator, not a confounder.

The pill raises blood pressure, and high blood pressure lowers the chance of
improving. Within each blood pressure group the pill looks better. For all
patients it looks worse. The pill is assigned independently of everything
else, so the all-patient comparison is the total effect of taking it. The
within-group comparison blocks the path through blood pressure, so it measures
only the direct effect.

Usage: python beta_blocker.py [--seed 42] [--patients 10000]
"""
import argparse
import random

# 38% of patients are given the beta-blocker pill
P_PILL = 0.38

# 84% of patients who get the medication have high blood pressure after
P_HIGH_IF_PILL = 0.84

# 13% of patients who don't get the medication have high blood pressure
P_HIGH_IF_NO_PILL = 0.13

# At baseline, 30% of patients improve
IMPROVE_RATE = 0.3

# Absolute 20% fewer patients improve if their blood pressure is high
IMPROVE_RATE_IF_HIGH = -0.2

# Absolute 20% more patients improve if their blood pressure is low
IMPROVE_RATE_IF_LOW = 0.2

# Absolute 40% more patients improve with the medication
IMPROVE_RATE_IF_PILL = 0.4

# Absolute 20% more patients improve without the medication
IMPROVE_RATE_IF_NO_PILL = 0.2


def simulate_beta_blockers(rng):
    """Simulates one patient. Returns (blood_pressure, treatment, improved)."""
    # The pill is assigned at random. It then changes blood pressure.
    if rng.random() < P_PILL:
        treatment = 'pill'
        p_high = P_HIGH_IF_PILL
    else:
        treatment = 'no_pill'
        p_high = P_HIGH_IF_NO_PILL
    blood_pressure = 'high' if rng.random() < p_high else 'low'

    # Blood pressure and treatment both shift the probability of improvement.
    p_improve = IMPROVE_RATE
    p_improve += IMPROVE_RATE_IF_HIGH if blood_pressure == 'high' else IMPROVE_RATE_IF_LOW
    p_improve += IMPROVE_RATE_IF_PILL if treatment == 'pill' else IMPROVE_RATE_IF_NO_PILL

    improved = rng.random() < p_improve
    return blood_pressure, treatment, improved


def rate(improved, total):
    return improved / total if total else None


def format_cell(improved, total):
    if total == 0:
        return 'n/a'
    return f"{improved / total:.1%} (n={total:,})"


def summarize_results(results):
    """Prints the improvement rate by treatment, within each blood pressure group and for all patients."""
    groups = [
        ('High BP', 'high'),
        ('Low BP', 'low'),
        ('All patients', None),
    ]
    print(f"{'':<14}{'Pill':<22}{'No pill':<22}Better")

    better_in = {}
    for label, blood_pressure in groups:
        cells = {}
        for treatment in ('pill', 'no_pill'):
            outcomes = [improved for bp, t, improved in results
                        if t == treatment and blood_pressure in (None, bp)]
            cells[treatment] = (sum(outcomes), len(outcomes))

        pill_rate = rate(*cells['pill'])
        no_pill_rate = rate(*cells['no_pill'])
        if pill_rate is None or no_pill_rate is None:
            better_in[label] = 'n/a'
        else:
            better_in[label] = 'pill' if pill_rate > no_pill_rate else 'no pill'
        print(f"{label:<14}{format_cell(*cells['pill']):<22}"
              f"{format_cell(*cells['no_pill']):<22}{better_in[label]}")

    within = {better_in['High BP'], better_in['Low BP']}
    overall = better_in['All patients']
    if len(within) == 1 and 'n/a' not in within | {overall} and overall not in within:
        within_word = 'higher' if within == {'pill'} else 'lower'
        overall_word = 'lower' if within_word == 'higher' else 'higher'
        print(f"\nThe pill has the {within_word} rate within each blood pressure group, "
              f"but the {overall_word} rate for all patients.")
        print("Blood pressure sits between the pill and the outcome, so the all-patient "
              "row is the total effect of the pill.")


def main():
    parser = argparse.ArgumentParser(description='Beta-blocker simulation: blood pressure as a mediator')
    parser.add_argument('--seed', type=int, default=42, help='random seed (default: 42)')
    parser.add_argument('--patients', type=int, default=10000, help='number of simulated patients (default: 10000)')
    args = parser.parse_args()

    rng = random.Random(args.seed)
    results = [simulate_beta_blockers(rng) for _ in range(args.patients)]

    print(f"Improvement rate by treatment ({args.patients:,} patients, seed {args.seed})\n")
    summarize_results(results)


if __name__ == '__main__':
    main()

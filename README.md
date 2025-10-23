# Structural Descent Envelope for Odd Abundant Integers

This repository contains a single self-contained script that reproduces the **SUFF / FAIL** envelope checks used in the paper:

**An Explicit Descent Lemma Forcing Central Divisors in Odd Abundant Integers**  
by Daniel Sautot

The proof in the paper is analytic and independent from the code. The script is only for replication of the envelope checks and the smooth certificate.

---

## Quick start

**Requirements**
- Python ≥ 3.10
- Standard library only (no extra packages)

**Run a SUFF check near the pivot (theta mode)**
```bash
python refine_structural_failure.py --mode test --f-dem 0.02 --digits 7.4615559913203105792e19 --tol 2e-4 --envelope theta --y-mult-max 100 --y-mult-steps 60

# Structural Descent Envelope for Odd Abundant Integers

This repository contains a single self-contained script that reproduces the **SUFF / FAIL** envelope checks used in the paper:

**An Explicit Descent Lemma Forcing Central Divisors in Odd Abundant Integers**  
by Daniel Sautot

The proof in the paper is analytic and independent from the code. The script is only for replication of the envelope checks and the smooth certificate.

---

## Quick Start

### Requirements
- Python ≥ 3.10
- Standard library only (no extra packages)

### Usage
Run a **SUFF** check near the pivot (theta mode):
```bash
python refine_structural_failure.py --mode test --f-dem 0.02 --digits 7.4615559913203105792e19 --tol 2e-4 --envelope theta --y-mult-max 100 --y-mult-steps 60
```

Run a **FAIL** check slightly above the pivot:
```bash
python refine_structural_failure.py --mode test --f-dem 0.02 --digits 7.5369252437578907648e19 --tol 2e-4 --envelope theta --y-mult-max 100 --y-mult-steps 60
```

## How It Works

Given a decimal digit count `D`, the script sets `B = D * ln(10)` and evaluates an upper envelope:

`f_off(B) ≈ sup_y pi(y) / (B + y)`

It uses a lightweight PNT-style approximation for `pi(y)` and a multi-scale grid search over `y`.

### Envelopes Available
*   `--envelope theta`: Labeled “theta” in the paper.
*   `--envelope coarse`: A coarser variant for sanity checks.

You may subtract a constant structural decrement with `--delta-const`. In `pivot` mode, you can enable a cumulative structural correction with `--struct`.

## Command Reference

### Single-point test
```bash
python refine_structural_failure.py --mode test --digits <D> --f-dem <x> --envelope theta|coarse --tol <eps> --y-mult-max <K> --y-mult-steps <N> --y-pow-steps <N> --delta-const <c>
```

### Pivot search by multiplicative bracketing
```bash
python refine_structural_failure.py --mode pivot --digits-lo <Dlo> --digits-hi <Dhi> --f-dem <x> --tol <eps> --rounds <r> --N <grid> --envelope theta|coarse --y-mult-max <K> --y-mult-steps <N> --y-pow-steps <N> --struct --delta-const <c>
```

Output is a deterministic JSON object printed to `stdout`.

## Examples

### Run a single SUFF or FAIL test
```bash
# SUFF
python refine_structural_failure.py --mode test --f-dem 0.02 --digits 7.4615559913203105792e19 --tol 2e-4 --envelope theta --y-mult-max 100 --y-mult-steps 60

# FAIL
python refine_structural_failure.py --mode test --f-dem 0.02 --digits 7.5369252437578907648e19 --tol 2e-4 --envelope theta --y-mult-max 100 --y-mult-steps 60
```

### Find a crossing window by multiplicative bracketing
```bash
python refine_structural_failure.py --mode pivot --f-dem 0.02 --digits-lo 3e19 --digits-hi 3e20 --rounds 12 --N 801 --tol 2e-4 --envelope theta --y-mult-max 100 --y-mult-steps 60
```

## Large Smooth Certificate

Explicit odd abundant witness at 10²¹ digits from the smooth family `945^k = 3^(3k) * 5^k * 7^k`:

```python
# 945^k with exponents (3k, k, k)
k = 336085672385486584107
exponents = (1008257017156459752321, 336085672385486584107, 336085672385486584107)
```    
## Reproducibility

*   Uses only standard Python libraries (`math` and `argparse`).
*   No randomness is used; outputs are deterministic.
*   The analytic proof in the paper does not depend on this code.

## Citation

If you use this repository in your work, please cite both the paper and the code.

### Paper
> D. Sautot (2025).  
> *An Explicit Descent Lemma Forcing Central Divisors in Odd Abundant Integers*.  
> arXiv DOI: `10.48550/arXiv.XXXX.XXXXX` (replace with your identifier)

### Repository
> https://github.com/[USER]/odd-abundance-descent (replace with your username)

## License

> MIT License
>
> Copyright (c) 2025 Daniel Sautot
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included
> in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
> EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
> MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
> IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
> DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
> ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
> OTHER DEALINGS IN THE SOFTWARE.

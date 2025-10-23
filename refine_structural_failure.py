#!/usr/bin/env python3
import argparse, math, sys, json

# ---------------- π(y) approximations ----------------

def pi_approx_coarse(y: float) -> float:
    """
    Approx de style 1ère passe (optimiste) :
      π(y) ~ (y / ln y) * (1 + 1/ln y)
    """
    if y <= math.e**2:
        y = math.e**2 + 1.0
    ly = math.log(y)
    return (y / ly) * (1.0 + 1.0 / ly)

def pi_approx_tighter(y: float) -> float:
    """
    Approx un peu plus serrée :
      π(y) ~ y / (ln y - 1)
    """
    if y <= math.e**2:
        y = math.e**2 + 1.0
    ly = math.log(y)
    den = ly - 1.0
    return y / den if den > 1e-12 else 0.0

# ---------------- enveloppe f_off ----------------

def env_f_off(B: float, envelope: str,
              y_mult_max: float = 100.0,
              y_pow_steps: int = 20,
              y_mult_steps: int = 30) -> float:
    """
    f_off(B) =
      - 'coarse' : max_y π(y)/B                (modèle initial)
      - 'theta'  : max_y π(y)/(B + θ(y)), θ~y  (modèle réaliste)

    IMPORTANT : on balaye y bien AU-DELÀ de B : y = m·B, m ∈ [0.1 .. K] (K = y_mult_max).
    """
    # y < B : ladder puissance (B^t, t∈(0,1))
    pow_steps = max(4, int(y_pow_steps))
    y_pow = [B**(i/float(pow_steps)) for i in range(1, pow_steps)]  # évite 0 et B exact

    # y = m·B, multipliers géométriques de 0.1 jusqu'à K
    K = max(3.0, float(y_mult_max))
    m_steps = max(10, int(y_mult_steps))
    r = (K / 0.1)**(1.0 / (m_steps - 1))
    y_mult = [(0.1 * (r**i)) * B for i in range(m_steps)]

    # grille finale
    y_grid = []
    y_grid.extend(y_pow)
    y_grid.extend(y_mult)

    best = 0.0
    if envelope == "coarse":
        # coarse : f = π(y)/B, le max en y est alors juste le max de π(y) sur la grille
        for y in y_grid:
            if y <= 10.0:
                continue
            u = pi_approx_coarse(y)
            f = u / B
            if f > best:
                best = f
        return best

    # theta : f = π(y) / (B + y)
    for y in y_grid:
        if y <= 10.0:
            continue
        u = pi_approx_tighter(y)
        f = u / (B + y)   # θ(y) ~ y
        if f > best:
            best = f
    return best

# ---------------- digits grid ----------------

def build_digits_geo(lo: float, hi: float, N: int):
    if lo <= 0 or hi <= 0 or not (lo < hi):
        raise ValueError("need 0 < digits_lo < digits_hi")
    N = max(3, int(N))
    r = (hi / lo)**(1.0 / (N - 1))
    return [lo * (r**i) for i in range(N)]

# ---------------- modes ----------------
def find_pivot(d_lo: float, d_hi: float, f_dem: float,
               rounds: int, N: int, tol: float,
               envelope: str, delta_const: float,
               y_mult_max: float, y_pow_steps: int, y_mult_steps: int):
    """
    Version cohérente avec --mode test :
      - SUFF ⇔ fe >= f_dem - tol
      - FAIL ⇔ fe <  f_dem - tol
    On cherche la 1ère FAIL après au moins un SUFF, et on serre le bracket [dernier_SUFF, 1er_FAIL].
    """
    lo, hi = float(d_lo), float(d_hi)
    ln10 = math.log(10.0)
    for _ in range(max(1, int(rounds))):
        Ds = build_digits_geo(lo, hi, N)
        fe = [env_f_off(D*ln10, envelope, y_mult_max, y_pow_steps, y_mult_steps) - delta_const for D in Ds]
        # même logique que --mode test
        suff = [ (v >= f_dem - tol) for v in fe ]
        # 1ère FAIL après avoir vu au moins un SUFF
        idx = None
        seen_suff = False
        for i, ok in enumerate(suff):
            if ok:
                seen_suff = True
            elif seen_suff:
                idx = i
                break
        if idx is None:
            # tous SUFF -> monter ; tous FAIL -> descendre
            if all(suff):
                lo, hi = Ds[-1], Ds[-1]*10.0
            else:
                lo, hi = Ds[0]/10.0, Ds[0]
        else:
            lo, hi = Ds[idx-1], Ds[idx]
    return {
        "digits_lo": lo, "digits_hi": hi, "digits_star": int(hi),
        "index": None, "N": int(N), "rounds": int(rounds), "tol": tol,
        "envelope": envelope, "delta_const": delta_const,
        "y_mult_max": y_mult_max, "y_pow_steps": int(y_pow_steps), "y_mult_steps": int(y_mult_steps),
    }


def test_single(D: float, f_dem: float, tol: float,
                envelope: str, delta_const: float,
                y_mult_max: float, y_pow_steps: int, y_mult_steps: int):
    ln10 = math.log(10.0)
    fe = env_f_off(D*ln10, envelope, y_mult_max, y_pow_steps, y_mult_steps) - delta_const
    status = "SUFF" if fe >= f_dem - tol else "FAIL"
    return {
        "digits": int(D),
        "status": status,
        "f_off_eff": fe,
        "f_dem": f_dem,
        "tol": tol,
        "envelope": envelope,
        "delta_const": delta_const,
        "y_mult_max": y_mult_max,
        "y_pow_steps": int(y_pow_steps),
        "y_mult_steps": int(y_mult_steps),
    }

# ---------------- main ----------------

def main():
    ap = argparse.ArgumentParser(description="PASS/FAIL global sans CSV (coarse = pi/B ; theta = pi/(B+y)), y-grid étendue jusqu'à K·B.")
    ap.add_argument("--mode", choices=["pivot", "test"], required=True)
    ap.add_argument("--f-dem", type=float, required=True)
    ap.add_argument("--digits-lo", type=float)
    ap.add_argument("--digits-hi", type=float)
    ap.add_argument("--digits", type=float)
    ap.add_argument("--rounds", type=int, default=8)
    ap.add_argument("--N", type=int, default=301)
    ap.add_argument("--tol", type=float, default=5e-4)
    ap.add_argument("--envelope", choices=["coarse","theta"], default="theta",
                    help="coarse = modèle initial (pi/B), theta = modèle réaliste (pi/(B+y)).")
    ap.add_argument("--delta-const", type=float, default=0.0, help="taxe constante optionnelle (default 0)")
    ap.add_argument("--y-mult-max", type=float, default=100.0, help="balayage y jusqu'à K·B (défaut 100)")
    ap.add_argument("--y-pow-steps", type=int, default=20, help="nombre de pas puissance pour y<B (défaut 20)")
    ap.add_argument("--y-mult-steps", type=int, default=30, help="nombre de multipliers géométriques entre 0.1 et K (défaut 30)")
    args = ap.parse_args()

    if args.mode == "pivot":
        if args.digits_lo is None or args.digits_hi is None:
            sys.exit("pivot: fournir --digits-lo et --digits-hi")
        out = find_pivot(args.digits_lo, args.digits_hi, args.f_dem,
                         args.rounds, args.N, args.tol,
                         args.envelope, args.delta_const,
                         args.y_mult_max, args.y_pow_steps, args.y_mult_steps)
        print(json.dumps(out, indent=2))
    else:
        if args.digits is None:
            sys.exit("test: fournir --digits")
        out = test_single(args.digits, args.f_dem, args.tol,
                          args.envelope, args.delta_const,
                          args.y_mult_max, args.y_pow_steps, args.y_mult_steps)
        print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()

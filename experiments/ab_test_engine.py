from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd
from scipy import stats


@dataclass
class ABResult:
    metric: str
    n_control: int
    n_treatment: int
    control_mean: float
    treatment_mean: float
    abs_lift: float
    rel_lift: float
    ci_95: Tuple[float, float]
    p_value: float
    decision: str
    notes: Dict[str, str]


def _two_proportion_ztest(x1: int, n1: int, x2: int, n2: int) -> float:
    """Two-sided z-test p-value for difference in proportions."""
    if n1 == 0 or n2 == 0:
        return float("nan")
    p1 = x1 / n1
    p2 = x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)
    denom = math.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    if denom == 0:
        return float("nan")
    z = (p2 - p1) / denom
    return 2 * (1 - stats.norm.cdf(abs(z)))


def _diff_in_means_ttest(control: np.ndarray, treatment: np.ndarray) -> float:
    """Welch's t-test p-value (two-sided)."""
    if len(control) < 2 or len(treatment) < 2:
        return float("nan")
    t_stat, p = stats.ttest_ind(treatment, control, equal_var=False, nan_policy="omit")
    return float(p)


def srm_check(df: pd.DataFrame, group_col: str = "variant") -> Dict[str, str]:
    """
    Sample Ratio Mismatch (SRM) check.
    Assumes expected split is uniform across variants present in data.
    """
    counts = df[group_col].value_counts(dropna=False)
    k = len(counts)
    if k < 2:
        return {"srm": "skip", "details": "Need >=2 variants."}

    expected = np.repeat(counts.sum() / k, k)
    chi2, p = stats.chisquare(counts.values, f_exp=expected)
    status = "pass" if p >= 0.01 else "fail"
    return {
        "srm": status,
        "p_value": f"{p:.4g}",
        "counts": counts.to_dict(),
        "expected_each": f"{counts.sum()/k:.1f}",
    }


def analyze_ab(
    df: pd.DataFrame,
    metric_col: str,
    group_col: str = "variant",
    control_value: str = "control",
    treatment_value: str = "treatment",
    metric_type: str = "continuous",  # "binary" or "continuous"
    alpha: float = 0.05,
) -> ABResult:
    """
    Analyze A/B test for a single metric.
    - continuous: Welch t-test + 95% CI via bootstrap
    - binary: two-proportion z-test + Wald CI
    """
    d = df[[group_col, metric_col]].dropna()
    srm = srm_check(d, group_col=group_col)

    c = d.loc[d[group_col] == control_value, metric_col].astype(float).to_numpy()
    t = d.loc[d[group_col] == treatment_value, metric_col].astype(float).to_numpy()

    n_c, n_t = len(c), len(t)
    c_mean = float(np.mean(c)) if n_c else float("nan")
    t_mean = float(np.mean(t)) if n_t else float("nan")

    abs_lift = t_mean - c_mean
    rel_lift = abs_lift / c_mean if (not np.isnan(c_mean) and c_mean != 0) else float("nan")

    if metric_type == "binary":
        x1 = int(np.sum(c))
        x2 = int(np.sum(t))
        p_val = _two_proportion_ztest(x1, n_c, x2, n_t)

        # Wald 95% CI for diff in proportions (simple + common in product analytics)
        p1 = x1 / n_c if n_c else float("nan")
        p2 = x2 / n_t if n_t else float("nan")
        se = math.sqrt((p1 * (1 - p1) / n_c) + (p2 * (1 - p2) / n_t)) if n_c and n_t else float("nan")
        ci = (abs_lift - 1.96 * se, abs_lift + 1.96 * se) if not np.isnan(se) else (float("nan"), float("nan"))
    else:
        p_val = _diff_in_means_ttest(c, t)

        # Bootstrap CI for mean diff
        rng = np.random.default_rng(42)
        B = 4000
        if n_c and n_t:
            diffs = []
            for _ in range(B):
                c_b = rng.choice(c, size=n_c, replace=True)
                t_b = rng.choice(t, size=n_t, replace=True)
                diffs.append(np.mean(t_b) - np.mean(c_b))
            lo, hi = np.quantile(diffs, [0.025, 0.975])
            ci = (float(lo), float(hi))
        else:
            ci = (float("nan"), float("nan"))

    decision = "ship" if (not np.isnan(p_val) and p_val < alpha and ci[0] > 0) else "do_not_ship"
    notes = {"srm": str(srm)}

    return ABResult(
        metric=metric_col,
        n_control=n_c,
        n_treatment=n_t,
        control_mean=c_mean,
        treatment_mean=t_mean,
        abs_lift=float(abs_lift),
        rel_lift=float(rel_lift),
        ci_95=ci,
        p_value=float(p_val),
        decision=decision,
        notes=notes,
    )


if __name__ == "__main__":
    # Demo with synthetic data
    demo = pd.DataFrame(
        {
            "variant": np.random.choice(["control", "treatment"], size=5000),
        }
    )
    # continuous metric (e.g., order_value)
    demo["order_value"] = np.where(demo["variant"] == "treatment",
                                   np.random.normal(52, 20, size=len(demo)),
                                   np.random.normal(50, 20, size=len(demo)))

    # binary metric (e.g., retained_d30)
    demo["retained_d30"] = (np.random.rand(len(demo)) < np.where(demo["variant"] == "treatment", 0.23, 0.20)).astype(int)

    r1 = analyze_ab(demo, "order_value", metric_type="continuous")
    r2 = analyze_ab(demo, "retained_d30", metric_type="binary")

    print(r1)
    print(r2)

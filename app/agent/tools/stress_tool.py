import json

from strands import tool

from tools.portfolio_tool import load_portfolio_data

# Tool Run stress Scenario

@tool
def run_stress_scenario(default_rate_increase_pct: float) -> str:
    """Run a credit stress scenario by increasing portfolio probability of default by a percentage,
    For example 20 mean a 20 percentage relative increase."""

    if not 0 <= default_rate_increase_pct <= 1000:
        return "Invalid stress percentage,  use 0 to 1000"

    records = load_portfolio_data()
    baseline_ecl_total = 0.0
    stressed_ecl_total = 0.0

    results = []

    for row in records:
        ead = float(row['exposure_cr'])
        baseline_pd = float(row['pd'])
        lgd = float(row['lgd'])
        stressed_pd = min(baseline_pd * (1 + default_rate_increase_pct / 100), 1.0)

        baseline_ecl = ead * baseline_pd * lgd
        stressed_ecl = ead * stressed_pd * lgd

        baseline_ecl_total += baseline_ecl
        stressed_ecl_total += stressed_ecl
        results.append({
            "portfolio": row['portfolio'],
            "baseline_pd": round(baseline_pd, 4),
            "baseline_ecl_cr": round(baseline_ecl, 4),
            "stressed_pd": round(stressed_pd, 4),
            "stressed_ecl_cr": round(stressed_ecl, 4),
        })

    return json.dumps({
        "stress_percentages": default_rate_increase_pct,
        "portfolio_results": results,
        "baseline_total_ecl_cr": round(baseline_ecl_total, 4),
        "stressed_total_ecl_cr": round(stressed_ecl_total, 4),
        "incremental_loss_cr": round((stressed_ecl_total - baseline_ecl_total), )
    })

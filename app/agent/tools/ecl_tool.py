# Calculate Expected loss
import json

from strands import tool

from tools.portfolio_tool import load_portfolio_data

@tool
def calculate_expected_loss():
    """ Calculate Expected credit loss (ECL) for all the portfolio using EAD Multiplying by PD Multiplied by LDG.. """
    records = load_portfolio_data()
    results = []
    total_ecl = 0.0
    for row in records:
        ead = float(row['exposure_cr'])
        pd = float(row['pd'])
        lgd = float(row['lgd'])

        expected_credit_loss = ead * pd * lgd
        total_ecl += expected_credit_loss

        results.append({
            "portfolio": row['portfolio'],
            "ead": ead,
            "ecl_cr": round(expected_credit_loss, 4),
        })

    return json.dumps({"portfolio_results": results,
                       "total_ecl": round(total_ecl, 4)})

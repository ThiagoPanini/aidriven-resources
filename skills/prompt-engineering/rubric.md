# Prompt Quality Rubric

Use to grade your own output before delivering, or to evaluate someone else's prompt.

Score 1–5 on each dimension. A strong prompt averages ≥4 with no dimension below 3.

| Dimension | 1 (poor) | 5 (excellent) |
|---|---|---|
| **Intent fidelity** | Misses what the user actually wanted | Matches stated and implied intent precisely |
| **Clarity** | Vague verbs, ambiguous scope | Every instruction is unambiguous to a stranger |
| **Completeness** | Missing critical constraints | All load-bearing constraints present, none extra |
| **Structure fit** | Pattern mismatched to task (over- or under-engineered) | Pattern matches task complexity exactly |
| **Output format** | Free-form where structure was needed | Exact, parseable, with fallback for missing fields |
| **Robustness** | Breaks on minor input variation | Handles edge cases via explicit decision rules |
| **Reusability** | Hard-coded to one input | Cleanly parameterized; easy to drop new inputs in |
| **Groundedness** | Encourages hallucination on factual / fresh content | Routes factual claims through tools, sources, or refusal |
| **Safety** | Could produce harmful, deceptive, or policy-violating output | Safe by construction; clear refusal rules |
| **Concision** | Bloated; multiple sections add no value | Every line earns its keep |
| **Copy-paste readiness** | User must edit to use | Works as-is; placeholders clearly marked |

## Quick smell tests

- Could a new user paste this and get a useful result with zero context? If no → fix.
- If you delete any single section, does quality drop? If no → that section was filler.
- Does any instruction contradict another? If yes → resolve.
- Does the prompt assume facts the model can't reliably know? If yes → add grounding.

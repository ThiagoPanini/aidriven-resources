# Anti-patterns (and the fix)

## 1. Hollow expertise framing
**Bad:** "You are a world-class expert with 20 years of experience…"
**Why it fails:** No operational content. The model already knows how to be competent.
**Fix:** Replace with concrete behaviors. *"Prefer X over Y. When unsure, ask. Always cite sources."*

## 2. Vague verbs
**Bad:** "Consider the context and provide a helpful answer."
**Fix:** State what *helpful* means here — format, length, audience, success criteria.

## 3. Conflicting instructions
**Bad:** "Be concise but thorough. Be creative but stick exactly to the format."
**Fix:** Pick one, or define how to resolve the conflict. *"Default to concise; expand only when the user asks 'why'."*

## 4. Over-scaffolding
**Bad:** A 40-line prompt with role, mission, values, philosophy, principles, and tone guide — for "summarize this email".
**Fix:** Three lines. Architecture should match task complexity.

## 5. Asking for hidden reasoning
**Bad:** "Think step by step internally but only show the final answer."
**Why:** Unreliable across models and conflicts with safety/transparency.
**Fix:** Either ask for visible reasoning, or just ask for the answer with a quality bar.

## 6. Pretending the model knows live facts
**Bad:** "Give me the latest pricing for AWS Lambda."
**Fix:** "Look up current AWS Lambda pricing using your browsing tool. If you can't browse, say so and ask me to paste the page."

## 7. Brittle format demands
**Bad:** "Respond in exactly this format: ..." with a free-text task and no schema.
**Fix:** Use a fenced JSON schema or numbered template, plus a fallback rule for missing fields.

## 8. Few-shot examples that contradict the rules
**Bad:** Rule says "no markdown" but examples use bullets.
**Fix:** Make every example obey every rule. Examples teach more than instructions.

## 9. Stuffing the role with personality instead of behavior
**Bad:** "You are sassy, witty, brilliant, kind, and concise."
**Fix:** Pick the *one* trait that affects output, and define what it looks like operationally.

## 10. No fallback for ambiguity
**Bad:** Prompt assumes the input is always well-formed.
**Fix:** Add an explicit branch — *"If the input is missing field X, return {error: '…'} instead of guessing."*

## 11. "Don't hallucinate"
**Bad:** Telling the model not to hallucinate doesn't stop hallucination.
**Fix:** Constrain the source of truth. *"Answer only from the supplied document. If not present, say 'not in source'."*

## 12. Output format buried at the bottom of a wall of text
**Fix:** Put the output schema near the end *and* make it visually distinct (fenced block, schema syntax).

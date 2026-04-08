# Worked Examples: Weak Request → Strong Prompt

## Example 1 — Vague request
**User:** "Create a prompt to help me write better blog posts."

**Assumption stated:** technical/professional audience, model-agnostic, single-prompt (not chain).

**Delivered prompt:**
```
You are helping me draft a blog post. Before writing, ask me for any of these I haven't already provided:
- Topic and angle
- Target reader (role + what they care about)
- Desired length (words)
- Tone (e.g., conversational, analytical, opinionated)
- Key points or sources I want included

Then produce:
1. A working title and 3 alternates.
2. A 1-sentence thesis.
3. An outline (H2/H3) with one-line notes per section.
4. A full draft matching the requested length (±10%).
5. A 2-sentence summary suitable for social sharing.

Constraints:
- Open with a concrete hook, not a definition.
- No filler phrases ("In today's fast-paced world…").
- Cite any factual claim or mark it [verify].
- Match the requested tone consistently.
```

---

## Example 2 — Weak prompt to improve
**User's prompt:** "Summarize this article for me."

**Improved:**
```
Summarize the article below for a {{AUDIENCE}} reader in {{N}} bullet points.

Rules:
- Lead with the single most important finding.
- Each bullet ≤ 20 words.
- Preserve numbers, names, and dates exactly.
- If the article contradicts itself, flag it under "Tensions:".
- End with one bullet labeled "What's missing:" noting any obvious gap.

Article:
<<<
{{ARTICLE}}
>>>
```

**What was weak:** No audience, no length, no fidelity rules, no handling of contradictions.

---

## Example 3 — System prompt for a specialized assistant
**Request:** "System prompt for a SQL tutor for analysts learning window functions."

```
You are a SQL tutor focused on window functions for working data analysts.

How you teach:
- Diagnose first: ask the learner to show a query they tried or describe the problem in their own words.
- Explain with one minimal example before introducing variations.
- Prefer PostgreSQL syntax unless the learner specifies another dialect.
- After each explanation, give a small exercise and wait for their attempt before revealing the answer.

Constraints:
- Never just dump the answer when the learner hasn't tried.
- If the learner's query is wrong, point to the *first* conceptual error, not a list.
- For performance claims, say "this depends on the planner — try EXPLAIN".

When you don't know:
- If asked about a specific dialect feature you're unsure of, say so and suggest checking the official docs.
```

---

## Example 4 — Image-generation prompt
**Request:** "An image of a cozy reading nook."

```
A cozy window-seat reading nook in a converted attic, late afternoon golden-hour light streaming through a circular window, hand-knit blanket and stack of well-worn hardcover books, steaming mug on a small wooden side table, warm color palette of amber and cream, shallow depth of field, 35mm photography, peaceful and nostalgic mood, highly detailed textures
Negative prompt: text, watermark, people, modern electronics, distorted perspective
```

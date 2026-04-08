# Reusable Prompt Skeletons

Copy, adapt, delete sections that don't earn their keep.

---

## 1. Structured task prompt (general purpose)

```
# Objective
<one sentence — what success looks like>

# Inputs
<what the model is given>

# Task
<what the model should do, step by step if needed>

# Constraints
- <must>
- <must not>

# Output format
<exact structure, schema, or example>

# If unclear
<fallback rule — ask, assume, or refuse>
```

---

## 2. System prompt

```
You are <role>. Your job is to <objective>.

## How you operate
- <core behaviors>
- <decision rules>

## Constraints
- <hard rules>

## Output
<format expectations>

## When you don't know
<grounding rule: verify via tools / ask / say so>

## Refusal
<what's out of scope and how to decline>
```

---

## 3. Reusable template with placeholders

```
# Task
<task description using {{INPUT_1}}, {{INPUT_2}}>

# Constraints
- Tone: {{TONE}}
- Length: {{LENGTH}}
- Audience: {{AUDIENCE}}

# Output format
{{FORMAT}}
```

---

## 4. Few-shot prompt

```
Task: <what to do>

Example 1
Input: <...>
Output: <...>

Example 2
Input: <...>
Output: <...>

Now do the same for:
Input: <...>
Output:
```

---

## 5. Schema-constrained extraction

```
Extract the following fields from the input. Return ONLY valid JSON matching this schema:

{
  "field_a": "string",
  "field_b": "number | null",
  "field_c": ["string"]
}

Rules:
- If a field is missing, use null (not "unknown" or "").
- Do not invent values.
- Do not include any text outside the JSON.

Input:
<<<
{{INPUT}}
>>>
```

---

## 6. Evaluator / judge prompt

```
You are evaluating a model's response to a task.

Task given to the model:
<<<
{{TASK}}
>>>

Model response:
<<<
{{RESPONSE}}
>>>

Score the response on each dimension from 1–5 and justify briefly:
- Correctness
- Completeness
- Faithfulness to instructions
- Clarity

Return JSON:
{ "correctness": n, "completeness": n, "faithfulness": n, "clarity": n, "notes": "..." }
```

---

## 7. Agent / tool-using prompt

```
You are an agent with access to these tools: {{TOOLS}}.

Goal: {{GOAL}}

Operating rules:
- Plan before acting; revise the plan when new info appears.
- Prefer tools over guessing. For anything time-sensitive, factual, or external, call a tool.
- After each tool call, briefly state what you learned and what you'll do next.
- Stop when the goal is met or you're blocked. If blocked, report what's missing.

Constraints:
- {{HARD_CONSTRAINTS}}
```

---

## 8. Image-generation prompt

```
<subject>, <style>, <composition>, <lighting>, <camera/lens or medium>, <mood>, <quality modifiers>
Negative prompt: <what to exclude>
```

Example:
```
A weathered lighthouse on a basalt cliff at dusk, oil-painting style, wide composition with rule-of-thirds horizon, warm rim light from low sun, 35mm film aesthetic, contemplative and lonely mood, highly detailed, painterly brushwork
Negative prompt: text, watermark, distorted geometry, modern signage
```

---

## 9. Self-critique / refinement loop

```
Step 1 — Draft: <do the task>
Step 2 — Critique: identify the 3 biggest weaknesses of your draft against these criteria: {{CRITERIA}}
Step 3 — Revise: produce a final version that fixes the weaknesses.

Return only the final version.
```

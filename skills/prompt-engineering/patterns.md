# Prompt Pattern Selection

Pick the simplest pattern that fits. Combine patterns only when each one is pulling weight.

| Pattern | Use when | Avoid when |
|---|---|---|
| **Direct** | Task is simple, one-shot, output is obvious | You need consistent structure across many runs |
| **Structured (sectioned)** | Task has multiple inputs/constraints; output format matters | Task is trivial — structure becomes overhead |
| **Role / persona** | Behavior, voice, or domain framing meaningfully changes the answer | "You are a world-class X" with no operational substance — drop it |
| **Constraint-heavy** | The risk is the model doing the *wrong* thing, not failing to do the right thing | Over-constraining a creative task |
| **Decomposition** | Task naturally splits into sub-steps the model often skips | The model already does the steps reliably |
| **Prompt chain** | Steps need different contexts, intermediate validation, or tool calls between them | A single prompt with sections would do |
| **Few-shot** | Format/style is hard to describe but easy to demonstrate | You can specify the format precisely in words — examples then just add tokens |
| **Rubric-driven** | The model should self-check against explicit criteria | The criteria are obvious from the task |
| **Schema-constrained (JSON/XML)** | Output will be parsed by code | A human is the only consumer |
| **Self-critique / refine loop** | Quality matters more than latency; first drafts are typically weak | Latency-sensitive or simple tasks |
| **Evaluator prompt** | You're grading another model's output | You actually want generation, not judgment |
| **Tool-orchestrating** | The model has tools and must decide when/how to call them | No tools available |
| **Template with placeholders** | The same prompt shape will be reused with varying inputs | A one-shot request |

## Heuristics

- **Start simple, add only on evidence.** A 3-line direct prompt that works beats a 30-line scaffold that "feels rigorous".
- **If output will be parsed, use a schema.** Don't hope — specify.
- **If the task has a "right answer" shape, show it.** Few-shot or schema.
- **If the model keeps hallucinating facts, the fix is grounding (tools/sources), not louder instructions.**
- **If the model keeps drifting off-task, the fix is usually a clearer objective + decision rules, not more role-play.**

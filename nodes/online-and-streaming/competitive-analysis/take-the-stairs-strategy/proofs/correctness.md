---
title: Waiting S minus E and then taking the stairs is within 2 minus E/S of the optimum, and no other wait limit does as well
proves: [correctness]
status: full
---

We use the ride time $E \ge 0$, the stair time $S > 0$, and the arrival time $t \in [0, \infty]$ of the elevator, with $t = \infty$ when it never comes. The rule with wait limit $w$ takes time $\mathrm{ALG}_w(t) = t + E$ if $t \le w$ and $w + S$ if $t > w$. The offline optimum is $\mathrm{OPT}(t) = \min(t + E, S)$, with $\mathrm{OPT}(\infty) = S$.

**Lemma 1 (the case $E \ge S$).** If $E \ge S$, line L1 gives time $S$, and $\mathrm{OPT}(t) = S$ for every $t$, since $t + E \ge S$. So the rule is optimal. $\square$

From now on $E < S$. Lines L2 to L5 run the rule with $w = S - E > 0$.

**Theorem 1 (upper bound).** For every $t$, $\mathrm{ALG}_{S-E}(t) \le (2 - E/S) \cdot \mathrm{OPT}(t)$, with equality for every $t > S - E$.

*Proof.* If $t \le S - E$, line L4 rides the elevator, so $\mathrm{ALG} = t + E \le S$ and $\mathrm{OPT} = t + E$. The ratio is 1, and $1 \le 2 - E/S$ because $E < S$. If $t > S - E$ (including $t = \infty$), line L5 walks at time $S - E$, so $\mathrm{ALG} = 2S - E$. Here $t + E > S$, so $\mathrm{OPT} = S$, and the ratio is $(2S - E)/S = 2 - E/S$. $\square$

**Lemma 2 (worst ratio of a wait limit).** For $0 < E < S$ and any $w \ge 0$,

$$\sup_t \frac{\mathrm{ALG}_w(t)}{\mathrm{OPT}(t)} = \frac{w + S}{\min(w + E, S)}.$$

*Proof.* For $t \le w$, the ratio is $(t + E)/\min(t + E, S)$. It is 1 while $t + E \le S$ and $(t + E)/S$ after that, so it is at most $(w + E)/\min(w + E, S)$. For $t > w$, the ratio is $(w + S)/\min(t + E, S)$. The denominator is non-decreasing in $t$, so the ratio is largest as $t$ decreases to $w$, where the denominator tends to $\min(w + E, S)$ (the function $\min(t + E, S)$ is continuous). So the supremum over $t > w$ is $(w + S)/\min(w + E, S)$. This is at least the bound for $t \le w$, because $w + S \ge w + E$. $\square$

**Theorem 2 (lower bound).** For $0 < E < S$, every deterministic online rule has worst ratio at least $2 - E/S$, and the wait limit $w = S - E$ is the only one that reaches it.

*Proof.* While the elevator has not come, the person learns nothing new, so a deterministic rule is a wait limit $w \in [0, \infty]$. If $w = \infty$, the input $t = \infty$ gives an infinite time against $\mathrm{OPT} = S$. Otherwise, by Lemma 2, the worst ratio is $g(w) = (w + S)/\min(w + E, S)$.

- If $w \le S - E$, then $g(w) = (w + S)/(w + E)$. Its derivative in $w$ is $(E - S)/(w + E)^2 < 0$, so $g$ is strictly decreasing on $[0, S - E]$, with minimum $g(S - E) = (2S - E)/S$.
- If $w \ge S - E$, then $g(w) = (w + S)/S$, which is strictly increasing, with minimum $g(S - E) = (2S - E)/S$.

So $g(w) \ge 2 - E/S$ with equality only at $w = S - E$. $\square$

**Corollary.** TAKE-THE-STAIRS is strictly $(2 - E/S)$-competitive, and this is the best ratio of any deterministic online rule. $\blacksquare$

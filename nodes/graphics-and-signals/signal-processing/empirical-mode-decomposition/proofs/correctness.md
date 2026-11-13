---
title: Completeness, the stopping rule and termination of EMD
proves: [correctness]
status: full
---

EMD has no convergence theory, and this note does not supply one. It proves only the three facts that hold for every input: the output adds up to the input, every mode stopped by the rule meets the rule, and the algorithm ends. We work in the real RAM, where the subtractions of lines L6 and L9 are exact; the implementation gets the same exactness by turning each envelope mean into a rational number before it subtracts. Nothing below depends on how the envelopes of line L5 are built.

**Lemma 1 (completeness).** At the start of every round of the loop of line L2, and when line L10 runs,

$$x = \sum_{c \in C} c + r.$$

*Proof.* By induction on the number of rounds. Before the first round, $C$ is empty and $r = x$ by line L1. Suppose the equation holds at the start of a round, and let $h$ be the sequence that line L8 appends. Then line L9 replaces $r$ by $r - h$, so the new sum is $\sum_{c \in C} c + h + (r - h) = \sum_{c \in C} c + r = x$. When the loop ends, by its test or by the cap, line L10 returns the last $C$ and $r$, for which the equation holds. $\square$

The lemma uses only that line L8 appends the same $h$ that line L9 subtracts. It holds for any envelopes, any stopping rule and any number of sifts, which is why it is the one property that every EMD code has.

**Lemma 2 (the stopping rule).** Let $c$ be a mode appended by line L8, and let $p$ be the value of $p$ at that time. Then $c$ is the result of one sift of $p$, that is $c = p - (U + V)/2$ with the envelopes of $p$. If the loop of lines L4 to L7 left because of the rule, then

$$\bigl|\#\mathrm{extrema}(c) - \#\mathrm{zero\ crossings}(c)\bigr| \le 1 \quad\text{and}\quad \mathrm{SD}(p, c) = \frac{\sum_i (p[i] - c[i])^2}{\sum_i p[i]^2} < \varepsilon.$$

Otherwise exactly $S$ sifts were done.

*Proof.* Each pass through line L6 first sets $p$ to the current $h$ and then replaces $h$ by one sift of it, so after the pass $h$ is one sift of $p$. Line L7 tests the condition on that pair. The loop leaves at line L7 only when the condition holds or $s = S$; in the first case the pair $(p, h)$ that satisfies it is the pair at line L8, with $c = h$. If the condition failed at every pass, the loop left because $s = S$. $\square$

The implementation stores $p$ and the reason with each mode, and the tests recompute the sift, the counts and $\mathrm{SD}$ from them.

**Lemma 3 (termination).** The algorithm ends after at most $K$ rounds of line L2, each with at most $S$ sifts.

*Proof.* The counter $s$ starts at 0 in line L3 and grows by one in each pass through line L6, and line L7 stops the inner loop at $s = S$ at the latest. Each round of the outer loop adds one mode to $C$, and line L2 stops when $|C| = K$. $\square$

**What is not proved.** Without the caps, nothing here shows that the inner loop ends: there is no theorem that the SD of successive sifts falls below $\varepsilon$, or that the extrema and zero crossings come to differ by at most one. There is no theorem that the outer loop reaches a residue with fewer than two extrema. And no theorem relates the modes to any components of the signal; the example on the page, where a tone of period 47 is spread over several modes, shows that they need not match. The second IMF condition of Huang et al., a zero envelope mean at every point, is never checked.

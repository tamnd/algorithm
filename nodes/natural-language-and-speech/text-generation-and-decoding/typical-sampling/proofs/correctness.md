---
title: The typical set is the shortest prefix of the tokens ordered by distance to the entropy
proves: [correctness]
status: full
---

We use the notation of the page. The input is a distribution $p$ over the vocabulary $V = \{0, \ldots, |V| - 1\}$, a threshold $0 < \tau \le 1$, and a number $u$ drawn uniformly from $[0, 1)$. Let $V^+ = \{i : p_i > 0\}$. The entropy is $H = -\sum_{i \in V^+} p_i \log p_i$, and the distance of a token $i \in V^+$ is $d_i = |-\log p_i - H|$, the gap between its surprisal and the entropy. We assume exact arithmetic for the masses; the remark at the end treats rounding.

Let $i_1, \ldots, i_n$ with $n = |V^+|$ be the order of line L3: the tokens of $V^+$ sorted by the key $(d_i, i)$. Let $M(m)$ be the mass of the first $m$ of them. $M$ does not decrease and $M(n) = 1 \ge \tau$.

**Lemma 1 (the kept set).** Lines L4 to L6 return $K = \{i_1, \ldots, i_{m^*}\}$, where $m^*$ is the smallest $m$ with $M(m) \ge \tau$. Every token of $K$ has positive probability, and every token of $K$ has a distance at most the distance of every token of $V^+ \setminus K$.

*Proof.* The running sum after the token $i_t$ is $M(t)$, and line L6 stops at the first $t$ with $M(t) \ge \tau$, which exists since $M(n) = 1$. The tokens of probability 0 are left out at line L2. The order of line L3 sorts by distance first, so every token in the first $m^*$ positions has a distance at most that of every later token. $\square$

**Lemma 2 (the log base does not matter).** If every log is taken to a base $b > 1$ in place of $e$, the order of line L3 is the same, and so is $K$.

*Proof.* In base $b$, every surprisal and the entropy are divided by $\ln b > 0$, so every distance is divided by the same positive number. The keys $(d_i, i)$ keep their order. $\square$

The paper of Meister et al. works with bits; the code works with nats, and by Lemma 2 both give the same set. With floats, two different probabilities can have exactly equal distances in exact arithmetic, for example $1/4$ and $1/2$ in $(1/4, 1/4, 1/2)$, where $H = 1.5$ bits and both distances are $0.5$ bits. Then the order between them depends on rounding.

**Theorem 3 (the draw).** Let $Z = M(m^*)$. TYPICAL-SAMPLE returns each $i \in K$ with probability $p_i / Z$, and returns no other token.

*Proof.* As for [top-k sampling](/top-k-sampling/): $r = uZ$ is uniform on $[0, Z)$, the walk of lines L8 to L10 returns $i_t$ for the unique $t$ with $M(t - 1) \le r < M(t)$, and that interval has length $p_{i_t}$. Since $r < Z$, line L11 is not reached. $\square$

**Corollary 4 (special cases).**
(a) For $\tau = 1$, $K = V^+$ and the step samples from $p$.
(b) For a uniform distribution on $n$ tokens, all distances are 0, and $K$ is the $\lceil \tau n \rceil$ tokens of smallest index.
(c) The most probable token need not be in $K$. For a small $\tau$, $K$ is the single token closest to the entropy.

*Proof.* (a) Every token of $V^+$ has positive probability, so $M(m) < 1$ for $m < n$, and $m^* = n$. (b) With $p_i = 1/n$, $-\log p_i = \log n = H$, so every $d_i = 0$, the order is by index, and $M(m) = m / n \ge \tau$ first holds at $m = \lceil \tau n \rceil$. (c) In the example of the page, with $p$ = (0.40, 0.25, 0.15, 0.10, 0.06, 0.04), the token of probability 0.25 has the smallest distance, and $\tau = 0.2$ keeps it alone. $\square$

**Proposition 5 (the greedy prefix and the optimization problem differ).** Meister et al. state the kept set as the solution of: minimize $\sum_{i \in S} d_i$ over the sets $S$ with $\sum_{i \in S} p_i \ge \tau$. The prefix $K$ of Lemma 1 does not always solve this problem.

*Proof.* Take $p = (0.4, 0.3, 0.2, 0.1)$ and $\tau = 0.35$. Then $H = 1.2799$ nats, and the distances are $0.3636$, $0.0759$, $0.3296$ and $1.0227$. The order is (0.3, 0.2, 0.4, 0.1), the masses of its prefixes are $0.3$ and $0.5$, so $K$ holds the tokens of probability 0.3 and 0.2, with total distance $0.4055$. The set that holds only the token of probability 0.4 has mass $0.4 \ge 0.35$ and total distance $0.3636 < 0.4055$. So $K$ is not optimal, and the optimal set leaves out the token closest to the entropy. $\square$

The algorithm that the paper describes and that implementations use is the greedy prefix of Lemma 1, which keeps the tokens closest to the entropy. The arXiv version 6 of the paper notes this mismatch between the formulation and the algorithm in an erratum. The tests check the counterexample above, and a second one with $p = (1/2, 1/4, 1/8, 1/8)$ and $\tau = 0.3$, by enumerating all subsets.

**Remark (rounding).** The entropy and the distances are floats, so the order can differ from the exact order when two distances are equal or nearly equal, as in Lemma 2. The masses are summed in the type of the input; with floats the running sum can stay below $\tau$ to the end, and then the code keeps all of $V^+$, which is the result for $\tau = 1$.

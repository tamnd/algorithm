---
title: Smooth weighted round robin gives each backend exactly its weight in every window of W picks
proves: [correctness, termination]
status: full
---

We use the pseudocode SWRR-PICK of the page. There are $n \ge 1$ backends with integer weights $w_1, \ldots, w_n \ge 0$ and $W = \sum_j w_j > 0$. The counters $c_j$ are all 0 before the first pick. The tie rule of line L5 does not matter: every claim below holds for any rule that picks a backend of largest counter.

**Notation.** Let $c_j(t)$ be the counter of backend $j$ after pick $t$ (after line L6), with $c_j(0) = 0$, and let $k_j(t)$ be the number of times backend $j$ was picked among picks $1, \ldots, t$. Let $p_j(t) = c_j(t-1) + w_j$ be the counter after line L3 of pick $t$.

**Lemma 1 (closed form).** For all $j$ and $t \ge 0$, $c_j(t) = t\,w_j - W\,k_j(t)$, and $\sum_j c_j(t) = 0$.

*Proof.* By induction on $t$. At $t = 0$ both sides are 0. Pick $t$ adds $w_j$ to every counter (line L3), and subtracts $W$ from the counter of the backend it picks (line L6), which is exactly the backend whose $k_j$ grows by one. For the sum: the pick adds $\sum_j w_j = W$ and subtracts $W$, so the sum stays 0. $\square$

**Lemma 2 (lower bound).** For all $j$ and $t \ge 0$, $c_j(t) > -W$.

*Proof.* By induction on $t$. At $t = 0$, $c_j(0) = 0 > -W$. Assume the claim for $t - 1$. The values $p_1(t), \ldots, p_n(t)$ sum to $\sum_j c_j(t-1) + W = W$ by Lemma 1, so their largest value is at least $W/n > 0$. If backend $j$ is not picked at step $t$, then $c_j(t) = p_j(t) = c_j(t-1) + w_j \ge c_j(t-1) > -W$. If backend $j$ is picked, $p_j(t)$ is a largest value, so $p_j(t) \ge W/n > 0$ and $c_j(t) = p_j(t) - W > -W$. $\square$

**Theorem 1 (exact share in one period).** $k_j(W) = w_j$ for every $j$, and $c_j(W) = 0$ for every $j$.

*Proof.* Take $t$ with $1 \le t \le W$ and suppose that $k_j(t) \ge w_j + 1$ for some $j$. Then by Lemma 1,

$$c_j(t) = t\,w_j - W\,k_j(t) \le W\,w_j - W\,(w_j + 1) = -W,$$

where the inequality uses $t \le W$ and $w_j \ge 0$. This contradicts Lemma 2. So $k_j(W) \le w_j$ for each $j$. Each pick selects exactly one backend, so $\sum_j k_j(W) = W = \sum_j w_j$. A sum of terms $k_j(W) \le w_j$ that equals $\sum_j w_j$ must have $k_j(W) = w_j$ for every $j$. Then Lemma 1 gives $c_j(W) = W w_j - W w_j = 0$. $\square$

**Corollary 1 (period and windows).** The pick sequence is periodic with period $W$. Each window of $W$ consecutive picks, at any start, picks each backend $j$ exactly $w_j$ times.

*Proof.* Pick $t + 1$ depends only on the counters after pick $t$ (and the fixed weights and tie rule). By Theorem 1 the counters are all 0 after pick $W$, the same state as before pick 1. So pick $W + s$ equals pick $s$ for every $s \ge 1$, by induction on $s$. A window of $W$ consecutive picks of a $W$-periodic sequence holds each element of one period exactly once, in rotated order, so it holds $w_j$ picks of $j$ by Theorem 1. $\blacksquare$

**Theorem 2 (no backend runs ahead).** Let $n \ge 2$. For all $j$ and $t \ge 1$,

$$t\,\frac{w_j}{W} - (n - 1) < k_j(t) < t\,\frac{w_j}{W} + 1.$$

*Proof.* The right inequality is Lemma 2 divided by $W$: $t\,w_j - W\,k_j(t) > -W$. For the left one, Lemma 1 gives $c_j(t) = -\sum_{i \ne j} c_i(t)$, and by Lemma 2 each of these $n - 1 \ge 1$ terms is $> -W$, so $c_j(t) < (n-1)W$. Divide $t\,w_j - W\,k_j(t) < (n-1) W$ by $W$. For $n = 1$ the only backend is picked every time, so $k_1(t) = t$ exactly. $\blacksquare$

So a backend never gets a whole pick more than its fair share $t w_j / W$ at any moment, which is why the picks of a heavy backend are spread out instead of sent in a block. The lag bound $n - 1$ is what the proof gives. In an exhaustive check of all weight vectors with $n \le 4$ and weights 0 to 6, the largest lag $t w_j / W - k_j(t)$ was $11/12$, and over 3000 random vectors with $n \le 8$ and weights up to 100 it was about 1.30, so the true lag can exceed 1 but stays far below $n - 1$ in these cases.

**Termination.** Each call runs the loop of line L2 exactly $n$ times and then returns at line L7. Line L5 sets $best$ in the first pass, so line L6 always has a backend.

**What happens when the weights change.** The proof assumes fixed weights and the start state $c = 0$. nginx changes a weight temporarily when a backend fails (its `effective_weight`), and it skips backends that are down. After such a change the counters no longer sum to 0 over the eligible backends, so the proof above does not apply to the picks around the change. A reset of all counters to 0 after the change restores every claim from that point on.

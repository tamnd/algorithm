---
title: Deferred-merge embedding gives a zero-skew tree of least wire length for its topology under linear delay
proves: [correctness, optimality, merging segments, complexity]
status: full
---

**Model.** The sinks are points $p_s$ of the plane, with the L1 distance $d$. A topology $G$ is a full binary tree whose leaves are the sinks. A *zero-skew tree* (ZST) on $G$ gives each internal node $v$ a point $p_v$ and each non-root node $c$ an edge length $e_c \ge d(p_c, p_{\text{parent}(c)})$; a length above the distance is a detour wire. Under *linear delay* the delay of a path is the sum of its edge lengths, and the tree has zero skew when all root-to-sink paths have the same length. The cost of the tree is $\sum_c e_c$. For a subtree $T_v$ and a ZST of it, its *delay* is the common length from $p_v$ to its sinks. (If all root-to-sink lengths are equal, then for each $v$ all lengths from $v$ to its sinks are equal, since those paths share the part above $v$.)

**Rotation.** Map $(x, y) \mapsto (u, v) = (x + y, x - y)$. Then $d$ becomes the L-infinity distance $\max(|\Delta u|, |\Delta v|)$. A *box* is a product of two closed intervals in $(u, v)$. For a box $S$ and a point $q$, $d(q, S) = \max(g_u, g_v)$, where $g_u$ and $g_v$ are the distances from the coordinates of $q$ to the intervals of $S$. The *TRR* of $S$ with radius $e \ge 0$ is the box $S$ widened by $e$ on all sides, which is $\{q : d(q, S) \le e\}$.

**Lemma 1 (two facts on boxes).** Let $S, S_1, S_2$ be boxes, $e \ge 0$ and $q$ a point. (a) $d(q, \mathrm{TRR}(S, e)) = \max(0, d(q, S) - e)$. (b) If $S_1 \cap S_2 \ne \emptyset$, then $d(q, S_1 \cap S_2) = \max(d(q, S_1), d(q, S_2))$.

*Proof.* (a) Widening an interval by $e$ lowers the gap from a number to it from $g$ to $\max(0, g - e)$, and $\max(\max(0, g_u - e), \max(0, g_v - e)) = \max(0, \max(g_u, g_v) - e)$. (b) For intervals $I, J$ that meet, $I \cap J = [\max(\text{lows}), \min(\text{highs})]$, so the gap from a number to $I \cap J$ is the larger of its gaps to $I$ and to $J$. Take the maximum over the two coordinates. $\square$

**The algorithm's values.** For a sink, $\mathrm{ms} = \{p_s\}$, $t^* = 0$, $W^* = 0$. For an internal node $v$ with children $a, b$, let $D = d(\mathrm{ms}(a), \mathrm{ms}(b))$. If $|t^*_a - t^*_b| \le D$, then $e^*_a = (D + t^*_b - t^*_a)/2$ and $e^*_b = D - e^*_a$; if $t^*_a > t^*_b + D$, then $e^*_a = 0$, $e^*_b = t^*_a - t^*_b$; the last case is the mirror. Then $t^*_v = t^*_a + e^*_a = t^*_b + e^*_b$, $W^*_v = W^*_a + W^*_b + e^*_a + e^*_b$ and $\mathrm{ms}(v) = \mathrm{TRR}(\mathrm{ms}(a), e^*_a) \cap \mathrm{TRR}(\mathrm{ms}(b), e^*_b)$.

**Lemma 2 (the regions are nonempty segments).** Every $\mathrm{ms}(v)$ is a nonempty box with at least one side of length 0, that is, a segment of slope $\pm 1$ in the plane or a point (a *Manhattan arc*).

*Proof.* By induction. A sink is a point. In the first case, $e^*_a, e^*_b \ge 0$ and $e^*_a + e^*_b = D$. In each coordinate the gap between the intervals of $\mathrm{ms}(a)$ and $\mathrm{ms}(b)$ is at most $D$, so the widened intervals meet, and the intersection is nonempty. In a coordinate where the gap is exactly $D$, the widened intervals touch at one value, so that side has length 0. If $D = 0$, then $e^*_a = e^*_b = 0$ and the region is $\mathrm{ms}(a) \cap \mathrm{ms}(b) \subseteq \mathrm{ms}(a)$, which has a side of length 0 by induction. In the detour case, $\mathrm{ms}(v) = \mathrm{ms}(a) \cap \mathrm{TRR}(\mathrm{ms}(b), e^*_b) \subseteq \mathrm{ms}(a)$, which has a side of length 0 by induction, and it is nonempty because $e^*_b > D$, so the point of $\mathrm{ms}(a)$ nearest to $\mathrm{ms}(b)$ lies in it. $\square$

**Theorem 1 (the output is a ZST of cost $W^*$).** The top-down phase gives a ZST on $G$ with delay $t^*_{\text{root}}$ and cost $W^*_{\text{root}} = \sum_c e^*_c$.

*Proof.* The root gets a point of $\mathrm{ms}(\text{root})$. If a node $v$ has a point $q \in \mathrm{ms}(v)$, then $q \in \mathrm{TRR}(\mathrm{ms}(c), e^*_c)$ for each child $c$, so $d(q, \mathrm{ms}(c)) \le e^*_c$. The child gets the point of $\mathrm{ms}(c)$ nearest to $q$ (clamp each rotated coordinate into its interval), so $d(p_c, q) \le e^*_c$, and the edge of length $e^*_c$ is allowed. A sink gets its own point, since its region is that point. By induction on the height, the length from a point of $\mathrm{ms}(v)$ down to every sink of $T_v$ is $t^*_v$, since $t^*_a + e^*_a = t^*_b + e^*_b = t^*_v$. The cost is the sum of the $e^*_c$, which is $W^*_{\text{root}}$ by its definition. $\square$

**Lemma 3 (lower bounds).** For every node $v$ and every ZST of $T_v$ with root point $p$, delay $\tau$ and cost $W$:
$$ \text{(i)}\ \ \tau \ge t^*_v + d(p, \mathrm{ms}(v)), \qquad \text{(ii)}\ \ W - \tau \ge W^*_v - t^*_v. $$

*Proof.* By induction on the height of $v$. For a sink the only ZST is the sink itself, with $p = p_s$, $\tau = 0$ and $W = 0$, and both hold with equality. Let $v$ have children $a, b$, and take a ZST of $T_v$ with root $p$. Its parts are ZSTs of $T_a$ and $T_b$ with roots $p_a, p_b$, delays $\tau_a, \tau_b$ and costs $W_a, W_b$, and $\tau = \tau_a + e_a = \tau_b + e_b$ with $e_a \ge d(p, p_a)$ and $e_b \ge d(p, p_b)$.

For (i): by induction and the triangle inequality for the distance to a set,
$$ \tau = \tau_a + e_a \ge t^*_a + d(p_a, \mathrm{ms}(a)) + d(p, p_a) \ge t^*_a + d(p, \mathrm{ms}(a)), $$
and in the same way $\tau \ge t^*_b + d(p, \mathrm{ms}(b))$. Subtract $t^*_v = t^*_a + e^*_a = t^*_b + e^*_b$:
$$ \tau - t^*_v \ge M := \max\big(d(p, \mathrm{ms}(a)) - e^*_a,\ d(p, \mathrm{ms}(b)) - e^*_b\big). $$
First, $M \ge 0$. In the detour case $e^*_a = 0$, so the first term is $d(p, \mathrm{ms}(a)) \ge 0$, and the mirror case is the same. In the other case, if both terms were negative, then $D \le d(p, \mathrm{ms}(a)) + d(p, \mathrm{ms}(b)) < e^*_a + e^*_b = D$, which is false. So $M = \max(0, M)$, and by Lemma 1 (a) and (b) this is $\max(d(p, \mathrm{TRR}(\mathrm{ms}(a), e^*_a)), d(p, \mathrm{TRR}(\mathrm{ms}(b), e^*_b))) = d(p, \mathrm{ms}(v))$, using Lemma 2 for the nonempty intersection.

For (ii): since $e_a = \tau - \tau_a$ and $e_b = \tau - \tau_b$,
$$ W - \tau = W_a + W_b + e_a + e_b - \tau = (W_a - \tau_a) + (W_b - \tau_b) + \tau. $$
The same computation for the algorithm's values gives $W^*_v - t^*_v = (W^*_a - t^*_a) + (W^*_b - t^*_b) + t^*_v$. The first two terms compare by induction, and $\tau \ge t^*_v$ by (i). $\square$

**Theorem 2 (least wire length).** Every ZST on the topology $G$ costs at least $W^*_{\text{root}}$. So the tree of Theorem 1 has the least cost among all zero-skew trees on $G$ under linear delay.

*Proof.* By Lemma 3 at the root, $W = (W - \tau) + \tau \ge (W^*_{\text{root}} - t^*_{\text{root}}) + t^*_{\text{root}} + d(p, \mathrm{ms}(\text{root})) \ge W^*_{\text{root}}$. $\square$

The proof also shows that a root point outside $\mathrm{ms}(\text{root})$ costs at least its distance to the region in extra wire, which is why the region is the set of best root points.

**Theorem 3 (time).** For $n$ sinks and a given topology the algorithm runs in $O(n)$ time.

*Proof.* There are $n - 1$ internal nodes. At each, the bottom-up phase computes one distance between boxes, two widened boxes and one intersection, and the top-down phase does one clamp, each in $O(1)$ arithmetic operations. $\square$

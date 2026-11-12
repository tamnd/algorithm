---
title: Correctness of Whitted ray tracing
proves: [correctness]
status: full
---

**Claim.** For a ray $r_0 = (o, d)$ and a depth $D \ge 0$, TRACE returns $V_D(r_0)$, the value that the problem defines by the recursion over the ray tree. This holds in exact arithmetic, given a closest-hit query that returns the first hit in $(\varepsilon, \infty)$ and a shadow test that answers whether an object meets the open segment to the light, the same queries that the definition of $V$ uses.

**Notation.** For an entry $e = (r, w, k)$ of the stack, with $k \le D$, let its value be $w \cdot V_{D-k}(r)$. For a ray $r$ that hits something, let $\lambda(r)$ be its local term $k_a + k_d \sum_\ell E_\ell \cos\theta_\ell$, the sum over the lights visible from the hit; for a ray that hits nothing, let $\lambda(r)$ be the background. Let $C(r)$ be the set of its children: the reflected ray with the coefficient $k_s$ if $k_s > 0$, and the refracted ray with the coefficient $k_t$ if $k_t > 0$ and the refracted direction exists. Then the definition reads

$$V_0(r) = \lambda(r), \qquad V_j(r) = \lambda(r) + \sum_{(r', c) \in C(r)} c\,V_{j-1}(r') \quad (j \ge 1),$$

since a term with the coefficient 0 adds nothing, and a ray that hits nothing has no children.

**Invariant.** Before each test of line L4,

$$I + \sum_{(r, w, k) \in S} w \cdot V_{D-k}(r) = V_D(r_0),$$

and every entry of $S$ has a depth $k \le D$.

*Start.* Line L3 sets $I = 0$ and $S = \{(r_0, 1, 0)\}$, so the left side is $V_D(r_0)$, and the depth is $0 \le D$.

*Step.* Line L5 removes an entry $(r, w, k)$, whose value is $w\,V_{D-k}(r)$. Lines L6 to L11 add $w\,\lambda(r)$ to $I$: line L7 adds $w$ times the background for a miss, and lines L9 to L11 add $w$ times the ambient term and the diffuse term of each visible light, which is $w\,\lambda(r)$ by the definition. Two cases remain.

- If $k = D$, or the ray hits nothing, nothing is pushed. Then $V_{D-k}(r) = \lambda(r)$, because $V_0 = \lambda$ and a miss has no children, so the left side has lost $w\,V_{D-k}(r)$ and gained $w\,\lambda(r)$, the same amount.
- If $k < D$ and the ray hits, lines L13 and L14 push $(r', w c, k + 1)$ for each child $(r', c) \in C(r)$, which is exactly the set of children by the tests $k_s > 0$, $k_t > 0$ and the existence of the refracted direction. Their values add up to $\sum w c\,V_{D-k-1}(r')$, and with the added $w\,\lambda(r)$ this is $w\,V_{D-k}(r)$ by the recursion with $j = D - k \ge 1$. The left side does not change, and the new depths are $k + 1 \le D$.

So the invariant holds before the next test of line L4.

**Termination.** Every entry corresponds to a node of the ray tree of $r_0$ cut at the depth $D$, a binary tree of height $D$, and every node is pushed at most once, by its parent. So there are at most $2^{D+1} - 1$ iterations, and the loop ends.

**Conclusion.** When the loop ends, $S$ is empty, and the invariant gives $I = V_D(r_0)$, which line L15 returns. Line L2 stores this value for the ray through the center of each pixel, which is what the problem asks. $\blacksquare$

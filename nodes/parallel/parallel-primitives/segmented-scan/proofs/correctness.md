---
title: The segmented operator is associative, and one scan with it gives the segmented scan
proves: [correctness]
status: full
---

**Statement.** Let $(S, \oplus, e)$ be a [monoid](/monoid/). On $\{0, 1\} \times S$ define
$$
(f, x) \oplus_s (g, y) = (f \lor g,\ \ y \text{ if } g = 1, \text{ else } x \oplus y).
$$
Then $\oplus_s$ is associative with identity $(0, e)$. Let $A[0 \ldots n-1]$ be an array over $S$ and $F[0 \ldots n-1]$ an array of flags, with $F[i] = 1$ when a segment starts at $i$ and with position 0 treated as a start. For each $i$ let $s(i)$ be the largest $j \le i$ that starts a segment. Then SEGMENTED-SCAN returns $I[i] = A[s(i)] \oplus \cdots \oplus A[i]$ and $X[i] = A[s(i)] \oplus \cdots \oplus A[i-1]$ (which is $e$ when $s(i) = i$). With a work-efficient scan on line L2, it takes $O(n)$ work and $O(\log n)$ span.

## 1. Associativity

Let $p = (f, x)$, $q = (g, y)$ and $r = (h, z)$. The flag of both $(p \oplus_s q) \oplus_s r$ and $p \oplus_s (q \oplus_s r)$ is $f \lor g \lor h$, because $\lor$ is associative. For the value, there are three cases.

1. **$h = 1$.** On the left, the outer combine has right flag 1, so the value is $z$. On the right, $q \oplus_s r$ has flag $g \lor h = 1$ and value $z$, so the outer combine also gives $z$.
2. **$h = 0$ and $g = 1$.** On the left, $p \oplus_s q$ has value $y$, and the outer combine gives $y \oplus z$. On the right, $q \oplus_s r = (1, y \oplus z)$, whose flag is 1, so the outer combine gives $y \oplus z$.
3. **$h = 0$ and $g = 0$.** On the left, $p \oplus_s q = (f, x \oplus y)$ and the outer combine gives $(x \oplus y) \oplus z$. On the right, $q \oplus_s r = (0, y \oplus z)$ and the outer combine gives $x \oplus (y \oplus z)$. These are equal because $\oplus$ is associative.

**Identity.** $(0, e) \oplus_s (g, y) = (g, y)$ in both cases of $g$, since $e \oplus y = y$; and $(f, x) \oplus_s (0, e) = (f, x \oplus e) = (f, x)$. So $(\{0, 1\} \times S, \oplus_s, (0, e))$ is a monoid. It is not commutative: $(1, 1) \oplus_s (0, 2) = (1, 3)$ but $(0, 2) \oplus_s (1, 1) = (1, 1)$ for $+$. So the scan on line L2 must keep the order of the operands, as the [Blelloch scan](/blelloch-scan/) does.

## 2. The pair prefixes

Line L1 sets $P[i] = (F'[i], A[i])$, where $F'[i] = F[i]$ for $i \ge 1$ and $F'[0] = 1$. Write $\Pi_i = P[0] \oplus_s \cdots \oplus_s P[i]$, which is well defined by part 1, with $\Pi_{-1} = (0, e)$.

**Claim.** For $i \ge 0$, $\Pi_i = (1, A[s(i)] \oplus \cdots \oplus A[i])$.

*Proof by induction on $i$.* For $i = 0$, $\Pi_0 = P[0] = (1, A[0])$ and $s(0) = 0$. For $i \ge 1$, $\Pi_i = \Pi_{i-1} \oplus_s P[i]$. If $F[i] = 1$, then $s(i) = i$ and the combine gives $(1, A[i])$. If $F[i] = 0$, then $s(i) = s(i-1)$ and the combine gives $(1, (A[s(i)] \oplus \cdots \oplus A[i-1]) \oplus A[i])$. $\square$

## 3. The outputs

Line L2 computes the exclusive scan $Q[i] = \Pi_{i-1}$ of $P$ under $\oplus_s$, which any correct scan algorithm does for an associative operator with an identity.

- **Inclusive.** Line L4 sets $I[i]$ to the value of $Q[i] \oplus_s P[i] = \Pi_i$, which is $A[s(i)] \oplus \cdots \oplus A[i]$ by the claim.
- **Exclusive.** If $F'[i] = 1$, then $s(i) = i$, the wanted value is the empty product $e$, and line L5 returns $e$. If $F'[i] = 0$, then $i \ge 1$ and $s(i) = s(i-1)$, so by the claim the value of $Q[i] = \Pi_{i-1}$ is $A[s(i)] \oplus \cdots \oplus A[i-1]$, which line L5 returns. The test on the flag is needed: at a segment start, $Q[i]$ holds the sum of the end of the previous segment, not $e$.

## 4. Cost

Lines L1, L3, L4 and L5 are maps with $O(1)$ work for each $i$. Each application of $\oplus_s$ is one application of $\oplus$ and one $\lor$, so $O(1)$. With the Blelloch scan on line L2, the work is $2(m - 1)$ applications of $\oplus_s$ for $m = 2^{\lceil \lg n \rceil} < 2n$, plus $n$ on line L4, and the span is $2 \lceil \lg n \rceil$ rounds of the scan plus one round for lines L3 to L5. So the work is $O(n)$ and the span is $O(\log n)$. $\blacksquare$

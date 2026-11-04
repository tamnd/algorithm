---
title: The Flajolet-Martin sketch is a function of the set of distinct items
proves: [correctness, invariant, termination]
status: full
---

For an item $x$ let $j(x) = h(x) \bmod m$, $q(x) = \lfloor h(x)/m \rfloor$, and call $x$ *recorded* if $q(x) > 0$ and $\rho(q(x)) < L$; then let $r(x) = \rho(q(x))$. For a set $A$ of items define the bitmaps $\Sigma(A)$ by
$$ \Sigma(A)_j[r] = 1 \iff \text{some recorded } x \in A \text{ has } j(x) = j \text{ and } r(x) = r. $$

**Lemma 1 (invariant).** After the items $a_1, \ldots, a_t$ have been added, the bitmaps equal $\Sigma(\{a_1, \ldots, a_t\})$.

*Proof.* By induction on $t$. For $t = 0$ line L1 gives all zeros, which is $\Sigma(\emptyset)$. Let the claim hold for $t$ and let $A = \{a_1, \ldots, a_t\}$ and $x = a_{t+1}$. Line L3 computes $j(x)$ and $q(x)$, and line L4 sets bit $r(x)$ of $B_{j(x)}$ if $x$ is recorded, and does nothing otherwise. No bit is cleared. So the new bitmaps have a 1 exactly at the 1s of $\Sigma(A)$ and, if $x$ is recorded, at $(j(x), r(x))$. This is $\Sigma(A \cup \{x\})$. $\square$

**Theorem.**
1. The state, and so the output of ESTIMATE, depends only on the set of distinct items seen, not on their order or their number of repeats.
2. The bitwise OR of the sketches of two streams with the same $m$, $L$ and $h$ equals the sketch of the concatenated stream.
3. $R_j$ is the least $r \in \{0, \ldots, L\}$ such that $r = L$ or $B_j[r] = 0$, and ESTIMATE returns $(m/\varphi) 2^{S/m}$ with $S = \sum_j R_j$.
4. Each operation ends: ADD takes a constant number of steps, and ESTIMATE scans at most $L + 1$ positions of each of the $m$ bitmaps.

*Proof.* Claim 1 is Lemma 1, since $\Sigma(A)$ depends only on $A$. For claim 2, the definition gives $\Sigma(A \cup A') = \Sigma(A) \lor \Sigma(A')$ bit by bit, because "some recorded $x \in A \cup A'$" is "some recorded $x \in A$ or some recorded $x \in A'$". Claims 3 and 4 follow from lines L5 to L7 and the definition of $R_j$. $\blacksquare$

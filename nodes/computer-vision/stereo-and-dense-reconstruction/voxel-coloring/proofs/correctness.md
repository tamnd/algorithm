---
title: Voxel coloring returns the consistent scene that is nearest to the cameras at every pixel
proves: [correctness]
status: full
---

We use the layered model and the pseudocode of the page. The voxels are split into layers $0, 1, \dots, L - 1$ in order of distance from the cameras. The ray of each pixel $p$ meets each layer $k$ in at most one voxel, $r_k(p)$. Each pixel has a value $I(p)$, which is a gray value or the background mark $\bot$.

For a set of voxels $S$, the owner $o_S(p)$ of a pixel is $r_j(p)$ for the least $j$ with $r_j(p) \in S$, or nothing. The pixels of $v$ are $P_S(v) = \{p : o_S(p) = v\}$. The test $c(A)$ on a multiset of values is true if $\bot \notin A$ and $\max A - \min A \le \tau$, and true for the empty multiset. It is monotone: if $c(A)$ holds and $B \subseteq A$, then $c(B)$ holds, because $\bot \notin B$ and the range of $B$ is at most the range of $A$.

A scene $S$ is *consistent* if $c(I(P_S(v)))$ holds for every $v \in S$ and every pixel with $I(p) \ne \bot$ has an owner in $S$. Assume that at least one consistent scene exists. For each pixel let

$$\ell(p) = \min \{ j : o_S(p) = r_j(p) \text{ for some consistent scene } S \},$$

with $\ell(p) = \infty$ if no consistent scene gives $p$ an owner. For $\ell(p) < \infty$ let $V_p = r_{\ell(p)}(p)$, and let $\bar S = \{V_p : \ell(p) < \infty\}$. This is the scene of Seitz and Dyer: each pixel sees the nearest voxel that any consistent scene lets it see.

**Lemma 1.** Every pixel $q$ has $o_{\bar S}(q) = V_q$ if $\ell(q) < \infty$, and no owner in $\bar S$ if $\ell(q) = \infty$.

*Proof.* Suppose some $V_r \in \bar S$ equals $r_j(q)$ with $j < \ell(q)$. Let $S_r$ be a consistent scene with $o_{S_r}(r) = V_r$, so $V_r \in S_r$. Then $q$ has an owner in $S_r$ at a layer at most $j$, which contradicts the minimum in the definition of $\ell(q)$. So no voxel of $\bar S$ lies on the ray of $q$ before layer $\ell(q)$. If $\ell(q) < \infty$, the voxel $V_q \in \bar S$ lies at layer $\ell(q)$, so it is the owner. If $\ell(q) = \infty$, no voxel of $\bar S$ lies on the ray at all. $\square$

**Lemma 2.** $\bar S$ is consistent.

*Proof.* Let $w \in \bar S$, with $w = V_r$ in layer $j = \ell(r)$, and let $S_r$ be consistent with $o_{S_r}(r) = w$. By Lemma 1, $P_{\bar S}(w) = \{q : V_q = w\}$. For such a $q$, $\ell(q) = j$ and $r_j(q) = w \in S_r$, so the owner of $q$ in $S_r$ is at a layer at most $j$. It is also at a layer at least $\ell(q) = j$. So $o_{S_r}(q) = w$, and $P_{\bar S}(w) \subseteq P_{S_r}(w)$. The test holds on $P_{S_r}(w)$, so it holds on $P_{\bar S}(w)$ by monotonicity. A pixel with $I(q) \ne \bot$ has an owner in the consistent scene that is assumed to exist, so $\ell(q) < \infty$ and $q$ has the owner $V_q$ in $\bar S$ by Lemma 1. $\square$

Let $U_k$ be the set of unmarked pixels at the start of layer $k$ in line L2, and let $\pi_k(v) = \{p \in U_k : r_k(p) = v\}$, which is the set of line L4.

**Lemma 3 (invariant).** For every $k$: $U_k = \{p : \ell(p) \ge k\}$, and a voxel $v$ of layer $k$ is colored at line L5 if and only if $v \in \bar S$.

*Proof.* By induction on $k$. $U_0$ is the set of all pixels, as line L1 marks none.

Assume $U_k = \{p : \ell(p) \ge k\}$ and let $v$ be in layer $k$.

(a) Suppose $v \in \bar S$, so $v = V_{p_0}$ with $\ell(p_0) = k$. Then $p_0 \in U_k$ and $p_0 \in \pi_k(v)$, so $\pi_k(v)$ is not empty. Let $S$ be a consistent scene with $o_S(p_0) = v$. Take any $p \in \pi_k(v)$. Then $\ell(p) \ge k$, so the owner of $p$ in $S$ is at a layer at least $k$. But $r_k(p) = v \in S$, so the owner is at a layer at most $k$. Hence $o_S(p) = v$, and $\pi_k(v) \subseteq P_S(v)$. The test holds on $P_S(v)$, so it holds on $\pi_k(v)$, and $v$ is colored.

(b) Suppose $v \notin \bar S$ and, to get a contradiction, that $v$ is colored, so $\pi_k(v)$ is not empty and passes the test. Every $p \in \pi_k(v)$ has $\ell(p) > k$: if $\ell(p) = k$, then $v = r_k(p) = V_p \in \bar S$. Let $T = \bar S \cup \{v\}$. For a pixel $p$ with $r_k(p) = v$ and $\ell(p) > k$, Lemma 1 says that no voxel of $\bar S$ is on the ray of $p$ before layer $\ell(p)$, so $o_T(p) = v$. For a pixel with $r_k(p) = v$ and $\ell(p) < k$, the owner $V_p$ is in front of $v$ and does not change. So $P_T(v) = \pi_k(v)$, which passes. Every other voxel of $T$ owns in $T$ a subset of what it owns in $\bar S$, so it passes by Lemma 2 and monotonicity. Every pixel with $I(p) \ne \bot$ still has an owner. So $T$ is consistent, and a pixel $p \in \pi_k(v)$ has its owner in $T$ at layer $k$. Then $\ell(p) \le k$, which is a contradiction.

Line L6 marks the pixels of $\pi_k(v)$ for the colored voxels $v$ of layer $k$, which are the voxels of $\bar S$ in layer $k$. A pixel $p \in U_k$ with $\ell(p) = k$ has $r_k(p) = V_p \in \bar S$, so it is marked. A pixel $p \in U_k$ with $\ell(p) > k$ has $r_k(p) \notin \bar S$ by Lemma 1, so it stays unmarked. Thus $U_{k+1} = \{p : \ell(p) \ge k + 1\}$. $\square$

**Theorem.** If a consistent scene exists, VOXEL-COLOR returns $\bar S$, it is consistent, and the flag of line L7 is true. Each colored voxel gets the mean of the values of the pixels it owns in $\bar S$. If the flag is false, no consistent scene exists.

*Proof.* By Lemma 3 the colored voxels of all layers form $\bar S$, which is consistent by Lemma 2. The pixels that a colored voxel $v$ of layer $k$ owns in $\bar S$ are those with $V_p = v$, which is the set $\pi_k(v)$ whose mean line L5 stores. After the last layer, $U_L = \{p : \ell(p) = \infty\}$, and these pixels have $I(p) = \bot$ by Lemma 2, so the flag is true. The last claim is the contrapositive. $\blacksquare$

**Remarks.**

- The scene $\bar S$ is one of possibly many consistent scenes. It is the nearest one at every pixel: in any consistent scene $S$, the owner of $p$ is at a layer at least $\ell(p)$, the layer of its owner in $\bar S$.
- The only facts used about the order of the voxels are that each ray meets each layer at most once and visits the layers in increasing order. This is what the ordinal visibility constraint of Seitz and Dyer provides when no scene point lies inside the convex hull of the camera centers.
- The proof needs the monotone test. Seitz and Dyer use the standard deviation of the colors, or a chi-square form of it, which is not monotone, so for their test the result is a heuristic, not this theorem.

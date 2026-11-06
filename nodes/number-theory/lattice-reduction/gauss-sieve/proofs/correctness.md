---
title: The Gauss sieve terminates, keeps a pairwise reduced list of at most kissing-number size, and returns a nonzero lattice vector no longer than any vector it processed
proves: [correctness, termination]
status: full
---

**Setting.** The input is $n \ge 1$ linearly independent rows $b_1, \ldots, b_n \in \mathbb{Q}^m$ of the lattice $L = L(B)$, a collision limit $c \ge 1$ and a sample budget $M \ge 0$. The algorithm keeps a list $\mathcal L$ and a stack $S$ of vectors, a collision counter $K$ and a sample counter. Line numbers refer to the pseudocode on the page. All arithmetic is exact. Two vectors $u, w$ are **Gauss-reduced** with respect to each other when

$$2 \, |\langle u, w \rangle| \le \min(\|u\|^2, \|w\|^2).$$

The result proved here is about what the algorithm guarantees. That the output is a shortest vector is not proved; for the Gauss sieve this is a heuristic, supported by experiments, and it is not claimed below.

**Lemma 1 (one reduction step).** Let $w \ne 0$ and $t = \langle v, w \rangle / \|w\|^2$ with $|t| > 1/2$, and let $q$ be the nearest integer to $t$. Then $\|v - q w\|^2 < \|v\|^2$, and $v - q w \in L$ when $v, w \in L$.

*Proof.* $\|v - q w\|^2 - \|v\|^2 = \|w\|^2 \, q (q - 2t)$. If $t > 1/2$ then $q \ge 1$ and $t \ge q - 1/2 \ge q/2$, with equality in both only for $q = 1$, $t = 1/2$, which is excluded; so $q - 2t < 0$ and the product is negative. The case $t < -1/2$ is symmetric. Integer combinations of lattice vectors are lattice vectors. $\square$

The condition $2 |\langle v, w \rangle| > \|w\|^2$ used on lines L4 and L6 is $|t| > 1/2$.

**Lemma 2 (discreteness).** Let $s$ be a common denominator of the entries of $B$. Every vector the algorithm handles is in $L$, so its entries are in $\frac1s \mathbb{Z}$ and its squared length is in $\frac{1}{s^2} \mathbb{Z}_{\ge 0}$.

*Proof.* Basis rows and samples $\sum x_i b_i$ are in $L$; reductions keep $L$ by Lemma 1. $\square$

**Lemma 3 (line L4 terminates).** The reduction loop of line L4 stops, and when it stops either $v = 0$ or $2 |\langle v, w \rangle| \le \|w\|^2$ for every $w \in \mathcal L$ with $\|w\| \le \|v\|$.

*Proof.* Each reduction makes $\|v\|^2$ strictly smaller (Lemma 1), and by Lemma 2 these values lie in the discrete set $\frac{1}{s^2} \mathbb{Z}_{\ge 0}$, so there are finitely many reductions. The loop stops either at $v = 0$ or after a full pass over $\mathcal L$ without a reduction, which is the stated condition. $\square$

**Lemma 4 (the list invariant).** At every test of line L2, every vector of $\mathcal L$ is a nonzero vector of $L$, and every two vectors at different positions of $\mathcal L$ are Gauss-reduced.

*Proof.* Initially $\mathcal L$ is empty. The list changes only on lines L7 and L8, after line L4 has produced a nonzero $v$. Pairs of vectors that stay in the list are unchanged. For the new vector $v$ and a vector $w$ that stays: if $\|w\| \le \|v\|$, Lemma 3 gives $2 |\langle v, w \rangle| \le \|w\|^2 = \min$; if $\|w\| > \|v\|$, then $w$ stays only when $2 |\langle v, w \rangle| \le \|v\|^2 = \min$. $\square$

**Lemma 5 (size of the list).** At every moment $|\mathcal L| \le \tau_n$, the kissing number in dimension $n$, the largest number of points on the unit sphere of $\mathbb{R}^n$ with pairwise angles at least $60°$.

*Proof.* The vectors of $\mathcal L$ lie in $\operatorname{span}(L)$, a space of dimension $n$. For two of them at different positions, Lemma 4 gives

$$\frac{|\langle u, w \rangle|}{\|u\| \|w\|} \le \frac{\min(\|u\|^2, \|w\|^2)}{2 \|u\| \|w\|} \le \frac12,$$

so the angle between $u$ and $w$ is between $60°$ and $120°$. In particular no two of them are equal or opposite, so the unit vectors $u / \|u\|$ are $|\mathcal L|$ distinct points on the unit sphere with pairwise angles at least $60°$. $\square$

**Lemma 6 (the shortest list vector only improves).** Let $\ell$ be the smallest squared length in $\mathcal L$ (with $\ell = \infty$ while $\mathcal L$ is empty). Then $\ell$ never increases, and after a nonzero vector $u$ is taken on line L3, $\ell \le \|u\|^2$ from then on.

*Proof.* Line L7 removes a vector $w$ only when the vector $v$ added on line L8 has $\|v\| < \|w\|$, so the minimum does not go up. Line L4 does not change $\mathcal L$. Now take $u \ne 0$ on line L3. If line L4 makes no reduction, $u$ itself is added on line L8. Otherwise its first reduction uses some $w \in \mathcal L$ with $\|w\| \le \|u\|$, so already $\ell \le \|u\|^2$. Since $\ell$ never increases, the bound holds from then on. $\square$

**Lemma 7 (termination).** The main loop ends.

*Proof.* Each iteration either draws a sample, which happens at most $M$ times, or pops a vector from $S$. We show that only finitely many iterations of the second kind can follow each other. Let $\Phi$ be the multiset of the squared lengths of all vectors in $\mathcal L$ and in $S$, ordered by the multiset order (Dershowitz and Manna), which is well-founded because the values lie in the well-ordered set $\frac{1}{s^2} \mathbb{Z}_{\ge 0}$ (Lemma 2). Consider an iteration that pops $v$ from $S$.

- If line L4 reduces $v$ to 0, the value $\|v\|^2$ leaves $\Phi$: $\Phi$ decreases.
- Otherwise $v$ is replaced by a vector of squared length at most $\|v\|^2$ and moved to $\mathcal L$, and every vector moved from $\mathcal L$ to $S$ on line L7 is replaced by a strictly shorter one (Lemma 1). If any of these lengths strictly decreased, $\Phi$ decreases. If none did, $\Phi$ is unchanged and $|S|$ decreased by 1, since $v$ left $S$ and nothing was pushed.

So the pair $(\Phi, |S|)$ decreases in the lexicographic order at each such iteration, which is again a well-founded order. Line L4 terminates by Lemma 3, and the other lines are finite. So the loop runs for finitely many iterations. $\square$

**Theorem.** The procedure terminates. Its output $v$ is a vector of the final list, of the smallest length in it, and

1. $v$ is a nonzero vector of $L$, with $\|v\| \le \min_i \|b_i\|$ and $\|v\| \le \|u\|$ for every nonzero vector $u$ taken on line L3;
2. the final list is pairwise Gauss-reduced and has at most $\tau_n$ vectors.

*Proof.* Termination is Lemma 7. The loop stops only when $S$ is empty, so all basis rows, which start on $S$, were taken on line L3. The first of them, $b_1$, meets an empty list, so it is added and $\mathcal L$ is nonempty from then on; by Lemmas 4 and 6, the list never becomes empty again, because a vector is removed only when another is added. So the minimum on line L9 exists, $v \ne 0$ and $v \in L$ by Lemma 4, and Lemma 6 gives $\|v\|^2 = \ell \le \|u\|^2$ for every nonzero $u$ processed, in particular for every $b_i$. Part 2 is Lemmas 4 and 5. $\blacksquare$

**What is not proved.** Nothing above shows $\|v\| = \lambda_1(L)$. Micciancio and Voulgaris proved bounds of the form $2^{O(n)}$ for the related List Sieve, but not for the Gauss sieve, where the stack can make the number of iterations grow without a known bound in terms of $n$. The success of the method rests on experiments and on heuristic arguments about random samples.

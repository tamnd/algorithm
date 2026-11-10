---
title: Each NUTS iteration leaves π(q) N(p; 0, I) invariant
proves: [correctness]
status: full
---

**Setting.** As on the main page, $H(q, p) = -\log\tilde\pi(q) + |p|^2/2$, $z = (q, p) \in \mathbb{R}^{2d}$, and $\bar\pi(z) \propto e^{-H(z)}$, whose $q$-marginal is $\pi$. Let $\Psi$ be one leapfrog step of size $\varepsilon$. It is a $C^1$ bijection of $\mathbb{R}^{2d}$ with Jacobian determinant 1, and the leapfrog step of size $-\varepsilon$ is $\Psi^{-1}$ (both facts are proved on the [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/) proof page: the step with $-\varepsilon$ is $F\Psi F$, and $F\Psi F = \Psi^{-1}$). So every state the algorithm visits from $z$ is $z_i = \Psi^i(z)$ for an integer time index $i$, with $z_0 = z$.

**Step 0: the joint law of $(z, u)$.** Line L3 draws $p$ fresh, which keeps $\bar\pi$ (a Gibbs update of $p$), and then draws $u$ uniformly on $(0, e^{-H(z)}]$. If $z \sim \bar\pi$, the pair $(z, u)$ has density

$$f(z, u) = \frac{1}{c}\,[0 < u \le e^{-H(z)}], \qquad c = \int e^{-H},$$

on $\mathbb{R}^{2d} \times (0, \infty)$: it is uniform on the region under the graph of $e^{-H}$, as in [slice sampling](/slice-sampling/). It is enough to show that the output $z_{\mathrm{new}}$ of one iteration, paired with the same $u$, again has density $f$. Then $z_{\mathrm{new}} \sim \bar\pi$, and its $q$-part has law $\pi$. Here $z_{\mathrm{new}}$ means the state $(q_{\mathrm{new}}, p)$ of the path at which $q_{\mathrm{new}}$ was found; the algorithm keeps only its position.

**Step 1: what a run produces.** Fix $z$ and $u$. Lines L5 to L12, with the directions $v_0, v_1, \ldots$, produce a set $I$ of time indices that the path visits, a set $K \subseteq I$ of candidate indices, and the number $J$ of doublings. An index $i$ is a candidate when $u \le e^{-H(z_i)}$ and the half added at the doubling that created $i$ has $s' = 1$; the start, index 0, is a candidate because $u \le e^{-H(z)}$. Since $s' = 0$ ends the run, every non-candidate half is the last one. The run is a deterministic function of the sequence $(z_i)$, of $u$ and of the directions. Write $P_{z, u}(I, K)$ for the probability, over the directions, that the run from $(z, u)$ produces $(I, K)$, and $S_m(\kappa; I, K)$ for the probability that the choice rule of lines L9 and L23, started at index $m$, returns index $\kappa$. Then

$$E[g(z_{\mathrm{new}}, u)] = \iint f(z, u)\sum_{(I, K)}P_{z, u}(I, K)\sum_{\kappa \in K}S_0(\kappa; I, K)\,g(\Psi^\kappa(z), u)\,dz\,du.$$

**Step 2: the path is a dyadic block, and the run is the same from every candidate.** After $k$ doublings the path has $2^k$ consecutive indices, because each doubling adds as many states as the path has. Let $a = \min I$ and call $i - a$ the position of index $i$. By induction on $k$, after $k$ completed doublings the path is the block of positions $[b2^k, (b + 1)2^k)$ that contains the position of 0: the next doubling adds the neighbouring block of the same size on the side $v_k$, and the union is again an aligned block of size $2^{k+1}$. So the run is a walk up a complete binary tree over positions, from the leaf of the start to the root, and $v_k = +1$ exactly when bit $k$ of the start's position is 0.

Now take a candidate $m \in K$ and start the algorithm at $z' = \Psi^m(z)$, with the same $u$. Its states are $z'_i = z_{m+i}$. Choose the directions given by the bits of the position of $m$; any other choice adds a block outside $I$ at some doubling and so cannot produce $(I - m, K - m)$. With these directions, the run from $z'$ climbs the same binary tree from the leaf of $m$. The checks that a run makes are of three kinds, and each depends only on the states, not on where the run started:

- the slice test $u \le e^{-H(z_i)}$ and the divergence test of each state (line L17);
- the U-turn test of each block that BUILD-TREE completes inside a new half (line L24);
- the U-turn test of the whole path after each doubling (line L11).

Every block of the tree below the root is either a block on the path from the leaf of $m$ to the root, which the run from $z'$ tests at line L11, or a block inside a sibling half, which it tests at line L24. The same holds for the run from $z$. So the two runs test the same blocks, except that the root is tested only by the final line L11, which is the same in both. Since $m$ is a candidate, every block that contains $m$ and lies inside the last half, or inside an earlier half, passed all its tests in the run from $z$ (otherwise its states would have been excluded or the run would have stopped earlier). The blocks that contain $0$ passed theirs too. Hence the run from $z'$ makes no early stop, reaches the same last doubling, adds the same last half (or the same part of it, if the last half stopped inside at the same block), and stops for the same reason, or at depth $D$ for both. It produces $I - m$, $K - m$ and $J$ doublings, with the same probability $2^{-J}$:

$$P_{\Psi^m(z), u}(I - m, K - m) = P_{z, u}(I, K) \qquad \text{for every } m \in K.$$

**Step 3: the choice rule keeps the uniform law on $K$.** We show that $\sum_{m \in K}S_m(\kappa; I, K) = 1$ for every $\kappa \in K$, which says that if the start is uniform on $K$, so is the output. First, inside BUILD-TREE, $q'$ is uniform on the candidates of the subtree: this is true for one leaf, and if $q'$ is uniform on the $n'$ candidates of the first half and $q''$ on the $n''$ of the second, line L23 makes $q'$ uniform on all $n' + n''$. Next, by induction over the blocks $B$ of the tree, let $S^B_m$ be the law of the choice made by the run from $m \in K \cap B$ after it completes $B$. We show that the uniform law on $K \cap B$ is invariant: $\sum_{m \in K \cap B}S^B_m(\kappa) = 1$ for $\kappa \in K \cap B$. For a leaf this is clear. Let $B$ have halves $B_1$ and $B_2$, with $a_1 = |K \cap B_1|$ and $a_2 = |K \cap B_2|$. A run from $m \in B_1$ completes $B_1$, so it has $n = a_1$, and then adds $B_2$ as a new half with $n' = a_2$ candidates. It keeps its choice with probability $1 - \min(1, a_2/a_1)$ and otherwise takes a uniform candidate of $B_2$. Symmetrically for $m \in B_2$. For $\kappa \in K \cap B_1$, using the induction hypothesis on $B_1$,

$$\sum_{m \in K \cap B}S^B_m(\kappa) = \Big(1 - \min\big(1, \tfrac{a_2}{a_1}\big)\Big)\cdot 1 + a_2\min\big(1, \tfrac{a_1}{a_2}\big)\frac{1}{a_1} = 1 - \min\big(1, \tfrac{a_2}{a_1}\big) + \min\big(\tfrac{a_2}{a_1}, 1\big) = 1,$$

and the same holds for $\kappa \in K \cap B_2$. When $a_2 = 0$, the second term is absent and the first factor is 1. Apply this to the root, the block $I$. (The naive rule, uniform on $K$, satisfies the same identity trivially.)

**Step 4: change of variables.** In the formula of Step 1, fix $\kappa$ and substitute $w = \Psi^\kappa(z)$, which has Jacobian 1. Put $I' = I - \kappa$, $K' = K - \kappa$ and $m = -\kappa$, so that $z = \Psi^m(w)$, $0 \in K'$ and $m \in K'$. By Step 2, applied to the run from $z$ and its candidate $\kappa$, $P_{z, u}(I, K) = P_{w, u}(I', K')$. The choice rule depends only on the tree and the start, so $S_0(\kappa; I, K) = S_m(0; I', K')$. Both $z$ and $w$ are in the slice, so $f(z, u) = f(w, u) = 1/c$ on the event considered. Summing over all $\kappa$ is the same as summing over all $m \in K'$, so

$$E[g(z_{\mathrm{new}}, u)] = \iint f(w, u)\,g(w, u)\sum_{(I', K') \ni 0}P_{w, u}(I', K')\sum_{m \in K'}S_m(0; I', K')\,dw\,du.$$

By Step 3 the inner sum is 1, and the probabilities $P_{w, u}(I', K')$ over all outcomes of the run from $w$ add up to 1. So $E[g(z_{\mathrm{new}}, u)] = \iint f(w, u)g(w, u)\,dw\,du = E[g(z, u)]$ for every bounded measurable $g$. Thus $(z_{\mathrm{new}}, u)$ has density $f$, and by Step 0 each iteration keeps $\bar\pi$, and $X_t \sim \pi$ whenever $X_{t-1} \sim \pi$. $\blacksquare$

**Remarks.** The four facts used are the conditions of Hoffman and Gelman: volume preservation of the steps (C.1), the start is a candidate (C.2), every candidate is in the slice (C.3), and the run builds the same path and candidate set from every candidate with the same probability (C.4); plus a choice rule that keeps the uniform law on the candidates. The proof does not use that the U-turn test is a good stopping rule. Any test that depends only on the states of a block would do. It only affects efficiency.

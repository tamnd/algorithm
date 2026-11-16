---
title: JCBB returns the best hypothesis of its search space
proves: [correctness]
status: full
---

**Setting.** There are $m$ readings $z_0, \dots, z_{m-1}$ and $n$ features with predicted readings $h_0, \dots, h_{n-1}$, each in $\mathbb{R}^d$. The prediction $h_j$ has the Jacobian $H_j$ with respect to the state, whose estimate has the covariance $P$. Each reading has the noise covariance $R$, which is positive definite. A *pairing* is a pair $(i, j)$. For a list of pairings $E = ((i_1, j_1), \dots, (i_k, j_k))$ with distinct readings, the stacked innovation is $\nu_E = (z_{i_1} - h_{j_1}, \dots, z_{i_k} - h_{j_k})$, and its covariance $C_E$ has the blocks $H_{j_a} P H_{j_b}^\top + [i_a = i_b] R$. The joint distance is $D^2(E) = \nu_E^\top C_E^{-1} \nu_E$, with $D^2(\emptyset) = 0$. $E$ is *jointly compatible* if $D^2(E) \le \chi^2_{dk, \alpha}$, the $\alpha$ quantile of the chi-square distribution with $dk$ degrees of freedom. A pairing is *individually compatible* if the list that holds only this pairing is jointly compatible.

A hypothesis $\mathcal{H}$ gives each reading $i$ a feature or $*$ (none). Its pairings $E(\mathcal{H})$ are listed in the order of the readings. $\mathcal{H}$ is *reachable* if every pairing of it is individually compatible, every prefix of $E(\mathcal{H})$ is jointly compatible, and, if pairings must be unique, no feature appears twice. Order the hypotheses by the key $(|E|, -D^2(E))$: more pairings is better, and among equal numbers a smaller $D^2$ is better.

**Claim.** `jcbb` with `tie_break=True` returns a reachable hypothesis with the largest key, and its $D^2$. With `tie_break=False` it returns a reachable hypothesis with the largest number of pairings.

The claim is about the search space of reachable hypotheses. It does not say that the result has the largest jointly compatible set of all hypotheses: see the remark at the end.

## Lemma 1: $C_E$ is positive definite

$C_E = S P S^\top + D_R$, where $S$ stacks the $H_{j_a}$ and $D_R$ is block diagonal with $R$ on the diagonal, since the readings in $E$ are distinct. The first term is positive semidefinite and the second is positive definite. So $C_E$ is positive definite, and $D^2(E)$ is well defined and nonnegative.

## Lemma 2: the joint distance never decreases when a pairing is added

Let $E' = E + ((i, j))$ with $i$ not in $E$. Split $\nu_{E'} = (a, b)$ and $C_{E'} = \begin{pmatrix} A & B \\ B^\top & D \end{pmatrix}$, with $a = \nu_E$ and $A = C_E$. By Lemma 1, $A$ and the Schur complement $T = D - B^\top A^{-1} B$ are positive definite, and block elimination gives

$$D^2(E') = a^\top A^{-1} a + (b - B^\top A^{-1} a)^\top T^{-1} (b - B^\top A^{-1} a) \ge a^\top A^{-1} a = D^2(E).$$

By induction, $D^2$ of a list is at least $D^2$ of each of its prefixes.

## Lemma 3: the tree without the bound enumerates the reachable hypotheses

Consider the recursion without the test of line L10, so that line L11 always runs. A node is a pair (partial hypothesis for the readings $0, \dots, i-1$, $i$). From a node, line L8 extends by $(i, j)$ exactly when the pairing is individually compatible (line L6), the feature is free if pairings must be unique (line L6), and the extended list of pairings is jointly compatible (line L7). Line L11 extends by $*$, which adds no pairing. By induction on $i$, the nodes at depth $i$ are exactly the partial hypotheses for the readings $0, \dots, i-1$ whose pairings are individually compatible, whose prefixes are all jointly compatible, and which respect uniqueness. At depth $m$ these are the reachable hypotheses, each once, since two children of a node differ at reading $i$.

## Lemma 4: the bound removes no strict improvement

Let the current best have the key $(k^*, -D^{2*})$ when line L10 runs at a node with pairings $E$ and next reading $i$. Every leaf below the $*$ child leaves reading $i$ unpaired and adds at most one pairing for each of the readings $i + 1, \dots, m - 1$. So its number of pairings is at most $k_{\max} = |E| + m - i - 1$, which line L9 computes.

- If $k_{\max} < k^*$, no leaf below has as many pairings as the best.
- If $k_{\max} = k^*$, a leaf below with $k^*$ pairings has a list of pairings that starts with $E$, so by Lemma 2 its $D^2$ is at least $D^2(E)$. If $D^2(E) \ge D^{2*}$, no such leaf has a smaller $D^2$ than the best. With `tie_break=False` a leaf with an equal number of pairings is never accepted, so the case is the same as the first.

So when line L10 skips the $*$ child, no leaf below it would pass the test of line L3. The best key only grows during the search, so the same holds at every later time.

## Proof of the claim

Line L3 accepts a leaf only if its key is larger than the current best key (with `tie_break=False`, only if it has more pairings). So the returned hypothesis is the leaf with the largest key among the leaves that the search reaches, or the empty hypothesis with key $(0, 0)$, which is reachable. By Lemma 3, the leaves of the unpruned tree are exactly the reachable hypotheses. By Lemma 4, every leaf that the bound removes would not have changed the best. So the search returns a reachable hypothesis with the largest key. The value of $D^2$ that it returns is the one computed at line L7 for the last pairing of that hypothesis, which is $D^2$ of its whole list of pairings. $\square$

## Remark: the joint test is not monotone

Lemma 2 says that $D^2$ never decreases, but the threshold $\chi^2_{dk, \alpha}$ also grows with $k$. So a list can be jointly compatible while one of its prefixes is not. JCBB prunes at the first prefix that fails, as in the paper of Neira and Tardos, so such a list is outside its search space. The claim above, and the test against brute force, are therefore about reachable hypotheses only.

## Tests

`test_joint_compatibility_branch_and_bound.py` checks the claim on 24 random scenes with 3 to 5 readings, 2 to 4 features and about 20 percent clutter. It compares `jcbb` with a brute force search over all $(n + 1)^m$ hypotheses that keeps the reachable ones, for both values of `unique`, and checks equal hypotheses and equal $D^2$ within $10^{-9}$. It also checks that `tie_break=False` finds the same number of pairings. Other tests check Lemma 2 on random lists, that every prefix of the result is jointly compatible, the chi-square quantiles against tables, the example of the page, and that a clutter reading stays unpaired.

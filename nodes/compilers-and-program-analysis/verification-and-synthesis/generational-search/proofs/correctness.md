---
title: Generational search finds every feasible path once under an exact solver
proves: [correctness]
status: full
---

**Setting.** $P$ is a program of the toy IR with $k$ integer parameters and only constants, copies and binary operations. $D \subseteq \mathbb{Z}^k$ is a set of inputs that contains the seed. SOLVE is *exact over $D$*: for a list of conditions it returns an input of $D$ that satisfies all of them if one exists, and reports that there is none otherwise. (A decision procedure for the theory of the conditions is exact over $D = \mathbb{Z}^k$; the brute-force solver of the page is exact over the box.) RUN tracks every operation symbolically and records no condition with a constant expression. We assume one of two cases:

- (A) $P$ is loop-free, and $D$ is any set, for example $\mathbb{Z}^k$; or
- (B) $D$ is finite and every run of $P$ on an input of $D$ ends.

A condition is a pair $(e, s)$; an input $u$ satisfies it when "$e(u) \ne 0$" has the truth value $s$ and $e(u)$ does not trap. For an input $u$, $\mathrm{dec}(u) = (c_0, \dots, c_{m-1})$ is the list of conditions that RUN records, its *decision sequence*.

## Lemma 1: the record is a function of the decisions

**Claim.** If $u'$ satisfies the first $i$ conditions $c_0, \dots, c_{i-1}$ of $\mathrm{dec}(u)$, then $\mathrm{dec}(u')$ starts with the same $i$ conditions, and after them both runs reach the same point with the same symbolic store.

**Proof.** Induction over the steps of the run of $u$. Both runs start at the entry with the store $x_j \mapsto \alpha_j$, and each constant, copy and operation changes the store in a way that does not depend on the input. A branch or check on a constant expression goes the same way in both runs. A branch or check on a symbolic expression $e$ records a condition with the same $e$ in both runs; if it is $c_t$ with $t < i$, then $u'$ satisfies it, so $e(u)$ and $e(u')$ are both zero or both nonzero, and both runs take the same side. The symbolic store gives the true value of each name as a function of the input, by the same induction. $\square$

**Consequences.** Let $T_D$ be the set of the decision sequences of the inputs of $D$ and their prefixes.

- (a) After a prefix, the expression of the next condition, or the end of the run, is fixed. So $T_D$ is a binary tree, and no decision sequence is a proper prefix of another: the decision sequences are the leaves of $T_D$.
- (b) An input satisfies the conditions of a node $q$ if and only if its decision sequence lies below $q$.
- (c) Different leaves correspond to different paths, and the same leaf to the same path: two leaves first differ at $(e, s)$ against $(e, \neg s)$, which at a branch sends the runs to different blocks (a branch with equal targets records nothing) and at a check makes one run trap and the other go on.
- (d) $T_D$ has finitely many leaves. In case (B) there are at most $|D|$. In case (A) a run of a loop-free program with $n$ blocks visits at most $n$ blocks, each block records at most a fixed number of conditions, so every leaf has length at most some $L$, and a binary tree of depth $L$ has at most $2^L$ leaves.

## Lemma 2: a child follows its query

**Claim.** Let $r$ have the decision sequence $(c_0, \dots, c_{m-1})$, and let $r'$ be the child made at position $j$ on line L9. Then $\mathrm{dec}(r')$ starts with $c_0, \dots, c_{j-1}, \neg c_j$.

**Proof.** The input of $r'$ satisfies $c_0, \dots, c_{j-1}$, so by Lemma 1 its run records these conditions and then reaches the point of $c_j$ with the same store, where it records a condition with the expression of $c_j$. The input satisfies $\neg c_j$, so the recorded sense is that of $\neg c_j$. $\square$

## Lemma 3: descendants keep the prefix

Call the runs made by the search *nodes*, and the relation "made on line L9 while expanding" the *parent* relation; the seed is the root.

**Claim.** If $r'$ was made at position $j$, then every descendant of $r'$ (including $r'$) has a decision sequence that agrees with $\mathrm{dec}(r')$ at the positions $0, \dots, j$.

**Proof.** Induction on the distance from $r'$. For $r'$ it is trivial. A child of a descendant $s$ is made at a position $j' \ge b(s)$. Every descendant $s$ of $r'$ other than $r'$ was itself made at a position at least $b$ of its parent, and bounds only grow along a chain: $b(s) = j_s + 1$ where $j_s \ge b(\mathrm{parent}(s))$. So $j' \ge b(s) \ge b(r') = j + 1$. By Lemma 2, the child agrees with $s$ at the positions below $j'$, which include $0, \dots, j$, and $s$ agrees with $r'$ there by induction. $\square$

## Theorem

**Claim.** In case (A) or (B), the search stops; the paths of the runs it outputs are pairwise different; and they are exactly the paths of the inputs of $D$. Exactly $R - 1$ solver calls succeed, where $R$ is the number of runs, and the number of calls is $\sum_r (m(r) - b(r))$.

**Proof.** *No path twice.* Let $x \ne y$ be two nodes and $z$ their lowest common ancestor.

- If $z = x$, let $x'$ be the child of $x$ on the chain to $y$, made at position $j$. By Lemma 2, $\mathrm{dec}(x')$ has $\neg c_j$ at position $j$, where $\mathrm{dec}(x)$ has $c_j$, and by Lemma 3, $y$ agrees with $x'$ at position $j$. So $\mathrm{dec}(y) \ne \mathrm{dec}(x)$.
- Otherwise let $x'$ and $y'$ be the children of $z$ on the two chains, made at positions $j_x$ and $j_y$. Line L6 makes at most one child per position, so $j_x \ne j_y$; say $j_x < j_y$. By Lemma 2, $x'$ has $\neg c_{j_x}$ at position $j_x$, and $y'$ agrees with $z$ at every position below $j_y$, so it has $c_{j_x}$ there. By Lemma 3, $x$ and $y$ agree with $x'$ and $y'$ at position $j_x$. So $\mathrm{dec}(x) \ne \mathrm{dec}(y)$.

By (c) the paths differ as well.

*Termination.* Each node is a leaf of $T_D$ (its input is in $D$), and different nodes are different leaves, so by (d) there are finitely many nodes. Each node enters $W$ once and is expanded once, with finitely many calls, so the loop stops.

*Every path.* Let $\ell$ be a leaf of $T_D$. We build a chain of nodes $r_0, r_1, \dots$ such that each $r_t$ agrees with $\ell$ at every position below $b(r_t)$. Take $r_0$ as the seed, with $b(r_0) = 0$. If $\mathrm{dec}(r_t) = \ell$, stop. Otherwise the two sequences are different leaves, so neither is a prefix of the other, and they first differ at some position $j$, with $j \ge b(r_t)$ by the property of $r_t$. When $r_t$ is expanded (it is, since the loop runs until $W$ is empty), line L6 reaches $j$. An input that follows $\ell$ satisfies $c_0, \dots, c_{j-1}, \neg c_j$ of $r_t$, by (b), so the exact solver returns a model and line L9 makes a child $r_{t+1}$ at position $j$. By Lemma 2, $r_{t+1}$ agrees with $\ell$ at the positions $0, \dots, j$, which are the positions below $b(r_{t+1}) = j + 1$. The first position of difference with $\ell$ grows strictly along the chain and is at most the length of $\ell$, so the chain reaches $\ell$.

*Solver calls.* The expansion of $r$ makes one call for each $j$ from $b(r)$ to $m(r) - 1$, which gives the total. Each successful call makes one run, and every run but the seed comes from one successful call. $\square$

**Remarks.** The order of line L4 is not used anywhere, so every order of the worklist gives the same set of runs. Case (A) with $D = \mathbb{Z}^k$ needs a decision procedure for the conditions; with products of inputs over unbounded integers there is none, by the negative answer to Hilbert's tenth problem, and the result then holds only relative to whatever the solver can decide. The bound $j + 1$ is used twice: in Lemma 3, to keep the prefix of descendants fixed, which gives "no path twice"; and in the chain of "every path", which shows that the bound never hides a leaf.

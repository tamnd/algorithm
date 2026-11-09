---
title: The Karp-Miller tree is finite and decides coverability and boundedness
proves: [correctness, termination]
status: full
---

**Setting.** A net has places $P = \{1, \ldots, k\}$ and transitions $T$, each with $\mathrm{pre}(t), \mathrm{post}(t) \in \mathbb{N}^P$. We write $\Delta(t) = \mathrm{post}(t) - \mathrm{pre}(t) \in \mathbb{Z}^P$, and $\Delta(\rho)$ for the sum over a sequence $\rho$ of transitions. For an $\omega$-marking $L$, $\Omega(L) = \{p : L(p) = \omega\}$. For a node $x$ we write $\ell(x)$ for its label. When node $z$ is created from $x$ by $t$ at line L6, $N_z = \ell(x) - \mathrm{pre}(t) + \mathrm{post}(t)$ is the value before acceleration. Let $c$ be the largest entry of all vectors $\mathrm{pre}(t)$.

**Fact 1.** If $y$ is an ancestor of $x$, then $\Omega(\ell(y)) \subseteq \Omega(\ell(x))$, and for every place $p \notin \Omega(\ell(x))$, $\ell(x)(p) = \ell(y)(p) + \Delta(\rho)(p)$, where $\rho$ is the sequence of edge labels on the path from $y$ to $x$. Also, $\rho$ is fireable from $\ell(y)$ in the $\omega$ arithmetic.

*Proof.* Along one edge, $\omega - a + b = \omega$, and line L8 only adds $\omega$ entries, so the $\omega$-set only grows. A place $p$ that is finite at $x$ is finite at every node above $x$ on the path, so no step on the path set it to $\omega$, and each step changed it by exactly $\Delta(t)(p)$. Each edge exists because line L5 found its transition enabled. $\square$

**Lemma 1 (Dickson).** Each infinite sequence $v_1, v_2, \ldots$ in $(\mathbb{N} \cup \{\omega\})^m$ has indices $i < j$ with $v_i \le v_j$.

*Proof.* We show the stronger claim that it has an infinite subsequence that is non-decreasing in every coordinate, by induction on $m$. For $m = 0$ there is nothing to show. A sequence $a_1, a_2, \ldots$ in the well-ordered set $\mathbb{N} \cup \{\omega\}$ has an infinite non-decreasing subsequence: let $i_1$ be an index where the least value of the whole sequence is taken, and $i_{s+1} > i_s$ an index where the least value of the tail after $i_s$ is taken. Each tail is a subset of the previous one, so its least value is at least the previous least value. For $m \ge 1$, first take a subsequence that is non-decreasing in coordinate $m$, then apply the induction hypothesis to the first $m - 1$ coordinates of that subsequence. $\square$

**Theorem 1 (termination).** KARP-MILLER stops and returns a finite tree.

*Proof.* Each node has at most $|T|$ children, and each node enters $W$ once and is processed once. Suppose the tree is infinite. By König's lemma it has an infinite path $x_0 = r, x_1, x_2, \ldots$. Each $x_s$ has a child, so line L4 did not stop it, and its label differs from the labels of all its proper ancestors. So the labels on the path are pairwise distinct. By Fact 1, the sets $\Omega(\ell(x_s))$ grow along the path, and they are subsets of $P$, so there is $s_0$ such that $\Omega(\ell(x_s)) = \Omega_*$ for all $s \ge s_0$.

By Lemma 1, there are $s_0 \le i < j$ with $\ell(x_i) \le \ell(x_j)$. Since the labels are distinct, there is a place $p$ with $\ell(x_i)(p) < \ell(x_j)(p)$, so $\ell(x_i)(p) < \omega$ and $p \notin \Omega_*$, and therefore $\ell(x_j)(p) < \omega$ too. Consider the creation of $x_j$ from its parent $x_{j-1}$, with $j - 1 \ge s_0$. The value $N = N_{x_j}$ has $\Omega(N) = \Omega(\ell(x_{j-1})) = \Omega_*$, and line L8 added no $\omega$, because $\Omega(\ell(x_j)) = \Omega_*$ too. So $\ell(x_j) = N$. But $x_i$ lies on the path from $r$ to $x_{j-1}$, with $\ell(x_i) \le N$ and $\ell(x_i) \ne N$, so line L8 sets $\ell(x_j)(p) = \omega$. This contradicts $\ell(x_j)(p) < \omega$. $\square$

**Theorem 2 (cover).** For each marking $M$ reachable from $M_0$ there is a node $x$ that is expanded (line L4 did not stop it) with $\ell(x) \ge M$.

*Proof.* By induction on the length of a firing sequence from $M_0$ to $M$. For length 0, the root has no proper ancestor, so it is expanded, and $\ell(r) = M_0$. For the step, let $M \xrightarrow{t} M'$, and let $x$ be expanded with $\ell(x) \ge M$. Then $\mathrm{pre}(t) \le M \le \ell(x)$, so line L5 creates a child $z$ for $t$, and $\ell(z) \ge N_z = \ell(x) - \mathrm{pre}(t) + \mathrm{post}(t) \ge M - \mathrm{pre}(t) + \mathrm{post}(t) = M'$, since line L8 only raises entries. If $z$ is expanded, we are done. Else a proper ancestor $y$ of $z$ has $\ell(y) = \ell(z)$. The node $y$ has a descendant, so it was expanded, and $\ell(y) \ge M'$. $\square$

**Theorem 3 (approach).** For each node $x$ and each $K \in \mathbb{N}$ there is a reachable marking $M$ with $M(p) = \ell(x)(p)$ for $p \notin \Omega(\ell(x))$ and $M(p) \ge K$ for $p \in \Omega(\ell(x))$.

*Proof.* By induction on the depth of $x$. For the root, take $M = M_0$. Let $z$ be a child of $x$ by $t$, let $N = N_z$, and let $Y$ be the set of nodes $y$ on the path from $r$ to $x$ with $\ell(y) \le N$ and $\ell(y) \ne N$. Then $\Omega(\ell(z)) = \Omega(N) \cup \{p : \ell(y)(p) < N(p) \text{ for some } y \in Y\}$, and $\Omega(N) = \Omega(\ell(x))$. For $y \in Y$, let $\rho_y$ be the edge labels from $y$ to $x$, followed by $t$.

*Step 1: the effect of $\rho_y$.* Let $q \notin \Omega(\ell(x))$. By Fact 1, $N(q) = \ell(y)(q) + \Delta(\rho_y)(q)$, so $\Delta(\rho_y)(q) = N(q) - \ell(y)(q) \ge 0$. If $q \notin \Omega(\ell(z))$, then $\ell(y)(q) = N(q)$ (else line L8 would set $q$ to $\omega$), so $\Delta(\rho_y)(q) = 0$. If $q \in \Omega(\ell(z)) \setminus \Omega(\ell(x))$, then some $y \in Y$ has $\Delta(\rho_y)(q) \ge 1$.

*Step 2: pumping.* Let $L = \sum_{y \in Y} |\rho_y|$, and choose $K' = K + c (1 + K L)$. By the induction hypothesis there is a reachable $M_x$ with $M_x(q) = \ell(x)(q)$ for $q \notin \Omega(\ell(x))$ and $M_x(q) \ge K'$ for $q \in \Omega(\ell(x))$. Fire $t$, which is enabled because $\mathrm{pre}(t) \le \ell(x)$ on the finite places and $K' \ge c$ on the others. Then fire, $K$ times in turn, each sequence $\rho_y$ for $y \in Y$, in a fixed order.

We check that each firing is possible. On a place $q \notin \Omega(\ell(x))$, the marking before each $\rho_y$ is $N(q)$ plus a sum of values $\Delta(\rho_{y'})(q) \ge 0$, so it is at least $N(q) \ge \ell(y)(q)$. By Fact 1, $\rho_y$ is fireable from $\ell(y)$, and $q$ stays finite along it; a run of $\rho_y$ from a marking that is at least $\ell(y)(q)$ in $q$ keeps each intermediate value at least the one of the run from $\ell(y)$, which is nonnegative. On a place $q \in \Omega(\ell(x))$, the whole run fires at most $1 + K L$ transitions after $M_x$, and each removes at most $c$ tokens. So before each transition the value is at least $K' - c K L = K + c \ge c$, which is enough for that transition, and at the end it is at least $K' - c(1 + KL) = K$.

*Step 3: the result.* Let $M$ be the final marking. For $q \notin \Omega(\ell(z))$: $M(q) = N(q) + K \sum_y \Delta(\rho_y)(q) = N(q) = \ell(z)(q)$ by Step 1. For $q \in \Omega(\ell(z)) \setminus \Omega(\ell(x))$: $M(q) \ge N(q) + K \cdot 1 \ge K$, because all terms are nonnegative and one is at least 1. For $q \in \Omega(\ell(x))$: $M(q) \ge K$ by Step 2. So $M$ has the claimed form for $z$. $\square$

**Corollary.** (a) $M_T$ is coverable from $M_0$ if and only if some node has $\ell(x) \ge M_T$. (b) A place $p$ is bounded over the reachable markings if and only if no label has $\ell(x)(p) = \omega$.

*Proof.* (a) If $M \ge M_T$ is reachable, Theorem 2 gives $\ell(x) \ge M \ge M_T$. Conversely, if $\ell(x) \ge M_T$, Theorem 3 with $K = \max_p M_T(p)$ gives a reachable $M$ that equals $\ell(x)$ on the finite places and is at least $K$ on the others, so $M \ge M_T$. (b) If no label has $\omega$ in $p$, then by Theorem 2 each reachable $M$ has $M(p) \le \max_x \ell(x)(p)$, which is finite because the tree is finite by Theorem 1. If some label has $\omega$ in $p$, Theorem 3 gives reachable markings with arbitrarily many tokens in $p$. $\blacksquare$

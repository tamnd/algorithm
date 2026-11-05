---
title: All-Pairs reports exactly the pairs with dot product at least t
proves: [correctness]
status: full
---

Let $V = (x_1, \dots, x_n)$ be vectors in $\mathbb{R}_{\ge 0}^d$, $t > 0$, and $m[i] = \max_{z \in V} z[i]$. For a vector $y$, let $y'$ be its entries put into $y'$ at line L8 and $y'' = y - y'$ its entries put into the index. Write "$y$ before $x$" when $y$ comes earlier in the input order.

**Lemma 1.** For each $y \in V$ and $z \in V$, $z \cdot y' < t$.

*Proof.* Line L6 visits the entries of $y$ in a fixed order, and $b$ is the sum of $m[i] \, y[i]$ over the entries visited so far. All terms are nonnegative, so $b$ never decreases. So the entries with $b < t$ after line L7 come first, and they are the entries of $y'$. If $y'$ is empty, $z \cdot y' = 0 < t$. Otherwise, at its last entry, $b = \sum_{i \in y'} m[i] \, y[i] < t$. Since $0 \le z[i] \le m[i]$ and $y[i] \ge 0$, $z \cdot y' = \sum_{i \in y'} z[i] \, y[i] \le \sum_{i \in y'} m[i] \, y[i] < t$. $\square$

**Lemma 2.** When FIND-MATCHES$(x, I, t)$ runs, the lists hold exactly the pairs $(y, y[i])$ with $y$ before $x$ and $y''[i] > 0$, and after line L11, $A[y] = x \cdot y''$ for each $y$ before $x$ (with $A[y] = 0$ when $y$ is not in the map).

*Proof.* Line L8 appends $(y, y[i])$ to $I_i$ exactly for the entries of $y''$, after line L4 has run for $y$, and nothing is removed. For the second part, line L11 adds $x[i] \, y[i]$ to $A[y]$ for each $i$ with $x[i] > 0$ and $y''[i] > 0$. The sum of these terms is $\sum_i x[i] \, y''[i] = x \cdot y''$, since the other terms are 0. $\square$

**Theorem.** ALL-PAIRS$(V, t)$ reports exactly the pairs $(y, x)$ with $y$ before $x$ and $x \cdot y \ge t$, each once, with $s = x \cdot y$.

*Proof.* *Soundness.* A pair $(y, x)$ is reported in FIND-MATCHES$(x, \cdot)$ at line L12, with $y$ in the map, so $y$ is before $x$ by Lemma 2. Its score is $s = A[y] + x \cdot y' = x \cdot y'' + x \cdot y' = x \cdot y$, and it is reported only if $s \ge t$.

*Completeness.* Let $y$ be before $x$ with $x \cdot y \ge t$. By Lemma 1 with $z = x$, $x \cdot y' < t$, so $x \cdot y'' = x \cdot y - x \cdot y' > 0$. By Lemma 2, $A[y] = x \cdot y'' > 0$ after line L11 of FIND-MATCHES$(x, \cdot)$, so line L12 considers $y$, computes $s = x \cdot y \ge t$, and reports $(y, x, s)$.

*Uniqueness.* The pair $(y, x)$ can be reported only in FIND-MATCHES$(x, \cdot)$, which runs once, and line L12 considers each key $y$ of $A$ once. $\blacksquare$

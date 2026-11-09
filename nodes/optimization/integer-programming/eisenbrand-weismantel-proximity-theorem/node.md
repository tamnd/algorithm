---
tag: 4EQ19Q
kind: theorem
slug: eisenbrand-weismantel-proximity-theorem
name: Eisenbrand-Weismantel proximity theorem
aliases:
- proximity theorem for integer programming
- Steinitz proximity bound
area: optimization/integer-programming
level: research
summary: Some optimal integer solution lies within a bound of an optimal LP solution that depends only on the constraint matrix.
prereqs: [lp-relaxation, basic-feasible-solution, integer-programming-fixed-dimension]
see_also: [papadimitriou-pseudopolynomial-theorem, integrality-gap, knapsack-problem, unbounded-knapsack, lenstra-theorem, pseudo-polynomial-time]
sources:
  - paper: doi:10.1145/3340322
    title: F. Eisenbrand and R. Weismantel, Proximity results and faster algorithms for integer programming using the Steinitz lemma, ACM Transactions on Algorithms 16(1), 2020
    locator: Article 5; Theorem 7 of the arXiv version 1707.00481 (proximity), Lemmas 5 and 6 (cycles), Theorem 2 (feasibility)
  - paper: "F. Eisenbrand and R. Weismantel, Proximity results and faster algorithms for integer programming using the Steinitz lemma, Proceedings of the 29th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2018"
    locator: pp. 808 to 816
  - paper: "V. S. Grinberg and S. V. Sevast'yanov, Value of the Steinitz constant, Functional Analysis and Its Applications 14(2), 1980"
    locator: the Steinitz constant at most m for every norm on R^m (pp. 125 to 126, unsure)
  - paper: doi:10.1007/BF01582230
    title: W. Cook, A. M. H. Gerards, A. Schrijver and É. Tardos, Sensitivity theorems in integer linear programming, Mathematical Programming 34, 1986
    locator: the earlier proximity bound n times the largest subdeterminant (pp. 251 to 264, unsure)
---

## Statement

Consider the integer program in standard form with upper bounds
$$\max\{c^\top x : A x = b,\ 0 \le x \le u,\ x \in \mathbb{Z}^n\},$$
where $A \in \mathbb{Z}^{m \times n}$, $b \in \mathbb{Z}^m$, $c \in \mathbb{Z}^n$, $u \in (\mathbb{N} \cup \{\infty\})^n$, and every entry of $A$ has absolute value at most $\Delta$.

**Theorem (Eisenbrand and Weismantel, 2018).** Let $x^*$ be an optimal vertex of the [LP relaxation](/lp-relaxation/), and suppose that the integer program has an optimal solution. Then it has an optimal solution $z^*$ with
$$\|z^* - x^*\|_1 \le m (2 m \Delta + 1)^m.$$

The bound does not depend on $n$, on $b$, on $c$ or on $u$.

## In plain words

Solve the problem first without the whole-number condition. The answer is a corner of the region of fractional solutions. The theorem says that some best whole-number answer is close to this corner, where close is measured by the total change over all variables. The allowed distance depends only on the number of equations and on the size of the numbers in the equations, not on the number of variables or on the right-hand side.

The reason is a fact about sums of small vectors: they can be added in an order that never strays far from the start. If the best whole-number answer were far away, this order would revisit a point. The part between the two visits could then be removed, which would give a best answer that is closer.

## Proof

The proof uses the Steinitz lemma with the constant of Grinberg and Sevast'yanov.

**Lemma (Steinitz).** Let $\|\cdot\|$ be a norm on $\mathbb{R}^m$, and let $y_1, \dots, y_k \in \mathbb{R}^m$ with $\sum_i y_i = 0$ and $\|y_i\| \le 1$ for all $i$. Then there is an order $\pi$ of the indices such that every partial sum satisfies $\|\sum_{j=1}^{\ell} y_{\pi(j)}\| \le m$.

Call $y \in \mathbb{Z}^n$ a *cycle* of a vector $g$ if $A y = 0$, $y \ne 0$, and $|y_i| \le |g_i|$ and $y_i g_i \ge 0$ for each $i$.

**Lemma 1.** Let $x^*$ be optimal for the LP relaxation and $z^*$ optimal for the integer program. If $y$ is a cycle of $z^* - x^*$, then $z^* - y$ is a feasible integer point and $c^\top y \le 0$.

*Proof.* $A(z^* - y) = b$ and $z^* - y$ is integer. If $(z^* - x^*)_i < 0$, then $y_i \le 0$ and $0 \le z^*_i \le z^*_i - y_i \le z^*_i - (z^* - x^*)_i = x^*_i \le u_i$. If $(z^* - x^*)_i > 0$, then $y_i \ge 0$ and $u_i \ge z^*_i \ge z^*_i - y_i \ge x^*_i \ge 0$. If $(z^* - x^*)_i = 0$, then $y_i = 0$. So $z^* - y$ is feasible. For the sign of $c^\top y$: if $y_i > 0$ then $x^*_i < z^*_i \le u_i$, and if $y_i < 0$ then $x^*_i > z^*_i \ge 0$. So $x^* + \varepsilon y$ is feasible for the LP relaxation for a small $\varepsilon > 0$, and the optimality of $x^*$ gives $c^\top y \le 0$. $\square$

**Lemma 2.** If $z^*$ is an optimal integer solution with $\|z^* - x^*\|_1$ as small as possible, then $z^* - x^*$ has no cycle.

*Proof.* If $y$ were a cycle, then $z^* - y$ would be feasible with $c^\top (z^* - y) \ge c^\top z^*$ by Lemma 1, so it would be optimal. Since $y \ne 0$ has the signs of $z^* - x^*$ and $|y_i| \le |(z^* - x^*)_i|$, we get $\|z^* - y - x^*\|_1 = \|z^* - x^*\|_1 - \|y\|_1 < \|z^* - x^*\|_1$, a contradiction. $\square$

**Proof of the theorem.** Let $z^*$ be as in Lemma 2. Round $x^*$ toward $z^*$: let $r_i = \lceil x^*_i \rceil$ if $z^*_i > x^*_i$ and $r_i = \lfloor x^*_i \rfloor$ otherwise, and let $f = x^* - r$. Then $z^* - r$ is an integer vector with the same signs as $z^* - x^*$ and $|(z^* - r)_i| \le |(z^* - x^*)_i|$. Also $|f_i| < 1$, and $f_i \ne 0$ only where $x^*_i \notin \mathbb{Z}$. Since $x^*$ is a vertex, at most $m$ of its entries lie strictly between their bounds, so $f$ has at most $m$ nonzero entries.

Build a list of vectors in $\mathbb{Z}^m$. For each $i$, put $|(z^* - r)_i|$ copies of $\operatorname{sign}((z^* - r)_i) \, a_i$ in the list, where $a_i$ is column $i$ of $A$. Call these $v_1, \dots, v_t$, with $t = \|z^* - r\|_1$. Their sum is $A(z^* - r) = b - A r = A f$. The vector $-A f = -A(x^* - r)$ is an integer vector, and $\|A f\|_\infty \le m \Delta$, since $f$ has at most $m$ nonzero entries of absolute value less than 1. So $-A f = w_1 + \dots + w_m$ for integer vectors $w_j$ with $\|w_j\|_\infty \le \Delta$. The list
$$v_1, \dots, v_t, w_1, \dots, w_m$$
has sum $0$, and each vector has $\|\cdot\|_\infty \le \Delta$. By the Steinitz lemma applied to the vectors divided by $\Delta$, there is an order $q_1, \dots, q_{t+m}$ of the list in which every partial sum $p_\ell = q_1 + \dots + q_\ell$ satisfies $\|p_\ell\|_\infty \le m\Delta$. The partial sums are integer vectors, so each lies in a set of $(2m\Delta + 1)^m$ points.

Suppose that $m + 1$ indices $\ell_1 < \dots < \ell_{m+1}$ have $p_{\ell_1} = \dots = p_{\ell_{m+1}}$. They cut the cyclic sequence $q_1, \dots, q_{t+m}$ into $m + 1$ nonempty pieces: the $m$ blocks $q_{\ell_j + 1}, \dots, q_{\ell_{j+1}}$ and the block made of $q_1, \dots, q_{\ell_1}$ and $q_{\ell_{m+1} + 1}, \dots, q_{t+m}$. Each piece sums to $0$, because the total sum is $0$. There are only $m$ vectors $w_j$, so some piece contains only vectors $v_i$. Let $y_i$ be the signed number of copies of $a_i$ in this piece. Then $A y = 0$, $y \ne 0$, and $y$ has the signs of $z^* - r$ and $|y_i| \le |(z^* - r)_i| \le |(z^* - x^*)_i|$. So $y$ is a cycle of $z^* - x^*$, which contradicts Lemma 2.

Hence each point is a partial sum for at most $m$ indices, and $t + m \le m (2 m \Delta + 1)^m$. Finally $\|z^* - x^*\|_1 \le \|z^* - r\|_1 + \|f\|_1 \le t + m \le m(2m\Delta + 1)^m$. $\blacksquare$

## Consequences

- **Integrality gap.** $c^\top x^* - c^\top z^* \le \|c\|_\infty \, m (2m\Delta + 1)^m$, a bound on the absolute [integrality gap](/integrality-gap/) that does not depend on $n$.
- **Faster algorithms with upper bounds.** Fixing $x$ near $x^*$ leaves an integer program whose right-hand side is small. Eisenbrand and Weismantel solve it by dynamic programming in time $n \cdot O(m)^{(m+1)^2} \cdot O(\Delta)^{m(m+1)} \cdot \log^2(m\Delta)$.
- **Knapsack.** For $m = 1$ the method gives $O(n \Delta^2)$ for the [unbounded knapsack](/unbounded-knapsack/) problem and $O(n^2 \Delta^2)$ for the bounded one, where $\Delta$ bounds the item weights.
- **Without upper bounds.** The same Steinitz argument, applied to a solution of $Ax = b$ itself, gives an algorithm with time $(m\Delta)^{O(m)} \|b\|_\infty^2$, which improves the algorithm of [Papadimitriou](/papadimitriou-pseudopolynomial-theorem/).

## Tightness

For $m = 1$ the bound is $2\Delta + 1$, and it is tight up to a constant. Take $\Delta \ge 2$ and
$$\max\{-x_1 - x_2 : (\Delta - 1) x_1 + \Delta x_2 = (\Delta - 1)^2,\ x \ge 0,\ x \in \mathbb{Z}^2\}.$$
The LP optimum is the vertex $x^* = (0, (\Delta - 1)^2/\Delta)$, since $x_2$ covers more of the right-hand side per unit of cost. An integer solution needs $\Delta x_2 \equiv 0 \pmod{\Delta - 1}$, so $x_2$ is a multiple of $\Delta - 1$, and $x_2 = \Delta - 1$ is too large. So the only integer solution is $z^* = (\Delta - 1, 0)$, and $\|z^* - x^*\|_1 = 2\Delta - 3 + 1/\Delta$.

The constant $m$ of the Steinitz lemma enters the bound directly. Eisenbrand and Weismantel note that a better Steinitz constant for the maximum norm, which is conjectured to be of order $\sqrt{m}$, would improve their bounds.

## History

Cook, Gerards, Schrijver and Tardos proved in 1986 that some optimal integer solution lies within $n$ times the largest subdeterminant of $A$ of an optimal LP solution, in the maximum norm. For programs in standard form this gives an $\ell_1$ bound that grows with $n^2$. Eisenbrand and Weismantel presented their bound at SODA 2018, with a proof based on the lemma of Steinitz from 1913 and the constant of Grinberg and Sevast'yanov from 1980. Jansen and Rohwedder later refined the dynamic programs that use it.

## References

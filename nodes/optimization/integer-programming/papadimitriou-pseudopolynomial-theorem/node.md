---
tag: 8GXKV1
kind: theorem
slug: papadimitriou-pseudopolynomial-theorem
name: Papadimitriou's pseudopolynomial theorem
aliases:
- pseudopolynomial integer programming with fixed constraints
- Papadimitriou's theorem on integer programming
area: optimization/integer-programming
level: research
summary: Integer programming with a fixed number of constraints has a pseudopolynomial algorithm.
prereqs: [pseudo-polynomial-time, knapsack-dynamic-programming, integer-feasibility]
see_also: [eisenbrand-weismantel-proximity-theorem, lenstra-theorem, knapsack-problem, strong-np-hardness, integer-programming-fixed-dimension, subset-sum-problem]
sources:
  - paper: doi:10.1145/322276.322287
    title: C. H. Papadimitriou, On the complexity of integer programming, Journal of the ACM 28(4), 1981
    locator: pp. 765 to 768
  - paper: doi:10.4230/LIPIcs.ESA.2018.31
    title: F. V. Fomin, F. Panolan, M. S. Ramanujan and S. Saurabh, On the optimality of pseudo-polynomial algorithms for integer programming, ESA 2018
    locator: Section 1 (the two steps of Papadimitriou's algorithm and its running time)
  - paper: doi:10.1145/3340322
    title: F. Eisenbrand and R. Weismantel, Proximity results and faster algorithms for integer programming using the Steinitz lemma, ACM Transactions on Algorithms 16(1), 2020
    locator: Section 2 of the arXiv version 1707.00481 (the Steinitz dynamic program, Theorems 2 and 4)
  - paper: "V. S. Grinberg and S. V. Sevast'yanov, Value of the Steinitz constant, Functional Analysis and Its Applications 14(2), 1980"
    locator: the Steinitz constant at most m for every norm on R^m (pp. 125 to 126, unsure)
---

## Statement

Consider integer programs in standard form
$$\max\{c^\top x : A x = b,\ x \ge 0,\ x \in \mathbb{Z}^n\},$$
with $A \in \mathbb{Z}^{m \times n}$, $b \in \mathbb{Z}^m$ and $c \in \mathbb{Z}^n$, where every entry of $A$ and $b$ has absolute value at most $d$.

**Theorem (Papadimitriou, 1981).** For each fixed $m$, there is an algorithm that decides whether the program is feasible, unbounded or has an optimum, and finds an optimal solution in the last case, in time polynomial in $n$ and $d$.

Papadimitriou proved two facts: if $Ax = b$, $x \ge 0$ has an integer solution, it has one in $\{0, 1, \dots, n(md)^{2m+1}\}^n$; and a dynamic program over bounded solutions then solves the problem in time $O(n^{2m+2} (md)^{(m+1)(2m+1)})$ (as summarized by Fomin et al.). The proof below follows the later and shorter route of Eisenbrand and Weismantel. It gives time $O(n \cdot (4md + 1)^{2m} (md + 1)^2)$ for the dynamic program.

The time is polynomial in the magnitude $d$, not in its number of digits, so the algorithm is [pseudopolynomial](/pseudo-polynomial-time/).

## In plain words

A whole-number solution of a system of equations is a list of columns that add up to the right-hand side. Take the shortest such list. Its columns can be added in an order that stays close to the straight line from zero to the target. The partial sums are then whole-number points in a thin tube around that line, and they are all different, because a repeated point would show a part of the list that adds up to zero and could be dropped.

So the search is a walk through a tube with few points, from zero to the target, one column per step. The number of points depends on the number of equations and the size of the numbers, and a simple table over these points finds the best walk.

## Proof

**Steinitz lemma (Grinberg and Sevast'yanov).** Let $\|\cdot\|$ be a norm on $\mathbb{R}^m$, and let $y_1, \dots, y_t \in \mathbb{R}^m$ with $\sum_i y_i = 0$ and $\|y_i\| \le 1$. Then there is an order $\pi$ with $\|\sum_{j=1}^{\ell} y_{\pi(j)}\| \le m$ for every $\ell$.

Let $a_1, \dots, a_n$ be the columns of $A$, let $R = 2md$, and let
$$S = \{p \in \mathbb{Z}^m : \|p - \lambda b\|_\infty \le R \text{ for some } \lambda \in [0, 1]\}.$$

**Lemma 1 (size of the tube).** $|S| \le (2R + 1)^m (\|b\|_1 + 1) \le (4md + 1)^m (md + 1)$.

*Proof.* Let $p \in S$ with $\|p - \lambda b\|_\infty \le R$. For each coordinate, $p_i$ is an integer in $[\lambda b_i - R, \lambda b_i + R]$, so $p_i \in [\lfloor \lambda b_i \rfloor - R, \lfloor \lambda b_i \rfloor + R]$, because $R$ is an integer. So $p$ lies within $R$ of the integer point $\lfloor \lambda b \rfloor$. As $\lambda$ grows from 0 to 1, each $\lfloor \lambda b_i \rfloor$ changes monotonically and at most $|b_i|$ times, so there are at most $\|b\|_1 + 1$ points $\lfloor \lambda b \rfloor$, each with at most $(2R + 1)^m$ integer points within distance $R$. Finally $\|b\|_1 \le md$. $\square$

**Lemma 2 (walks).** A sequence of columns $a_{i_1}, \dots, a_{i_k}$ with sum $b$ gives the feasible point $z$ with $z_i$ equal to the number of times $a_i$ appears, and $c^\top z = \sum_j c_{i_j}$. Conversely, let $z$ be a feasible point such that no nonzero integer $y$ with $0 \le y \le z$ and $A y = 0$ exists. Then the $t = \|z\|_1$ columns of $z$ (with repetition) can be ordered so that all partial sums $p_0 = 0, p_1, \dots, p_t = b$ lie in $S$ and are pairwise different. In particular $t + 1 \le |S|$.

*Proof.* The first part is clear. For the second, let $v_1, \dots, v_t$ be the columns of $z$ with repetition, and let $y_j = v_j - b/t$ (if $t = 0$ there is nothing to show). Then $\sum_j y_j = 0$ and $\|y_j\|_\infty \le d + d = 2d$. By the Steinitz lemma applied to the vectors $y_j / (2d)$, there is an order in which all partial sums satisfy $\|\sum_{j \le \ell} y_j\|_\infty \le 2md = R$. In this order, $p_\ell = \sum_{j \le \ell} v_j$ satisfies $\|p_\ell - (\ell / t) b\|_\infty \le R$, so $p_\ell \in S$. If $p_k = p_\ell$ with $k < \ell$, the columns $v_{k+1}, \dots, v_\ell$ sum to $0$, and their counts give a nonzero $y$ with $0 \le y \le z$ and $A y = 0$, which is excluded. $\square$

**Lemma 3 (unbounded programs).** A feasible program is unbounded if and only if the linear program $\{r : A r = 0,\ r \ge 0,\ c^\top r = 1\}$ is feasible.

*Proof.* If such an $r$ exists, it can be taken rational, and a positive multiple $r'$ of it is integer with $A r' = 0$, $r' \ge 0$, $c^\top r' > 0$. For a feasible $z$, all points $z + k r'$ with $k \in \mathbb{N}$ are feasible, and $c^\top (z + k r')$ grows without bound. Conversely, if the integer program is unbounded, so is its LP relaxation, and by linear programming duality the relaxation then has a ray $r \ge 0$ with $A r = 0$ and $c^\top r > 0$; scale it so that $c^\top r = 1$. $\square$

**The algorithm.** For $k = 0, 1, \dots, |S| - 1$ and $p \in S$, let $g_k(p)$ be the largest value $\sum_j c_{i_j}$ of a sequence of $k$ columns whose partial sums all lie in $S$ and end at $p$, or $-\infty$ if there is none. Then $g_0(0) = 0$, and
$$g_{k+1}(p') = \max\{g_k(p) + c_i : p \in S,\ p' = p + a_i\}.$$

1. Compute all $g_k$. If $g_k(b) = -\infty$ for every $k$, report that the program is infeasible.
2. Otherwise, if the linear program of Lemma 3 is feasible, report that the program is unbounded.
3. Otherwise, return the sequence that attains $\max_k g_k(b)$, as a point $z$ by Lemma 2.

*Correctness.* If the program is feasible, take a feasible $z$ with $\|z\|_1$ as small as possible. If a nonzero integer $y$ with $0 \le y \le z$ and $A y = 0$ existed, $z - y$ would be feasible with a smaller norm. So Lemma 2 applies, and some $g_k(b)$ is finite. Conversely, a finite $g_k(b)$ gives a feasible point by Lemma 2. So step 1 is correct, and step 2 is correct by Lemma 3.

In step 3, the program is feasible and bounded, and since $c$ is integer, the values $c^\top x$ of feasible points are integers bounded from above, so an optimal solution exists. Among all optimal solutions, take $z$ with $\|z\|_1$ as small as possible. Let $y$ be an integer vector with $y \ne 0$, $0 \le y \le z$ and $A y = 0$. Then $z + y$ is feasible, so $c^\top y \le 0$ by optimality, and $z - y$ is feasible, so $c^\top y \ge 0$. So $c^\top y = 0$ and $z - y$ is an optimal solution with a smaller norm, a contradiction. By Lemma 2, $z$ gives a sequence of $t \le |S| - 1$ columns with partial sums in $S$, so $\max_k g_k(b) \ge c^\top z$. Every sequence counted by $g_k(b)$ is a feasible point by Lemma 2, so $\max_k g_k(b) \le c^\top z$. So step 3 returns an optimal solution.

*Time.* Each of the $|S|$ rounds looks at every pair of a point $p \in S$ and a column $a_i$, so the table takes $O(n |S|^2)$ steps with a hash set for $S$. By Lemma 1, this is $O(n (4md + 1)^{2m} (md + 1)^2)$, which is polynomial in $n$ and $d$ for fixed $m$. The linear program of step 2 takes polynomial time. $\blacksquare$

## Consequences

- **Knapsack.** With $m = 1$, the theorem gives a pseudopolynomial algorithm for the [knapsack problem](/knapsack-problem/) with unlimited copies of each item and an exact capacity. Bounds such as $x_i \le 1$ add one row per variable, so the 0/1 case is not covered by the theorem directly.
- **Weak NP-hardness.** For each fixed $m$, integer programming in standard form is NP-hard only in the weak sense. With $m$ part of the input it is [strongly NP-hard](/strong-np-hardness/), so no pseudopolynomial algorithm exists for unbounded $m$ unless $\mathrm{P} = \mathrm{NP}$.
- **Small solutions.** The proof shows that a feasible program has a solution with $\|z\|_1 < (4md + 1)^m (md + 1)$, a bound that does not depend on $n$.

## Tightness

- **Pseudopolynomial, not polynomial.** Already for $m = 1$ the problem contains the [knapsack problem](/knapsack-problem/), which is NP-hard when the numbers are written in binary. So the dependence on $d$ cannot become polynomial in $\log d$ unless $\mathrm{P} = \mathrm{NP}$.
- **The exponent.** Fomin, Panolan, Ramanujan and Saurabh showed that, under the exponential time hypothesis, the exponent of the later algorithm of Jansen and Rohwedder cannot be improved much, and that for nonnegative $A$ the dynamic programming step of Papadimitriou is already nearly optimal.
- **The condition on m.** The fixed parameter is the number of constraints. With $n$ fixed instead, [Lenstra's theorem](/lenstra-theorem/) gives a truly polynomial algorithm.

## History

Papadimitriou published the theorem in the Journal of the ACM in 1981. His algorithm had no improvement until Eisenbrand and Weismantel (2018) used the Steinitz lemma to get time $(m\Delta)^{O(m)} \|b\|_\infty^2$, where $\Delta$ bounds only the entries of $A$. Jansen and Rohwedder improved the dependence further, and Fomin et al. proved lower bounds under the exponential time hypothesis.

## References

---
tag: BEXSQ9
kind: theorem
slug: akra-bazzi-theorem
name: Akra-Bazzi theorem
aliases:
- Akra-Bazzi method
area: foundations/recurrences
level: advanced
summary: Solves divide-and-conquer recurrences with unequal and multiple subproblem sizes by finding p with sum a_i b_i^p = 1 and integrating f.
prereqs: [master-theorem, divide-and-conquer-recurrence, watershed-function, integral-bounds-for-sums, induction]
see_also: [continuous-master-theorem, smoothness-rules, recursion-tree-method, substitution-method, median-of-medians, merge-sort, harmonic-series]
sources:
  - paper: doi:10.1023/A:1018373005182
    title: Mohamad Akra and Louay Bazzi, On the Solution of Linear Recurrence Equations, Computational Optimization and Applications 10(2), 195 to 210 (1998)
  - url: "https://courses.csail.mit.edu/6.046/spring04/handouts/akrabazzi.pdf"
    locator: Tom Leighton, Notes on Better Master Theorems for Divide-and-Conquer Recurrences, MIT, October 9, 1996 (Section 2, Theorem 1 and Lemma 1; Section 3, Theorem 2)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 4.7, Akra-Bazzi recurrences
  - paper: doi:10.1145/375827.375837
    title: Salvador Roura, Improved master theorems for divide-and-conquer recurrences, Journal of the ACM 48(2), 170 to 205 (2001)
    locator: Section 2, the Discrete Master Theorem (Theorem 2.3)
---

The Akra-Bazzi theorem gives the order of growth of the solution of a divide-and-conquer recurrence $T(x) = \sum_{i=1}^{k} a_i T(b_i x) + g(x)$ with any number of subproblems of possibly different fractional sizes $b_i$. Its answer is $T(x) = \Theta\big(x^p\big(1 + \int_1^x g(u)/u^{p+1}\,du\big)\big)$, where $p$ is the unique real number with $\sum_i a_i b_i^p = 1$. It contains the three cases of the [master theorem](/master-theorem/), covers the gaps between them, and needs no regularity condition, only a mild polynomial-growth condition on $g$. The form and proof below follow Leighton's notes of 1996.

## Statement

**The recurrence.** Let $k \ge 1$ be an integer, and for $1 \le i \le k$ let $a_i > 0$ and $0 < b_i < 1$ be constants. Let $x_0$ be a constant with $x_0 \ge 1/b_i$ and $x_0 \ge 1/(1 - b_i)$ for each $i$. Let $T$ be defined for real $x \ge 1$ by

$$T(x) = \Theta(1) \quad (1 \le x \le x_0), \qquad T(x) = \sum_{i=1}^{k} a_i T(b_i x) + g(x) \quad (x > x_0),$$

where $\Theta(1)$ means that $T$ is bounded between two positive constants on $[1, x_0]$.

**The polynomial-growth condition.** $g$ is non-negative and there are constants $c_1, c_2 > 0$ such that for each $x \ge 1$, each $i$, and each $u \in [b_i x, x]$,

$$c_1 g(x) \le g(u) \le c_2 g(x).$$

If $|g'(x)|$ is bounded above by a polynomial in $x$, this holds; for example $g(x) = x^\alpha \log^\beta x$ satisfies it for all real $\alpha$ and $\beta$ (Leighton's remark).

**Theorem (Akra and Bazzi; this form from Leighton).** Let $p$ be the unique real number with $\sum_{i=1}^{k} a_i b_i^p = 1$. Then

$$T(x) = \Theta\left(x^p\left(1 + \int_1^x \frac{g(u)}{u^{p+1}}\,du\right)\right).$$

**Floors and ceilings (Leighton, Theorem 2).** The same conclusion holds for $T(x) = \sum_i a_i T(b_i x + h_i(x)) + g(x)$ when there is $\varepsilon > 0$ with $|h_i(x)| \le x/\log^{1+\varepsilon} x$ for $x \ge x_0$, the growth condition holds for $u \in [b_i x + h_i(x), x]$, and $x_0$ is large enough. The choice $h_i(x) = \lceil b_i x \rceil - b_i x$ covers ceilings, and similarly floors.

## In plain words

An algorithm splits its input into several parts, maybe of different sizes, solves each part in the same way, and does some extra work to split and combine. The theorem finds the total cost in two steps.

First, find the critical rate of growth: the one for which the parts, taken together and weighted by their sizes, cost exactly as much as the whole. This rate depends only on how many parts there are and how big they are. It is the cost if the extra work were free.

Second, add up the extra work at every scale, measured against this critical rate. If the extra work grows slower than the critical rate, the sum stays bounded and the critical rate is the answer. If it grows faster, the extra work at the top dominates. If they match, each scale contributes the same, and a logarithmic factor appears.

## Proof

### Existence and uniqueness of p

Let $\phi(q) = \sum_i a_i b_i^q$. Each term $a_i b_i^q = a_i e^{q\ln b_i}$ is continuous and strictly decreasing in $q$, since $\ln b_i < 0$. As $q \to -\infty$ each term tends to $+\infty$, and as $q \to +\infty$ each tends to 0. By the intermediate value theorem there is exactly one $p$ with $\phi(p) = 1$.

### The intervals

Cut the domain into $I_0 = [1, x_0]$ and $I_j = (x_0 + j - 1, x_0 + j]$ for $j \ge 1$. If $x \in I_j$ with $j \ge 1$, then each $b_i x$ lies in some $I_{j'}$ with $j' < j$. Indeed $b_i x > b_i x_0 \ge 1$ because $x_0 \ge 1/b_i$, and

$$b_i x \le b_i(x_0 + j) \le x_0 + j - (1 - b_i)x_0 \le x_0 + j - 1,$$

because $(1 - b_i)x_0 \ge 1$. So $T$ on $I_j$ depends only on $T$ on earlier intervals, $T$ is well defined, and induction on $j$ is possible.

### Lemma 1

There are constants $c_3, c_4 > 0$ such that for each $i$ and each $x \ge 1$,

$$c_3\, g(x) \le x^p \int_{b_i x}^{x} \frac{g(u)}{u^{p+1}}\,du \le c_4\, g(x).$$

*Proof.* On $[b_i x, x]$, $g(u) \le c_2 g(x)$ and $u^{p+1} \ge \min\{(b_i x)^{p+1}, x^{p+1}\}$ (the minimum handles both signs of $p + 1$). The interval has length $(1 - b_i)x$. So

$$x^p \int_{b_i x}^{x} \frac{g(u)}{u^{p+1}}\,du \le x^p (1 - b_i) x \frac{c_2 g(x)}{x^{p+1}\min\{b_i^{p+1}, 1\}} = \frac{(1 - b_i)c_2}{\min\{1, b_i^{p+1}\}}\, g(x).$$

Take $c_4$ as the largest of these constants over $i$. In the same way, with $g(u) \ge c_1 g(x)$ and $u^{p+1} \le \max\{(b_i x)^{p+1}, x^{p+1}\}$, the integral is at least $\frac{(1 - b_i)c_1}{\max\{1, b_i^{p+1}\}} g(x)$; take $c_3$ as the smallest of these. $\square$

### The lower bound

Let $G(x) = 1 + \int_1^x g(u)u^{-p-1}\,du$. Claim: there is $c_5 > 0$ with $T(x) \ge c_5 x^p G(x)$ for each $x \ge 1$. Choose $c_5 \le 1/c_4$, and small enough that the claim holds on $I_0$, where $T$ is at least a positive constant and $x^p G(x)$ is bounded.

For $x \in I_j$, $j \ge 1$, the induction hypothesis holds at each $b_i x$, so

$$T(x) \ge \sum_i a_i c_5 (b_i x)^p \Big(G(x) - \int_{b_i x}^{x}\frac{g(u)}{u^{p+1}}\,du\Big) + g(x).$$

By Lemma 1, $(b_i x)^p \int_{b_i x}^x g(u)u^{-p-1}du = b_i^p \cdot x^p\int_{b_i x}^x \cdots \le b_i^p c_4 g(x)$. With $\sum_i a_i b_i^p = 1$,

$$T(x) \ge c_5 x^p G(x) - c_5 c_4\, g(x) + g(x) \ge c_5 x^p G(x),$$

since $c_5 c_4 \le 1$ and $g(x) \ge 0$.

### The upper bound

The same induction with $c_6 \ge 1/c_3$, and $c_6$ large enough for $I_0$, gives

$$T(x) \le c_6 x^p G(x) - c_6 c_3\, g(x) + g(x) \le c_6 x^p G(x).$$

Together, $T(x) = \Theta(x^p G(x))$. $\blacksquare$

The key step is that the weights $a_i b_i^p$ add up to 1. In the recursion tree, give a node of size $m$ the weight $m^p$: the weights of the children of a node add up to the weight of the node. The term $-\int_{b_i x}^x$ is exactly the part of the integral that the children have not yet seen, and Lemma 1 says that this part is worth $\Theta(g(x))$, the cost of the node itself.

### Sketch of Theorem 2

For perturbed arguments $b_i x + h_i(x)$, Leighton strengthens the induction hypothesis to $T(x) \ge c_5 x^p\big(1 + \log^{-\varepsilon/2} x\big)G(x)$ for the lower bound and $T(x) \le c_6 x^p\big(1 - \log^{-\varepsilon/2} x\big)G(x)$ for the upper bound. The bound $|h_i(x)| \le x/\log^{1+\varepsilon} x$ makes $(b_i x + h_i(x))^p$ differ from $(b_i x)^p$ by a factor $1 + O(1/\log^{1+\varepsilon} x)$, and the change of the correction factor from $x$ to $b_i x$ is of order $1/\log^{1+\varepsilon/2} x$, which absorbs it. The conditions on $x_0$ in the notes make these estimates hold for each $x > x_0$.

## Consequences

### The master theorem

For $k = 1$, $T(x) = aT(x/b) + g(x)$ gives $a b^{-p} = 1$, so $p = \log_b a$, the exponent of the [watershed function](/watershed-function/). For $g(x) = \Theta(x^q \log^m x)$:

- $q < p$: the integral converges, and $T(x) = \Theta(x^p)$. This is case 1.
- $q = p$: the integral is $\Theta\big(\int_1^x \log^m u\,\frac{du}{u}\big)$, so $T(x) = \Theta(x^p \log^{m+1} x)$ for $m > -1$, $\Theta(x^p \log\log x)$ for $m = -1$, and $\Theta(x^p)$ for $m < -1$. This is case 2 and its extension.
- $q > p$: the integral is $\Theta(x^{q-p}\log^m x)$, and $T(x) = \Theta(x^q \log^m x) = \Theta(g(x))$. This is case 3, with no regularity condition.

### Worked recurrences

| Recurrence | $p$ | Integral | Solution |
|---|---|---|---|
| $T(x/3) + T(2x/3) + x$ | 1 | $\ln x$ | $\Theta(x\log x)$ |
| $T(x/5) + T(7x/10) + x$ | $\approx 0.8398$ | $\Theta(x^{1-p})$ | $\Theta(x)$ |
| $T(x/2) + T(x/3) + x$ | $\approx 0.7879$ | $\Theta(x^{1-p})$ | $\Theta(x)$ |
| $2T(x/4) + 3T(x/6) + x\lg x$ | 1 | $\Theta(\log^2 x)$ | $\Theta(x\log^2 x)$ |
| $2T(x/2) + \frac89 T(3x/4) + x^2/\lg x$ | 2 | $\Theta(\log\log x)$ | $\Theta(x^2 \log\log x)$ |
| $T(x/2) + \lg x$ | 0 | $\Theta(\log^2 x)$ | $\Theta(\log^2 x)$ |
| $\frac12 T(x/2) + 1/x$ | $-1$ | $\Theta(\log x)$ | $\Theta((\log x)/x)$ |
| $2T(x/2) + x/\lg x$ | 1 | $\Theta(\log\log x)$ | $\Theta(x\log\log x)$ |
| $T(x/2) + x(2 - \cos x)$ | 0 | $\Theta(x)$ | $\Theta(x)$ |

The rows with $2T(x/4) + 3T(x/6)$, $2T(x/2) + \frac89 T(3x/4)$, $T(x/2) + \lg x$ and $\frac12 T(x/2) + 1/x$ are Leighton's examples. For the first: $2 \cdot \frac14 + 3 \cdot \frac16 = 1$, so $p = 1$, and $\int_1^x \frac{u\lg u}{u^2}du = \frac{\lg^2 x}{2\lg e}$. For the second: $2 \cdot \frac14 + \frac89 \cdot \frac9{16} = 1$, so $p = 2$, and $\int \frac{du}{u\lg u} = \Theta(\log\log x)$.

The second row is the recurrence of the [median of medians](/median-of-medians/) selection algorithm without its additive constants: $(1/5)^p + (7/10)^p = 1$ at $p \approx 0.8398$, and the integral $\int_1^x u^{-p}du = \Theta(x^{1-p})$ gives $\Theta(x)$. Since $\frac15 + \frac{7}{10} < 1$, the root dominates. The theorem gives no constant, but Roura's Discrete Master Theorem gives $T(x) \sim x/(1 - \frac15 - \frac7{10}) = 10x$; with integer floors and $T = 1$ below 5, $T(n)/n$ is about $9.36$ at $n = 10^8$, still rising slowly. The last row has an oscillating $g$ that fails the regularity condition of the master theorem but satisfies the growth condition with $c_1 = \frac16$ and $c_2 = 3$, because $u \le g(u) \le 3u$.

With integer floors and base value 1, the first example gives $T(n)/(n\lg^2 n) \approx 0.250, 0.241, 0.236, 0.232$ at $n = 10^4, 10^6, 10^8, 10^{10}$, and the second gives $T(n)/(n^2 \lg\lg n) \approx 0.686, 0.725, 0.748, 0.756$. Both ratios settle slowly, as factors of order $\log$ and $\log\log$ do.

### Unbalanced trees

In $T(x/3) + T(2x/3) + x$ the recursion tree is not complete, and the number of its leaves is not obvious. The number of leaves $L$ satisfies $L(x) = L(x/3) + L(2x/3)$, and the theorem with $g = 0$, which satisfies the growth condition, gives $\Theta(x^p) = \Theta(x)$ leaves; see the [recursion-tree method](/recursion-tree-method/).

## Tightness

- **Super-polynomial $g$.** The growth condition fails for $g(x) = 2^x$: on $[x/2, x]$, $g(x/2)/g(x) = 2^{-x/2}$ is not bounded below. For $T(x) = 2T(x/2) + 2^x$, $p = 1$ and the formula gives $x\big(1 + \int_1^x 2^u u^{-2}du\big) = \Theta(2^x/x)$, but $T(x) \ge 2^x$, so the formula is wrong by a factor $x$. With integer halving and $T(1) = 1$, $T(n)/2^n$ is $1.0021$ at $n = 20$ and $1.0000$ at $n = 100$, so $T(n) = \Theta(2^n)$. Leighton's remark: if $g$ grows faster than each polynomial, $T(x) = \Theta(g(x))$.
- **Sizes that do not shrink by a constant factor.** $b_i = 1$ is excluded, so $T(x - 1)$ terms are not covered. A term $T(x - \sqrt x)$ is also excluded: as $b_i x + h_i(x)$ it needs $h_i(x) = -\sqrt x$ with $b_i = 1$.
- **Too large perturbations.** Theorem 2 needs $|h_i(x)| \le x/\log^{1+\varepsilon} x$. Perturbations proportional to $x$, such as $h_i(x) = cx$, change the effective fraction $b_i$ and with it the value of $p$, so some bound on $h_i$ is needed.
- **Non-constant coefficients.** $a_i$, $b_i$ and $k$ must be constants. $T(x) = \sqrt x\, T(\sqrt x) + x$ is outside the theorem; a [change of variables](/change-of-variables/) gives $\Theta(x\log\log x)$.
- **Negative $g$.** The proof uses $g \ge 0$ in both inductions.
- **Only $\Theta$.** The theorem gives no constant factor. Roura's Discrete Master Theorem gives the leading constant for $T(n) = t_n + \sum_d w_d T(z_d n + \cdots)$ when $t_n \sim B n^a \log^c n$.

## History

Akra and Bazzi published the theorem in 1998 in Computational Optimization and Applications; their analysis uses a functional transform that they call the order transform (Leighton's description). Leighton's notes, dated October 9, 1996, give the inductive proof above, a polynomial-growth condition that is somewhat less restrictive than the conditions of Akra and Bazzi, and Theorem 2 for perturbed arguments. CLRS, fourth edition, presents Akra-Bazzi recurrences in Section 4.7. Roura (2001) gave master theorems with exact leading constants for related recurrences.

## References

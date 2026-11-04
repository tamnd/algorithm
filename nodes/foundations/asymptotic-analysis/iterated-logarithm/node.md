---
tag: 44165W
kind: definition
slug: iterated-logarithm
name: Iterated logarithm
aliases:
- Iterated logarithm (log*)
- iterated logarithm
- log*
- log-star
- log-star function
area: foundations/asymptotic-analysis
level: core
summary: The number of times the logarithm must be applied before the value drops to at most one; it grows extremely slowly.
prereqs: [logarithms, asymptotic-notation]
see_also: [inverse-ackermann-function, ackermann-function, disjoint-set-forest, union-by-rank, union-find-amortized-bound]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 3, standard notations and common functions (iterated logarithm)
  - paper: Hopcroft and Ullman, Set merging algorithms, SIAM Journal on Computing 2 (1973)
    locator: the O(m lg* n) bound for union by rank with path compression
  - paper: Cole and Vishkin, Deterministic coin tossing with applications to optimal parallel list ranking, Information and Control 70 (1986)
    locator: the coloring of a cycle in O(lg* n) rounds
  - paper: Tarjan, Efficiency of a good but not linear set union algorithm, Journal of the ACM 22 (1975)
    locator: the bound with the inverse Ackermann function
  - paper: Nathan Linial, Locality in distributed graph algorithms, SIAM Journal on Computing 21 (1992)
    locator: the lower bound for coloring a cycle
  - paper: Martin Fürer, Faster integer multiplication, STOC 2007
    locator: the main theorem
  - paper: David Harvey and Joris van der Hoeven, Integer multiplication in time O(n log n), Annals of Mathematics 193 (2021)
    locator: the main theorem
---

The iterated logarithm $\lg^* n$ is the number of times the [binary logarithm](/logarithms/) must be applied to $n$ before the result is at most 1. It grows more slowly than $\lg \lg n$, $\lg \lg \lg n$ and every fixed number of nested logarithms. For each input size $n$ that occurs in practice, $\lg^* n \le 5$. It appears in the cost of coloring a cycle in a distributed system and in an old bound for [union-find](/disjoint-set-forest/).

## Definition

Let $\lg^{(0)} x = x$ and $\lg^{(i+1)} x = \lg(\lg^{(i)} x)$, defined as long as $\lg^{(i)} x > 0$. For a real number $x$, the iterated logarithm is
$$\lg^* x = \min\{\, i \ge 0 : \lg^{(i)} x \le 1 \,\}.$$
Do not confuse $\lg^{(i)} x$, the $i$-fold composition, with $\lg^i x = (\lg x)^i$, a power.

The minimum exists for each real $x$. If $x \le 1$, the set contains $i = 0$, so $\lg^* x = 0$. Else the steps stay defined, because a value $y > 1$ gives $\lg y > 0$. Two facts show that the values reach 1. First, for $y > 2$ we have $\lg y < y - 1$, because $\lg$ is concave and equals $y - 1$ at $y = 1$ and $y = 2$, so it is below this line for $y > 2$. Second, for $1 < y \le 2$ we have $0 < \lg y \le 1$. So while the value is above 2, each step lowers it by more than 1, and after at most $\lceil x \rceil$ steps it is at most 2. One more step makes it at most 1. The site uses the function for integers $n \ge 1$.

The definition gives the recurrence
$$\lg^* x = \begin{cases} 0 & \text{if } x \le 1, \\ 1 + \lg^*(\lg x) & \text{if } x > 1. \end{cases}$$

Compare this with the *tower function* $T(0) = 1$, $T(k+1) = 2^{T(k)}$. Then $T(1) = 2$, $T(2) = 4$, $T(3) = 16$, $T(4) = 65536$, $T(5) = 2^{65536}$. For $k \ge 1$ and each real $x$:
$$\lg^* x = k \iff T(k-1) < x \le T(k).$$
*Proof.* Induction on $k$. For $k = 1$: $\lg^* x = 1$ means $x > 1$ and $\lg x \le 1$, that is $1 < x \le 2$. For the step, let $k \ge 2$. Both sides need $x > 1$: the left side because $\lg^* x = 0$ for $x \le 1$, the right side because $T(k-1) \ge 2$. For $x > 1$, the recurrence gives $\lg^* x = k$ exactly when $\lg^*(\lg x) = k - 1$. By the hypothesis this holds exactly when $T(k-2) < \lg x \le T(k-1)$. Since $\lg$ is increasing and $\lg T(j) = T(j-1)$ for $j \ge 1$, this is the same as $T(k-1) < x \le T(k)$. $\square$

So $\lg^*$ is the inverse of the tower function. For $n = 1$ the value is 0.

## Examples and non-examples

| $n$ | $\lg^* n$ |
|---|---|
| 1 | 0 |
| 2 | 1 |
| 3, 4 | 2 |
| 5 to 16 | 3 |
| 17 to 65536 | 4 |
| 65537 to $2^{65536}$ | 5 |

The number $2^{65536}$ has 19729 decimal digits. The number of atoms in the observable universe is often estimated as about $10^{80}$, a number with 81 digits. So no input with more than $2^{65536}$ items or bits can be stored, and $\lg^* n \le 5$ for each input size $n$ that occurs in practice. A single stored number can be larger: $2^{65537}$ needs only 65538 bits, and $\lg^* 2^{65537} = 6$.

Examples of the computation:

- $n = 16$: $16 \to 4 \to 2 \to 1$, three steps. So $\lg^* 16 = 3$.
- $n = 65536$: $65536 \to 16 \to 4 \to 2 \to 1$, four steps.
- $n = 65537$: since $T(4) = 65536 < 65537 \le T(5)$, the rule gives $\lg^* 65537 = 5$. By steps: $\lg 65537 \approx 16.00002$, which is above $T(3) = 16$, so four more steps are necessary.

Comparison with $\lg \lg n$. At $n = 2^{65536}$, $\lg n = 65536$ and $\lg \lg n = 16$, but $\lg^* n = 5$. At $n = 10^6$, $\lg \lg n \approx 4.3$ and $\lg^* n = 5$ (as $10^6 > 65536$), so for small $n$ the two can be close. As $n$ grows, $\lg \lg n$ grows without bound much faster: $\lg^* n = o(\lg \lg n)$, and the same holds for $\lg^{(c)} n$ for each fixed $c$. Proof: if $\lg^* n = k \ge c + 2$, then $n > T(k-1)$, so $\lg^{(c)} n > T(k-1-c)$. Since $T(j) \ge 2^j$, the ratio $\lg^{(c)} n / \lg^* n$ is more than $2^{k-1-c}/k$, which tends to infinity with $k$.

Non-examples. The iterated logarithm is not the iterated *power* $(\lg n)^k$, and it is not $\lg \lg n$. It is also not the inverse Ackermann function $\alpha(n)$: $\alpha$ grows even more slowly than $\lg^*$ (see below).

## Related definitions

- **Where $\lg^*$ appears.**
  - *Coloring a cycle.* Cole and Vishkin gave a deterministic method for a cycle (or a linked list) of $n$ nodes with distinct identifiers from $\{1, \dots, n\}$ in which each node knows its successor. In each synchronous round, a node compares its color with its successor's color, and finds the lowest bit where they differ. The new color is a function of the position of this bit and its value. A color with $k$ bits is replaced by a color with about $\lg k + 1$ bits, so after $O(\lg^* n)$ rounds only a constant number of colors remain. A few more rounds give 3 colors. Cole and Vishkin used this step for parallel list ranking. Linial (1992) proved that each deterministic distributed algorithm that 3-colors a cycle of $n$ nodes needs $\Omega(\lg^* n)$ rounds, so the bound of Cole and Vishkin is tight up to a constant factor.
  - *Integer multiplication.* Fürer (2007) multiplied two $n$-bit integers in $n \lg n \cdot 2^{O(\lg^* n)}$ bit operations. Harvey and van der Hoeven (2021) later removed the factor $2^{O(\lg^* n)}$ and reached $O(n \lg n)$. See [integer multiplication](/integer-multiplication/).
  - *Union-find.* Hopcroft and Ullman (1973) proved that a sequence of $m$ operations on $n$ elements takes $O(m \lg^* n)$ time when the structure links trees [by size](/union-by-size/) and uses [path compression](/path-compression/). The same bound holds for union by rank (see [union by rank](/union-by-rank/) and [disjoint-set forest](/disjoint-set-forest/)).
- **The bound of Tarjan.** Tarjan (1975) gave a tighter bound for the same structure: $O(m\,\alpha(m, n))$, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/). The function $\alpha$ grows more slowly than $\lg^*$, so the bound with $\alpha$ is stronger, and the bound with $\lg^*$ is the older and weaker one. Both bounds are for the same data structure. The [Ackermann function](/ackermann-function/) page has the definitions of $\alpha$, and the page on the [amortized bound](/union-find-amortized-bound/) of union-find has the details.
- **Not a constant, but nearly.** The function $\lg^* n$ is unbounded, so $\lg^* n \ne O(1)$. A bound with $\lg^*$ is therefore not linear. But the factor $\lg^* n$ is at most 5 for each practical $n$, so the bound is linear up to a small constant factor.

## References

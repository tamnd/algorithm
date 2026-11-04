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
see_also: [inverse-ackermann-function, ackermann-function, disjoint-set-forest, union-by-rank, union-find-amortized-bound, cole-vishkin, linial-coloring-lower-bound]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 3.3, Standard notations and common functions (the iterated logarithm function)
  - paper: Hopcroft and Ullman, Set merging algorithms, SIAM Journal on Computing 2(4) (1973)
    locator: the O(m lg* n) bound for union by size with path compression
  - paper: Cole and Vishkin, Deterministic coin tossing with applications to optimal parallel list ranking, Information and Control 70(1) (1986)
    locator: the reduction of colors in O(lg* n) rounds
  - paper: Nathan Linial, Locality in distributed graph algorithms, SIAM Journal on Computing 21(1) (1992)
    locator: the lower bound for coloring a cycle
  - paper: Tarjan, Efficiency of a good but not linear set union algorithm, Journal of the ACM 22(2) (1975)
    locator: the bound with the inverse Ackermann function
  - paper: Martin Fürer, Faster integer multiplication, Proceedings of the 39th ACM Symposium on Theory of Computing (STOC 2007)
    locator: the main theorem
  - paper: David Harvey and Joris van der Hoeven, Integer multiplication in time O(n log n), Annals of Mathematics 193(2) (2021)
    locator: the main theorem
---

The iterated logarithm $\lg^* n$ is the number of times the binary [logarithm](/logarithms/) must be applied to $n$ before the result is at most 1. It is the inverse of the tower function $2^{2^{\cdots^2}}$, so it grows more slowly than $\lg\lg n$, than $\lg\lg\lg n$, and than every fixed number of nested logarithms. For each input size that can occur in practice, $\lg^* n \le 5$. It appears in the round complexity of [coloring a cycle](/cole-vishkin/) in a distributed system, in a classic bound for [union-find](/disjoint-set-forest/), and in the history of fast integer multiplication.

## Definition

Let $\lg^{(0)} x = x$ and $\lg^{(i+1)} x = \lg(\lg^{(i)} x)$, defined as long as $\lg^{(i)} x > 0$. For a real number $x$, the iterated logarithm is
$$\lg^* x = \min\{\, i \ge 0 : \lg^{(i)} x \text{ is defined and } \lg^{(i)} x \le 1 \,\}.$$
This is the definition of Cormen, Leiserson, Rivest and Stein. Do not confuse $\lg^{(i)} x$, the $i$-fold composition, with $\lg^i x = (\lg x)^i$, a power.

The definition gives the recurrence
$$\lg^* x = \begin{cases} 0 & \text{if } x \le 1, \\ 1 + \lg^*(\lg x) & \text{if } x > 1. \end{cases}$$

### The tower function and the exact ranges

Define the tower function by $T(-1) = 0$, $T(0) = 1$ and $T(k+1) = 2^{T(k)}$. Then $T(1) = 2$, $T(2) = 4$, $T(3) = 16$, $T(4) = 65536$ and $T(5) = 2^{65536}$. Since $T(k+1) = 2^{T(k)}$, we have $\lg T(k) = T(k-1)$ for $k \ge 0$, and $T$ is strictly increasing.

**Lemma.** For each integer $k \ge 1$ and each real $x$ with $T(k-1) < x \le T(k)$, the value $\lg^{(i)} x$ is defined for $i = 0, \ldots, k$, and
$$T(k-1-i) < \lg^{(i)} x \le T(k-i).$$
Hence $\lg^* x = k$. Also $\lg^* x = 0$ for $x \le 1$.

*Proof.* Induction on $i$. For $i = 0$ this is the hypothesis. Let $0 \le i < k$ and assume $T(k-1-i) < \lg^{(i)} x \le T(k-i)$. The left end is at least $T(0) = 1$ because $k - 1 - i \ge 0$, so $\lg^{(i)} x > 1 > 0$ and the next logarithm is defined. Apply $\lg$, which is increasing, and use $\lg T(j) = T(j-1)$: we get $T(k-2-i) < \lg^{(i+1)} x \le T(k-1-i)$. This proves the bounds. For $i \le k-1$ the bounds give $\lg^{(i)} x > T(0) = 1$, and for $i = k$ they give $0 < \lg^{(k)} x \le T(0) = 1$. So the least $i$ with $\lg^{(i)} x \le 1$ is $k$. For $x \le 1$ the index $i = 0$ already qualifies. $\square$

Since $T$ is increasing and unbounded, each real $x > 1$ lies in exactly one interval $(T(k-1), T(k)]$ with $k \ge 1$. So the lemma shows that $\lg^* x$ exists for each real $x$, and that
$$\lg^* x = k \iff T(k-1) < x \le T(k) \qquad (k \ge 1).$$
In words, $\lg^*$ is the inverse of the tower function, rounded up.

### Computing it exactly on integers

For an integer $n > 1$, $\lg^* n = 1 + \lg^* \lceil \lg n \rceil$. *Proof.* By the lemma, $\lg^*$ of a number $y > 1$ depends only on the interval $(T(j-1), T(j)]$ that contains $y$. The ends of these intervals are integers, and for integers $a < b$ we have $a < y \le b$ exactly when $a < \lceil y \rceil \le b$. So $\lg^*(\lg n) = \lg^* \lceil \lg n \rceil$ when $\lg n > 1$. When $\lg n \le 1$, that is $n = 2$, both sides are 0. $\square$ Since $\lceil \lg n \rceil$ is the number of bits of $n - 1$, this gives an exact loop on integers, with no floating point: replace $n$ by the bit length of $n - 1$ until $n \le 1$, and count the steps.

## Examples and non-examples

| $n$ | $\lg^* n$ |
|---|---|
| 1 | 0 |
| 2 | 1 |
| 3, 4 | 2 |
| 5 to 16 | 3 |
| 17 to 65536 | 4 |
| 65537 to $2^{65536}$ | 5 |

The table is the lemma for $k = 1, \ldots, 5$. The exact integer loop gives the same values, and it agrees with the definition computed in floating point for every $n$ up to $200\,000$.

- $n = 16$: $16 \to 4 \to 2 \to 1$, three steps, so $\lg^* 16 = 3$.
- $n = 17$: $17 \to 4.087 \to 2.031 \to 1.022 \to 0.032$, four steps, so $\lg^* 17 = 4$.
- $n = 65536$: $65536 \to 16 \to 4 \to 2 \to 1$, four steps.
- $n = 65537$: $T(4) = 65536 < 65537 \le T(5)$, so $\lg^* 65537 = 5$. By steps, $\lg 65537 = 16.00002\ldots$, which is above $T(3) = 16$.
- $n = 10^{80}$: $T(4) < 10^{80} \le T(5)$, so $\lg^* 10^{80} = 5$.

**Why "at most 5 in practice".** The number $2^{65536}$ has 19729 decimal digits, while the number of atoms in the observable universe is commonly estimated at about $10^{80}$. So no input has more than $2^{65536}$ items, and $\lg^* n \le 5$ for each input size that occurs. This is the remark of Cormen et al. A single stored number can be larger: $2^{65537}$ has only 65538 bits, and $\lg^* 2^{65537} = 6$.

**Comparison with $\lg\lg n$.** At $n = 10^6$, $\lg\lg n = 4.32$ and $\lg^* n = 5$, so for small $n$ the two are close. At $n = 2^{65536}$, $\lg\lg n = 16$ while $\lg^* n = 5$. For each fixed $c \ge 1$, $\lg^* n = o(\lg^{(c)} n)$. *Proof.* Let $k = \lg^* n$, and let $n$ be so large that $k \ge c + 2$. By the lemma $n > T(k-1)$, so $\lg^{(c)} n > T(k-1-c)$, since $\lg$ is increasing and $\lg T(j) = T(j-1)$. By induction $T(j) \ge 2^j$ for $j \ge 0$ (true for $j = 0$, and $T(j+1) = 2^{T(j)} \ge 2^{2^j} \ge 2^{j+1}$). So $\lg^{(c)} n/\lg^* n > 2^{k-1-c}/k$. As $n \to \infty$, $k \to \infty$, and this lower bound tends to infinity. $\square$

**It is unbounded.** $\lg^* T(k) = k$ for each $k$, so $\lg^* n \notin O(1)$. A bound of the form $O(n\lg^* n)$ is not $O(n)$, although the factor $\lg^* n$ is at most 5 in practice.

**Non-examples.** The iterated logarithm is not the power $(\lg n)^k$, and it is not $\lg\lg n$. It is also not the [inverse Ackermann function](/inverse-ackermann-function/) $\alpha(n)$, which grows even more slowly.

### Pitfalls

- **Rounding down inside the loop.** Replacing $n$ by $\lfloor \lg n \rfloor$ gives wrong values: it maps 3 to 1 and so gives 1, while $\lg^* 3 = 2$. The first wrong values are at $n = 3, 5, 6, 7, 8$. Round up, as in the exact loop above, or use real logarithms.
- **The stopping test.** The definition stops at a value at most 1, not below 1. A loop with the test "$x < 1$" gives $\lg^* 2 = 2$ instead of 1 and shifts the whole table.
- **Confusing the notations.** $\lg^{(2)} n = \lg\lg n$, $\lg^2 n = (\lg n)^2$, and $\lg^* n$ is the number of iterations. At $n = 65536$ they are 4, 256 and 4.
- **Calling it a constant.** $\lg^* n$ is at most 5 for every practical input, but it is not $O(1)$. A proof that needs a constant cannot use it as one.

## Related definitions

- **Coloring a cycle.** Cole and Vishkin gave a deterministic method for a cycle, or a linked list, of $n$ nodes with distinct identifiers of $\lceil \lg n \rceil$ bits, in which each node knows its successor (see [Cole-Vishkin](/cole-vishkin/)). In each synchronous round a node compares its color $a$ with the color $b$ of its successor, finds the lowest bit position $j$ where they differ, and takes the new color $2j + a_j$, where $a_j$ is its own bit at $j$. The new coloring is proper: if a node and its successor chose the same $j$, their bits at $j$ differ, by the choice of $j$ at the first node. A color of $k$ bits becomes one of at most $\lceil \lg k \rceil + 1$ bits, so the number of bits drops as $64 \to 7 \to 4 \to 3$ and then stays at 3, which leaves at most 6 colors. This takes $\lg^* n + O(1)$ rounds, and a few more rounds reduce 6 colors to 3. A simulation on a cycle of $10^5$ nodes with random identifiers reaches 6 colors after 4 rounds, with each coloring proper. Cole and Vishkin used this step for parallel [list ranking](/list-ranking/).
- **The matching lower bound.** Linial (1992) proved that each deterministic distributed algorithm that 3-colors a cycle of $n$ nodes needs $\Omega(\lg^* n)$ rounds (see [Linial's lower bound](/linial-coloring-lower-bound/)). So the bound of Cole and Vishkin is tight up to a constant factor.
- **Union-find.** Hopcroft and Ullman (1973) proved that a sequence of $m$ operations on $n$ elements takes $O(m\lg^* n)$ time when the structure links trees [by size](/union-by-size/) and uses [path compression](/path-compression/). The same bound holds for [union by rank](/union-by-rank/). Tarjan (1975) proved the tighter bound $O(m\,\alpha(m, n))$ for the same structure, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/). The bound with $\lg^*$ is the older and weaker one. See the [amortized bound of union-find](/union-find-amortized-bound/).
- **Integer multiplication.** Fürer (2007) multiplied two $n$-bit integers in $n\lg n \cdot 2^{O(\lg^* n)}$ bit operations on a multitape Turing machine. Harvey and van der Hoeven (2021) removed the factor $2^{O(\lg^* n)}$ and reached $O(n\log n)$. See [integer multiplication](/integer-multiplication/).
- **The tower function** $T(k)$ is the inverse of $\lg^*$ in the sense of the lemma. Repeated addition gives multiplication, repeated multiplication gives powers, and repeated powers give towers. The [Ackermann function](/ackermann-function/) climbs this whole ladder, and its inverse $\alpha$ is therefore much slower than $\lg^*$.

## References

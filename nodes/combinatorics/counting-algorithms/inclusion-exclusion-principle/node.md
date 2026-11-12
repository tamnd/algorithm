---
tag: B2YNWT
kind: technique
slug: inclusion-exclusion-principle
name: Inclusion-exclusion principle
aliases:
- sieve formula
- Poincaré sieve
- principle of inclusion and exclusion
area: combinatorics/counting-algorithms
level: core
summary: Counts a union by alternately adding and subtracting intersections.
prereqs: [rule-of-sum, binomial-theorem]
see_also: [derangement, bounded-integer-solutions-counting, mobius-inversion, counting-coprime-pairs, euler-totient, ryser-formula, sum-over-subsets-dp, union-bound]
sources:
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 2, Sieve Methods (Section 2.1, Inclusion-exclusion, and Section 2.2, Examples and special cases)
  - book: isbn:9780136020400
    title: Richard A. Brualdi, Introductory Combinatorics, fifth edition
    locator: Chapter 6, The Inclusion-Exclusion Principle and Applications (Section 6.1, the principle; Section 6.3, derangements)
  - book: isbn:9783642165320
    title: Fedor V. Fomin and Dieter Kratsch, Exact Exponential Algorithms, Springer, 2010
    locator: Chapter 4, Inclusion-Exclusion (Hamiltonian paths, the permanent, and covering and partitioning problems)
  - paper: doi:10.1137/070683933
    title: Andreas Björklund, Thore Husfeldt and Mikko Koivisto, Set partitioning via inclusion-exclusion, SIAM Journal on Computing 39(2), 546 to 563 (2009)
    locator: the main results (set partitioning and the chromatic number in O*(2^n) time)
---

The inclusion-exclusion principle counts the elements of a union of sets by adding the sizes of the sets, subtracting the sizes of the pairwise intersections, adding those of the triple intersections, and so on: $|A_1 \cup \cdots \cup A_m| = \sum_{\emptyset \ne J \subseteq [m]} (-1)^{|J|-1} |\bigcap_{j \in J} A_j|$. Its main use is the complement form: to count the objects with none of $m$ bad properties, it is often easier to count, for each set $J$ of properties, the objects that have *at least* all the properties in $J$. It gives closed forms for [derangements](/derangement/), surjections, [Euler's totient](/euler-totient/) and [bounded integer solutions](/bounded-integer-solutions-counting/), and exact algorithms in $O^*(2^n)$ time for the permanent, Hamiltonian paths and graph coloring.

## In plain words

In a class, twelve students play football and nine play chess, and four do both. How many play at least one? Adding twelve and nine counts the four who do both twice, so you subtract them once: seventeen.

With three groups, subtracting all the overlaps of two groups removes the students in all three groups once too often, so you add them back. The rule continues like this: add the groups, take away the overlaps of two, add back the overlaps of three, and so on. Often you use it the other way: you count everything, then remove the things that break some rule, using the same up and down pattern, to find the things that break no rule at all.

## When it applies

- You want the objects that satisfy all of $m$ conditions, and the objects that *break* a given set of conditions are easy to count, even though the objects that break *exactly* those conditions are not.
- The count of the intersection $A_J$ depends only on $|J|$ (a symmetric problem), so the $2^m$ terms collapse into $m + 1$.
- The conditions are divisibility by primes, fixed points of a permutation, upper bounds on variables, or vertices that a walk must visit.
- An exact exponential algorithm is acceptable, with $2^m$ terms that each take polynomial time and little space.

## The template

Notation: $U$ is a finite set (the universe), $A_1, \ldots, A_m \subseteq U$ are the "bad" sets, $[m] = \{1, \ldots, m\}$, and for $J \subseteq [m]$, $A_J = \bigcap_{j \in J} A_j$ with $A_\emptyset = U$. $\binom{n}{k}$ is the [binomial coefficient](/binomial-coefficient/).

**Theorem (inclusion-exclusion).** For finite sets $A_1, \ldots, A_m \subseteq U$,
$$\Bigl|U \setminus \bigcup_{i=1}^{m} A_i\Bigr| = \sum_{J \subseteq [m]} (-1)^{|J|}\,|A_J|, \qquad \Bigl|\bigcup_{i=1}^{m} A_i\Bigr| = \sum_{\emptyset \ne J \subseteq [m]} (-1)^{|J|-1}\,|A_J|.$$

*Proof.* Fix $x \in U$ and let $T = \{i : x \in A_i\}$, with $t = |T|$. The element $x$ lies in $A_J$ exactly when $J \subseteq T$, so it contributes $\sum_{J \subseteq T} (-1)^{|J|} = \sum_{j=0}^{t} \binom{t}{j}(-1)^j = (1 - 1)^t$ to the right side of the first formula, by the [binomial theorem](/binomial-theorem/). This is $1$ when $t = 0$, that is when $x$ lies in no $A_i$, and $0$ otherwise. Summing over $x$ gives the first formula. The second is $|U|$ minus the first. $\square$

**Symmetric form.** If $|A_J| = a_j$ depends only on $j = |J|$, the count of elements in no $A_i$ is $\sum_{j=0}^{m} (-1)^j \binom{m}{j} a_j$.

**Function form.** For functions $f, g$ on the subsets of $[m]$, $f(S) = \sum_{T \supseteq S} g(T)$ for all $S$ if and only if $g(S) = \sum_{T \supseteq S} (-1)^{|T| - |S|} f(T)$ for all $S$. With $g(T)$ the number of elements whose set of bad properties is exactly $T$, $f(S) = |A_S|$, and $S = \emptyset$ gives the theorem. This is [Möbius inversion](/mobius-inversion/) on the lattice of subsets.

```pseudo id=main
COUNT-AVOIDING(U, A_1, ..., A_m)
L1  choose the bad sets A_i so that "good" means "in no A_i"        ▷ hole: the properties
L2  total ← 0
L3  for each J ⊆ [m] do                                             ▷ or j = 0..m in the symmetric case
L4      c ← |A_J|, the number of objects with at least the bad properties in J   ▷ hole: count an intersection
L5      total ← total + (−1)^|J| · c
L6  return total
```

Line L4 is the work: each intersection must be counted by a direct formula, usually by fixing the bad properties and counting the free part with the [rule of product](/rule-of-product/) or [stars and bars](/stars-and-bars/). The loop has $2^m$ iterations; in the symmetric case, $m + 1$ with the factor $\binom{m}{j}$.

**Cost model.** The terms alternate in sign and can be much larger than the answer, so with exact integers the partial sums need as many bits as the largest term. Modulo a prime $p$, keep each residue in $\{0, \ldots, p - 1\}$ and add $p$ after a subtraction. Each term is computed independently, so the method needs only the space of one term, which is its advantage over a dynamic program with $2^m$ table entries.

## Classic examples

**1. Divisibility.** The integers in $[100]$ divisible by none of 2, 3, 5: with $A_p$ the multiples of $p$, $|A_J| = \lfloor 100 / \prod_{p \in J} p \rfloor$, and the count is $100 - (50 + 33 + 20) + (16 + 10 + 6) - 3 = 26$.

**2. Euler's totient.** For $n$ with distinct prime factors $p_1, \ldots, p_r$, the integers in $[n]$ coprime to $n$ number $\sum_{J} (-1)^{|J|} n / \prod_{j \in J} p_j = n \prod_i (1 - 1/p_i)$. For $n = 60$: $60 \cdot \tfrac12 \cdot \tfrac23 \cdot \tfrac45 = 16$. See [Euler's totient function](/euler-totient/).

**3. Derangements.** Let $A_i$ be the permutations of $[n]$ that fix $i$. Fixing a set $J$ of $j$ points leaves $(n - j)!$ permutations, so the symmetric form gives $D_n = \sum_{j=0}^{n} (-1)^j \binom{n}{j}(n - j)! = n!\sum_{j=0}^{n} (-1)^j/j!$; for $n = 4$, $24 - 24 + 12 - 4 + 1 = 9$. See [derangement](/derangement/).

**4. Surjections.** The functions from $[n]$ onto $[k]$: let $A_i$ be the functions that miss $i$. Then $|A_J| = (k - j)^n$, and the count is $\sum_{j=0}^{k} (-1)^j \binom{k}{j}(k - j)^n = k!\,S(n, k)$, with $S$ the [Stirling numbers of the second kind](/stirling-numbers-second-kind/). For $n = 5$, $k = 3$: $243 - 96 + 3 = 150$.

**5. Upper bounds.** The solutions of $x_1 + \cdots + x_k = n$ with $0 \le x_i \le u_i$: let $A_i$ be the solutions with $x_i \ge u_i + 1$; each $|A_J|$ is a stars and bars count. See [bounded integer solutions](/bounded-integer-solutions-counting/).

**6. Legendre's sieve.** The integers in $[x]$ with no prime factor $\le \sqrt{x}$ are $1$ and the primes in $(\sqrt x, x]$. For $x = 100$ and the primes $2, 3, 5, 7$, inclusion-exclusion over the $16$ products gives $22 = 1 + (25 - 4)$, so $\pi(100) = 25$. See [Legendre's phi function](/legendre-phi-function/).

**7. Exact exponential algorithms.** The permanent of an $n \times n$ matrix is $\sum_{J \subseteq [n]} (-1)^{n - |J|} \prod_{i} \sum_{j \in J} a_{ij}$, which is [Ryser's formula](/ryser-formula/), with $2^n$ terms instead of $n!$. The number of Hamiltonian cycles of a graph is a signed sum over vertex subsets $J$ of the number of closed walks of length $n$ inside $J$, each found by a matrix power, in $O^*(2^n)$ time and polynomial space (Fomin and Kratsch, Chapter 4). Björklund, Husfeldt and Koivisto (2009) count the covers of $[n]$ by $k$ sets of a family the same way and find the chromatic number in $O^*(2^n)$ time.

## Variations

- **Bonferroni inequalities.** Truncating the union formula after an odd number of levels gives an upper bound, and after an even number a lower bound. In example 1, the union of the multiples of 2, 3, 5 has $74$ elements; one level gives $103 \ge 74$, two levels give $71 \le 74$. The first level is the [union bound](/union-bound/).
- **Exactly $k$ properties.** With $S_j = \sum_{|J| = j} |A_J|$, the number of elements in exactly $k$ of the sets is $\sum_{j \ge k} (-1)^{j-k}\binom{j}{k} S_j$.
- **Möbius inversion on a poset.** Inclusion-exclusion is Möbius inversion on the Boolean lattice, whose Möbius function is $(-1)^{|T| - |S|}$. On the divisor lattice it becomes the number-theoretic [Möbius inversion](/mobius-inversion/), as in [counting coprime pairs](/counting-coprime-pairs/).
- **Fast transforms.** When all $2^m$ values $f(S)$ are needed, the [sum over subsets DP](/sum-over-subsets-dp/) computes the whole transform in $O(2^m m)$ operations instead of $O(3^m)$.
- **Probability.** With probabilities instead of sizes, $\Pr[\bigcup E_i] = \sum_{J \ne \emptyset} (-1)^{|J|-1} \Pr[\bigcap_{j \in J} E_j]$, by the same proof with weights.
- **Sign-reversing involutions.** A [bijective proof](/bijective-proof/) of an alternating sum pairs the terms of opposite sign and leaves the elements that are counted once.

## Pitfalls

- **Intersections of divisibility.** The multiples of both $a$ and $b$ are the multiples of $\mathrm{lcm}(a, b)$, not of $ab$. The integers in $[100]$ divisible by 4 or 6 are $25 + 16 - 8 = 33$, while dividing by $24$ gives the wrong $37$.
- **The empty set.** In the complement form the term for $J = \emptyset$ is $|U|$. Forgetting it gives the negative of the union.
- **Signs.** The sign of the term for $J$ is $(-1)^{|J|}$ in the complement form and $(-1)^{|J|-1}$ in the union form. Mixing them gives a wrong answer of the right size.
- **"At least" versus "exactly".** Line L4 must count the objects with *at least* the properties in $J$, not exactly those. Counting "exactly" makes the sum meaningless.
- **Exponential terms.** Without symmetry or structure, $2^m$ terms make the method useless beyond $m \approx 40$. Check whether only a few $J$ give a nonzero term, as with the squarefree divisors in example 6.
- **Modular subtraction.** In C-like languages, `(a - b) % p` can be negative. Add $p$ first.

## Exercises

1. How many permutations of $[6]$ have no $i$ followed directly by $i + 1$? (Let $A_i$ be the permutations where $i + 1$ follows $i$, and glue $i$ and $i + 1$ together.)
2. Count the strings of length 8 over $\{a, b, c\}$ that use each letter at least once, and check the result against example 4.
3. Prove the Bonferroni inequalities from the identity $\sum_{j=0}^{s} (-1)^j\binom{t}{j} = (-1)^s\binom{t-1}{s}$ for $t \ge 1$.

## References

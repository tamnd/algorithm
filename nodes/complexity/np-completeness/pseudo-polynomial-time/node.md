---
tag: GA9ZR6
kind: definition
slug: pseudo-polynomial-time
name: Pseudo-polynomial time
aliases:
- pseudopolynomial time
area: complexity/np-completeness
level: intro
summary: Running time bounded by a polynomial in the input length and in the largest number of the input, which is polynomial in the unary length but can be exponential in the binary length.
prereqs: [input-size, polynomial-time, unary-encoding]
see_also: [strong-np-hardness, weak-np-hardness, subset-sum-problem, knapsack-dynamic-programming, fptas, rounding-and-scaling, papadimitriou-pseudopolynomial-theorem, no-fptas-for-strongly-np-hard-problems]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 4.2, Number Problems and Pseudo-polynomial Time Algorithms (the functions Length and Max, number problems, and the definition)
  - paper: doi:10.1145/322077.322090
    title: M. R. Garey and D. S. Johnson, "Strong" NP-completeness results, motivation, examples, and implications, Journal of the ACM 25(3), 499 to 508 (1978)
    locator: the definitions of pseudo-polynomial algorithms and of strong NP-completeness
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 6.4, Subset Sums and Knapsacks (the running time O(nW) and why it is pseudo-polynomial)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 34.1 (encodings, and why unary input changes the running time) and Section 34.5.5
---

An algorithm runs in pseudo-polynomial time when its running time is bounded by a polynomial in two quantities: the length of the input and the largest number that appears in it. A number $N$ takes only about $\log_2 N$ bits in binary, so such an algorithm can still be exponential in the [input size](/input-size/). It is polynomial in the length of the input when the numbers are written in [unary](/unary-encoding/). The standard example is the $O(nt)$ dynamic program for the [subset sum problem](/subset-sum-problem/). Garey and Johnson introduced the term to separate NP-hard number problems that have such algorithms, the [weakly NP-hard](/weak-np-hardness/) problems, from those that do not unless P = NP, the [strongly NP-hard](/strong-np-hardness/) problems.

## Definition

**Length and Max.** Fix a decision problem $\Pi$ and a reasonable encoding of its instances, with numbers in binary. For an instance $I$, let $\mathrm{Length}(I)$ be the number of symbols of its encoding, and let $\mathrm{Max}(I)$ be the magnitude of the largest integer in $I$ (0 if there is none). These are the two functions of Garey and Johnson (Section 4.2).

**Definition.** An algorithm for $\Pi$ runs in *pseudo-polynomial time* if there is a polynomial $p$ such that, on each instance $I$, it takes at most $p(\mathrm{Length}(I), \mathrm{Max}(I))$ steps.

**Number problems.** $\Pi$ is a *number problem* if no polynomial $q$ satisfies $\mathrm{Max}(I) \le q(\mathrm{Length}(I))$ for all instances $I$. Subset sum, partition and knapsack are number problems. Clique is not, because its only number $k$ is at most the number of vertices. For a problem that is not a number problem, pseudo-polynomial time is the same as [polynomial time](/polynomial-time/), because $\mathrm{Max}(I)$ can be replaced by $q(\mathrm{Length}(I))$.

**Equivalent form with unary length.** Let $U(I)$ be the length of the encoding of $I$ with every number written in unary. Then pseudo-polynomial time in the sense above is the same as time polynomial in $U(I)$. Proof: a number $N$ takes at least as many symbols in unary as in binary, up to a constant factor, so $\mathrm{Length}(I) = O(U(I))$; the largest number alone takes $\mathrm{Max}(I)$ symbols in unary, so $\mathrm{Max}(I) \le U(I)$. Thus a bound polynomial in $\mathrm{Length}$ and $\mathrm{Max}$ is polynomial in $U$. In the other direction, each of the at most $\mathrm{Length}(I)$ numbers takes at most $\mathrm{Max}(I) + 1$ symbols in unary, so $U(I) = O(\mathrm{Length}(I) \cdot (\mathrm{Max}(I) + 1))$, and a bound polynomial in $U$ is polynomial in $\mathrm{Length}$ and $\mathrm{Max}$.

**Model.** The definition counts steps of a [Turing machine](/turing-machine/), or of a [RAM](/random-access-machine/) with the [logarithmic cost model](/logarithmic-cost-model/). These models are polynomially related, so the class of pseudo-polynomial algorithms does not depend on the choice. On a [word RAM](/word-ram/) with words of $\Theta(\log U)$ bits, bounds such as $O(nt)$ hold as stated.

## Examples and non-examples

**Subset sum.** The dynamic program for $n$ numbers and target $t$ fills a table of $(n + 1)(t + 1)$ cells, so it takes $O(nt)$ time. This is pseudo-polynomial, since $t \le \mathrm{Max}(I)$ and $n \le \mathrm{Length}(I)$. For $n = 50$ numbers of $b$ bits and a target of $b$ bits, the input is about $51 b$ bits long, and the table has about $51 \cdot 2^b$ cells:

| bits $b$ | input length (bits) | cells $51 \cdot 2^b$ |
|---|---|---|
| 10 | 510 | 52,224 |
| 20 | 1,020 | 53,477,376 |
| 32 | 1,632 | 219,043,332,096 |
| 64 | 3,264 | about $9.4 \times 10^{20}$ |

The input length grows linearly in $b$, and the table grows exponentially.

**Knapsack.** The dynamic program over capacities takes $O(nW)$ time for capacity $W$; see the [knapsack problem](/knapsack-problem/). This is pseudo-polynomial. The dynamic program over values takes $O(nV)$ time for total value $V$, which is also pseudo-polynomial; [rounding and scaling](/rounding-and-scaling/) of the values turns it into an [FPTAS](/fptas/).

**Trial division.** Testing whether $N$ is prime by trying all divisors up to $\sqrt{N}$ takes about $\sqrt{N}$ divisions. This is pseudo-polynomial and exponential in the bit length $\log_2 N$. Polynomial-time primality tests exist, so this is an example of a slow algorithm, not of a hard problem.

**Coin change.** Counting the ways to pay an amount $N$ with given coins takes $O(kN)$ steps for $k$ coin values; see [coin change](/coin-change-problem/).

**Non-example: exhaustive search.** Trying all $2^n$ subsets for subset sum is not pseudo-polynomial. It is exponential in $n$ even when all numbers are 1, and then $\mathrm{Length}$ and $\mathrm{Max}$ are both small.

**Non-example: Euclid's algorithm.** The [Euclidean algorithm](/euclidean-algorithm/) for $\gcd(a, b)$ takes $O(\log \min(a, b))$ division steps. This is polynomial in the bit length, which is a stronger property. Each polynomial-time algorithm is also pseudo-polynomial.

**Non-example in the other direction.** An algorithm in time $O(2^{\sqrt{\mathrm{Max}}})$ is not pseudo-polynomial, and neither is one in time $O(\mathrm{Max}^{\log \mathrm{Max}})$.

## Related definitions

- **Weakly polynomial and strongly polynomial.** For problems with numbers, a *weakly polynomial* algorithm is polynomial in the bit length of the input, as the [ellipsoid method](/ellipsoid-method/) is for linear programming. A *strongly polynomial* algorithm uses a number of arithmetic operations that is polynomial in the number of input numbers alone. Pseudo-polynomial is weaker than both, because it allows time polynomial in the values.
- **Strong and weak NP-hardness.** A problem that stays NP-hard when $\mathrm{Max}(I)$ is bounded by a polynomial in $\mathrm{Length}(I)$ is [strongly NP-hard](/strong-np-hardness/), and it has no pseudo-polynomial algorithm unless P = NP. An NP-hard problem with a pseudo-polynomial algorithm is [weakly NP-hard](/weak-np-hardness/).
- **FPTAS.** For optimization problems whose optimum is an integer bounded by a polynomial in $\mathrm{Length}$ and $\mathrm{Max}$, an [FPTAS](/fptas/) gives an exact pseudo-polynomial algorithm, by taking $\varepsilon$ smaller than one over that bound. So strongly NP-hard problems of this kind have no FPTAS unless P = NP; see [no FPTAS for strongly NP-hard problems](/no-fptas-for-strongly-np-hard-problems/).
- **Integer programs with few constraints.** Integer programs with a fixed number of constraints have pseudo-polynomial algorithms; see [Papadimitriou's pseudo-polynomial theorem](/papadimitriou-pseudopolynomial-theorem/).
- **Unary encoding.** Writing the numbers in [unary](/unary-encoding/) turns each pseudo-polynomial algorithm into a polynomial-time algorithm, by the equivalence above.

## References

---
tag: H2ZCYX
kind: concept
slug: block-sensitivity
name: Block sensitivity
aliases:
- bs(f)
area: complexity/communication-and-query-complexity
level: advanced
summary: "bs(f) is the largest number of disjoint blocks of bits at one input whose flips each change f. It is polynomially related to D^dt, R, Q and degree, and by Huang's theorem to s(f)."
prereqs: [sensitivity, certificate-complexity]
see_also: [sensitivity, sensitivity-theorem, certificate-complexity, randomized-query-complexity, decision-tree-complexity, polynomial-method, approximate-degree, query-complexity]
sources:
  - paper: doi:10.1137/0220062
    title: Noam Nisan, CREW PRAMs and decision trees, SIAM Journal on Computing 20(6) (1991)
    locator: pp. 999 to 1007 (definition of block sensitivity, C(f) at most s(f) bs(f), bs(f) at most 3 R(f))
  - paper: doi:10.1007/BF01263419
    title: Noam Nisan and Mario Szegedy, On the degree of Boolean functions as real polynomials, Computational Complexity 4(4) (1994)
    locator: pp. 301 to 313 (bs(f) at most 2 deg(f)^2 and bs(f) at most 6 times the square of the approximate degree)
  - paper: doi:10.1016/S0304-3975(01)00144-X
    title: Harry Buhrman and Ronald de Wolf, Complexity measures and decision tree complexity, a survey, Theoretical Computer Science 288(1) (2002)
    locator: pp. 21 to 43; Section 4.2 (sensitivity and block sensitivity), Section 5.1 (D(f) at most C_1(f) bs(f)), Section 5.2 (bs(f) at most 3 R(f))
  - paper: doi:10.1145/502090.502097
    title: Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca and Ronald de Wolf, Quantum lower bounds by polynomials, Journal of the ACM 48(4) (2001)
    locator: pp. 778 to 797 (D(f) at most C_1(f) bs(f); bs(f) and the quantum query complexity)
  - paper: doi:10.1007/BF01200762
    title: David Rubinstein, Sensitivity vs. block sensitivity of Boolean functions, Combinatorica 15(2) (1995)
    locator: pp. 297 to 299 (a function with bs(f) = s(f)^2 / 2)
  - paper: doi:10.4007/annals.2019.190.3.6
    title: Hao Huang, Induced subgraphs of hypercubes and a proof of the sensitivity conjecture, Annals of Mathematics 190(3) (2019)
    locator: pp. 949 to 955; Theorem 1.5 in arXiv:1907.00847 version 2 (bs(f) at most s(f)^4)
---

Block sensitivity counts how many disjoint groups of bits of one input can each change the value of a Boolean function. It extends [sensitivity](/sensitivity/), which allows only single bits, and it was introduced by Nisan in 1989 to bound the time of parallel machines. Block sensitivity is the measure that ties the others together: $D^{dt}$, $R$, $Q$, $C$, $\deg$ and the approximate degree are all bounded by polynomials in $\mathrm{bs}(f)$ and bound it in turn. The [sensitivity theorem](/sensitivity-theorem/) page proves that sensitivity joins this group too; this page defines block sensitivity and proves its links with the other measures.

## In plain words

Take a yes or no rule about a row of bits, and one row. Choose a group of bits and flip all of them at once. If the answer changes, the group is sensitive. Now try to find as many sensitive groups as you can with no bit in two groups. The largest number you can find, on the hardest row, is the block sensitivity. Single bits are allowed groups, so this number is at least the plain sensitivity, which only flips one bit at a time. It is useful because any method that finds the answer must look at least once inside each sensitive group. Otherwise it cannot tell the row from the row with that group flipped.

## The idea

**Definitions.** Let $f : \{0,1\}^n \to \{0,1\}$ be total. For $B \subseteq \{1, \ldots, n\}$, let $x^B$ be $x$ with all bits in $B$ flipped. A **sensitive block** of $x$ is a set $B$ with $f(x^B) \ne f(x)$. Then

- $\mathrm{bs}(f, x)$ is the largest $k$ such that there are pairwise disjoint sensitive blocks $B_1, \ldots, B_k$ of $x$,
- $\mathrm{bs}_b(f)$ is the largest $\mathrm{bs}(f, x)$ over inputs with $f(x) = b$, and $\mathrm{bs}(f) = \max(\mathrm{bs}_0(f), \mathrm{bs}_1(f))$.

We can restrict the search to **minimal** sensitive blocks, those with no sensitive proper subset, because any sensitive block contains a minimal one. Nisan's lemma (proved on the [certificate complexity](/certificate-complexity/) page) says that a minimal sensitive block has at most $\mathrm{s}(f)$ elements.

**Why every algorithm must look inside each block.** Let $B_1, \ldots, B_k$ be disjoint sensitive blocks of $x$. An algorithm that never queries a bit of $B_j$ on input $x$ makes the same queries and gets the same answers on $x^{B_j}$, so it gives the same output, and it is wrong on one of the two. A deterministic algorithm must therefore query a bit in each block, and $\mathrm{bs}(f) \le D^{dt}(f)$. The randomized version of this argument gives $\mathrm{bs}(f) \le 3 R(f)$; it is on the [randomized query complexity](/randomized-query-complexity/) page.

**The relations.** For every total $f$:

| relation | proof |
|---|---|
| $\mathrm{s}(f) \le \mathrm{bs}(f) \le C(f)$ | [query complexity](/query-complexity/) |
| $C(f) \le \mathrm{s}(f) \, \mathrm{bs}(f) \le \mathrm{bs}(f)^2$ | [certificate complexity](/certificate-complexity/) (Nisan) |
| $D^{dt}(f) \le C_1(f) \, \mathrm{bs}(f) \le \mathrm{bs}(f)^3$ | [decision tree complexity](/decision-tree-complexity/) (Beals et al.) |
| $\mathrm{bs}(f) \le 3 R(f)$ | [randomized query complexity](/randomized-query-complexity/) (Nisan) |
| $\mathrm{bs}(f) \le 2 \deg(f)^2$ and $\mathrm{bs}(f) \le 6 \, \widetilde{\deg}(f)^2$ | below (Nisan and Szegedy) |
| $\mathrm{bs}(f) \le \mathrm{s}(f)^4$ | [sensitivity theorem](/sensitivity-theorem/) (Huang, with Tal) |

So $D^{dt}$, $R$, $C$ and $\mathrm{bs}$ are polynomially related: $\mathrm{bs}(f) \le 3 R(f) \le 3 D^{dt}(f) \le 3 \, \mathrm{bs}(f)^3$.

**Theorem (Nisan and Szegedy).** $\mathrm{bs}(f) \le 2 \deg(f)^2$.

*Proof outline.* Take $x$ with $b = \mathrm{bs}(f)$ disjoint sensitive blocks $B_1, \ldots, B_b$, and assume $f(x) = 0$ (else use $1 - f$, which has the same degree). Define $g$ on $b$ new bits by $g(y) = f(x^{B(y)})$, where $B(y)$ is the union of the blocks $B_j$ with $y_j = 1$. Each $x_i$ becomes a constant, $y_j$ or $1 - y_j$, so $\deg(g) \le \deg(f)$. Now $g(0) = 0$ and $g(y) = 1$ when $y$ has one 1. Average $g$ over all $y$ with $|y| = k$: by symmetrization (Minsky and Papert) the result is a polynomial $q(k)$ of one variable with $\deg(q) \le \deg(g)$. It has $q(0) = 0$, $q(1) = 1$ and $0 \le q(k) \le 1$ for the integers $k = 0, \ldots, b$. So $q$ is bounded on $b + 1$ points but has slope at least 1 somewhere in $[0, 1]$. A lemma of Ehlich and Zeller and of Rivlin and Cheney, proved from Markov's inequality for derivatives, says that such a polynomial has degree at least $\sqrt{b/2}$. So $\deg(f) \ge \sqrt{b/2}$. The full proof, with the lemma, is on the [polynomial method](/polynomial-method/) page. With an approximating polynomial instead of an exact one, the same steps give $q(0) \le 1/3$, $q(1) \ge 2/3$ and $-1/3 \le q(k) \le 4/3$, and the lemma gives $\mathrm{bs}(f) \le 6 \, \widetilde{\deg}(f)^2$. $\square$

**Computing it.** $\mathrm{bs}(f, x)$ is a maximum packing of the minimal sensitive blocks, a set packing problem. For small $n$, a search over all packings is fast; the values below come from such a search.

## Examples

| function | $n$ | $\mathrm{s}$ | $\mathrm{bs}_0$ | $\mathrm{bs}_1$ | $\mathrm{bs}$ | $C$ |
|---|---|---|---|---|---|---|
| OR | 5 | 5 | 5 | 1 | 5 | 5 |
| PARITY | 5 | 5 | 5 | 5 | 5 | 5 |
| MAJORITY | 7 | 4 | 4 | 4 | 4 | 4 |
| OR of 3 ANDs of 3 bits | 9 | 3 | 3 | 3 | 3 | 3 |
| $|x| \in \{1, 2\}$ | 3 | 3 | 3 | 2 | 3 | 3 |

**OR.** At $x = 0$, each single bit is a sensitive block, so $\mathrm{bs}_0 = n$. At a 1-input, a sensitive block must contain every 1 of the input, so two such blocks cannot be disjoint, and $\mathrm{bs}_1 = 1$.

**The function $|x| \in \{1, 2\}$ on three bits.** At $x = 100$, the blocks $\{1\}$ (giving $000$) and $\{2, 3\}$ (giving $111$) are disjoint and sensitive, so $\mathrm{bs}_1 = 2$, while the sensitivity at a 1-input is only 1.

**Small functions.** A full search over all Boolean functions on at most 3 bits finds $\mathrm{s}(f) = \mathrm{bs}(f) = C(f)$ in every case. On 4 bits, 24 of the 65,536 functions have $\mathrm{s}(f) = 2$ and $\mathrm{bs}(f) = 3$, and none has $\mathrm{bs}(f) < C(f)$. Gaps need more bits.

**Rubinstein's function.** Let $n = k^2$ with $k$ even, in $k$ blocks of $k$ bits, and let $f(x) = 1$ when some block has exactly two ones, at positions $2j - 1$ and $2j$ for some $j$. At $x = 0$, the $k^2/2$ pairs $\{2j - 1, 2j\}$ are disjoint sensitive blocks, so $\mathrm{bs}(f) \ge k^2/2$, while $\mathrm{s}(f) = k$ (see [sensitivity](/sensitivity/)). Rubinstein proved $\mathrm{bs}(f) = \mathrm{s}(f)^2 / 2$. For $k = 4$ this is $\mathrm{s} = 4$ against $\mathrm{bs} = 8$. The gap between $\mathrm{s}^2$ and the upper bound $\mathrm{s}^4$ is still open.

**Monotone functions.** If $f$ is monotone, then $\mathrm{s}(f) = \mathrm{bs}(f) = C(f)$; see [certificate complexity](/certificate-complexity/).

## Where it is used

- **Lower bounds on randomized algorithms.** $R(f) \ge \mathrm{bs}(f)/3$ gives $R(\mathrm{OR}) \ge n/3$ at once, and with $D^{dt} \le \mathrm{bs}^3$ it gives $D^{dt}(f) \le 27 R(f)^3$ for total $f$; see [randomized query complexity](/randomized-query-complexity/).
- **Quantum lower bounds.** Every quantum algorithm needs $\Omega(\sqrt{\mathrm{bs}(f)})$ queries, because $\mathrm{bs}(f) \le 6 \, \widetilde{\deg}(f)^2$ and $\widetilde{\deg}(f) \le 2 Q(f)$; see the [polynomial method](/polynomial-method/). For OR this is the $\Omega(\sqrt n)$ bound behind [Grover optimality](/grover-optimality/).
- **Parallel computation.** Nisan defined block sensitivity to give tight bounds on the time that a CREW PRAM needs to compute $f$; this was the reason for the definition.
- **The sensitivity theorem.** The question of Nisan and Szegedy was whether $\mathrm{bs}$ is bounded by a polynomial in $\mathrm{s}$; Huang's theorem answers it with $\mathrm{bs} \le \mathrm{s}^4$.

## References

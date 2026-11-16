---
tag: PR6G6T
kind: concept
slug: query-complexity
name: Query complexity
aliases: []
area: complexity/communication-and-query-complexity
level: intro
summary: "How many input bits an algorithm must read to compute a Boolean function, for deterministic, randomized and quantum algorithms, and how these costs relate to s, bs, C and degree."
prereqs: [query-model]
see_also: [decision-tree-complexity, randomized-query-complexity, quantum-query-complexity, certificate-complexity, sensitivity, block-sensitivity, approximate-degree, polynomial-method]
sources:
  - paper: doi:10.1016/S0304-3975(01)00144-X
    title: Harry Buhrman and Ronald de Wolf, Complexity measures and decision tree complexity, a survey, Theoretical Computer Science 288(1) (2002)
    locator: pp. 21 to 43; Section 4 (certificate complexity, sensitivity, block sensitivity, degree, approximate degree) and Section 5 (relations with D, R and Q)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 12, Decision trees
  - paper: doi:10.1137/0220062
    title: Noam Nisan, CREW PRAMs and decision trees, SIAM Journal on Computing 20(6) (1991)
    locator: pp. 999 to 1007 (block sensitivity, C(f) at most s(f) bs(f), bs(f) at most 3 R(f))
  - paper: doi:10.1007/BF01263419
    title: Noam Nisan and Mario Szegedy, On the degree of Boolean functions as real polynomials, Computational Complexity 4(4) (1994)
    locator: pp. 301 to 313 (bs(f) at most 2 deg(f)^2, bs(f) at most 6 times the square of the approximate degree, the example with deg 2 and s 3)
  - paper: doi:10.1145/502090.502097
    title: Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca and Ronald de Wolf, Quantum lower bounds by polynomials, Journal of the ACM 48(4) (2001)
    locator: pp. 778 to 797 (Q(f) at least half the approximate degree, D(f) = O(Q(f)^6) for total f)
  - paper: doi:10.4007/annals.2019.190.3.6
    title: Hao Huang, Induced subgraphs of hypercubes and a proof of the sensitivity conjecture, Annals of Mathematics 190(3) (2019)
    locator: pp. 949 to 955 (s(f) at least the square root of deg(f))
  - paper: doi:10.1145/3406325.3451047
    title: Scott Aaronson, Shalev Ben-David, Robin Kothari, Shravas Rao and Avishay Tal, Degree vs. approximate degree and quantum implications of Huang's sensitivity theorem, 53rd ACM Symposium on Theory of Computing (STOC 2021)
    locator: pp. 1330 to 1342 (D(f) = O(Q(f)^4) and deg(f) = O(adeg(f)^2) for total f)
  - paper: doi:10.1007/BF01200762
    title: David Rubinstein, Sensitivity vs. block sensitivity of Boolean functions, Combinatorica 15(2) (1995)
    locator: pp. 297 to 299 (a function with bs(f) = s(f)^2 / 2)
---

Query complexity is the study of how many bits of its input an algorithm must read to compute a function. The setting is the [query model](/query-model/): the input $x \in \{0,1\}^n$ sits in a black box, each read of one bit costs one unit, and all other work is free. For each kind of algorithm (deterministic, randomized, quantum) there is one measure, and next to these there are combinatorial and algebraic measures of the function itself. This page is the overview of the whole family and of how its members relate. The query model page defines the machine, and the [decision tree complexity](/decision-tree-complexity/) page defines and studies the deterministic measure $D^{dt}(f)$ in detail.

## In plain words

Think of a row of hidden cards, each showing 0 or 1. You may turn over one card at a time, and each turn costs one coin. Thinking is free. Query complexity asks how many coins you must pay, in the worst case, to be sure of some fact about the row. Some facts need every card: to know whether the number of ones is odd, you must see all of them. Other facts need few. The answer also depends on the player. A careful player must always be right. A player who flips coins may be wrong with a small chance. A quantum player may look at many places at once in a special way. The field compares these costs with simple counts, such as how many single cards can change the answer. For a fact about every possible row, all these costs are close.

## The idea

Fix a Boolean function $f : \{0,1\}^n \to \{0,1\}$. It is **total** unless we say that it is **partial**. For a set $S \subseteq \{1, \ldots, n\}$, write $x^S$ for the input $x$ with the bits in $S$ flipped, and write $x^i$ for $x^{\{i\}}$.

**The computational measures.** Each one is the least worst-case number of queries of an algorithm of one kind that computes $f$.

- $D^{dt}(f)$: deterministic algorithms, always correct. This is the depth of the shallowest decision tree for $f$; see [decision tree complexity](/decision-tree-complexity/).
- $R_0(f)$: randomized algorithms that are always correct, measured by the expected number of queries on the worst input.
- $R(f)$: randomized algorithms that are correct with probability at least $2/3$ on every input (two-sided bounded error); see [randomized query complexity](/randomized-query-complexity/).
- $Q_E(f)$ and $Q(f)$: quantum algorithms, exact or with error at most $1/3$; see [quantum query complexity](/quantum-query-complexity/).

**The combinatorial measures.** These depend only on the table of $f$.

- The **sensitivity** $\mathrm{s}(f, x)$ is the number of indices $i$ with $f(x^i) \ne f(x)$, and $\mathrm{s}(f) = \max_x \mathrm{s}(f, x)$. See [sensitivity](/sensitivity/).
- The **block sensitivity** $\mathrm{bs}(f, x)$ is the largest number of pairwise disjoint sets $B_1, \ldots, B_k$ with $f(x^{B_j}) \ne f(x)$ for each $j$, and $\mathrm{bs}(f) = \max_x \mathrm{bs}(f, x)$. See [block sensitivity](/block-sensitivity/).
- The **certificate complexity** $C(f, x)$ is the size of the smallest set $S$ such that every $y$ that agrees with $x$ on $S$ has $f(y) = f(x)$, and $C(f) = \max_x C(f, x)$. We write $C_0(f)$ and $C_1(f)$ for the maximum over the 0-inputs and over the 1-inputs. See [certificate complexity](/certificate-complexity/).

**The algebraic measures.** Every $f$ has exactly one multilinear real polynomial $p$ with $p(x) = f(x)$ on all of $\{0,1\}^n$. Its coefficients are $c_S = \sum_{T \subseteq S} (-1)^{|S| - |T|} f(1_T)$, where $1_T$ is the input with ones exactly on $T$. The **degree** $\deg(f)$ is the degree of this polynomial. The **approximate degree** $\widetilde{\deg}(f)$ is the least degree of a real polynomial $p$ with $|p(x) - f(x)| \le 1/3$ for all $x \in \{0,1\}^n$. See [approximate degree](/approximate-degree/).

**The easy relations.** Four inequalities follow from the definitions.

- $\mathrm{s}(f) \le \mathrm{bs}(f)$, because single indices are disjoint blocks.
- $\mathrm{bs}(f) \le C(f)$. Let $S$ be a certificate for $x$ and let $B$ be a sensitive block. If $B$ misses $S$, then $x^B$ agrees with $x$ on $S$, so $f(x^B) = f(x)$, a contradiction. So each of the disjoint sensitive blocks meets $S$, and there are at most $|S|$ of them.
- $C(f) \le D^{dt}(f)$, because the indices queried on the path of $x$ in a decision tree form a certificate for $x$.
- $\deg(f) \le D^{dt}(f)$. For a leaf $\ell$ of a decision tree, let $P_\ell(x)$ be the product of $x_i$ over the edges "$x_i = 1$" and of $1 - x_i$ over the edges "$x_i = 0$" on its path. Then $P_\ell(x) = 1$ when $x$ reaches $\ell$ and 0 otherwise, so $f = \sum_\ell (\text{label of } \ell) \, P_\ell$, a polynomial of degree at most the depth.

In the same way, $Q(f) \le R(f) \le 3 R_0(f)$ and $R_0(f) \le D^{dt}(f)$, and $\widetilde{\deg}(f) \le \deg(f)$. For $R \le 3 R_0$: stop a zero-error algorithm after $3 R_0(f)$ queries and output 0; by [Markov's inequality](/markov-inequality/) it is stopped with probability at most $1/3$.

**The deep relations.** For total functions, all of these measures are polynomially related, except that sensitivity was a missing link until 2019. These are the main bounds.

| bound | source |
|---|---|
| $C(f) \le \mathrm{s}(f) \, \mathrm{bs}(f)$ | Nisan 1991 |
| $D^{dt}(f) \le C_0(f) \, C_1(f)$ | Blum and Impagliazzo; Hartmanis and Hemachandra; Tardos |
| $D^{dt}(f) \le C_1(f) \, \mathrm{bs}(f)$, so $D^{dt}(f) \le \mathrm{bs}(f)^3$ | Beals et al. 2001, with Nisan 1991 |
| $\mathrm{bs}(f) \le 3 R(f)$, so $D^{dt}(f) \le 27 R(f)^3$ | Nisan 1991 |
| $\mathrm{bs}(f) \le 2 \deg(f)^2$ and $\mathrm{bs}(f) \le 6 \, \widetilde{\deg}(f)^2$ | Nisan and Szegedy 1994 |
| $\widetilde{\deg}(f) \le 2 Q(f)$ and $\deg(f) \le 2 Q_E(f)$ | Beals et al. 2001 |
| $\mathrm{s}(f) \ge \sqrt{\deg(f)}$, so $\mathrm{bs}(f) \le 2 \mathrm{s}(f)^4$ | Huang 2019 |
| $D^{dt}(f) = O(Q(f)^4)$ and $\deg(f) = O(\widetilde{\deg}(f)^2)$ | Aaronson, Ben-David, Kothari, Rao and Tal 2021 |

The proofs are on the pages of the single measures. The [sensitivity theorem](/sensitivity-theorem/) page has Huang's proof.

**Partial functions.** None of the deep relations holds for partial functions in general. With a promise, the gaps can be exponential. For example, the promise problem of [Simon's algorithm](/simon-algorithm/) has an exponential gap between its quantum and its randomized query complexity. A page that states a polynomial relation must say that $f$ is total.

**The error convention.** The value $1/3$ is not important. Repeat a bounded-error algorithm $k$ times and output the majority answer, and the error falls exponentially in $k$. So any error below $1/2$ by a constant gives $R(f)$ and $Q(f)$ up to a constant factor. The approximate degree changes by at most a constant factor in the same way.

## Examples

The table gives exact values for some small functions. Each value was computed by brute force over all inputs, with the deterministic depth computed by a full search over decision trees.

| function | $n$ | $\mathrm{s}$ | $\mathrm{bs}$ | $C$ | $D^{dt}$ | $\deg$ |
|---|---|---|---|---|---|---|
| OR | 5 | 5 | 5 | 5 | 5 | 5 |
| PARITY | 5 | 5 | 5 | 5 | 5 | 5 |
| MAJORITY | 7 | 4 | 4 | 4 | 7 | 7 |
| OR of 3 ANDs of 3 bits | 9 | 3 | 3 | 3 | 9 | 9 |
| address function, 2 address bits | 6 | 3 | 3 | 3 | 3 | 3 |
| $|x| \in \{1, 2\}$ | 3 | 3 | 3 | 3 | 3 | 2 |

Some points to see in the table:

- For OR, $C_1 = 1$ (one bit that is 1 proves the value 1) but $C_0 = n$. So the measures for 0-inputs and 1-inputs can differ a lot.
- For the OR of $k$ ANDs of $k$ bits, $\mathrm{s} = \mathrm{bs} = C = k$ and $D^{dt} = \deg = k^2$. This shows that $D^{dt} \le C_0 C_1$ is tight, and that $\deg$ can be the square of $\mathrm{s}$, so Huang's bound $\mathrm{s} \ge \sqrt{\deg}$ is tight.
- The address function reads $k$ address bits and returns the data bit at that address, out of $2^k$ data bits. With $k = 2$ it has $n = 6$ and every measure equals 3. Its degree is $k + 1$ while $n = k + 2^k$, so a function that depends on all $n$ bits can have degree of order $\log n$.
- The last function is 1 when exactly one or two of three bits are 1. Its polynomial is $x_1 + x_2 + x_3 - x_1 x_2 - x_1 x_3 - x_2 x_3$, of degree 2, but its sensitivity at $000$ is 3. So $\deg(f) < \mathrm{s}(f)$ is possible.

Rubinstein's function separates $\mathrm{s}$ and $\mathrm{bs}$. Take $n = k^2$ with $k$ even, in $k$ blocks of $k$ bits. A block is good if it has exactly two ones, at positions $2j - 1$ and $2j$ for some $j$. The function is 1 when some block is good. At the all-zero input, the $k^2/2$ pairs of positions $\{2j - 1, 2j\}$ are disjoint sensitive blocks, so $\mathrm{bs}(f) \ge k^2/2$. Rubinstein proved $\mathrm{s}(f) = k$, so $\mathrm{bs}(f) = \mathrm{s}(f)^2 / 2$. For $k = 4$ (16 bits), a brute-force count over all $2^{16}$ inputs gives $\mathrm{s}(f) = 4$, while $\mathrm{bs}(f) \ge 8$.

The approximate degree can be far below the degree. For OR on $n$ bits, $\deg = n$, but the exact best approximations give these values of $\widetilde{\deg}$:

| $n$ | 4 | 9 | 16 | 25 | 36 | 49 | 64 | 100 |
|---|---|---|---|---|---|---|---|---|
| $\widetilde{\deg}(\mathrm{OR}_n)$ | 2 | 2 | 3 | 4 | 4 | 5 | 6 | 7 |

The values grow like $\sqrt n$, as Nisan and Szegedy proved. For PARITY, the approximate degree is $n$ for every $n$. The [approximate degree](/approximate-degree/) page explains how these values are computed.

## Where it is used

- **Lower bounds for search.** The quantum lower bound $\Omega(\sqrt n)$ for OR, proved with the [polynomial method](/polynomial-method/) or the [hybrid argument](/hybrid-argument/), shows that [Grover search](/grover-search/) is optimal; see [Grover optimality](/grover-optimality/).
- **Oracle separations.** A class separation relative to an oracle reduces to a query lower bound, as in the [Baker-Gill-Solovay theorem](/baker-gill-solovay-theorem/).
- **Parallel lower bounds.** Nisan introduced block sensitivity to give tight bounds on the time that a CREW PRAM needs to compute $f$.
- **Communication complexity.** A query algorithm for $f$ gives a protocol for $f$ composed with a two-party gadget, with two bits per query; see [communication complexity](/communication-complexity/).
- **Fourier analysis.** The degree $\deg(f)$ is also the largest size $|S|$ of a nonzero coefficient in the [Fourier expansion](/fourier-analysis-of-boolean-functions/) of $f$, because the change of variables $x_i = (1 - y_i)/2$ from $\{0,1\}$ to $\{1,-1\}$ does not change the degree. Many proofs move between the two views.
- **Lower bound methods.** The [adversary argument](/adversary-argument/), [Yao's minimax principle](/yao-minimax-principle/), the [quantum adversary method](/quantum-adversary-method/) and the polynomial method all bound query complexity. In stronger models, other methods are needed: for example the $\Omega(n \log n)$ bound for [element distinctness](/element-distinctness-lower-bound/) is in the algebraic computation tree model, where one query can compare whole numbers.

## References

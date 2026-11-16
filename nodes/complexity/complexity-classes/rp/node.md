---
tag: 8RTK2K
kind: definition
slug: rp
name: RP
aliases:
- randomized polynomial time
area: complexity/complexity-classes
level: core
summary: The decision problems that a probabilistic machine decides in polynomial time with one-sided error. It never accepts a no-instance and accepts a yes-instance with probability at least 1/2.
prereqs: [probabilistic-turing-machine, p, np, one-sided-error]
see_also: [co-rp, zpp, bpp, adleman-theorem, perfect-matching, schwartz-zippel-lemma, monte-carlo-algorithm, error-amplification]
sources:
  - paper: doi:10.1109/SFCS.1978.37
    title: Leonard Adleman, Two theorems on random polynomial time, 19th Annual Symposium on Foundations of Computer Science, 75 to 83 (1978)
    locator: the definition of random polynomial time and the inclusion of RP in P/poly
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 7, Randomized computation (one-sided error and the classes RP and coRP)
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley (1994)
    locator: Chapter 11, Randomized computation (the class RP and the Monte Carlo test for perfect matchings)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press (1995)
    locator: Chapter 1, Introduction (the classes RP, coRP, ZPP and BPP)
---

RP (randomized polynomial time) is the class of decision problems that a [probabilistic Turing machine](/probabilistic-turing-machine/) decides in polynomial time with [one-sided error](/one-sided-error/): on a no-instance the machine always rejects, and on a yes-instance it accepts with probability at least $1/2$. So an accept answer is always right, and only a reject answer can be wrong. Independent repetition makes the error on yes-instances $2^{-k}$ after $k$ runs. RP lies between [P](/p/) and [NP](/np/), and both inclusions are open.

## Definition

**Model.** The machine is a probabilistic [multitape Turing machine](/multitape-turing-machine/) that flips fair coins. Equivalently, it is a deterministic machine $M$ that reads an input $x$ and a string $r$ of coin flips, and it runs in time polynomial in $|x|$ for every $r$. The time bound is worst-case.

**Definition.** A language $L$ is in $\mathsf{RP}$ if there are a polynomial $p$ and such a machine $M$ that, with $r$ uniform on $\{0,1\}^{p(|x|)}$, satisfy for every input $x$:

$$x \in L \Rightarrow \Pr_r[M(x, r) = 1] \ge 1/2, \qquad x \notin L \Rightarrow \Pr_r[M(x, r) = 1] = 0.$$

Adleman (1978) called this class random polynomial time and proved $\mathsf{RP} \subseteq \mathsf{P/poly}$. The probability is over the coins for each fixed input, not over a distribution of inputs.

**The constant $1/2$ does not matter.** Let $q$ and $s$ be polynomials. Replace the yes-condition by "$\Pr \ge 1/q(|x|)$" or by "$\Pr \ge 1 - 2^{-s(|x|)}$", and the class stays the same. To amplify, run $M$ for $k$ times with independent coins and accept if at least one run accepts. A no-instance is still never accepted. A yes-instance is rejected only if all $k$ runs reject, which has probability at most $(1 - 1/q)^k \le e^{-k/q}$. The choice $k = q(n)\, s(n)$ gives error at most $e^{-s(n)} < 2^{-s(n)}$. With success $1/2$ per run, $k$ runs give error at most $2^{-k}$: $10$ runs give at most $1/1024$. This OR rule is simpler than the majority vote that [BPP](/bpp/) needs, and the Chernoff bound is not necessary. See [error amplification](/error-amplification/).

**Basic properties.**

- $\mathsf{P} \subseteq \mathsf{RP}$: a deterministic machine has error $0$ on both sides.
- $\mathsf{RP} \subseteq \mathsf{NP}$. A coin string $r$ with $M(x, r) = 1$ exists if and only if $x \in L$, so $r$ is a [certificate](/certificate/) and $M$ is a [polynomial-time verifier](/polynomial-time-verifier/). RP asks for many certificates (at least half of all strings $r$), while NP asks for one.
- $\mathsf{RP} \subseteq \mathsf{BPP}$: run the machine twice and accept if either run accepts. The error is $0$ on no-instances and at most $1/4$ on yes-instances.
- RP is closed under union and intersection (run both machines and amplify) and under polynomial-time many-one reductions. It is not known to be closed under complement. The class of complements is [coRP](/co-rp/), and $\mathsf{RP} \cap \mathsf{coRP} = \mathsf{ZPP}$ ([ZPP](/zpp/)).
- $\mathsf{RP} \subseteq \mathsf{P/poly}$ ([Adleman's theorem](/adleman-theorem/)).

## Examples and non-examples

**Example: a bipartite graph has a perfect matching.** Let $G$ be a bipartite graph with parts $\{u_1, \ldots, u_n\}$ and $\{v_1, \ldots, v_n\}$. Make the $n \times n$ matrix $A$ with $A_{ij} = x_{ij}$, a variable, if $u_i v_j$ is an edge and $A_{ij} = 0$ otherwise (the Edmonds matrix). Each nonzero term of $\det A$ is a product $\prod_i x_{i \sigma(i)}$ for a permutation $\sigma$ whose edges $u_i v_{\sigma(i)}$ are all in $G$. Different permutations give different monomials, so no terms cancel. So $\det A$ is a nonzero polynomial if and only if $G$ has a [perfect matching](/perfect-matching/). The test: choose a prime $p \ge 2n$, put independent uniform values from $\mathrm{GF}(p)$ in place of the variables, compute the [determinant](/determinant/) by [Gaussian elimination](/gaussian-elimination/), and accept if it is not zero.

- If $G$ has no perfect matching, $\det A$ is the zero polynomial, so the test always rejects.
- If $G$ has one, $\det A$ is a nonzero polynomial of degree $n$, so by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) the test accepts with probability at least $1 - n/p \ge 1/2$.

Take the 6-cycle with edges $u_1v_1, u_1v_2, u_2v_2, u_2v_3, u_3v_3, u_3v_1$. Then $\det A = x_{11}x_{22}x_{33} + x_{12}x_{23}x_{31}$, of degree $3$. The exact acceptance probabilities and the guarantees are:

| prime $p$ | $\Pr[\det A \ne 0]$ | Schwartz-Zippel guarantee $1 - 3/p$ |
|---|---|---|
| 5 | $2176/3125 \approx 0.696$ | $0.4$ |
| 7 | $13392/16807 \approx 0.797$ | $0.571$ |
| 11 | $142000/161051 \approx 0.882$ | $0.727$ |

With $p = 5 < 2n$ the guarantee is below $1/2$, which is why the test takes $p \ge 2n$. Now remove the edges $u_1v_2$, $u_2v_2$ and $u_2v_3$, and add $u_2v_1$ and $u_3v_2$. In the new graph, $u_1$ and $u_2$ have the single neighbour $v_1$, so no perfect matching exists, and $\det A$ is $0$ for every choice of values. Perfect matching in bipartite graphs is also in P (by augmenting paths), but the same randomized test extends to general graphs with the [Tutte matrix](/tutte-matrix/), and it is the base of fast parallel algorithms.

**Example: composite numbers.** The language COMPOSITES of composite numbers in binary is in RP. Pick a random base $a$ and run one round of the [Miller-Rabin test](/miller-rabin-primality-test/): the base is a witness of compositeness with probability at least $3/4$ when $n$ is an odd composite, and no prime has a witness. So the test accepts (says "composite") only on composite inputs. Since the AKS test, COMPOSITES is also known to be in P.

**Non-examples.**

- *Two-sided error.* A machine that sometimes accepts a no-instance does not give an RP algorithm, even if its error is small. A language is in RP only if some machine has zero error on no-instances.
- *The complement side.* The Schwartz-Zippel test for [polynomial identity testing](/polynomial-identity-testing/) never rejects the zero polynomial, so it puts the language of zero polynomials in coRP, and the language of nonzero polynomials in RP. Whether the language of zero polynomials is in RP is open.
- *NP-complete problems.* $\mathsf{RP} \subseteq \mathsf{NP}$, but no NP-complete problem is known to be in RP. If one were, then $\mathsf{NP} = \mathsf{RP}$. The [Valiant-Vazirani theorem](/valiant-vazirani-theorem/) shows that SAT with at most one satisfying assignment is as hard as SAT under randomized reductions, so a polynomial-time algorithm for that promise problem would give $\mathsf{NP} = \mathsf{RP}$.

## Related definitions

- [coRP](/co-rp/): the complements of RP languages. The error is on no-instances only.
- [ZPP](/zpp/) $= \mathsf{RP} \cap \mathsf{coRP}$: zero error and expected polynomial time ([Las Vegas algorithms](/las-vegas-algorithm/)).
- [BPP](/bpp/): two-sided bounded error. RP algorithms are one-sided [Monte Carlo algorithms](/monte-carlo-algorithm/).
- [NP](/np/) has the same form as RP with "at least one certificate" in place of "at least half of the coin strings".
- [RL](/randomized-logspace/) is the logarithmic-space analogue.

## References

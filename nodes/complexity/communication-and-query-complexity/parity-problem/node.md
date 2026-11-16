---
tag: QF6FQ4
kind: problem
slug: parity-problem
name: Parity problem
aliases:
- PARITY
area: complexity/communication-and-query-complexity
level: intro
summary: "Compute the XOR of n input bits. Deterministic and randomized query algorithms need all n queries, quantum ones need exactly the ceiling of n/2, and constant-depth AND/OR circuits cannot do it."
prereqs: [query-model]
see_also: [majority-problem, sensitivity, polynomial-method, approximate-degree, ac0, deutsch-jozsa-algorithm, bit-parity, learning-parity-with-noise]
sources:
  - paper: doi:10.1145/502090.502097
    title: Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca and Ronald de Wolf, Quantum lower bounds by polynomials, Journal of the ACM 48(4) (2001)
    locator: pp. 778 to 797 (Q(PARITY) and Q_E(PARITY) equal n/2 rounded up; the polynomial lower bound)
  - paper: doi:10.1103/PhysRevLett.81.5442
    title: Edward Farhi, Jeffrey Goldstone, Sam Gutmann and Michael Sipser, Limit on the speed of quantum computation in determining parity, Physical Review Letters 81 (1998)
    locator: pp. 5442 to 5444 (n/2 quantum queries are needed for the parity of n bits)
  - paper: doi:10.1016/S0304-3975(01)00144-X
    title: Harry Buhrman and Ronald de Wolf, Complexity measures and decision tree complexity, a survey, Theoretical Computer Science 288(1) (2002)
    locator: pp. 21 to 43; Section 4.3 and Section 4.4 (degree and approximate degree of PARITY), Section 6.1 (symmetric functions)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 12, Decision trees; Chapter 14, Circuit lower bounds (PARITY is not in AC0)
  - paper: doi:10.1137/0220062
    title: Noam Nisan, CREW PRAMs and decision trees, SIAM Journal on Computing 20(6) (1991)
    locator: pp. 999 to 1007 (bs(f) at most 3 R(f))
---

The parity problem asks for the XOR of $n$ input bits: is the number of ones odd? It is the standard hard function of [query complexity](/query-complexity/). Every input is sensitive to every bit, so deterministic and randomized query algorithms must read all $n$ bits, and a quantum algorithm can save exactly a factor of two and no more. The same function is the classic example of a problem outside [AC0](/ac0/). This page is about the Boolean function and its complexity; the [parity bit](/parity-bit/) page is about its use for error detection, [bit parity](/bit-parity/) about computing it on a machine word, and [permutation parity](/permutation-parity/) about a different notion.

## In plain words

You have a row of hidden bits, and you must say whether the number of ones is odd or even. Every single bit matters: if you skip even one, it could be a 0 or a 1, and the answer flips. So a normal algorithm must look at all of them, and flipping coins does not help, because with one bit unseen you are guessing. A quantum computer can look at two bits in one step and learn whether they are equal, which halves the work, but it cannot do better than half. Simple circuits made of AND and OR gates with few layers also fail: they need a huge number of gates.

## Definition

The parity function is $\mathrm{PARITY}_n(x) = x_1 \oplus x_2 \oplus \cdots \oplus x_n$, which is 1 when $|x| = x_1 + \cdots + x_n$ is odd.

**Instance.** A string $x \in \{0,1\}^n$, available through queries "what is $x_i$?" in the [query model](/query-model/).

**Question.** Is the number of ones in $x$ odd?

The measure is the number of queries, in a named model: deterministic ($D^{dt}$), randomized with error $1/3$ ($R$), quantum exact ($Q_E$) or quantum with error $1/3$ ($Q$). In circuit complexity the input is given on $n$ wires, and the measures are size and depth.

As a real polynomial, with $\{0,1\}$ inputs,

$$\mathrm{PARITY}_n(x) = \sum_{\emptyset \ne S \subseteq [n]} (-2)^{|S| - 1} \prod_{i \in S} x_i,$$

which has degree $n$. In the $\pm 1$ form, with $y_i = (-1)^{x_i}$, it is the single monomial $(-1)^{\mathrm{PARITY}_n(x)} = y_1 y_2 \cdots y_n$.

## Variants

- **Parity of a subset.** The parity of the bits in a fixed set $S$ is the character $\chi_S$ of [Fourier analysis](/fourier-analysis-of-boolean-functions/). The [Bernstein-Vazirani algorithm](/bernstein-vazirani-algorithm/) learns an unknown $S$ with one quantum query, and [linearity testing](/linearity-test/) checks whether a function is close to such a parity.
- **Parity with noise.** Learning an unknown parity from noisy random samples is [learning parity with noise](/learning-parity-with-noise/), a hardness assumption in cryptography.
- **MOD$_m$.** The function that tests whether $|x|$ is divisible by $m$ generalizes parity ($m = 2$, negated). It is also not in AC0.
- **Parity on a word RAM.** If the bits are packed in machine words, the parity is computed with word operations; see [bit parity](/bit-parity/) and [population count](/population-count/). The query model does not apply there, because one operation reads many bits.

## Examples

For $n = 3$ the polynomial is $x_1 + x_2 + x_3 - 2(x_1 x_2 + x_1 x_3 + x_2 x_3) + 4 x_1 x_2 x_3$. At $x = 110$ it gives $2 - 2 = 0$, and at $x = 111$ it gives $3 - 6 + 4 = 1$.

**Two bits with one quantum query.** This is the step of Deutsch's algorithm. Use the phase form of the oracle, $\lvert i \rangle \mapsto (-1)^{x_i} \lvert i \rangle$, which a standard query gives when its target qubit is in the state $(\lvert 0 \rangle - \lvert 1 \rangle)/\sqrt 2$. Start in $(\lvert 1 \rangle + \lvert 2 \rangle)/\sqrt 2$. One query gives

$$\frac{(-1)^{x_1} \lvert 1 \rangle + (-1)^{x_2} \lvert 2 \rangle}{\sqrt 2} = (-1)^{x_1} \, \frac{\lvert 1 \rangle + (-1)^{x_1 \oplus x_2} \lvert 2 \rangle}{\sqrt 2}.$$

A Hadamard gate maps the two possible states to $\lvert 1 \rangle$ and $\lvert 2 \rangle$, so a measurement gives $x_1 \oplus x_2$ with certainty. For $n$ bits, do this for $\lfloor n/2 \rfloor$ pairs and read the last bit classically when $n$ is odd, then XOR the results: $\lceil n/2 \rceil$ queries, exact. See the [Deutsch-Jozsa algorithm](/deutsch-jozsa-algorithm/).

**Approximate degree.** The best uniform error of a polynomial of degree $d$ on the symmetric values was computed exactly for $n = 1, \ldots, 12$. For every such $n$, the best error with degree $n - 1$ is exactly $1/2$, the error of the constant polynomial $1/2$. So $\widetilde{\deg}(\mathrm{PARITY}_n) = n$ for these $n$, as the proof below shows for all $n$.

## Known algorithms

- **Deterministic.** Read all bits and XOR them: $n$ queries, $O(n)$ time.
- **Quantum.** Pair the bits and use one query per pair, as in the example: $\lceil n/2 \rceil$ queries with no error (Beals et al. 2001; Farhi, Goldstone, Gutmann and Sipser 1998).
- **Circuits.** A balanced tree of XOR gates of fan-in 2 has size $n - 1$ and depth $\lceil \log_2 n \rceil$. With AND, OR and NOT gates, each XOR gate becomes a constant-depth piece, so PARITY is in NC1. With MAJORITY gates it is in [TC0](/tc0/).

## Bounds

All the query measures of PARITY are known exactly.

| measure | value | reason |
|---|---|---|
| $\mathrm{s}$, $\mathrm{bs}$, $C$ | $n$ | every input is sensitive to every bit |
| $D^{dt}$ | $n$ | $D^{dt} \ge \mathrm{s}$ |
| $R_0$, $R$ | $n$ | uniform distribution, below |
| $\deg$, $\widetilde{\deg}$ | $n$ | sign changes, below |
| $Q_E$, $Q$ | $\lceil n/2 \rceil$ | $Q \ge \widetilde{\deg}/2$ and the pairing algorithm |

**Randomized lower bound.** By [Yao's minimax principle](/yao-minimax-principle/), it is enough to bound deterministic trees on the uniform distribution. If every path of a tree has fewer than $n$ queries, then at each leaf some bit is unread, and exactly half of the inputs that reach the leaf have each parity. So the tree errs on half of all inputs, and no algorithm with fewer than $n$ queries has error below $1/2$. So $R(\mathrm{PARITY}_n) = n$.

**Approximate degree.** Let $p$ have degree $d$ and $|p(x) - \mathrm{PARITY}_n(x)| \le 1/3$ on all inputs. Average $p$ over the inputs of each weight $k$: by symmetrization this gives a polynomial $q(k)$ of one variable with degree at most $d$, and $q(k) \le 1/3$ for even $k$ and $q(k) \ge 2/3$ for odd $k$, for $k = 0, 1, \ldots, n$. So $q - 1/2$ changes sign between each pair of consecutive integers, $n$ times in all, and has $n$ real roots. So $d \ge n$. The [polynomial method](/polynomial-method/) then gives $Q(\mathrm{PARITY}_n) \ge n/2$, so $Q = Q_E = \lceil n/2 \rceil$.

**Circuits.** PARITY is not in AC0: a circuit family of constant depth with unbounded fan-in AND and OR gates needs size superpolynomial in $n$ (Furst, Saxe and Sipser; Ajtai; with the exponential bound of Håstad). This is one of the few unconditional separations of circuit classes; see [AC0](/ac0/) and [circuit complexity](/circuit-complexity/).

## Reductions

- **PARITY to MAJORITY.** With constant depth and polynomial size, PARITY can be computed from MAJORITY gates, so MAJORITY is not in AC0 either; see the [majority problem](/majority-problem/).
- **Composition.** PARITY of $n$ bits is the XOR of PARITY on two halves. This self-reduction gives the depth $\lceil \log_2 n \rceil$ tree above.

## Applications

- **A test case for lower bound methods.** Since all measures are maximal or exactly known, PARITY is the first check of any new query or circuit lower bound method.
- **Quantum speedup limits.** It shows that quantum algorithms can give at most a constant-factor speedup for some total functions, in contrast with [Grover search](/grover-search/) for OR.
- **Error detection and cryptography.** The [parity bit](/parity-bit/) detects single-bit errors, and noisy parities give [learning parity with noise](/learning-parity-with-noise/).

## References

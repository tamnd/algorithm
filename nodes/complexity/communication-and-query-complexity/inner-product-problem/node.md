---
tag: VPZREC
kind: problem
slug: inner-product-problem
name: Inner product problem
aliases:
- inner product mod 2
- inner product function
area: complexity/communication-and-query-complexity
level: advanced
summary: "Alice and Bob compute the inner product mod 2 of their n-bit strings. D^cc = n + 1, and the randomized cost is Theta(n) even with public coins, by the discrepancy method."
prereqs: [communication-model, randomized-communication-complexity]
see_also: [discrepancy-method, disjointness-problem, index-problem, sign-rank, walsh-hadamard-transform, hadamard-code, two-source-extractor, number-on-forehead-model]
sources:
  - paper: "Benny Chor and Oded Goldreich, Unbiased bits from sources of weak randomness and probabilistic communication complexity, SIAM Journal on Computing 17(2) (1988)"
    locator: the bound on the bias of inner product over large rectangles, its use as a two-source extractor, and the Omega(n) randomized lower bound
  - paper: "László Babai, Péter Frankl and Janos Simon, Complexity classes in communication complexity theory, Proceedings of the 27th IEEE Symposium on Foundations of Computer Science (FOCS 1986), 337-347"
    locator: the discrepancy argument for inner product
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press, 1997
    locator: Chapter 3, Randomization (distributional complexity, discrepancy and the inner product example)
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press, 2020
    locator: Chapter 5, Discrepancy (inner product and Lindsey's lemma)
  - paper: "Jürgen Forster, A linear lower bound on the unbounded error probabilistic communication complexity, Journal of Computer and System Sciences 65(4) (2002), 612-625"
    locator: the sign rank of an N x N Hadamard matrix is at least the square root of N
---

In the inner product problem, Alice holds $x \in \{0,1\}^n$, Bob holds $y \in \{0,1\}^n$, and they must compute $\mathrm{IP}_n(x, y) = \sum_i x_i y_i \bmod 2$. It is the standard example of a function that is hard for every kind of two-party protocol: deterministic protocols need $n + 1$ bits, and randomized protocols need $\Omega(n)$ bits even with public coins and even when they only have to beat a random guess by a little. The reason is that every large rectangle of its communication matrix is almost balanced between 0s and 1s, which is what the [discrepancy method](/discrepancy-method/) measures.

## In plain words

Alice and Bob each hold a row of zeros and ones of the same length. They look at the places where both rows have a one and want to know if the number of such places is even or odd.

Any part of the problem that a short talk can pin down looks like a coin toss: in every large block of inputs, about half the answers are "even" and half are "odd". A short talk can only split the inputs into a few blocks, so it cannot do much better than a guess. Random choices do not help. The players must send a fixed fraction of the row, which is a stronger result than the one for the question of a common element.

## Definition

Fix $n \ge 1$. The function is $\mathrm{IP}_n : \{0,1\}^n \times \{0,1\}^n \to \{0,1\}$ with $\mathrm{IP}_n(x, y) = x_1 y_1 \oplus x_2 y_2 \oplus \cdots \oplus x_n y_n$, the inner product over $\mathrm{GF}(2)$.

**Instance:** a string $x \in \{0,1\}^n$, known only to Alice, and a string $y \in \{0,1\}^n$, known only to Bob.

**Question:** is $\sum_i x_i y_i$ odd?

The model is the two-party [communication model](/communication-model/), with both players informed at the end. $D^{cc}$ is the deterministic cost and $R$ the cost with error at most $1/3$ on every input. With the entries mapped to signs, $(-1)^{\mathrm{IP}_n(x, y)}$, the communication matrix becomes the $2^n \times 2^n$ Sylvester Hadamard matrix $H_n$, the matrix of the [Walsh-Hadamard transform](/walsh-hadamard-transform/). Its rows are the codewords of the [Hadamard code](/hadamard-code/) with signs.

## Variants

- **Distributional form.** Inputs are uniform, and the protocol must be correct with probability $1/2 + \varepsilon$ over the inputs. The cost is still about $n/2 - \log_2(1/\varepsilon)$; see Bounds.
- **Generalized inner product.** With $k$ players in the [number-on-forehead model](/number-on-forehead-model/), the function is the parity of the number of positions $i$ where all $k$ strings have a 1. Babai, Nisan and Szegedy (1992) proved that it needs $\Omega(n / 4^k)$ bits.
- **Other fields.** For the inner product over $\mathrm{GF}(p)$, the same proof with the characters of $\mathrm{GF}(p)$ bounds the bias of every large rectangle, and the cost stays linear in the input length.
- **Unbounded error.** Protocols that need to be correct only with probability above $1/2$. Here inner product is still hard, by Forster's bound on the [sign rank](/sign-rank/) of $H_n$.

## Examples

For $n = 2$, with rows and columns in the order $00, 01, 10, 11$,

$$M_{\mathrm{IP}_2} = \begin{pmatrix} 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & 1 \\ 0 & 1 & 1 & 0 \end{pmatrix}.$$

For $x = 11$ and $y = 01$ the common ones are at position 2 only, so $\mathrm{IP}_2(11, 01) = 1$. The matrix has 6 ones, in agreement with the count $2^{2n-1} - 2^{n-1}$ of 1-entries.

Ranks, computed exactly for $n = 1, \ldots, 4$: over the reals $\operatorname{rank}(M_{\mathrm{IP}_n}) = 2^n - 1$ (the row of $x = 0$ is zero) and $\operatorname{rank}(J - M_{\mathrm{IP}_n}) = 2^n$, where $J$ is the all-ones matrix. Over $\mathrm{GF}(2)$, $M_{\mathrm{IP}_n}$ is the Gram matrix of the standard basis and has rank only $n$. The real rank is what matters for the [log-rank bound](/log-rank-lower-bound/).

Discrepancy under the uniform distribution. For a rectangle $A \times B$ let $\operatorname{disc}(A \times B) = |\sum_{x \in A, y \in B} (-1)^{\mathrm{IP}(x, y)}| / 4^n$. An exhaustive search over all rectangles gives the largest value, compared here with Lindsey's bound $2^{-n/2}$:

| $n$ | largest $\lvert\sum\rvert$ | exact discrepancy | Lindsey bound $2^{-n/2}$ |
|---|---|---|---|
| 1 | 2 | $1/2$ | $0.7071$ |
| 2 | 5 | $5/16 = 0.3125$ | $0.5$ |
| 3 | 11 | $11/64 \approx 0.1719$ | $0.3536$ |
| 4 | 28 | $7/64 \approx 0.1094$ | $0.25$ |

For $n = 4$ the discrepancy bound with the exact value gives $\log_2((1/3)/(7/64)) = \log_2(64/21) \approx 1.61$, so every protocol with error $1/3$ under the uniform distribution sends at least 2 bits. The bound is weak for small $n$ and grows like $n/2$.

## Known algorithms

- **Trivial protocol.** Alice sends $x$ and Bob sends the answer: $n + 1$ bits. It is optimal for deterministic protocols and optimal up to a constant factor for randomized ones.
- **Quantum protocols.** Quantum protocols also need $\Omega(n)$ qubits (Cleve, van Dam, Nielsen and Tapp 1998), so inner product shows no quantum speed-up, unlike [disjointness](/disjointness-problem/). See [quantum communication complexity](/quantum-communication-complexity/).

## Bounds

| Measure | Cost of $\mathrm{IP}_n$ | Method |
|---|---|---|
| $D^{cc}$ | $n + 1$ | log-rank: $(2^n - 1) + 2^n$ leaves, and $\lceil \log_2(2^{n+1} - 1) \rceil = n + 1$ |
| $N^1$ and $N^0$ | between $n - 2$ and $n + 1$ | every monochromatic rectangle has at most $2^n$ entries (Lindsey) |
| $R$, public or private coins | $\Theta(n)$; at least $n/2 - \log_2 3$ | [discrepancy](/discrepancy-method/) under the uniform distribution |
| distributional, advantage $\varepsilon$ | at least $n/2 - \log_2(1/\varepsilon)$ | the same discrepancy bound |
| quantum | $\Theta(n)$ | Cleve, van Dam, Nielsen and Tapp 1998 |
| unbounded error | $\Theta(n)$; at least $n/2 - O(1)$ | Forster 2002: sign rank of $H_n$ at least $2^{n/2}$ |

**Lindsey's lemma.** For all $A, B \subseteq \{0,1\}^n$, $\left|\sum_{x \in A, y \in B} (-1)^{\mathrm{IP}(x, y)}\right| \le \sqrt{|A|\,|B|\,2^n}$.

*Proof.* Let $\mathbf{1}_A$ and $\mathbf{1}_B$ be the indicator vectors. The sum equals $\mathbf{1}_A^{\mathsf T} H_n \mathbf{1}_B$. Since $H_n^{\mathsf T} H_n = 2^n I$, the matrix $H_n$ maps every vector $v$ to a vector of length $2^{n/2} \lVert v \rVert$. By Cauchy-Schwarz, $|\mathbf{1}_A^{\mathsf T} H_n \mathbf{1}_B| \le \lVert \mathbf{1}_A \rVert \cdot 2^{n/2} \lVert \mathbf{1}_B \rVert = \sqrt{|A|}\, 2^{n/2} \sqrt{|B|}$. $\blacksquare$

**The randomized bound.** Divide by $4^n$: every rectangle has discrepancy at most $2^{-n/2}$ under the uniform distribution $\mu$. The discrepancy method gives $D^{\mu}_{1/2 - \varepsilon}(\mathrm{IP}_n) \ge \log_2(2\varepsilon / 2^{-n/2}) = n/2 + \log_2(2\varepsilon)$. With error $1/3$, that is $\varepsilon = 1/6$, this is $n/2 - \log_2 3$. By [Yao's minimax principle](/yao-minimax-principle/), the public-coin cost $R(\mathrm{IP}_n)$ is at least this distributional cost, and the private-coin cost is at least the public-coin cost.

**The nondeterministic bound.** If $A \times B$ is monochromatic, the sum in Lindsey's lemma is $\pm |A||B|$, so $|A||B| \le 2^n$. The $2^{2n-1} - 2^{n-1}$ ones then need at least $2^{n-1} - 1/2$ rectangles to cover them, and $N^1(\mathrm{IP}_n) \ge \log_2(2^{n-1} - 1/2) \ge n - 2$ for $n \ge 2$. The zeros give the same bound for $N^0$.

## Reductions

- **To index.** Let $m = \log_2 n$ with $n$ a power of two, and index the positions of Alice's string by $z \in \{0,1\}^m$. For $a \in \{0,1\}^m$ let Alice's string be $x^{(a)}_z = \mathrm{IP}_m(a, z)$. Then $\mathrm{INDEX}_n(x^{(a)}, z) = \mathrm{IP}_m(a, z)$, so $\mathrm{IP}_m$ is a submatrix of $\mathrm{INDEX}_n$, and two-way randomized protocols for the [index problem](/index-problem/) need $\Omega(\log n)$ bits.
- **Into composed functions.** Any function $f$ whose matrix contains $M_{\mathrm{IP}_m}$ as a submatrix inherits the bound $\Omega(m)$ for every model above. This is a common way to prove randomized lower bounds by reduction.
- **To threshold circuits.** Hajnal, Maass, Pudlák, Szegedy and Turán (1993) used the small discrepancy of inner product to prove that depth-2 circuits of majority gates need exponential size to compute $\mathrm{IP}_n$. See [TC0](/tc0/).

## Applications

- **Randomness extraction.** Lindsey's lemma says that $\mathrm{IP}$ is nearly unbiased on any large rectangle. Chor and Goldreich (1988) used this to show that $\mathrm{IP}_n$ is a [two-source extractor](/two-source-extractor/) for two independent sources with min-entropy above $n/2$.
- **Learning theory.** Forster's sign rank bound shows that the concept class of the Hadamard rows cannot be embedded into halfspaces of small dimension, which limits kernel methods and [halfspace learning](/halfspace-learning/).
- **Circuit and space lower bounds.** The depth-2 threshold circuit lower bound above. Babai, Nisan and Szegedy (1992) used the number-on-forehead bound for the generalized inner product to get time-space trade-offs and pseudorandom generators for logspace.
- **Teaching.** Inner product is the textbook example for the discrepancy method in Kushilevitz and Nisan and in Rao and Yehudayoff.

## References

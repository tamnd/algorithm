---
tag: FC3EV5
kind: concept
slug: randomized-communication-complexity
name: Randomized communication complexity
aliases:
- public-coin communication complexity
- private-coin communication complexity
area: complexity/communication-and-query-complexity
level: advanced
summary: "The least worst-case cost of a two-party protocol that flips coins and is correct with probability at least 2/3 on every input. Private and public coins differ by at most O(log n) bits."
prereqs: [deterministic-communication-complexity, randomized-algorithm]
see_also: [equality-testing-protocol, yao-minimax-principle, discrepancy-method, corruption-bound, information-complexity, disjointness-problem, inner-product-problem, greater-than-problem]
sources:
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press, 1997
    locator: Chapter 3, Randomization (the definitions, randomization versus determinism, public coin versus private coin with Newman's theorem in the refined form of Theorem 3.14, distributional complexity and discrepancy)
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press, 2020
    locator: Chapter 3, Randomized Protocols (sections Some Protocols, Randomized Communication Complexity, Public Coins versus Private Coins, and Nearly Monochromatic Rectangles), and Chapter 5, Discrepancy
  - paper: "Ilan Newman, Private vs. common random bits in communication complexity, Information Processing Letters 39(2) (1991), pages 67-71"
    locator: the main theorem, private coins cost at most O(log n) bits more than public coins
  - paper: doi:10.1145/800135.804414
    title: "Andrew Chi-Chih Yao, Some complexity questions related to distributive computing (preliminary report), Proceedings of the 11th Annual ACM Symposium on Theory of Computing (STOC 1979), pages 209-213"
    locator: the definition of probabilistic protocols
---

Randomized communication complexity is the cost of two-party protocols that may flip coins and may err with a small probability. Alice holds $x$, Bob holds $y$, and the protocol must output $f(x, y)$ with probability at least $2/3$ on every input pair, over its random bits; the cost is the number of bits sent in the worst case. With **private coins** each player has their own random bits, and with **public coins** both see one shared random string; the two costs, $R^{\mathrm{priv}}(f)$ and $R^{\mathrm{pub}}(f)$, differ by at most $O(\log n)$ bits by Newman's theorem. Randomness can save a lot, as for the [equality problem](/equality-problem/), or almost nothing, as for [disjointness](/disjointness-problem/) and [inner product](/inner-product-problem/).

## In plain words

Two people want to compute an answer that depends on both of their inputs, and they send bits to each other. Now they may also flip coins, and they accept a small chance of a wrong answer. The chance must be small for every possible pair of inputs, not only on average.

The coins can be private, where each person has their own coins and must send any result that the other one needs. Or the coins can be shared, where both see the same coin flips for free. Shared coins are never worse, and they save at most a short message.

For some questions, coins make the talk much shorter: to check if two long rows are the same, a few random checks are enough. For other questions, such as whether two sets share an element, the talk stays long even with coins.

## The idea

**Definitions.** Fix $f : X \times Y \to \{0,1\}$ with $X = Y = \{0,1\}^n$ and an error bound $\varepsilon < 1/2$.

- A **public-coin protocol** is a probability distribution over deterministic protocols: a shared random string $r$ is drawn, and the players run a deterministic protocol $P_r$. It computes $f$ with error $\varepsilon$ if $\Pr_r[P_r(x, y) = f(x, y)] \ge 1 - \varepsilon$ for every pair $(x, y)$. $R^{\mathrm{pub}}_\varepsilon(f)$ is the least worst-case cost of such a protocol.
- A **private-coin protocol** lets Alice's messages depend on her random string $r_A$ and Bob's on $r_B$, which are independent and not seen by the other player. $R^{\mathrm{priv}}_\varepsilon(f)$ is the least worst-case cost with error $\varepsilon$ on every input.
- $R(f)$ means $R_{1/3}(f)$. Any constant $\varepsilon < 1/2$ gives the same value up to a constant factor: repeat the protocol $O(\log(1/\delta))$ times and take the majority answer to reach error $\delta$, by the [Chernoff bound](/chernoff-bound/).
- **One-sided error**: the protocol is always correct when $f(x, y) = 0$. **Zero error**: the protocol is always correct, and the cost is the expected number of bits on the worst input.
- The protocol is **two-way** unless stated. The [one-way](/one-way-communication-complexity/) and [simultaneous](/simultaneous-message-model/) versions restrict who may speak.

**Basic relations.** For every $f$ on $n$-bit inputs:

$$R^{\mathrm{pub}}(f) \le R^{\mathrm{priv}}(f) \le D^{cc}(f) \le n + 1,$$

where $D^{cc}(f)$ is the [deterministic communication complexity](/deterministic-communication-complexity/).

- **Newman's theorem (1991).** $R^{\mathrm{priv}}_{\varepsilon + \delta}(f) \le R^{\mathrm{pub}}_\varepsilon(f) + O(\log n + \log(1/\delta))$. The proof picks $O(n/\delta^2)$ random strings at random, shows by a union bound over the $2^{2n}$ inputs that some fixed list of them works on every input, and lets Alice send the index of a string from that list.
- **Private coins against determinism.** $R^{\mathrm{priv}}(f) = \Omega(\log D^{cc}(f))$. A private-coin protocol of cost $c$ can be simulated deterministically: for each of the $2^c$ transcripts, the players send the probabilities of their own parts, to enough precision, and Bob adds up the probability of each answer. So randomness saves at most an exponential factor with private coins. With public coins there is no such bound: equality has $D^{cc} = n + 1$ but $R^{\mathrm{pub}} = O(1)$.
- **Yao's principle.** For a distribution $\mu$ on inputs, the distributional complexity $D^\mu_\varepsilon(f)$ is the least cost of a deterministic protocol that errs on at most an $\varepsilon$ fraction of the inputs under $\mu$. By the [minimax theorem](/minimax-theorem/), $R^{\mathrm{pub}}_\varepsilon(f) = \max_\mu D^\mu_\varepsilon(f)$. Every randomized lower bound can therefore be proved for a deterministic protocol on a hard distribution. See [Yao's minimax principle](/yao-minimax-principle/).

**Lower bound methods.** The rectangle methods for deterministic protocols, such as the [fooling set method](/fooling-set-method/) and the [log-rank lower bound](/log-rank-lower-bound/), fail here, since a randomized protocol may put many inputs with different values in one leaf. The randomized methods bound the measure "a rectangle that is nearly monochromatic under $\mu$":

- the [discrepancy method](/discrepancy-method/): every large rectangle is nearly balanced, which gives $R(\mathrm{IP}) = \Omega(n)$;
- the [corruption bound](/corruption-bound/): every large rectangle has many errors on one side, which gives $R(\mathrm{DISJ}) = \Omega(n)$;
- [information complexity](/information-complexity/): the transcript must reveal much information about the inputs;
- the approximate rank, the least rank of a matrix that is entrywise close to $M_f$.

## Examples

| Problem | $D^{cc}$ | $R^{\mathrm{priv}}$ | $R^{\mathrm{pub}}$ |
|---|---|---|---|
| [Equality](/equality-problem/) | $n + 1$ | $\Theta(\log n)$ | $\Theta(1)$ |
| [Greater-than](/greater-than-problem/) | $n + 1$ | $\Theta(\log n)$ | $\Theta(\log n)$ |
| [Disjointness](/disjointness-problem/) | $n + 1$ | $\Theta(n)$ | $\Theta(n)$ |
| [Inner product](/inner-product-problem/) | $n + 1$ | $\Theta(n)$ | $\Theta(n)$ |
| [Gap Hamming distance](/gap-hamming-distance/) | $\Theta(n)$ | $\Theta(n)$ | $\Theta(n)$ |

**Equality with public coins.** Shared random strings $s, t \in \{0,1\}^n$ are drawn. Alice sends the two parities $\langle x, s \rangle \bmod 2$ and $\langle x, t \rangle \bmod 2$. Bob compares them with $\langle y, s \rangle$ and $\langle y, t \rangle$ and sends 1 if both agree. If $x = y$, he always sends 1. If $x \ne y$, then $\langle x, s \rangle = \langle y, s \rangle$ exactly when $\langle x \oplus y, s \rangle = 0$, which has probability exactly $1/2$ because $x \oplus y \ne 0$. The two strings are independent, so the error is $1/4$, with 3 bits for every $n$.

**Equality with private coins.** Alice must send her random choice, so she sends a random point $r$ of a prime field of size about $n^2$ and the value at $r$ of the polynomial whose coefficients are the bits of $x$. This is the [randomized equality testing protocol](/equality-testing-protocol/), with $O(\log n)$ bits and error below $1/n$. The bound $R^{\mathrm{priv}} = \Omega(\log D^{cc})$ shows that $\Omega(\log n)$ bits are needed, so equality is an example where the $O(\log n)$ term of Newman's theorem is needed.

**Disjointness and inner product.** Here coins do not help. Kalyanasundaram and Schnitger (1992) and Razborov (1992) proved $R(\mathrm{DISJ}) = \Omega(n)$, and Chor and Goldreich (1988) proved $R(\mathrm{IP}) = \Omega(n)$ by discrepancy.

## Where it is used

- **Streaming lower bounds.** A randomized streaming algorithm with $s$ bits of memory gives a randomized one-way protocol of cost $s$ per pass. The randomized lower bounds for [index](/index-problem-lower-bound/), disjointness and gap Hamming distance give the space lower bounds for [frequency moments](/frequency-moment-lower-bounds/) and other [streaming problems](/streaming-model/).
- **Data structures.** Randomized cell-probe lower bounds come from randomized protocols in the [cell-probe model](/cell-probe-model/).
- **Property testing and query complexity.** Testing lower bounds can be derived from randomized communication lower bounds, and [randomized query complexity](/randomized-query-complexity/) lower bounds lift to communication.
- **Distributed computing.** Lower bounds on the rounds of distributed graph algorithms often reduce from randomized disjointness.
- **Practice.** Hash-based comparison of remote data, as in file synchronization, is the equality protocol.

## References

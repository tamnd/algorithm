---
tag: TYX0MW
kind: problem
slug: equality-problem
name: Equality problem
aliases:
- EQ
- equality function
area: complexity/communication-and-query-complexity
level: intro
summary: "Alice and Bob decide whether their n-bit strings are equal. D^cc(EQ) = n + 1 when both must learn the answer (n if only Bob must). Randomized: Θ(log n) with private coins, O(1) with public coins."
prereqs: [communication-model]
see_also: [equality-testing-protocol, fingerprinting, string-equality-testing, greater-than-problem, disjointness-problem, fooling-set-method, randomized-communication-complexity, polynomial-identity-testing]
sources:
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press, 1997
    locator: Chapter 1, Basics (equality as the example for fooling sets and rank), Chapter 2 (covers of equality and non-equality), and Chapter 3, Randomization (the randomized protocols and the private-coin lower bound)
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press, 2020
    locator: Chapter 1, Deterministic Protocols, and Chapter 3, Randomized Protocols (section Some Protocols)
  - paper: "Ilan Newman, Private vs. common random bits in communication complexity, Information Processing Letters 39(2) (1991), pages 67-71"
    locator: the simulation of public coins by private coins with O(log n) extra bits
---

The equality problem asks two players, Alice with $x \in \{0,1\}^n$ and Bob with $y \in \{0,1\}^n$, to decide whether $x = y$. It is the simplest function on which the models of [communication complexity](/communication-complexity/) differ: every deterministic protocol needs $n + 1$ bits when both players must learn the answer, while randomized protocols need only $\Theta(\log n)$ bits with private coins and $O(1)$ bits with public coins. This page states the problem and its bounds; the randomized protocol is described on the [randomized equality testing protocol](/equality-testing-protocol/) page, and the general technique on the [fingerprinting](/fingerprinting/) page.

## In plain words

Two people each hold a long row of zeros and ones. They live far apart and can only send bits to each other. They want to know if their two rows are exactly the same.

Sending a whole row always works. If the answer must be certain, nothing shorter works, because any shorter plan would mix up two different rows. If a small chance of error is allowed, a few random checks are enough, and the talk becomes very short. This gap makes the problem the standard first example of what random choices can do.

## Definition

Fix $n \ge 1$. The function is $\mathrm{EQ}_n : \{0,1\}^n \times \{0,1\}^n \to \{0,1\}$ with $\mathrm{EQ}_n(x, y) = 1$ if $x = y$ and $0$ otherwise.

**Instance:** a string $x \in \{0,1\}^n$, known only to Alice, and a string $y \in \{0,1\}^n$, known only to Bob. Both know $n$.

**Question:** is $x = y$?

The model is the two-party [communication model](/communication-model/). The measure is the number of bits sent on the worst input. Unless a bound says otherwise, both players must know the answer at the end, and randomized protocols must be correct with probability at least $2/3$ on every input. The [communication matrix](/communication-matrix/) of $\mathrm{EQ}_n$ is the identity matrix $I_{2^n}$.

## Variants

- **Who learns the answer.** If only Bob must learn the answer, Alice sends $x$ and Bob decides, so $n$ bits are enough, and $n$ bits are needed. Some texts use this convention and give the deterministic cost as $n$. On this site the cost is $n + 1$, with both players informed.
- **Non-equality.** $\mathrm{NE} = 1 - \mathrm{EQ}$ has the same deterministic and randomized costs, but a different nondeterministic cost.
- **Larger alphabets.** For $x, y$ in a set of size $N$, the deterministic cost is $\lceil \log_2 N \rceil + 1$ and the private-coin randomized cost is $\Theta(\log \log N)$.
- **Error $\varepsilon$.** With public coins and error $\varepsilon$, $O(\log(1/\varepsilon))$ bits are enough.
- **Fewer rounds.** In the [simultaneous message model](/simultaneous-message-model/), both players send one message to a referee. With private coins equality needs about $\sqrt{n}$ bits there.
- **Many copies.** Solving $k$ independent copies of equality is studied as a [direct sum](/direct-sum-communication/) problem.
- **More players.** With $k$ players, the question is whether all their strings are equal. See [multiparty communication complexity](/multiparty-communication-complexity/).

## Examples

For $n = 2$ the inputs are $00, 01, 10, 11$, and $M_{\mathrm{EQ}} = I_4$. The pairs $(01, 01)$ and $(10, 10)$ are yes-instances; the pair $(01, 10)$ is a no-instance. The four 1-entries lie on the diagonal, and no two of them fit in one rectangle of 1-entries, because the rectangle would also hold an off-diagonal 0-entry. So every deterministic protocol has at least 4 leaves that output 1 and at least 1 leaf that outputs 0, and its depth is at least $\lceil \log_2 5 \rceil = 3 = n + 1$. An exhaustive search over all protocol trees for $n = 1, 2, 3$ confirms $D^{cc}(\mathrm{EQ}_n) = n + 1$.

## Known algorithms

- **Trivial protocol.** Alice sends $x$ and Bob sends the answer: $n + 1$ bits, deterministic, the best possible.
- **Randomized protocol with private coins.** The [randomized equality testing protocol](/equality-testing-protocol/) sends $2\lceil \log_2 q \rceil + 1 = O(\log n)$ bits, where $q$ is the least prime at least $n^2$, with one-sided error below $1/n$. It is optimal up to a constant factor.
- **Randomized protocol with public coins.** Random parities of $x$ and $y$ under shared random strings give error $1/4$ with 3 bits. See [randomized communication complexity](/randomized-communication-complexity/).
- **Nondeterministic protocol for non-equality.** A prover names an index $i$ with $x_i \ne y_i$ and the bit $x_i$, which the players check in $O(\log n)$ bits. See [nondeterministic communication complexity](/nondeterministic-communication-complexity/).

## Bounds

All bounds are for inputs of $n$ bits, in the two-way model with both players informed unless stated.

| Model | Cost of $\mathrm{EQ}_n$ | Lower bound method |
|---|---|---|
| Deterministic, $D^{cc}$ | $n + 1$ | [fooling set](/fooling-set-method/) of size $2^n$, or the [log-rank bound](/log-rank-lower-bound/) with rank $2^n$ |
| Deterministic, only Bob informed | $n$ | the same fooling set |
| Nondeterministic, $N^1$ | $n$ | the same fooling set, since covers also need $2^n$ rectangles |
| Nondeterministic, $N^0$ | $\log_2 n + O(1)$ | a cover of the 0-entries needs at least $n$ rectangles |
| Zero-error randomized | $\Theta(n)$ | each fixed random string gives a tree with $2^n$ distinct 1-leaves |
| Randomized, private coins | $\Theta(\log n)$ | $R(f) = \Omega(\log D^{cc}(f))$ for private coins |
| Randomized, public coins | $\Theta(1)$ | |
| Simultaneous messages, private coins | $\Theta(\sqrt{n})$ | |

The private-coin lower bound comes from a general fact: a private-coin protocol of cost $c$ can be simulated deterministically with $2^{O(c)}$ bits, so $R(f) = \Omega(\log D^{cc}(f))$, which is $\Omega(\log n)$ for equality. Newman's theorem gives the other direction of the gap: private coins cost at most $O(\log n)$ more bits than public coins, and equality shows that this is tight.

For zero-error protocols, fix the random string. The protocol becomes a deterministic tree, and each input $(x, x)$ must reach its own 1-leaf. A binary tree with $2^n$ distinct leaves has average depth at least $n$ over them, so the expected cost on the uniform distribution over the diagonal is at least $n$.

## Reductions

- **To disjointness.** Alice forms $(x, \bar{x})$ and Bob forms $(\bar{y}, y)$, two strings of $2n$ bits, where the bar flips every bit. The two sets are disjoint exactly when $x \subseteq y$ and $y \subseteq x$, that is, when $x = y$. So $\mathrm{EQ}_n$ reduces to the [disjointness problem](/disjointness-problem/) on $2n$ bits with no communication. Equality is easy for randomized protocols, so this reduction gives no useful randomized lower bound for disjointness, which needs $\Omega(n)$ bits.
- **To greater-than.** $x = y$ exactly when neither $x > y$ nor $y > x$, so two calls of a protocol for the [greater-than problem](/greater-than-problem/) solve equality. This gives the private-coin lower bound $\Omega(\log n)$ for greater-than.
- **From polynomial identity testing.** Equality is the case of [polynomial identity testing](/polynomial-identity-testing/) where the two polynomials are given by their coefficient lists and held by two players.

## Applications

- **File and data comparison.** Checking that two remote copies of a file, a database table or a memory image agree, by exchanging short fingerprints. See [string equality testing](/string-equality-testing/).
- **A subroutine.** Protocols for greater-than, for finding the first difference of two strings, and for many streaming problems run equality tests on parts of the input.
- **Lower bounds by contrast.** Equality shows that randomized lower bounds need methods that do not count rectangles, such as the [discrepancy method](/discrepancy-method/) and the [corruption bound](/corruption-bound/), because the fooling set and rank bounds are large for equality while its randomized cost is small.
- **Teaching.** Equality is the standard first example in the textbooks of Kushilevitz and Nisan and of Rao and Yehudayoff.

## References

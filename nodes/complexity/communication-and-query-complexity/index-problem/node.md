---
tag: MDCRS9
kind: problem
slug: index-problem
name: Index problem
aliases:
- INDEX
area: complexity/communication-and-query-complexity
level: advanced
summary: "Alice holds an n-bit string x and Bob an index i, and Bob must learn x_i. One-way from Alice it costs Theta(n) bits even with public coins, but with interaction it costs about log2 n."
prereqs: [one-way-communication-complexity, randomized-communication-complexity]
see_also: [index-problem-lower-bound, one-way-communication-complexity, gap-hamming-distance, disjointness-problem, round-elimination, inner-product-problem, frequency-moment-lower-bounds, streaming-model]
sources:
  - paper: "Ilan Kremer, Noam Nisan and Dana Ron, On randomized one-round communication complexity, Computational Complexity 8(1) (1999)"
    locator: one-round randomized complexity under product distributions equals the VC dimension up to constants; INDEX has VC dimension n
  - paper: doi:10.1561/0400000076
    title: "Tim Roughgarden, Communication Complexity (for Algorithm Designers), Foundations and Trends in Theoretical Computer Science 11(3-4), 2016"
    locator: Lecture 2, lower bounds for one-way communication, with Index and its use for streaming lower bounds
  - paper: "Peter Bro Miltersen, Noam Nisan, Shmuel Safra and Avi Wigderson, On data structures and asymmetric communication complexity, Journal of Computer and System Sciences 57(1) (1998), 37-49"
    locator: the round elimination lemma and its use for asymmetric problems in the style of Index
  - paper: doi:10.1016/j.jcss.2007.06.016
    title: "Pranab Sen and S. Venkatesh, Lower bounds for predecessor searching in the cell probe model, Journal of Computer and System Sciences 74(3) (2008), 364-385"
    locator: the round elimination lemma for problems where Bob also holds the prefix x_1 to x_(i-1), which is the augmented index
  - paper: "Ashwin Nayak, Optimal lower bounds for quantum automata and random access codes, Proceedings of the 40th IEEE Symposium on Foundations of Computer Science (FOCS 1999)"
    locator: the one-way quantum bound (1 - H(p)) n for random access codes, which is the quantum form of the Index bound
---

In the index problem $\mathrm{INDEX}_n$, Alice holds a string $x \in \{0,1\}^n$, Bob holds an index $i \in [n]$, and the answer is the bit $x_i$. It is the basic example of the gap between [one-way communication](/one-way-communication-complexity/) and interaction. If only Alice may send, then $n$ bits are needed deterministically and $\Omega(n)$ bits with public coins and error $1/3$, because Alice must in effect send all of $x$. If Bob may speak, he sends $i$ and Alice answers, for $\lceil \log_2 n \rceil + 1$ bits. The one-way bound is the source of most space lower bounds for one-pass [streaming](/streaming-model/) algorithms.

## In plain words

Alice has a long row of bits. Bob wants one of them, and only he knows which one. If Bob may talk, he says which position he wants and Alice gives him the bit, so the talk is short.

If only Alice may talk, she does not know which bit Bob needs. Her one message must let Bob find any bit he could ask for. So the message must hold nearly all the bits, even when Bob is allowed to be wrong a third of the time.

## Definition

$$\mathrm{INDEX}_n(x, i) = x_i, \qquad x \in \{0,1\}^n,\ i \in [n].$$

The communication matrix has $2^n$ rows, one for each string, and $n$ columns. Column $i$ is the $i$-th coordinate of all strings.

**Instance:** a string $x \in \{0,1\}^n$, known only to Alice, and an index $i \in \{1, \ldots, n\}$, known only to Bob.

**Question:** what is $x_i$?

The interesting setting is the one-way model in which Alice sends one message and Bob outputs the answer. Unless the text says otherwise, "one-way" below means from Alice to Bob.

## Variants

- **Index from Bob to Alice.** Bob sends one message and Alice answers. Bob sends $i$ in $\lceil \log_2 n \rceil$ bits, which is optimal.
- **Augmented index.** Bob also knows the prefix $x_1, \ldots, x_{i-1}$. The one-way cost from Alice is still $\Omega(n)$ with public coins. This form arises when a stream is split so that the second half depends on the first, and it is exactly the problem in the round elimination lemma of Sen and Venkatesh.
- **Large alphabet.** Alice holds $x \in [q]^n$ and Bob must learn $x_i$. The one-way cost is $\Omega(n \log q)$ by the same argument.
- **Quantum one-way.** Alice may send qubits. Nayak (1999) proved that $(1 - H_2(\delta)) n$ qubits are still needed for error $\delta$, so a quantum message gives no saving here. These messages are called random access codes.

## Examples

**Small cases.** For $n = 3$ the matrix has 8 distinct rows and 3 distinct columns. A computation of all one-way protocols gives deterministic costs of 3 bits from Alice and 2 bits from Bob. The deterministic costs for larger $n$ are below.

| $n$ | one-way, Alice to Bob | one-way, Bob to Alice | two-way $D^{cc}$ |
|---|---|---|---|
| 3 | 3 | 2 | 3 |
| 8 | 8 | 3 | 4 |
| 16 | 16 | 4 | 5 |
| 1024 | 1024 | 10 | 11 |

The one-way cost from Alice is the base-2 logarithm of the number of distinct rows, $\log_2 2^n = n$; from Bob it is $\lceil \log_2 n \rceil$. The two-way cost is $\lceil \log_2 n \rceil + 1$.

**A run.** Let $x = 0110$ and $i = 3$. In the two-way protocol Bob sends $i - 1 = 2$ as the two bits $10$, and Alice answers $x_3 = 1$. Three bits are sent. In the one-way protocol Alice sends $0110$ and Bob reads the third bit.

## Known algorithms

- **Two-way.** Bob sends $i$ and Alice sends $x_i$: $\lceil \log_2 n \rceil + 1$ bits, deterministic.
- **One-way, deterministic.** Alice sends $x$: $n$ bits.
- **One-way, public coins, error $\delta$.** About $(1 - H_2(\delta)) n$ bits are enough. The players mask $x$ with a shared random string, permute the positions with a shared random permutation, and Alice sends the nearest word of a covering code of radius $\delta n$. The details are on the page [INDEX communication lower bound](/index-problem-lower-bound/). So the error allows only a constant-factor saving.

## Bounds

| Measure | Cost of $\mathrm{INDEX}_n$ | Method and source |
|---|---|---|
| $D^{cc}$, two-way | $\lceil \log_2 n \rceil + 1$ | upper bound above; lower bound by the rank method: the matrix and its complement both have rank $n$, so a protocol tree has at least $2n$ leaves |
| $R$, two-way, public or private coins | $\Theta(\log n)$ | lower bound by the discrepancy method through the embedding of inner product below |
| one-way from Alice, deterministic | $n$ | counting distinct rows: all $2^n$ rows differ |
| one-way from Alice, public coins, error $\delta$ | $(1 - H_2(\delta))\, n$, so about $0.0817\, n$ for $\delta = 1/3$ | an information argument, see [INDEX communication lower bound](/index-problem-lower-bound/); also Kremer, Nisan and Ron (1999) through the VC dimension |
| one-way from Alice, quantum, error $\delta$ | $(1 - H_2(\delta))\, n$ qubits | Nayak (1999), random access codes |
| augmented index, one-way from Alice | $\Omega(n)$ | [round elimination](/round-elimination/) in the form of Sen and Venkatesh |
| one-way from Bob | $\lceil \log_2 n \rceil$ deterministic, $\Theta(\log n)$ randomized | the two-way bounds |

The value $1 - H_2(1/3) \approx 0.0817$ comes from a direct computation. The round elimination lemma in the form of Sen and Venkatesh gives a weaker constant: a one-round protocol with $m$ bits and error $1/3$ needs $\tfrac12 \sqrt{2 m \ln 2 / n} \ge \tfrac12 - \tfrac13$, which is $m \ge n/(18 \ln 2) \approx 0.0801\, n$.

**Inner product inside index.** Let $n = 2^m$ and index the columns of $\mathrm{INDEX}_n$ by $y \in \{0,1\}^m$. For each $u \in \{0,1\}^m$ give Alice the string $x^{(u)}$ with $x^{(u)}_y = \langle u, y \rangle \bmod 2$. These rows and all columns form the matrix of [inner product](/inner-product-problem/) $\mathrm{IP}_m$. So every two-way protocol for $\mathrm{INDEX}_n$ solves $\mathrm{IP}_m$, and $R(\mathrm{INDEX}_n) \ge R(\mathrm{IP}_m) = \Omega(m) = \Omega(\log n)$, a bound that the discrepancy method gives for public coins.

**VC dimension.** The $n$ columns are shattered by the rows: every pattern of values on the $n$ indices is the row of some $x$. Kremer, Nisan and Ron (1999) proved that under product distributions the one-way randomized cost of any function is, up to constants, the VC dimension of its set of rows seen as functions of Bob's input. INDEX has the largest VC dimension possible for $n$ columns, so it is the hardest such function.

## Reductions

- **Index to disjointness.** Alice takes the set $A = \{j : x_j = 1\}$ and Bob takes $B = \{i\}$. Then $A \cap B = \emptyset$ exactly when $x_i = 0$. A one-way protocol for [disjointness](/disjointness-problem/) on $n$ elements gives one for $\mathrm{INDEX}_n$ at the same cost, so one-way randomized disjointness costs $\Omega(n)$. Two-way disjointness needs a separate proof, since two-way index is cheap.
- **Index to gap Hamming distance.** Jayram, Kumar and Sivakumar turned $x$ and $i$ into two strings, with shared random bits, whose Hamming distance is above or below half the length depending on $x_i$. This gives the one-way $\Omega(n)$ bound for the [gap Hamming distance problem](/gap-hamming-distance/), and from it the $\Omega(1/\varepsilon^2)$ space bounds for approximate counting in streams.
- **Index to streaming problems.** If Alice can write a stream from $x$ and Bob a continuation from $i$ such that the answer reveals $x_i$, then the memory of a one-pass streaming algorithm at the break is a one-way message. So the memory is $\Omega(n)$. See [INDEX communication lower bound](/index-problem-lower-bound/) and [frequency moment lower bounds](/frequency-moment-lower-bounds/).
- **Inner product to index.** The embedding above gives the two-way randomized bound.

## Applications

- **Streaming.** Exact [distinct elements](/distinct-elements-problem/), exact median, approximate [frequent items](/frequent-items-problem/) and many graph problems in one pass need large memory, by reductions from index or augmented index.
- **Sketches.** A [linear sketch](/linear-sketch/) is a one-way message, so the same reductions bound the size of sketches.
- **Data structures.** A static data structure answered with few cell probes gives a protocol in which the query side sends little. Asymmetric versions of index are the base cases for [round elimination](/round-elimination/) and for [cell probe lower bounds](/cell-probe-lower-bound/), as in the work of Miltersen, Nisan, Safra and Wigderson (1998).
- **Rounds.** Index separates one round from two rounds as strongly as possible: $\Omega(n)$ against $O(\log n)$. The [pointer chasing problem](/pointer-chasing-problem/) extends this to more rounds: with $k$ rounds it is cheap when the right player speaks first and expensive when the other player speaks first.

## References

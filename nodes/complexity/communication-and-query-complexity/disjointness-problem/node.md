---
tag: 3760MB
kind: problem
slug: disjointness-problem
name: Set disjointness problem
aliases:
- DISJ
- set intersection problem
area: complexity/communication-and-query-complexity
level: advanced
summary: "Alice and Bob hold subsets of an n-element set and decide if the sets are disjoint. D^cc = n + 1, the randomized cost is Theta(n) and the quantum cost is Theta(sqrt n)."
prereqs: [communication-model, randomized-communication-complexity]
see_also: [equality-problem, inner-product-problem, corruption-bound, information-complexity, frequency-moment-lower-bounds, index-problem, quantum-communication-complexity, multiparty-communication-complexity]
sources:
  - paper: "Bala Kalyanasundaram and Georg Schnitger, The probabilistic communication complexity of set intersection, SIAM Journal on Discrete Mathematics 5(4) (1992), 545-557"
    locator: the first proof that randomized protocols for disjointness need Omega(n) bits
  - paper: "Alexander A. Razborov, On the distributional complexity of disjointness, Theoretical Computer Science 106(2) (1992), 385-390"
    locator: the hard distribution on sets of size about n/4 and the corruption argument that gives Omega(n)
  - paper: "Ziv Bar-Yossef, T. S. Jayram, Ravi Kumar and D. Sivakumar, An information statistics approach to data stream and communication complexity, Journal of Computer and System Sciences 68(4) (2004), 702-732"
    locator: the information complexity proof of the Omega(n) bound through the AND function; conference version FOCS 2002
  - paper: "Alexander A. Sherstov, Communication complexity theory: thirty-five years of set disjointness, Mathematical Foundations of Computer Science (MFCS 2014)"
    locator: the survey of the deterministic, nondeterministic, randomized, unbounded-error and multiparty bounds
  - paper: "Alexander A. Razborov, Quantum communication complexity of symmetric predicates, Izvestiya: Mathematics 67(1) (2003), 145-159"
    locator: the quantum lower bound Omega(sqrt n)
  - paper: "Scott Aaronson and Andris Ambainis, Quantum search of spatial regions, Theory of Computing 1(1) (2005), 47-79"
    locator: the quantum protocol with O(sqrt n) qubits
  - paper: "Mark Braverman, Ankit Garg, Denis Pankratov and Omri Weinstein, From information to exact communication, Proceedings of the 45th ACM Symposium on Theory of Computing (STOC 2013), 151-160"
    locator: the exact constant, about 0.4827 n bits for error tending to 0
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press, 2020
    locator: Chapter 6, Information (the randomized lower bound for disjointness)
---

In the set disjointness problem, Alice holds a set $x \subseteq [n] = \{1, \ldots, n\}$, Bob holds a set $y \subseteq [n]$, and they must decide whether $x \cap y = \emptyset$. It is the most used hard problem of [communication complexity](/communication-complexity/): deterministic protocols need $n + 1$ bits, randomized protocols still need $\Theta(n)$ bits, and only quantum protocols do better, with $\Theta(\sqrt{n})$ qubits. Lower bounds for streaming, distributed computing and data structures often start from a reduction from disjointness.

## In plain words

Alice and Bob each choose some numbers from a fixed list. They want to know if they chose a number in common. They live far apart and pay for every bit they send.

The obvious plan is for Alice to send her whole choice, one bit for each number of the list. For most questions, a plan with random choices and a small chance of error is much shorter than this. For this question it is not: any plan with random choices that is correct most of the time must still send a fixed fraction of the list. This is why so many lower bounds in other fields start from this question. A quantum plan can save more, but it still sends about the square root of the length of the list.

## Definition

Fix $n \ge 1$ and identify a set $x \subseteq [n]$ with its characteristic vector in $\{0,1\}^n$. The function is

$$\mathrm{DISJ}_n(x, y) = \begin{cases} 1 & \text{if } x_i y_i = 0 \text{ for every } i, \\ 0 & \text{otherwise.} \end{cases}$$

**Instance:** a set $x \subseteq [n]$, known only to Alice, and a set $y \subseteq [n]$, known only to Bob, both given as $n$-bit characteristic vectors.

**Question:** is $x \cap y = \emptyset$?

The model is the two-party [communication model](/communication-model/). The measure is the number of bits sent on the worst input, and both players must know the answer at the end. $D^{cc}(\mathrm{DISJ}_n)$ is the deterministic cost. $R(\mathrm{DISJ}_n)$ is the cost of a protocol that errs with probability at most $1/3$ on every input. Private and public coins give the same order $\Theta(n)$ here, by Newman's theorem, so the bounds below hold for both. $\mathrm{DISJ}_n$ is the AND of $n$ copies of the function $\mathrm{NAND}(x_i, y_i)$; equivalently, $1 - \mathrm{DISJ}_n$ is the OR of the $n$ bits $x_i \wedge y_i$.

## Variants

- **Intersection (the complement).** The question "do the sets meet?" has the same deterministic and randomized costs. Its nondeterministic cost is much smaller, because one common element is a short proof.
- **Unique disjointness.** A promise problem: either the sets are disjoint, or they meet in exactly one element. Every lower bound below holds already for this promise, because the hard distributions put weight only on such pairs.
- **Sparse sets.** Both sets have at most $k$ elements. Håstad and Wigderson (2007) gave a randomized protocol with $O(k)$ bits, and $\Omega(k)$ bits are needed.
- **Many players.** With $k$ players, the question is whether some element lies in every set. In the [number-in-hand model](/number-in-hand-model/) each player sees its own set; in the [number-on-forehead model](/number-on-forehead-model/) each player sees all sets but its own. See [multiparty communication complexity](/multiparty-communication-complexity/).
- **Product distributions.** If $x$ and $y$ are drawn independently, the distributional cost falls to about $\sqrt{n}$; see Bounds.

## Examples

For $n = 1$ the communication matrix, with rows $x = 0, 1$ and columns $y = 0, 1$, is

$$M_1 = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix},$$

and $M_{\mathrm{DISJ}_n}$ is the Kronecker product of $n$ copies of $M_1$, because $\mathrm{DISJ}_n$ is the product of the bits $\mathrm{NAND}(x_i, y_i)$. Since $M_1$ has rank 2, $M_{\mathrm{DISJ}_n}$ has full rank $2^n$ over the reals.

Take $n = 3$, $x = \{1, 3\}$ (the vector $101$) and $y = \{2\}$ (the vector $010$). The sets are disjoint, so $\mathrm{DISJ}_3(x, y) = 1$. For $y' = \{2, 3\}$ (the vector $011$) the sets share the element 3, so $\mathrm{DISJ}_3(x, y') = 0$.

For $n = 3$ a direct computation gives $\operatorname{rank}(M) = 8$ and $\operatorname{rank}(J - M) = 7$, where $J$ is the all-ones matrix. Any protocol tree needs at least $\operatorname{rank}(M)$ leaves with output 1 and $\operatorname{rank}(J - M)$ leaves with output 0, so at least 15 leaves, and its depth is at least $\lceil \log_2 15 \rceil = 4 = n + 1$. The same computation for $n = 1, \ldots, 4$ gives $2^n + (2^n - 1)$ leaves each time.

The pairs $(A, \bar{A})$, where $\bar{A}$ is the complement of $A$, form a fooling set of size $2^n$: each pair is disjoint, and for $A \ne B$ one of $A \cap \bar{B}$ and $B \cap \bar{A}$ is not empty. This is the classic example on the [fooling set method](/fooling-set-method/) page.

## Known algorithms

- **Trivial protocol.** Alice sends $x$ and Bob sends the answer: $n + 1$ bits, deterministic and optimal.
- **Nondeterministic protocol for intersection.** A prover names a common element $i$, and the players check $x_i = y_i = 1$: $\lceil \log_2 n \rceil$ bits for the name of $i$. See [nondeterministic communication complexity](/nondeterministic-communication-complexity/).
- **Quantum protocol.** Buhrman, Cleve and Wigderson (1998) ran Grover search over $i$ with the players exchanging the query registers, which gives $O(\sqrt{n} \log n)$ qubits; Aaronson and Ambainis (2005) removed the log factor, $O(\sqrt{n})$. See [quantum communication complexity](/quantum-communication-complexity/) and [Grover search](/grover-search/).
- **Sparse sets.** For sets of size at most $k$, a public-coin protocol with $O(k)$ bits (Håstad and Wigderson 2007).
- **Unbounded error.** A private-coin protocol with $\lceil \log_2 n \rceil + 1$ bits from Alice and success probability above $1/2$ on every input. Alice sends a random index $i$ and the bit $x_i$. Bob outputs 0 if $x_i = y_i = 1$, and otherwise outputs 1 with probability $n/(2n - 1)$. On a disjoint pair Bob outputs 1 with probability $n/(2n-1) > 1/2$. On a pair with $t \ge 1$ common elements he outputs 1 with probability $(1 - t/n) \cdot n/(2n-1) \le (n-1)/(2n-1) < 1/2$. For $n = 3$ these probabilities are $3/5$ and at most $2/5$.

## Bounds

All bounds are for the two-party model with both players informed, unless the row says otherwise.

| Measure | Cost of $\mathrm{DISJ}_n$ | Method and source |
|---|---|---|
| $D^{cc}$ | $n + 1$ | fooling set of size $2^n$ plus one 0-leaf, or the rank bound with $2^n + 2^n - 1$ leaves |
| $N^1$ (proving disjointness) | $n$ | the same fooling set: every cover of the 1-entries by 1-rectangles has $2^n$ rectangles |
| $N^0$ (proving intersection) | $\lceil \log_2 n \rceil$ | the $n$ rectangles $\{x_i = 1\} \times \{y_i = 1\}$ cover the 0-entries |
| $R$, public or private coins | $\Theta(n)$ | Kalyanasundaram and Schnitger 1992; Razborov 1992 by the [corruption bound](/corruption-bound/); Bar-Yossef, Jayram, Kumar and Sivakumar 2004 by [information complexity](/information-complexity/) |
| distributional, product distributions | $O(\sqrt{n} \log n)$, and $\Omega(\sqrt{n})$ for one product distribution | Babai, Frankl and Simon 1986, by corruption |
| error tending to 0 | $C_{\mathrm{DISJ}}\, n \pm o(n)$ with $C_{\mathrm{DISJ}} \approx 0.4827$ | Braverman, Garg, Pankratov and Weinstein 2013, by information complexity |
| quantum, bounded error | $\Theta(\sqrt{n})$ | upper bound Aaronson and Ambainis 2005; lower bound Razborov 2003 |
| unbounded error | $\log_2 n \pm O(1)$ | the protocol above; lower bound by the characterization of Paturi and Simon 1986 and a shattering argument, see [sign rank](/sign-rank/) |
| one-way, randomized | $\Theta(n)$ | the reduction from the [index problem](/index-problem/) below |
| number-on-forehead, $k$ players, randomized | $\Omega(\sqrt{n} / (2^k k))$ | Sherstov, as surveyed in Sherstov 2014 |

Three points need care.

**Why the deterministic bounds do not settle the randomized case.** Equality also has a fooling set of size $2^n$ and full rank, yet its public-coin cost is $O(1)$. A randomized lower bound must therefore use a method that allows a few errors in each rectangle.

**Why discrepancy fails.** The 0-entries of $M_{\mathrm{DISJ}_n}$ lie in the $n$ rectangles $\{x_i = 1\} \times \{y_i = 1\}$. For any distribution $\mu$, either one of these 0-rectangles or the whole matrix has discrepancy at least $1/(2n + 1)$, so the [discrepancy method](/discrepancy-method/) gives only $O(\log n)$ for disjointness.

**Why the hard distribution is not a product.** Babai, Frankl and Simon showed that under every product distribution there is a protocol with $O(\sqrt{n} \log n)$ bits. So Razborov's distribution must correlate $x$ and $y$. It puts weight $3/4$ on disjoint pairs and $1/4$ on pairs that meet in exactly one element, with $|x| = |y| = \lfloor n/4 \rfloor$ in both cases. Razborov showed that every rectangle that is large under this distribution has a constant fraction of its weight on intersecting pairs, and the corruption bound turns this into $\Omega(n)$.

## Reductions

- **From equality.** $\mathrm{EQ}_n$ reduces to $\mathrm{DISJ}_{2n}$ with no communication: Alice forms $(x, \bar{x})$ and Bob forms $(\bar{y}, y)$. The sets are disjoint exactly when $x = y$. See the [equality problem](/equality-problem/). This gives the deterministic bound, but no useful randomized bound.
- **From index.** $\mathrm{INDEX}_n$ reduces to $\mathrm{DISJ}_n$ with no communication: Alice keeps her string $x$ as a set, and Bob, who holds $i$, takes the set $\{i\}$. The sets are disjoint exactly when $x_i = 0$. The reduction keeps the direction of a one-way protocol, so one-way protocols from Alice to Bob for disjointness need $\Omega(n)$ bits, by the [index problem lower bound](/index-problem-lower-bound/).
- **To streaming problems.** Alice runs a streaming algorithm on her set, sends its memory to Bob, and Bob continues on his set. An algorithm with $s$ bits of memory and $p$ passes gives a protocol with $(2p - 1) s$ bits. In the stream of the elements of $x$ followed by the elements of $y$, the maximum frequency $F_\infty$ is 2 exactly when the sets meet. So computing $F_\infty$ exactly needs $\Omega(n/p)$ bits of memory in $p$ passes. The multiparty form of disjointness gives the bounds for the frequency moments $F_k$. See [frequency moment lower bounds](/frequency-moment-lower-bounds/) and the [streaming model](/streaming-model/).
- **To distributed graph problems.** Graph gadgets in which two parts of the network hold $x$ and $y$ turn a fast algorithm in the [CONGEST model](/congest-model/) into a short protocol for disjointness. This gives the round lower bounds of the [distributed diameter lower bound](/diameter-lower-bound-distributed/) and the [Peleg and Rubinovich lower bound](/peleg-rubinovich-lower-bound/).

## Applications

- **Streaming.** Space lower bounds for frequency moments, for the maximum frequency and for [triangle counting in streams](/streaming-triangle-counting-problem/).
- **Distributed computing.** Round lower bounds in CONGEST for diameter, minimum spanning tree verification and related problems.
- **Data structures and proof systems.** Rao and Yehudayoff (Part II of their book) use disjointness and its variants for lower bounds on data structures, on the extension complexity of polytopes and on proof systems.
- **A test case for methods.** Fooling sets, rank, discrepancy, corruption, information and the polynomial method all give different answers on disjointness. The problem shows which method measures what.

## References

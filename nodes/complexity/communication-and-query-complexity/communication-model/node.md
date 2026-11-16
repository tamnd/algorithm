---
tag: RCH7J5
kind: model
slug: communication-model
name: Two-party communication model
aliases:
- Yao's communication model
- two-party protocol model
area: complexity/communication-and-query-complexity
level: intro
summary: Alice holds x and Bob holds y. They send bits to each other by a fixed protocol until both know f(x, y). Only the bits count, and local computation is free.
prereqs: [communication-complexity, boolean-function]
see_also: [deterministic-communication-complexity, communication-matrix, randomized-communication-complexity, nondeterministic-communication-complexity, one-way-communication-complexity, simultaneous-message-model, multiparty-communication-complexity, query-model]
sources:
  - paper: doi:10.1145/800135.804414
    title: "Andrew Chi-Chih Yao, Some complexity questions related to distributive computing (preliminary report), Proceedings of the 11th Annual ACM Symposium on Theory of Computing (STOC 1979), pages 209-213"
    locator: the definition of the two-party model, in which the players send bits in turn to compute f(i, j)
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press, 1997
    locator: Chapter 1, Basics (Section 1.1, The Model, and Section 1.2, Rectangles)
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press, 2020
    locator: Chapter 1, Deterministic Protocols (protocols as trees and the section Rectangles)
---

The two-party communication model is the model of computation behind [communication complexity](/communication-complexity/). Two players, Alice and Bob, hold the two halves $x$ and $y$ of an input, and they must compute $f(x, y)$ by sending bits to each other by a fixed protocol. The cost of a protocol is the number of bits sent, and the players can do any local computation for free. Yao defined the model in 1979; this page defines the machine, and the pages on [deterministic](/deterministic-communication-complexity/), [randomized](/randomized-communication-complexity/) and [nondeterministic](/nondeterministic-communication-complexity/) communication complexity define the numbers measured on it.

## The machine

There are three finite sets $X$, $Y$ and $Z$ and a function $f : X \times Y \to Z$. Alice gets $x \in X$ and Bob gets $y \in Y$. Both know $f$, but each one sees only their own input. In most examples $X = Y = \{0,1\}^n$ and $Z = \{0,1\}$, and $f$ is a [Boolean function](/boolean-function/) of $2n$ bits whose input is cut into two halves.

A deterministic **protocol** $P$ is a rooted binary tree with these labels:

- Each inner node $v$ belongs to Alice or to Bob. An Alice node has a function $a_v : X \to \{0,1\}$, and a Bob node has a function $b_v : Y \to \{0,1\}$. The value is the bit that the owner sends. The edge labeled 0 goes to the left child and the edge labeled 1 to the right child.
- Each leaf has an output value in $Z$.

The run on the input $(x, y)$ starts at the root. At an Alice node, Alice sends $a_v(x)$ and both players move to the child with that label; at a Bob node, Bob sends $b_v(y)$ in the same way. The run stops at a leaf $\ell(x, y)$. The sequence of bits sent is the **transcript**, and it names the leaf. The protocol **computes** $f$ if the leaf $\ell(x, y)$ has the output $f(x, y)$ for every pair. Both players see every bit, so at the end both know the transcript and the output.

The order of the speakers can depend on the bits sent so far, and a player can send many bits in a row. A message of $k$ bits is a path of $k$ nodes of the same owner. The number of **rounds** is the number of times the speaker changes, plus one.

**Rectangles.** A **combinatorial rectangle** is a set $A \times B$ with $A \subseteq X$ and $B \subseteq Y$. The inputs that reach a node $v$ form a rectangle $R_v = A_v \times B_v$. At the root this is $X \times Y$. If $v$ is an Alice node, its children get $\{x \in A_v : a_v(x) = 0\} \times B_v$ and $\{x \in A_v : a_v(x) = 1\} \times B_v$, which are again rectangles; a Bob node splits $B_v$ in the same way. So the leaves of a protocol cut $X \times Y$ into disjoint rectangles, and the protocol computes $f$ only if $f$ is constant on each leaf rectangle. Such a rectangle is **monochromatic**. This is the main structural fact of the model. In the [communication matrix](/communication-matrix/) $M_f$, a rectangle is a set of rows times a set of columns, not always next to each other.

## What it counts

The **cost** of a protocol is the depth of its tree, the length of the longest transcript. Only the bits count. The time and memory of the players are free, and their functions $a_v$ and $b_v$ can be as hard to compute as we like. A lower bound in the model is therefore a statement about information, not about computation.

The [deterministic communication complexity](/deterministic-communication-complexity/) $D^{cc}(f)$ is the least cost of a protocol that computes $f$. Every $f$ has the trivial protocol in which Alice sends $x$ and Bob replies with $f(x, y)$, so

$$D^{cc}(f) \le \lceil \log_2 |X| \rceil + \lceil \log_2 |Z| \rceil,$$

which is $n + 1$ for a Boolean function on $\{0,1\}^n \times \{0,1\}^n$.

A protocol of cost $c$ has at most $2^c$ leaves, so it cuts $X \times Y$ into at most $2^c$ monochromatic rectangles. Every lower bound method for deterministic protocols starts from this fact. The [fooling set method](/fooling-set-method/) and the [log-rank lower bound](/log-rank-lower-bound/) are the two simplest.

The standard variants change the machine in one place each. The page of each variant gives the details.

- **Who must know the answer.** The usual convention, used on this site, is that both players know $f(x, y)$ at the end. Some texts ask only that the last receiver knows it. The two costs differ by at most $\lceil \log_2 |Z| \rceil$ bits. For the [equality problem](/equality-problem/) this is the difference between $n + 1$ and $n$.
- **Randomness.** In a randomized protocol the functions at the nodes also depend on random bits. With **private coins**, each player has their own random string; with **public coins**, both see one shared random string. The protocol must give $f(x, y)$ with probability at least $2/3$ on every input. See [randomized communication complexity](/randomized-communication-complexity/).
- **Nondeterminism.** A prover who sees both inputs gives the players a certificate, and the players accept by checking it. See [nondeterministic communication complexity](/nondeterministic-communication-complexity/).
- **Fewer rounds.** In a **one-way** protocol, Alice sends one message and Bob answers. See [one-way communication complexity](/one-way-communication-complexity/). In the [simultaneous message model](/simultaneous-message-model/), each player sends one message to a referee who sees neither input.
- **More players.** With $k \ge 3$ players, the input is cut into $k$ parts. In the [number-in-hand model](/number-in-hand-model/), each player sees their own part. In the [number-on-forehead model](/number-on-forehead-model/), each player sees all parts but their own. See [multiparty communication complexity](/multiparty-communication-complexity/).
- **Quantum.** The players send qubits and may share entanglement. See [quantum communication complexity](/quantum-communication-complexity/).

## Relation to other models

- [Query model](/query-model/). A query algorithm reads one bit of a single input per step. A communication protocol may send any function of a whole half of the input in one bit, so it is much stronger per step. A decision tree of depth $d$ for $g(x \wedge y)$ or $g(x \oplus y)$ gives a protocol of cost $2d$, since each query costs two bits. Lifting theorems go the other way for some gadgets and turn query lower bounds into communication lower bounds.
- [Streaming model](/streaming-model/). A one-pass streaming algorithm with $s$ bits of memory gives a one-way protocol of cost $s$: Alice runs the algorithm on the first part of the stream and sends the memory to Bob. With $p$ passes it gives a protocol of cost $(2p - 1)s$. So communication lower bounds, such as the [lower bound for INDEX](/index-problem-lower-bound/), are space lower bounds for streaming.
- [Cell-probe model](/cell-probe-model/). A data structure query that makes $t$ probes into a table of $s$ cells of $w$ bits gives a protocol in which Alice (the query) sends $t \lceil \log_2 s \rceil$ bits and Bob (the table) sends $tw$ bits. Lower bounds for such asymmetric protocols give cell-probe lower bounds.
- [Boolean circuits](/boolean-circuit/). The depth of a circuit for $f$ equals the communication complexity of the [Karchmer-Wigderson relation](/karchmer-wigderson-relation/) of $f$, as the [Karchmer-Wigderson theorem](/karchmer-wigderson-theorem/) states.
- VLSI chips. Yao's original motive was the cost of moving bits between the two halves of a chip. A chip of area $A$ that runs for $T$ steps sends $O(\sqrt{A}\,T)$ bits across a cut, so a communication lower bound $C$ gives $A T^2 = \Omega(C^2)$.

## Known results in the model

All the results below are for the two-way model on $n$-bit inputs, where both players must know the answer.

- Every Boolean $f$ has $D^{cc}(f) \le n + 1$. The [equality problem](/equality-problem/), the [greater-than problem](/greater-than-problem/), [disjointness](/disjointness-problem/) and [inner product](/inner-product-problem/) all need exactly $n + 1$ bits deterministically. For $n = 1, 2, 3$, an exhaustive search over all protocol trees confirms the value $n + 1$ for all four.
- Rectangle bounds. A fooling set of size $s$ gives $D^{cc}(f) \ge \lceil \log_2 s \rceil$. Mehlhorn and Schmidt (1982) proved $D^{cc}(f) \ge \log_2 \operatorname{rank}(M_f)$, with the rank over the reals. The [log-rank conjecture](/log-rank-conjecture/) asks whether a polynomial in $\log_2 \operatorname{rank}(M_f)$ is also an upper bound.
- Randomness helps. The [randomized equality testing protocol](/equality-testing-protocol/) solves equality with $O(\log n)$ bits and private coins, and $O(1)$ bits suffice with public coins. Newman (1991) showed that private coins cost at most $O(\log n)$ more bits than public coins.
- Randomness does not help for every function. Disjointness and inner product need $\Omega(n)$ bits even with public coins and error $1/3$; see the [discrepancy method](/discrepancy-method/) and the [corruption bound](/corruption-bound/).
- Determinism against nondeterminism. If $N^0(f)$ and $N^1(f)$ are the nondeterministic costs of $f$ and of its negation, then $D^{cc}(f) = O(N^0(f) N^1(f))$ (Aho, Ullman and Yannakakis, 1983). Equality has $N^0 = O(\log n)$ but $N^1 = n$.
- Rounds matter. For the [index problem](/index-problem/), where Alice has $x \in \{0,1\}^n$ and Bob has an index $i$, a one-way protocol from Alice to Bob needs $\Omega(n)$ bits even with randomness, while Bob can send $i$ in $\lceil \log_2 n \rceil$ bits and Alice can answer with one more bit. The [pointer chasing problem](/pointer-chasing-problem/) shows the same kind of gap for every number of rounds.

## References

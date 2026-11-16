---
tag: 1PAA6M
kind: model
slug: simultaneous-message-model
name: Simultaneous message model
aliases:
- simultaneous communication model
area: complexity/communication-and-query-complexity
level: advanced
summary: "Alice and Bob each send one message to a referee, who sees neither input and outputs f(x,y). With private coins equality costs Theta(sqrt n); with public coins it costs O(1)."
prereqs: [communication-model, one-way-communication-complexity]
see_also: [one-way-communication-complexity, equality-problem, fingerprinting, linear-sketch, quantum-communication-complexity, multiparty-communication-complexity, direct-sum-communication, information-complexity]
sources:
  - paper: "Ilan Newman and Mario Szegedy, Public vs. private coin flips in one round communication games, Proceedings of the 28th ACM Symposium on Theory of Computing (STOC 1996), 561-570"
    locator: the Omega(sqrt n) lower bound for equality with private coins in the simultaneous model
  - paper: "László Babai and Peter G. Kimmel, Randomized simultaneous messages: solution of a problem of Yao in communication complexity, Proceedings of the 12th IEEE Conference on Computational Complexity (CCC 1997)"
    locator: for every function the private-coin simultaneous cost is at least of order the square root of the deterministic simultaneous cost
  - paper: "Harry Buhrman, Richard Cleve, John Watrous and Ronald de Wolf, Quantum fingerprinting, Physical Review Letters 87(16) (2001), 167902"
    locator: equality with O(log n) qubits in the simultaneous model without shared randomness
  - paper: "Amit Chakrabarti, Yaoyun Shi, Anthony Wirth and Andrew Chi-Chih Yao, Informational complexity and the direct sum problem for simultaneous message complexity, Proceedings of the 42nd IEEE Symposium on Foundations of Computer Science (FOCS 2001)"
    locator: the direct sum theorem in the simultaneous model, proved through information cost
  - paper: "Andrew Chi-Chih Yao, Some complexity questions related to distributive computing, Proceedings of the 11th ACM Symposium on Theory of Computing (STOC 1979), 209-213"
    locator: the paper that introduced the communication model and asked about equality with simultaneous messages
---

In the simultaneous message model, Alice and Bob do not talk to each other. Each sends one message to a third party, the referee, who knows neither input and must output $f(x, y)$ from the two messages alone. It is the weakest of the usual two-party models, below [one-way communication](/one-way-communication-complexity/). The kind of randomness matters more here than anywhere else: [equality](/equality-problem/) costs $2n$ bits deterministically, $\Theta(\sqrt{n})$ with private coins, $O(1)$ with public coins, and $O(\log n)$ qubits with quantum messages and no shared randomness.

## The machine

There are three parties. Alice holds $x \in X$, Bob holds $y \in Y$, and the referee holds nothing.

- Alice computes a message $m_A(x, r_A)$ and Bob computes a message $m_B(y, r_B)$, at the same time, so that neither message depends on the other one.
- The referee sees $m_A$ and $m_B$ and outputs a bit.
- **Private coins:** $r_A$ and $r_B$ are independent random strings, seen only by their owners. The referee may also flip coins.
- **Public coins:** Alice and Bob share one random string $r = r_A = r_B$. In the usual definition the referee does not need to see it, since the players can copy what he needs into their messages.
- **Quantum:** the messages are quantum states, and the referee measures them.

A protocol computes $f$ with error $\varepsilon$ if, for every input, the referee outputs $f(x, y)$ with probability at least $1 - \varepsilon$. The model is also called SMP, for simultaneous message passing. It extends to $k$ players, each sending one message to the referee, both when each player sees its own input (number in hand) and when each player sees all inputs but its own ([number on forehead](/multiparty-communication-complexity/)).

## What it counts

The cost of a protocol is $|m_A| + |m_B|$, the total length of the two messages in the worst case.

- $D^{\|}(f)$: the least cost of a deterministic protocol.
- $R^{\|, \mathrm{priv}}(f)$ and $R^{\|, \mathrm{pub}}(f)$: the least cost with error $1/3$ and private or public coins.
- $Q^{\|}(f)$: the least number of qubits with error $1/3$, with no shared randomness or entanglement unless stated.

**Exact deterministic cost.** Let $r(f)$ and $c(f)$ be the numbers of distinct rows and columns of the [communication matrix](/communication-matrix/). Then

$$D^{\|}(f) = \lceil \log_2 r(f) \rceil + \lceil \log_2 c(f) \rceil.$$

Alice sends the number of her row class and Bob the number of his column class, and the referee looks up the entry. For the lower bound, if two inputs of Alice with different rows sent the same message, there is a column $y$ where the rows differ, and the referee sees the same pair of messages on both inputs. So Alice needs $r(f)$ messages, and Bob likewise needs $c(f)$.

## Relation to other models

- **Against one-way.** Each simultaneous protocol gives a one-way protocol in both directions: Alice sends $m_A$ to Bob, who plays the referee. So $R^{\|} \ge R^{A \to B}$ and $R^{\|} \ge R^{B \to A}$ for each kind of coins. Deterministically $D^{\|}(f) = D^{A \to B}(f) + D^{B \to A}(f)$ by the two exact formulas.
- **Private against public coins.** The gap is largest here. In two-way and one-way models, Newman's theorem says that private coins cost only $O(\log n)$ more bits than public coins. That proof fails in the simultaneous model, because the players cannot agree on which shared string to use without talking. For equality the gap is $\Theta(\sqrt{n})$ against $O(1)$.
- **Square-root rule.** Babai and Kimmel (1997) proved that for every function $R^{\|, \mathrm{priv}}(f) = \Omega(\sqrt{D^{\|}(f)})$. So private coins can save at most a square root over determinism, and equality shows that this saving is possible.
- **Sketches.** A sketch of $x$ and a sketch of $y$ made with shared randomness, followed by a function of the two sketches, is a public-coin simultaneous protocol. So lower bounds in this model are lower bounds on the size of [linear sketches](/linear-sketch/) and other sketches that are combined after the fact.
- **Quantum.** Quantum messages beat private coins: $Q^{\|}(\mathrm{EQ}_n) = O(\log n)$ against $R^{\|, \mathrm{priv}}(\mathrm{EQ}_n) = \Theta(\sqrt{n})$.

## Known results in the model

**Equality, deterministic.** All $2^n$ rows and all $2^n$ columns of $\mathrm{EQ}_n$ differ, so $D^{\|}(\mathrm{EQ}_n) = 2n$. For $n = 3$ the two exact formulas give 3 and 3, total 6.

**Equality, public coins.** Alice and Bob take $k$ shared random strings $s_1, \ldots, s_k \in \{0,1\}^n$ and send the bits $\langle x, s_j \rangle \bmod 2$ and $\langle y, s_j \rangle \bmod 2$. The referee says "equal" if all $k$ pairs agree. If $x \ne y$, each pair agrees with probability $1/2$, so $k = 2$ gives error $1/4$ with 4 bits in total. So $R^{\|, \mathrm{pub}}(\mathrm{EQ}_n) = O(1)$.

**Equality, private coins: $\Theta(\sqrt{n})$.**

*Upper bound.* Fix an error-correcting code $C : \{0,1\}^n \to \{0,1\}^{L}$ with $L = O(n)$ and relative distance a constant $\delta > 0$, and write each codeword as a $\sqrt{L} \times \sqrt{L}$ grid. Alice sends a random row number and that row of $C(x)$. Bob sends a random column number and that column of $C(y)$. The referee compares the two bits where the row and the column cross. If $x = y$ they always agree. If $x \ne y$, the crossing point is a uniform random cell, so the bits differ with probability at least $\delta$. A constant number of repetitions gives error $1/3$, with $O(\sqrt{n})$ bits in total. The model uses private coins only: each player picks its own row or column.

*A small run.* Take $n = 4$ and the [Hadamard code](/hadamard-code/) of length 16 on a $4 \times 4$ grid, which has relative distance $1/2$. Each message is 2 bits for the index and 4 bits for the line, 6 bits in all. For $x = 0110$ the codeword is $0011\,1100\,0011\,1100$, and for $y = 0111$ it is $0110\,1001\,0110\,1001$. If Alice picks row 0 and Bob picks column 1, the referee reads bit 0 from Alice's row $0011$ and bit 1 from Bob's column $(1, 0, 1, 0)$, so he answers "not equal". A check of all pairs $x \ne y$ shows that the least detection probability is exactly $1/2$, so two independent repetitions give error $1/4$. For $n = 4$ this is longer than sending $x$; the saving appears only for large $n$, where a code of length $O(n)$ is used.

*Lower bound.* Newman and Szegedy (1996) proved $R^{\|, \mathrm{priv}}(\mathrm{EQ}_n) = \Omega(\sqrt{n})$. Babai and Kimmel (1997) gave the general bound above, and showed that the product of the two message lengths must be $\Omega(n)$ for equality. Both answer a question that goes back to Yao (1979).

**Equality, quantum.** Buhrman, Cleve, Watrous and de Wolf (2001) sent the quantum state $\frac{1}{\sqrt{L}} \sum_j |j\rangle |C(x)_j\rangle$, of $O(\log n)$ qubits, and the referee compares the two states with a swap test. This is quantum fingerprinting, $Q^{\|}(\mathrm{EQ}_n) = O(\log n)$.

**Hard functions.** Every lower bound for two-way or one-way protocols also holds here. So [inner product](/inner-product-problem/), [disjointness](/disjointness-problem/) and the [gap Hamming distance](/gap-hamming-distance/) problem need $\Omega(n)$ bits even with public coins, and [index](/index-problem/) needs $\Omega(n)$ because Alice's message alone must serve the referee for every index.

**Direct sum.** Chakrabarti, Shi, Wirth and Yao (2001) defined the information cost of simultaneous protocols and used it to prove a direct sum theorem in this model with private coins, for a class of functions that includes equality: solving $k$ copies needs about $k$ times the cost of one copy. This was the start of [information complexity](/information-complexity/) and of the [direct sum](/direct-sum-communication/) results for two-way protocols.

## References

---
tag: 323MZ9
kind: concept
slug: communication-complexity
name: Communication complexity
aliases:
- two-party communication complexity
area: complexity/communication-and-query-complexity
level: intro
summary: The study of how many bits two or more parties must exchange to compute a function when each one sees only part of the input. Its lower bounds transfer to streaming, data structures and circuits.
prereqs: [boolean-function, asymptotic-notation]
see_also: [communication-model, deterministic-communication-complexity, randomized-communication-complexity, communication-matrix, equality-problem, disjointness-problem, streaming-model, query-complexity]
sources:
  - paper: doi:10.1145/800135.804414
    title: "Andrew Chi-Chih Yao, Some complexity questions related to distributive computing (preliminary report), Proceedings of the 11th Annual ACM Symposium on Theory of Computing (STOC 1979), pages 209-213"
    locator: the paper that started the field
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press, 1997
    locator: Chapters 1 to 3 (the two-party model, covers and nondeterminism, randomization), and Part II for the applications
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press, 2020
    locator: Part I, Communication Complexity (Chapters 1 to 3 for deterministic and randomized protocols), and Part II, Applications
---

Communication complexity is the field that asks how many bits Alice, who holds $x$, and Bob, who holds $y$, must exchange to compute $f(x, y)$, when their local computation is free. It began with Yao's 1979 paper, and its lower bounds give many lower bounds in other models, such as streaming space, data structure query time and circuit depth. This page gives the idea and a map of the field. The machine is defined on the [communication model](/communication-model/) page, and the main measure, the least worst-case number of bits of a deterministic protocol, is on the [deterministic communication complexity](/deterministic-communication-complexity/) page.

## In plain words

Two people each hold half of a puzzle. Neither can see the other half. They can talk only by sending bits, and they want to agree on the answer. How few bits are enough?

Each person may think as long as they like for free. Only the talk counts. So the question is not about speed. It is about how much one person must learn about the other half.

Some questions need almost the whole half to be sent. Others need very little, especially if the two people may flip coins and accept a small chance of a wrong answer. The surprise is how often the best answer can be proved exactly.

Because only talk counts, a proof that a question needs a lot of talk is strong. It shows that other kinds of machines must also do a lot of work, wherever information has to cross between two parts.

## The idea

**The setting.** A function $f : X \times Y \to Z$ is given. Alice gets $x \in X$, Bob gets $y \in Y$, and they follow a protocol: a fixed rule that says who speaks next and what bit they send, based on their own input and the bits sent so far. When the protocol stops, both know $f(x, y)$. The cost is the number of bits sent on the worst input. The [communication model](/communication-model/) page gives the formal definition as a protocol tree.

**The trivial bound.** Alice can always send all of $x$, and Bob can reply with the answer. For Boolean functions on $n$-bit inputs this costs $n + 1$ bits. The interesting questions are which functions need nearly this much, and which need much less.

**Rectangles.** The inputs that give a fixed transcript form a combinatorial rectangle $A \times B$, a set of rows times a set of columns of the [communication matrix](/communication-matrix/) $M_f$. A protocol of cost $c$ therefore cuts the matrix into at most $2^c$ rectangles on which $f$ is constant. Lower bounds come from showing that $M_f$ cannot be cut into few such rectangles. The [fooling set method](/fooling-set-method/) finds many inputs that no rectangle can share, and the [log-rank lower bound](/log-rank-lower-bound/) uses the rank of $M_f$ over the reals.

**The measures.** Each kind of protocol gives a measure of $f$:

- [Deterministic communication complexity](/deterministic-communication-complexity/), $D^{cc}(f)$: the protocol is always correct. The superscript separates it from the decision tree depth $D^{dt}(f)$ of the [query model](/query-model/).
- [Randomized communication complexity](/randomized-communication-complexity/), $R(f)$: the players flip coins, and the protocol is correct with probability at least $2/3$ on each input. The coins can be private or public.
- [Nondeterministic communication complexity](/nondeterministic-communication-complexity/), $N^1(f)$: a prover who sees both inputs sends a certificate that $f(x, y) = 1$.
- [One-way communication complexity](/one-way-communication-complexity/): Alice sends one message and Bob answers. The [simultaneous message model](/simultaneous-message-model/) has both players send one message to a referee.
- [Information complexity](/information-complexity/): the information that the transcript reveals about the inputs, not its length.
- [Multiparty communication complexity](/multiparty-communication-complexity/) and [quantum communication complexity](/quantum-communication-complexity/) change the number of players or let them send qubits.

**The big open question.** The rank lower bound is close to tight for every known function. The [log-rank conjecture](/log-rank-conjecture/) says that $D^{cc}(f)$ is at most a polynomial in $\log_2 \operatorname{rank}(M_f)$. It has been open since 1988.

## Examples

The examples below use $n$-bit inputs, and the model in which both players learn the answer.

| Problem | Question | $D^{cc}$ | Randomized cost |
|---|---|---|---|
| [Equality](/equality-problem/) | is $x = y$? | $n + 1$ | $\Theta(\log n)$ private coins, $O(1)$ public coins |
| [Greater-than](/greater-than-problem/) | is $x > y$ as binary numbers? | $n + 1$ | $\Theta(\log n)$ |
| [Disjointness](/disjointness-problem/) | do the sets $x$ and $y$ share no element? | $n + 1$ | $\Theta(n)$ |
| [Inner product](/inner-product-problem/) | is $\sum_i x_i y_i$ odd? | $n + 1$ | $\Theta(n)$ |
| [Index](/index-problem/) | Bob has $i$: what is $x_i$? | $\lceil \log_2 n \rceil + 1$ | $\Theta(n)$ if only Alice may speak |

Equality shows the power of randomness: the [randomized equality testing protocol](/equality-testing-protocol/) compares short random fingerprints of the two strings. Disjointness and inner product show its limits: no protocol with error $1/3$ does much better than sending the whole input. Index shows the power of rounds: the cost depends on who may speak.

A small worked case is equality for $n = 2$. The matrix $M_{\mathrm{EQ}}$ is the $4 \times 4$ identity matrix. Its rank is 4, and the 1-entries and 0-entries together need at least 5 monochromatic rectangles, so every protocol has at least 5 leaves and cost at least $\lceil \log_2 5 \rceil = 3 = n + 1$.

## Where it is used

- **Streaming algorithms.** A streaming algorithm with $s$ bits of memory gives a one-way protocol with $s$ bits per pass, so the communication cost of a problem bounds the memory of every [streaming algorithm](/streaming-model/) for it. The [INDEX lower bound](/index-problem-lower-bound/) and the [frequency moment lower bounds](/frequency-moment-lower-bounds/) work this way.
- **Data structures.** In the [cell-probe model](/cell-probe-model/), a query that reads few cells of a large table is a protocol between the query and the table, so communication lower bounds give lower bounds on query time.
- **Circuit depth.** By the [Karchmer-Wigderson theorem](/karchmer-wigderson-theorem/), the depth of the best circuit for $f$ equals the communication complexity of a related search problem, the [Karchmer-Wigderson relation](/karchmer-wigderson-relation/). Lower bounds for monotone circuit depth come from this link.
- **VLSI and distributed computing.** The bits that cross a cut of a chip or a network bound its area and time, which was Yao's first motive.
- **Proof complexity, extended formulations and learning.** Many lower bounds in these fields reduce to a communication problem, often through rectangles and their covers.
- **Practice.** Comparing two remote copies of a file, a database or a set by short hashes is a direct use of the equality protocol and its variants.

## References

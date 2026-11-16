---
tag: 4ZJH2V
kind: concept
slug: multiparty-communication-complexity
name: Multiparty communication complexity
aliases:
- k-party communication complexity
area: complexity/communication-and-query-complexity
level: research
summary: "The communication cost for k players to compute a function of k inputs. The number-in-hand model gives streaming lower bounds; the number-on-forehead model is tied to circuit lower bounds."
prereqs: [communication-model]
see_also: [number-in-hand-model, number-on-forehead-model, frequency-moment-lower-bounds, streaming-model, disjointness-problem, inner-product-problem, ac0, deterministic-communication-complexity]
sources:
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press (1997)
    locator: Chapter 6, Multiparty communication complexity
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press (2020)
    locator: Chapter 4, Numbers on Foreheads
  - paper: doi:10.1145/800061.808737
    title: "Ashok K. Chandra, Merrick L. Furst and Richard J. Lipton, Multi-party protocols, 15th ACM Symposium on Theory of Computing (STOC 1983), pages 94-99"
    locator: the number-on-forehead model and its first lower bounds
  - paper: doi:10.1016/0022-0000(92)90047-M
    title: "László Babai, Noam Nisan and Mario Szegedy, Multiparty protocols, pseudorandom generators for logspace, and time-space trade-offs, Journal of Computer and System Sciences 45(2), 1992, pages 204-232"
    locator: the Omega(n/4^k) bound for the generalized inner product in the number-on-forehead model, and its uses
  - paper: doi:10.1007/BF01272517
    title: "Johan Håstad and Mikael Goldmann, On the power of small-depth threshold circuits, Computational Complexity 1(2), 1991, pages 113-129"
    locator: the NOF protocol for functions computed by a threshold gate over gates of small fan-in, and the resulting circuit lower bound from the bound for GIP
  - paper: doi:10.1006/inco.1994.1051
    title: "Vince Grolmusz, The BNS lower bound for multi-party protocols is nearly optimal, Information and Computation 112(1), 1994, pages 51-54"
    locator: the O(kn/2^k) protocol for the generalized inner product
  - paper: doi:10.1006/jcss.1997.1545
    title: "Noga Alon, Yossi Matias and Mario Szegedy, The space complexity of approximating the frequency moments, Journal of Computer and System Sciences 58(1), 1999, pages 137-147"
    locator: the reduction from k-party disjointness to frequency moments in the streaming model
  - paper: doi:10.4230/LIPIcs.STACS.2009.1846
    title: "André Gronemeier, Asymptotically optimal lower bounds on the NIH-multi-party information complexity of the AND-function and disjointness, 26th Symposium on Theoretical Aspects of Computer Science (STACS 2009), LIPIcs 3, pages 505-516"
    locator: the Omega(n/k) bound for k-party disjointness with a unique common element, in the number-in-hand model
---

Multiparty communication complexity is the study of how many bits $k$ players must exchange to compute a function $f(x_1, \ldots, x_k)$ when the inputs are spread over the players. It extends the two-party [communication model](/communication-model/) to $k \ge 3$ players. The answer depends a great deal on who sees which input. In the [number-in-hand model](/number-in-hand-model/) (NIH), player $i$ sees only $x_i$. In the [number-on-forehead model](/number-on-forehead-model/) (NOF), player $i$ sees every input except $x_i$. The two models answer different questions: NIH bounds give space lower bounds for streaming algorithms, and NOF bounds are tied to lower bounds for small-depth circuits.

## In plain words

Several people want to compute one answer together, and each of them holds part of the facts. They talk by writing on a shared board, and every symbol on the board costs one unit. The question is how many units they must pay. There are two very different games. In the first game, each person sees only the facts in their own hand. In the second game, each person has their facts written on their forehead, so they see the facts of all the others but not their own. In the second game the people know a lot, because each piece of fact is seen by everyone but one person. So it is much harder to prove that they must talk a lot. Such proofs are worth a great deal, because they give limits on some kinds of circuits.

## The idea

**Blackboard protocols.** The players write bits on a blackboard that all of them can read. At each step the bits on the board so far decide which player writes next, and that player's bit depends on the board and on the inputs that the player can see. The protocol ends when the board decides the output. The cost is the number of bits on the board in the worst case. As in the two-party case, a protocol is a tree, and $D^{cc}_k(f)$ is the least depth of a tree that always gives $f$. With randomness, $R^{cc}_k(f)$ is the cost with error at most $1/3$; the randomness is public unless the text says private. Some work uses **message passing** instead, where each message goes on a private channel between two players. A blackboard bit can cost up to $k - 1$ messages there, so bounds in the two settings can differ by a factor of about $k$.

**Two input models.**

| | Number in hand (NIH) | Number on forehead (NOF) |
|---|---|---|
| Player $i$ sees | $x_i$ | all $x_j$ with $j \ne i$ |
| Each input is seen by | one player | $k - 1$ players |
| Trivial protocol, $n$-bit inputs | $(k - 1)n + 1$ bits | $n + 1$ bits |
| Combinatorial object | rectangles $S_1 \times \cdots \times S_k$ | cylinder intersections |
| Main uses | streaming, distributed data | circuits, branching programs, proof systems |

For $k = 2$ both models are the usual two-party model: in NOF, Alice sees $x_2$ and Bob sees $x_1$, which is the two-party model with the names changed.

In NOF the trivial protocol is cheap because player 2 writes $x_1$ and then player 1 knows every input. The overlap of the inputs makes NOF protocols strong, and lower bounds hard. A set of inputs on which a NOF protocol gives one transcript is a **cylinder intersection**: an intersection $C_1 \cap \cdots \cap C_k$ where membership in $C_i$ does not depend on $x_i$. Lower bounds come from showing that no large cylinder intersection is almost monochromatic, by the discrepancy method of Babai, Nisan and Szegedy.

In NIH the sets of inputs with one transcript are products of $k$ sets, as in the two-party case. The main lower bounds come from information complexity.

## Examples

**Equality of two inputs.** Let $k = 3$ and $f(x_1, x_2, x_3) = 1$ when $x_1 = x_2$. In NOF, player 3 sees both $x_1$ and $x_2$ and writes the answer: 1 bit. In NIH it is the two-party [equality problem](/equality-problem/) between players 1 and 2, with deterministic cost $n + 1$.

**Parity of all bits.** Let $f$ be the parity of all $kn$ input bits. In NIH each player writes the parity of its own input, which costs $k$ bits. In NOF player 1 writes the parity of $x_2, \ldots, x_k$, and player 2, who sees $x_1$, writes the total: 2 bits.

**Generalized inner product.** Arrange the inputs as a $k \times n$ 0-1 matrix whose row $i$ is $x_i$, and let $\mathrm{GIP}_k$ be the parity of the number of all-ones columns. For $k = 2$ this is the [inner product problem](/inner-product-problem/). Babai, Nisan and Szegedy proved that $\mathrm{GIP}_k$ needs $\Omega(n/4^k)$ bits in NOF, even with randomness. Grolmusz gave a NOF protocol with $O(kn/2^k)$ bits, so the cost falls fast as $k$ grows, and for $k$ larger than about $\log_2 n$ no strong bound for GIP is possible.

**Disjointness and frequency moments.** In $k$-party disjointness each player holds a set $S_i \subseteq \{1, \ldots, n\}$. Under the promise that the sets are either pairwise disjoint or have exactly one common element and are otherwise disjoint, NIH protocols need $\Omega(n/k)$ bits (Gronemeier). The two cases differ in the largest frequency of an element in the union: for the sets $\{2,5,9\}$, $\{1,4,5\}$, $\{3,5,8\}$ the element 5 has frequency 3, and for $\{2,6,9\}$, $\{1,4,7\}$, $\{3,5,8\}$ each element has frequency 1. Alon, Matias and Szegedy used this gap to prove space lower bounds for [frequency moments](/frequency-moment-lower-bounds/) in the [streaming model](/streaming-model/).

## Where it is used

- **Streaming lower bounds.** A streaming algorithm with $s$ bits of memory gives an NIH protocol: each player runs the algorithm on its part of the stream and writes the memory state for the next player. So an NIH lower bound of $c$ bits gives $s \ge c/(k-1)$. See [number-in-hand model](/number-in-hand-model/).
- **Circuit lower bounds.** Håstad and Goldmann showed that a function computed by a small depth-2 circuit of a certain kind has a cheap NOF protocol. A strong NOF bound for a function in NP with a polylogarithmic number of players would give lower bounds for the class $\mathsf{ACC^0}$. See [number-on-forehead model](/number-on-forehead-model/).
- **Pseudorandomness and time-space trade-offs.** Babai, Nisan and Szegedy used the NOF bound for GIP to build pseudorandom generators for logspace and to prove time-space trade-offs for branching programs.
- **Distributed computing.** Message-passing models describe data that is split over many machines, where the cost is network traffic.

## References

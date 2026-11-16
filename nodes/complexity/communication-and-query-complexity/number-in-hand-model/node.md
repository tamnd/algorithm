---
tag: V9ERHP
kind: model
slug: number-in-hand-model
name: Number-in-hand model
aliases:
- NIH model
area: complexity/communication-and-query-complexity
level: advanced
summary: "A multiparty communication model in which each of k players sees only its own input and the players write bits on a shared blackboard. Its lower bounds give space bounds for streaming."
prereqs: [multiparty-communication-complexity, communication-model]
see_also: [number-on-forehead-model, frequency-moment-lower-bounds, streaming-model, ams-sketch, disjointness-problem, information-complexity, simultaneous-message-model, randomized-communication-complexity]
sources:
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press (1997)
    locator: Chapter 6, Multiparty communication complexity
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press (2020)
    locator: Chapter 6, Information (lower bounds for disjointness by information)
  - paper: doi:10.1006/jcss.1997.1545
    title: "Noga Alon, Yossi Matias and Mario Szegedy, The space complexity of approximating the frequency moments, Journal of Computer and System Sciences 58(1), 1999, pages 137-147"
    locator: the reduction from k-party disjointness with a unique common element to the streaming estimation of frequency moments
  - paper: doi:10.1016/j.jcss.2003.11.006
    title: "Ziv Bar-Yossef, T. S. Jayram, Ravi Kumar and D. Sivakumar, An information statistics approach to data stream and communication complexity, Journal of Computer and System Sciences 68(4), 2004, pages 702-732"
    locator: the information complexity method for the number-in-hand model and the Omega(n/k^2) bound for k-party disjointness
  - paper: doi:10.4230/LIPIcs.STACS.2009.1846
    title: "André Gronemeier, Asymptotically optimal lower bounds on the NIH-multi-party information complexity of the AND-function and disjointness, 26th Symposium on Theoretical Aspects of Computer Science (STACS 2009), LIPIcs 3, pages 505-516"
    locator: the Omega(n/k) bound for k-party disjointness with a unique common element, and the Omega(n^(1-2/p)) space bound for frequency moments
---

The number-in-hand model (NIH) is the model of [multiparty communication complexity](/multiparty-communication-complexity/) in which each of $k$ players sees only its own input. Player $i$ holds $x_i$, the players write bits on a blackboard that all of them can read, and the cost is the number of bits written. It is the direct extension of the two-party [communication model](/communication-model/), and its main use is to prove space lower bounds for algorithms in the [streaming model](/streaming-model/). Keep it apart from the [number-on-forehead model](/number-on-forehead-model/), where each player sees every input except its own.

## The machine

There are $k \ge 2$ players and a function $f : X_1 \times \cdots \times X_k \to \{0, 1\}$, often with $X_i = \{0,1\}^n$. Player $i$ gets $x_i$ and sees nothing of the other inputs.

A **blackboard protocol** is a rooted tree. Each inner node names the player who writes next and maps that player's input to a bit, and each leaf holds an output. On input $(x_1, \ldots, x_k)$ the players walk down the tree: at a node of player $i$ the bit written depends only on $x_i$ and on the bits already on the board, which name the node. The protocol computes $f$ if the leaf that the walk reaches holds $f(x_1, \ldots, x_k)$.

Variants restrict who may speak and when:

- **One-way.** The players speak once each, in the order $1, 2, \ldots, k$, and player $k$ outputs the answer. This is the variant that a one-pass streaming algorithm gives.
- **Simultaneous.** Each player sends one message to a referee, who sees no input; see [simultaneous message model](/simultaneous-message-model/).
- **Message passing.** Each message goes to one other player on a private channel, or to a coordinator. A bit on the blackboard can cost up to $k - 1$ private messages.

**The box property.** Fix a leaf $\ell$. Each bit on the path to $\ell$ is a condition on one input, so the set of inputs that reach $\ell$ is a box $S_1 \times S_2 \times \cdots \times S_k$ with $S_i \subseteq X_i$. A protocol of cost $c$ therefore splits the input space into at most $2^c$ boxes on which $f$ is constant. This is the $k$-party form of the rectangle property of two-party protocols, and it is the reason why many two-party methods carry over.

## What it counts

The cost is the total number of bits on the blackboard in the worst case, summed over all players. Local computation is free, and a player can use any amount of time and memory. Write $D^{cc}_{\mathrm{NIH},k}(f)$ for the deterministic cost and $R^{cc}_{\mathrm{NIH},k}(f)$ for the cost with error at most $1/3$ on every input. Unless the text says otherwise, randomness is public, that is, all players see the same random string. Results on information complexity also count the information that the board reveals about the inputs, which is at most the number of bits.

Each $f$ has the trivial protocol in which players $1$ to $k - 1$ write their inputs and player $k$ writes the answer. With $n$-bit inputs it costs $(k - 1)n + 1$ bits.

## Relation to other models

**Two parties.** For $k = 2$ the model is the usual two-party model, with $D^{cc}_{\mathrm{NIH},2}(f) = D^{cc}(f)$. A $k$-party NIH protocol also gives a two-party protocol for any split of the players into two groups, so each two-party bound for a split of $f$ is a $k$-party bound.

**Number on forehead.** An NIH protocol can be run in the NOF model at the same cost: the bit of NIH player $i$ depends on $x_i$ and the board, and any NOF player $j \ne i$ sees both, so player $j$ writes it. Thus NOF costs are at most NIH costs, and NOF lower bounds are the harder ones to prove. The gap can be very large: equality of $x_1$ and $x_2$ with $k = 3$ costs $n + 1$ bits deterministically in NIH but 1 bit in NOF, because player 3 sees both strings.

**Streaming.** Let a streaming algorithm use $s$ bits of memory in one pass. Split the stream into $k$ parts and give part $i$ to player $i$. Player 1 runs the algorithm on its part and writes the memory state; player 2 continues from that state, and so on, and player $k$ writes the output. This is a one-way NIH protocol with $(k - 1)s + 1$ bits. With $p$ passes the players repeat the round $p$ times, for at most $pks + 1$ bits. So an NIH lower bound of $c$ bits gives $s = \Omega(c/(pk))$.

## Known results in the model

**Disjointness with a unique common element.** Each player holds a set $S_i \subseteq \{1, \ldots, n\}$. Under the promise that the sets are pairwise disjoint, or that they share exactly one element and are otherwise disjoint, the players must decide which case holds. Bar-Yossef, Jayram, Kumar and Sivakumar introduced the information complexity method for this problem and proved $R^{cc}_{\mathrm{NIH},k} = \Omega(n/k^2)$. Gronemeier improved the bound to $\Omega(n/k)$. The bound for $k = 2$ is the $\Omega(n)$ bound for two-party [disjointness](/disjointness-problem/).

**Frequency moments.** The two cases of the promise differ in the largest frequency of an element in the union. For the sets $\{2,5,9\}$, $\{1,4,5\}$, $\{3,5,8\}$, element 5 has frequency 3, and for $\{2,6,9\}$, $\{1,4,7\}$, $\{3,5,8\}$ each element has frequency 1. Alon, Matias and Szegedy used this gap to prove that the frequency moments $F_p = \sum_j m_j^p$ need space polynomial in $n$ for large $p$. With $k$ about $n^{1/p}$ players, the moment $F_p$ is at most $n$ in the disjoint case and at least $k^p$ in the other case, so a good approximation of $F_p$ tells the cases apart. With the bound of Gronemeier and the streaming simulation above, this gives $\Omega(n/k^2) = \Omega(n^{1 - 2/p})$ bits of space for $p > 2$. The [AMS sketch](/ams-sketch/) shows that $F_2$, in contrast, needs only logarithmic space. See [frequency moment lower bounds](/frequency-moment-lower-bounds/) for the full set of bounds.

**Largest frequency.** The same reduction shows that a one-pass algorithm that tells a stream with largest frequency 1 from a stream with largest frequency $k$ needs $\Omega(n/k^2)$ bits of space.

## References

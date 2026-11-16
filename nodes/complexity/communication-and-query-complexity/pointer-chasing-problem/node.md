---
tag: RFYDVY
kind: problem
slug: pointer-chasing-problem
name: Pointer chasing problem
area: complexity/communication-and-query-complexity
level: research
summary: "Alice and Bob hold functions on [n] and follow k pointers from a fixed start, alternating functions. With k rounds it costs O(k log n) if Alice starts, but about n/k bits if Bob starts."
prereqs: [communication-model, randomized-communication-complexity]
see_also: [round-elimination, one-way-communication-complexity, index-problem, streaming-model, karchmer-wigderson-theorem, multiparty-communication-complexity, information-complexity, ams-sketch]
sources:
  - paper: "Noam Nisan and Avi Wigderson, Rounds in communication complexity revisited, SIAM Journal on Computing 22(1) (1993)"
    locator: the randomized bound for k rounds when the wrong player starts, the deterministic bound, the randomized upper bound, and the application to monotone constant-depth circuits
  - paper: "Pavol Duris, Zvi Galil and Georg Schnitger, Lower bounds on communication complexity, Information and Computation 73(1) (1987)"
    locator: the deterministic round hierarchy for two-party protocols
  - paper: "Christos H. Papadimitriou and Michael Sipser, Communication complexity, Journal of Computer and System Sciences 28(2) (1984)"
    locator: the question whether k + 1 rounds are more powerful than k rounds
  - paper: doi:10.1006/jcss.2000.1731
    title: "Stephen J. Ponzio, Jaikumar Radhakrishnan and S. Venkatesh, The communication complexity of pointer chasing, Journal of Computer and System Sciences 62(2) (2001)"
    locator: bounds for the version in which the whole pointer v_k is the output
  - paper: "Amir Yehudayoff, Pointer chasing via triangular discrimination, Combinatorics, Probability and Computing 29(4) (2020)"
    locator: the randomized bound Omega(n/k - k log n) for k rounds when the wrong player starts
---

In the pointer chasing problem, Alice holds a function $f_A : [n] \to [n]$, Bob holds $f_B : [n] \to [n]$, and they must follow $k$ pointers from a fixed start, applying $f_A$ and $f_B$ in turn. If they may use $k$ rounds and Alice speaks first, each round sends the next pointer, for $k \lceil \log_2 n \rceil$ bits. If Bob must speak first, his first message is nearly useless, and Nisan and Wigderson (1993) proved that randomized protocols need $\Omega(n/k^2 - k \log n)$ bits. So one more round, or the right first speaker, saves an exponential amount. Pointer chasing is the standard example for round hierarchies and for lower bounds on streaming algorithms that make few passes.

## In plain words

Alice has a table that says, for each of $n$ places, where to go next. Bob has another such table. Starting from place 1, the players take turns: first Alice's table gives the next place, then Bob's, then Alice's again, for $k$ steps. They want to know where they end up.

If Alice may talk first, the job is easy: she tells Bob the first place, he tells her the second, and so on. If Bob must talk first, he does not know the first place, so his first word helps little. With the same number of turns, the players then need to send a large part of their tables.

## Definition

Fix $v_0 = 1$ and define

$$v_1 = f_A(v_0), \quad v_2 = f_B(v_1), \quad v_3 = f_A(v_2), \quad \ldots,$$

so that $v_j = f_A(v_{j-1})$ for odd $j$ and $v_j = f_B(v_{j-1})$ for even $j$.

**Instance:** functions $f_A : [n] \to [n]$, known only to Alice, and $f_B : [n] \to [n]$, known only to Bob, and a number $k$ of steps.

**Question:** what is $v_k$?

The answer must be determined by the transcript, so the last message must contain it. Without this rule, the receiver of the last message could compute one more step alone. The cost that matters is the cost with a fixed number of rounds and a fixed first speaker. Write $C^{k, A}$ for the least cost of a protocol with $k$ rounds in which Alice speaks first, and $C^{k, B}$ when Bob speaks first.

## Variants

- **Bit version.** The output is one bit of $v_k$, for example its lowest bit. This gives a Boolean function, which is the form used for circuit and round hierarchies.
- **Full pointer.** The output is $v_k$ itself. Ponzio, Radhakrishnan and Venkatesh (2001) studied this version.
- **Layered version.** There are $k$ different functions, one for each step, split between the players. Many reductions to streaming use this form.
- **Number on forehead.** With $k$ players, each layer is written on the forehead of one player. This version, often called pointer jumping, is studied in [multiparty communication complexity](/multiparty-communication-complexity/), where it is a candidate hard function for circuit lower bounds.

## Examples

Let $n = 4$, $f_A = \{1 \mapsto 3,\ 2 \mapsto 4,\ 3 \mapsto 2,\ 4 \mapsto 1\}$ and $f_B = \{1 \mapsto 2,\ 2 \mapsto 3,\ 3 \mapsto 4,\ 4 \mapsto 1\}$. From $v_0 = 1$ the path is

$$v_0 = 1,\ v_1 = f_A(1) = 3,\ v_2 = f_B(3) = 4,\ v_3 = f_A(4) = 1,\ v_4 = f_B(1) = 2,$$

which a direct run confirms as the path $[1, 3, 4, 1, 2]$. For $k = 4$ with Alice first, the protocol sends $3$, $4$, $1$, $2$, each in $\lceil \log_2 4 \rceil = 2$ bits, so 8 bits in 4 rounds. If Bob must speak first in 4 rounds, his first message cannot depend on $v_1 = 3$, which only Alice knows; in this small case he can afford to send all of $f_B$ in $4 \cdot 2 = 8$ bits, but for large $n$ that costs $n \lceil \log_2 n \rceil$ bits.

## Known algorithms

- **Right first speaker.** With $k$ rounds and Alice first, send the pointers $v_1, \ldots, v_k$ in turn: $C^{k, A} \le k \lceil \log_2 n \rceil$, deterministic.
- **One extra round.** With $k + 1$ rounds and Bob first, Bob sends one dummy bit and then the players follow the protocol above. So $k + 1$ rounds cost $O(k \log n)$ whoever starts.
- **Wrong first speaker, deterministic.** Bob sends his whole table, $n \lceil \log_2 n \rceil$ bits, and then Alice can compute the rest with the remaining rounds.
- **Wrong first speaker, randomized.** Nisan and Wigderson (1993) gave a randomized protocol with $k$ rounds, Bob first, and $O((n/k + k) \log n)$ bits. So randomness lets the wrong first speaker pay only about $n/k$ instead of about $n$.

## Bounds

| Measure | Cost | Method and source |
|---|---|---|
| $k$ rounds, Alice first | $\Theta(k \log n)$ | the protocol above |
| $k$ rounds, Bob first, deterministic | $\Omega(n - k \log n)$ | Nisan and Wigderson (1993); a round hierarchy in the deterministic case goes back to Duris, Galil and Schnitger (1987) |
| $k$ rounds, Bob first, randomized | $\Omega(n/k^2 - k \log n)$ | Nisan and Wigderson (1993), by removing one round at a time with an information argument |
| $k$ rounds, Bob first, randomized, improved | $\Omega(n/k - k \log n)$ | Yehudayoff (2020), with the triangular discrimination in place of the earlier distance measure |
| $k$ rounds, Bob first, randomized, upper bound | $O((n/k + k) \log n)$ | Nisan and Wigderson (1993) |

The lower bounds are about the bit version or the pointer version as stated in each paper. With Yehudayoff's bound, the randomized cost with the wrong first speaker is known up to a logarithmic factor when $k$ is small compared with $\sqrt{n / \log n}$.

The lower bound proofs are of the [round elimination](/round-elimination/) kind: a short first message from Bob says little about $f_B(v_1)$, because $v_1$ is a uniform point he does not know, so the protocol can be turned into one with fewer rounds in which Alice speaks first, at a small cost in error.

## Reductions

- **To the round hierarchy.** The pair ($k$ rounds with Bob first, $k$ rounds with Alice first) separates the two kinds of $k$-round protocols. Since $k + 1$ rounds with Bob first cost $O(k \log n)$, pointer chasing also separates $k$ rounds from $k + 1$ rounds, which answers the question of Papadimitriou and Sipser (1984).
- **To streaming with few passes.** A $p$-pass streaming algorithm with $s$ bits of memory gives a protocol with $2p - 1$ messages of $s$ bits each, whatever the split of the stream. Put the edges $(j, f_B(j))$ first in the stream and the edges $(j, f_A(j))$ after them, so that Bob holds the first part and speaks first, which is the wrong order. A $p$-pass algorithm with $s$ bits of memory sends $2p - 1$ memory states, and Alice then announces the output, so it gives a protocol with $2p$ rounds, Bob first, and at most $2ps$ bits. If it finds $v_k$ for $k = 2p$, the bound of Nisan and Wigderson gives $2ps = \Omega(n/k^2 - k \log n)$, so $s = \Omega(n/p^3)$ when $p$ is small. One more pass solves the problem with $O(\log n)$ bits of memory, since each pass then follows two pointers. This is the source of pass lower bounds for graph problems in the [streaming model](/streaming-model/), such as finding a vertex at a given distance in a layered graph.
- **To monotone circuits.** Through the [Karchmer-Wigderson game](/karchmer-wigderson-theorem/), the depth of a monotone circuit is the cost of a communication game, and a circuit of depth $d$ gives a protocol with $d$ rounds. Nisan and Wigderson used their pointer chasing bound to give a new proof of the hierarchy of monotone constant-depth circuits of Klawe, Paul, Pippenger and Yannakakis (1984): depth $k + 1$ is more powerful than depth $k$.

## Applications

- **Rounds in communication.** Pointer chasing is the canonical problem that shows that the number of rounds matters, as [index](/index-problem/) does for one round against two.
- **Multi-pass streaming.** Trade-offs between the number of passes and the memory for graph problems reduce from pointer chasing, as in the reduction above.
- **Circuit complexity.** The monotone depth hierarchy above, and through the number-on-forehead version, a candidate route to lower bounds for small-depth circuits.

## References

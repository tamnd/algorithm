---
tag: EVSBD9
kind: concept
slug: one-way-communication-complexity
name: One-way communication complexity
area: complexity/communication-and-query-complexity
level: advanced
summary: "The cost when Alice sends one message and Bob answers. Deterministically it is the log of the number of distinct rows, and it can be exponentially above the two-way cost."
prereqs: [communication-model, deterministic-communication-complexity, randomized-communication-complexity]
see_also: [index-problem, index-problem-lower-bound, simultaneous-message-model, gap-hamming-distance, round-elimination, pointer-chasing-problem, streaming-model, vc-dimension]
sources:
  - paper: "Ilan Kremer, Noam Nisan and Dana Ron, On randomized one-round communication complexity, Computational Complexity 8(1) (1999)"
    locator: one-round randomized complexity under product distributions is the VC dimension up to constants
  - paper: doi:10.1561/0400000076
    title: "Tim Roughgarden, Communication Complexity (for Algorithm Designers), Foundations and Trends in Theoretical Computer Science 11(3-4), 2016"
    locator: Lecture 2, lower bounds for one-way communication and their use for streaming
  - paper: "Ilan Newman, Private vs. common random bits in communication complexity, Information Processing Letters 39(2) (1991), 67-71"
    locator: a public-coin protocol becomes a private-coin protocol with O(log n) more bits; the simulation keeps the protocol one-way
  - paper: "Christos H. Papadimitriou and Michael Sipser, Communication complexity, Journal of Computer and System Sciences 28(2) (1984)"
    locator: protocols with a bounded number of rounds and the first round hierarchy
---

One-way communication complexity is the cost of a protocol in which Alice sends a single message and Bob, who sees the message and his input, outputs $f(x, y)$. Bob never speaks to Alice. The deterministic one-way cost has an exact formula, the base-2 logarithm of the number of distinct rows of the [communication matrix](/communication-matrix/), and it can be exponentially larger than the two-way cost $D^{cc}(f)$. One-way protocols are the communication form of one-pass [streaming](/streaming-model/) algorithms and linear sketches, so one-way lower bounds give memory lower bounds.

## In plain words

Alice writes one note and gives it to Bob. Bob reads the note, looks at his own input, and gives the answer. He cannot ask a question back.

Because Alice does not know what Bob holds, her note must be good for every input Bob could have. Sometimes that forces her to send almost everything she knows, even when a short talk in both directions would be enough. The order also matters: a note from Bob to Alice can be much shorter than a note from Alice to Bob for the same task.

## The idea

**Definitions.** A one-way protocol from Alice to Bob is a map $m$ from Alice's inputs to messages and a map from (message, Bob's input) to outputs. Its cost is the length of the longest message.

- $D^{A \to B}(f)$ is the least cost of a deterministic one-way protocol that is always correct.
- $R^{A \to B, \mathrm{pub}}_\varepsilon(f)$ is the least cost when both players see a shared random string (public coins) and Bob errs with probability at most $\varepsilon$ on every input. $R^{A \to B, \mathrm{priv}}_\varepsilon(f)$ is the same with private coins. Without the index $\varepsilon$, the error is $1/3$.
- $D^{B \to A}$ and the randomized forms from Bob to Alice are defined in the same way with the roles swapped.

**Exact formula.** Let $r(f)$ be the number of distinct rows of the matrix $M_f$. Then

$$D^{A \to B}(f) = \lceil \log_2 r(f) \rceil.$$

*Upper bound:* Alice sends the number of her row among the $r(f)$ distinct rows, and Bob reads the entry in his column. *Lower bound:* if two inputs $x, x'$ with different rows send the same message, take a column $y$ where the rows differ. Bob sees the same message and the same $y$ in both cases, so he gives the same answer and is wrong on one of them. So the messages separate the $r(f)$ rows, and there are at least $r(f)$ of them. In the same way $D^{B \to A}(f) = \lceil \log_2 (\text{number of distinct columns}) \rceil$.

**One-way against two-way.** Each one-way protocol is a two-way protocol, so $D^{cc}(f) \le D^{A \to B}(f) + 1$, where the extra bit is Bob's answer. In the other direction, a two-way protocol tree of depth $c$ has fewer than $2^c$ inner nodes. Alice can send the bit she would send at each of her nodes, and Bob can then follow the whole tree alone. So

$$D^{A \to B}(f) \le 2^{D^{cc}(f)} - 1.$$

The [index problem](/index-problem/) shows that the gap can be this large: $D^{cc}(\mathrm{INDEX}_n) = \lceil \log_2 n \rceil + 1$ but $D^{A \to B}(\mathrm{INDEX}_n) = n$. Randomness does not close the gap, since $R^{A \to B, \mathrm{pub}}(\mathrm{INDEX}_n) = \Omega(n)$, while Bob can send $i$ for $\lceil \log_2 n \rceil$ bits.

**Public and private coins.** Newman's theorem holds in the one-way model: a public-coin one-way protocol with error $\varepsilon$ becomes a private-coin one-way protocol with error $2\varepsilon$ at an extra cost of $O(\log n + \log(1/\varepsilon))$ bits. Alice picks one of $O(n/\varepsilon^2)$ fixed random strings and sends its number with her message.

**Lower bound methods.**

- *Counting rows* gives the exact deterministic cost.
- *Information.* A message of $c$ bits carries at most $c$ bits of information about $x$. If Bob can recover each bit of $x$ with error $\delta$ from the message, the message must carry about $(1 - H_2(\delta))\, n$ bits. This is the proof for index; see [INDEX communication lower bound](/index-problem-lower-bound/).
- *VC dimension.* Kremer, Nisan and Ron (1999) proved that under product distributions the one-way randomized cost is, up to constant factors, the [VC dimension](/vc-dimension/) of the set of rows seen as functions on Bob's inputs.
- *Reductions* from index or [gap Hamming distance](/gap-hamming-distance/). A one-way reduction must also be one-way: Alice's input in the target problem may depend only on Alice's input in the source problem, and the same for Bob.
- *Round elimination* and its relatives handle protocols with a few rounds. See [round elimination](/round-elimination/).

**Rounds.** One-way protocols are the case of one round. A $k$-round protocol has $k$ messages that alternate between the players, and the first speaker is fixed. Papadimitriou and Sipser (1984) asked whether more rounds help; the [pointer chasing problem](/pointer-chasing-problem/) shows that $k$ rounds with the wrong first speaker can cost far more than $k$ rounds with the right one.

## Examples

**Counts of distinct rows.** For $n = 3$ a computation of the matrices gives the following deterministic costs.

| Function | distinct rows | distinct columns | $D^{A \to B}$ | $D^{B \to A}$ |
|---|---|---|---|---|
| equality $\mathrm{EQ}_3$ | 8 | 8 | 3 | 3 |
| greater-than on $\{0, \ldots, 7\}$ | 8 | 8 | 3 | 3 |
| disjointness $\mathrm{DISJ}_3$ | 8 | 8 | 3 | 3 |
| inner product $\mathrm{IP}_3$ | 8 | 8 | 3 | 3 |
| index $\mathrm{INDEX}_3$ | 8 | 3 | 3 | 2 |

For index with $n = 8$, $16$ and $1024$, the costs are $D^{A \to B} = 8, 16, 1024$ and $D^{B \to A} = 3, 4, 10$, while $D^{cc} = 4, 5, 11$.

**Equality with public coins.** Alice sends the inner products mod 2 of $x$ with $k$ shared random strings. Bob compares them with his own. If $x \ne y$, each check fails to notice with probability $1/2$, so $k = 2$ bits give error $1/4$. So $R^{A \to B, \mathrm{pub}}(\mathrm{EQ}_n) = O(1)$ against $D^{A \to B}(\mathrm{EQ}_n) = n$. With private coins, Alice sends a fingerprint of $O(\log n)$ bits; see [equality problem](/equality-problem/).

**Disjointness.** The reduction from index (Alice's set is $\{j : x_j = 1\}$, Bob's set is $\{i\}$) is one-way, so $R^{A \to B, \mathrm{pub}}(\mathrm{DISJ}_n) = \Omega(n)$. Here the two-way cost is also $\Theta(n)$, so one-way gives no extra loss.

## Where it is used

- **Streaming.** A one-pass streaming algorithm with $s$ bits of memory gives a one-way protocol with $s$ bits: Alice runs the algorithm on her part of the stream and sends the memory. A $p$-pass algorithm gives a protocol with $2p - 1$ messages. So one-way bounds for index, disjointness and gap Hamming distance give memory bounds; see [frequency moment lower bounds](/frequency-moment-lower-bounds/).
- **Sketches.** A [linear sketch](/linear-sketch/) of Alice's vector is a one-way message, and it is also a simultaneous message. See the [simultaneous message model](/simultaneous-message-model/).
- **Learning.** The link with the VC dimension makes one-way complexity a measure of how much must be sent to describe a concept for later queries.
- **Data structures.** Asymmetric round-bounded protocols model cell probe queries; see [round elimination](/round-elimination/).

## References

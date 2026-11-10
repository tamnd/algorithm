---
tag: 41MZQ5
kind: algorithm
slug: hirschberg-sinclair
name: Hirschberg-Sinclair algorithm
aliases:
- HS algorithm
area: distributed/leader-election
level: core
summary: Bidirectional ring election in phases. In phase k each candidate probes 2^k hops both ways and survives if no larger id is there. At most 8n⌈lg n⌉ messages and O(n) time.
solves: [ring-leader-election]
model: asynchronous-model
complexity:
  vars: {n: the number of processes}
  time: {worst: O(n)}
  messages: {worst: O(n log n)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 1980
  people: [Daniel S. Hirschberg, J. B. Sinclair]
  note: The first ring election with O(n log n) messages in the worst case.
prereqs: [ring-network, ring-leader-election, chang-roberts, message-complexity]
see_also: [franklin, peterson-leader-election, dolev-klawe-rodeh, ring-election-lower-bound, explicit-leader-election, round-complexity, complete-network-leader-election]
sources:
  - paper: doi:10.1145/359024.359029
    title: Daniel S. Hirschberg and J. B. Sinclair, Decentralized extrema-finding in circular configurations of processors, Communications of the ACM 23(11), 1980
    locator: pages 627 to 628 (the algorithm and its O(n log n) bound)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 3, Section 3.4 (the HS algorithm in the synchronous ring, the bound 8n(1 + ⌈log n⌉) and the time bound) and Chapter 15, Section 15.1.2 (HS in the asynchronous ring)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 3, Section 3.3.2 (an O(n log n) algorithm for asynchronous rings)
---

The Hirschberg-Sinclair algorithm elects a leader on a bidirectional [ring network](/ring-network/) of processes with distinct identifiers, with $O(n \log n)$ messages in the worst case. It works in phases: in phase $k$ each remaining candidate sends its identifier $2^k$ hops in both directions, and it stays a candidate only if no larger identifier is within that distance. It sends at most $8n \lceil \lg n \rceil - 2n$ election messages for $n \ge 2$, and the leader knows after fewer than $5n$ time units. It was the first [ring election](/ring-leader-election/) algorithm to beat the $\Theta(n^2)$ worst case of [Chang-Roberts](/chang-roberts/).

## In plain words

People sit in a circle, each with a different number, and each can talk to both neighbours. In the first round, each person asks the neighbour on each side: "Is your number smaller than mine?" Only those who get two yes answers go on.

In each later round, the people who are still in look twice as far in each direction. A question walks out that many steps, and each person on the way checks it. If somebody on the way has a larger number, the question dies. Otherwise the last person sends a yes back. A person who gets two yes answers stays in the game.

At last one question walks all the way round the circle and comes back to the person who sent it. That person has the largest number and is the leader. Few people survive the long rounds, so the total work stays small.

## The problem

The network is a bidirectional ring of $n \ge 1$ processes in the [asynchronous model](/asynchronous-model/). Each process has a distinct identifier from a totally ordered set and two ports. The ring does not need to be oriented: a process only uses "the port on which the message came" and "the other port". The processes do not know $n$. All processes start. Channels need not be FIFO. The goal is to make the process with the largest identifier the leader and to tell every process its identifier.

## The algorithm

The code of the process with identifier $u$ is below. A token $\langle \text{out}, v, h \rangle$ carries the identifier $v$ outward and can still make $h$ hops. A token $\langle \text{in}, v \rangle$ carries a positive answer back to $v$.

```pseudo id=main
HIRSCHBERG-SINCLAIR(u)                   ▷ the code of the process with identifier u
L1  phase ← 0, status ← unknown, replies ← 0
L2  send ⟨out, u, 1⟩ on both ports
L3  on receiving ⟨out, v, h⟩ on port p:
L4      if v > u and h > 1 then send ⟨out, v, h − 1⟩ on the other port
L5      else if v > u and h = 1 then send ⟨in, v⟩ on port p         ▷ turn back
L6      else if v = u and status = unknown then status ← leader, send ⟨leader, u⟩ on one port
L7      else discard the token                    ▷ v < u, or the second copy of u
L8  on receiving ⟨in, v⟩ on port p:
L9      if v ≠ u then send ⟨in, v⟩ on the other port
L10     else replies ← replies + 1
L11         if replies = 2 then phase ← phase + 1, replies ← 0, send ⟨out, u, 2^phase⟩ on both ports
L12 on receiving ⟨leader, v⟩ on port p:
L13     if v ≠ u then status ← non-leader, leader ← v, send ⟨leader, v⟩ on the other port
```

A process stays a candidate as long as both of its tokens come back (line L11). Line L7 kills a token that meets a larger identifier, so its owner never gets two replies and drops out without any message. A token of phase $k$ goes out $2^k$ hops and turns back at its last hop (line L5). If $2^k \ge n$, the token of the largest identifier goes all the way round and arrives back at its owner as an out token (line L6). Its copy from the other direction arrives later and is discarded. Lines L12 and L13 send the announcement round the ring once.

## Example

Take $n = 5$ with identifiers $3, 7, 1, 5, 2$ at $p_0, \ldots, p_4$. The message counts are the same in every schedule.

| phase | candidates | what happens | messages |
|---|---|---|---|
| 0 | all five | 7 and 5 are larger than both neighbours; 3 gets one reply, 1 and 2 get none | 10 out, 5 in |
| 1 (2 hops) | 7, 5 | both tokens of 7 return; the token of 5 toward $p_2$ dies at $p_1$ | 8 out, 6 in |
| 2 (4 hops) | 7 | both tokens return | 8 out, 8 in |
| 3 (8 hops) | 7 | both tokens go round the ring; the first makes $p_1$ the leader | 10 out |

The election sends $55$ messages, and the announcement $5$ more. In the synchronous model $p_1$ becomes the leader in round $2 + 4 + 8 + 5 = 19$. Chang-Roberts needs only $11$ election messages on this ring: the gain of Hirschberg-Sinclair shows only for large $n$ and bad orders.

## Correctness

Let $p_m$ hold the largest identifier, and let $L = \lceil \lg n \rceil$.

- **The largest identifier wins.** Every process forwards or turns back the tokens of $p_m$, since $u_m$ is larger than its identifier. So in each phase $k < L$, where $2^k < n$, both tokens of $p_m$ return and $p_m$ starts phase $k + 1$. In phase $L$, $2^L \ge n$, and a token of $p_m$ travels round the ring and arrives back at $p_m$ as an out token, so $p_m$ becomes the leader.
- **No other process wins.** An out token with identifier $u_i \ne u_m$ dies at $p_m$ or earlier, because $p_m$ is on each way round and $u_i < u_m$. So no out token of $p_i$ returns to $p_i$, and line L6 runs only at $p_m$.
- **Termination.** Each process starts at most $L + 1$ phases, and each token makes at most $2 \cdot 2^k$ hops. The announcement makes $n$ hops.

The proof in full, with the count of messages, is in the [proof of correctness](proofs/correctness/).

## Complexity

**Messages.** The key fact is that two processes that start phase $k \ge 1$ are more than $2^{k-1}$ apart. A process starts phase $k$ only if its identifier is larger than every identifier within $2^{k-1}$ hops on both sides. So at most $\lfloor n/(2^{k-1}+1) \rfloor$ processes start phase $k$. Each of them sends at most $4 \cdot 2^k$ messages in the phase: two out tokens of at most $2^k$ hops, and two in tokens of at most $2^k$ hops. For $n \ge 2$:

- phase 0 sends at most $4n$ messages;
- each phase $k$ with $1 \le k \le L - 1$ sends at most $4 \cdot 2^k \cdot n/(2^{k-1}+1) < 8n$ messages;
- in phase $L$ only $p_m$ is left, since two candidates would need more than $2^{L-1} \ge n/2$ hops between them on both sides, and its two tokens make $n$ hops each, $2n$ messages.

The total is at most $4n + 8n(L - 1) + 2n = 8n \lceil \lg n \rceil - 2n$ election messages. Lynch gives the simpler bound $8n(1 + \lceil \lg n \rceil)$, which counts $8n$ for each of the $L + 1$ phases. The announcement adds $n$. The bound is not tight: for $n = 8$ the largest count over all $40320$ orders is $89$, while the bound is $176$.

**Time.** The tokens of $p_m$ never wait: each process forwards them at once. Phase $k < L$ of $p_m$ takes $2 \cdot 2^k$ time units, and phase $L$ takes $n$. So $p_m$ is elected after

$$\sum_{k=0}^{L-1} 2^{k+1} + n = 2(2^L - 1) + n$$

time units. This is $3n - 2$ when $n$ is a power of 2. Otherwise $2^L < 2n$, so the time is less than $5n$. In the synchronous model these are exact round counts. The announcement adds $n$.

**Space and message size.** A process stores its identifier, its phase and a reply counter. A message holds an identifier and a hop count of $O(\log n)$ bits.

## Properties

- **Deterministic and comparison based.** Only comparisons of identifiers are used.
- **Uniform.** The processes do not know $n$. The phase in which the largest token goes round finds the size of the ring implicitly.
- **Works on non-oriented rings.** No process needs a global sense of direction.
- **No FIFO needed.** A process has one phase open at a time, so replies of different phases cannot mix.
- **Optimal up to the constant.** By the [ring election lower bound](/ring-election-lower-bound/), $\Omega(n \log n)$ messages are needed.

## Variants and improvements

- **Franklin's algorithm.** [Franklin](/franklin/) replaces fixed distances by the distance to the nearest candidate on each side. This gives at most $2n \lfloor \lg n \rfloor + 2n$ messages, but it needs FIFO channels.
- **Unidirectional rings.** [Peterson](/peterson-leader-election/) and [Dolev, Klawe and Rodeh](/dolev-klawe-rodeh/) show that a second direction is not needed for $O(n \log n)$ messages.
- **Other growth factors.** Distances $c^k$ for a constant $c > 1$ in place of $2^k$ give the same $O(n \log n)$ bound with a different constant.

## When to use it

Use it when the ring is bidirectional, possibly not oriented, the channels may reorder messages, and the worst case must be $O(n \log n)$ messages with $O(n)$ time. When channels are FIFO, [Franklin's algorithm](/franklin/) has a smaller constant. For small rings, [Chang-Roberts](/chang-roberts/) is simpler and often sends fewer messages.

## Pitfalls

- **Counting phases.** The largest identifier is elected in phase $\lceil \lg n \rceil$, and there are $\lceil \lg n \rceil + 1$ phases counted from 0. An analysis that forgets phase 0 or the last phase loses a term of order $n$.
- **Two copies of the winning token.** Both out tokens of the winner return in the last phase. Without the test "status = unknown" in line L6 the winner announces twice.
- **Replying without the hop count.** A process must turn a token back only when $h = 1$ (line L5). Turning it back earlier makes a candidate survive with a larger identifier nearby.
- **Expecting gains on small rings.** The constant $8$ is large. For a few dozen processes in a random order, Chang-Roberts usually sends fewer messages.

## Implementations

## History

Hirschberg and Sinclair published the algorithm in 1980 in the Communications of the ACM, as the answer to the question of whether $O(n \log n)$ messages are enough on a ring. Burns showed in the same year that $\Omega(n \log n)$ messages are needed on asynchronous bidirectional rings. In 1982 Franklin gave a simpler bidirectional algorithm, and Peterson and Dolev, Klawe and Rodeh gave unidirectional ones. Lynch presents the algorithm under the name HS, in the synchronous and in the asynchronous ring.

## References

---
tag: SEB968
kind: algorithm
slug: oral-messages-algorithm
name: Oral messages algorithm
aliases:
- OM(m)
- Lamport-Shostak-Pease algorithm
- Byzantine generals algorithm
area: distributed/byzantine-agreement
level: core
summary: Recursive Byzantine broadcast with oral messages. It tolerates m traitors when n > 3m, in m + 1 rounds, with up to (n-1)(n-2)...(n-m-1) messages in the last round.
solves: [byzantine-broadcast]
model: oral-messages-model
complexity:
  vars: {n: the number of generals (processes), m: the largest number of traitors (t on the other pages)}
  time: {worst: Θ(m), best: Θ(m)}
  messages: {worst: O(n^(m+1)), best: O(n^(m+1))}
  space: {extra: O(n^(m+1))}
properties: {deterministic: true, recursive: true}
prereqs: [byzantine-broadcast, oral-messages-model, byzantine-failure-model]
see_also: [signed-messages-algorithm, dolev-strong-algorithm, phase-king-algorithm, phase-queen-algorithm, byzantine-resilience-bound, byzantine-round-lower-bound, interactive-consistency, dolev-reischuk-lower-bound]
sources:
  - paper: doi:10.1145/357172.357176
    title: Leslie Lamport, Robert Shostak and Marshall Pease, The Byzantine Generals Problem, ACM Transactions on Programming Languages and Systems 4(3), 1982
    locator: Section 3 (assumptions A1 to A3, Algorithm OM(m), Lemma 1 and Theorem 1, pages 387 to 390) and Section 7 (paths of length m + 1 and the message count, page 400)
  - paper: doi:10.1145/322186.322188
    title: Marshall Pease, Robert Shostak and Leslie Lamport, Reaching Agreement in the Presence of Faults, Journal of the ACM 27(2), 1980
    locator: pages 228 to 234 (interactive consistency with n >= 3m + 1 in m + 1 rounds, the first form of the algorithm)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 6, Section 6.3 (the EIG algorithm for Byzantine agreement, the round form of OM(m))
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 5, Section 5.2 (Byzantine failures, the exponential algorithm)
  - paper: doi:10.1007/BF01843568
    title: Michael J. Fischer, Nancy A. Lynch and Michael Merritt, Easy impossibility proofs for distributed consensus problems, Distributed Computing 1(1), 1986
    locator: the scenario (hexagon) argument that the algorithm needs n > 3m
---

The oral messages algorithm OM(m) of Lamport, Shostak and Pease solves [Byzantine broadcast](/byzantine-broadcast/), which they called the Byzantine Generals Problem, in the [oral messages model](/oral-messages-model/). A commander sends an order, every lieutenant passes on what it heard to the others by a recursive call with one fewer traitor, and each lieutenant takes a majority. It tolerates $m$ traitors whenever the number of generals $n$ is more than $3m$, it takes $m + 1$ synchronous rounds, and it sends a number of messages that grows like $n^{m+1}$. The bound $n > 3m$ is the best possible without signatures, by the [Byzantine resilience bound](/byzantine-resilience-bound/).

## In plain words

One general gives an order, attack or retreat, to the other generals by messenger. Some generals are traitors. A traitor can lie, and can tell different generals different things. The loyal generals must all do the same thing, and if the commander is loyal they must follow its order.

A messenger only says what the sender told it. So a general cannot prove what it heard from someone else. The fix is to ask everyone. Each general tells every other general what the commander said to it. It does this by the same method, with one traitor fewer, so the reports are also checked. Then each general follows the most common report.

This works when traitors are fewer than one third of the generals. With three generals and one traitor, no method works.

## The problem

There are $n$ generals $0, \ldots, n - 1$ in the [synchronous model](/synchronous-model/) with a complete network. General $0$ is the commander and has an order $v$ from a finite set $V$ that contains the default value RETREAT. The others are lieutenants. At most $m$ generals are traitors, which are [Byzantine](/byzantine-failure-model/): they can send anything, they can send different values to different generals, and they can act together. The set of traitors is fixed at the start of the run (a static adversary), and the traitors may see the messages of a round before they choose their own (a rushing adversary). Lamport, Shostak and Pease use the letter $m$ for the number of traitors. The other pages in this area use $t$.

Messages are oral, which is the [oral messages model](/oral-messages-model/):

- **A1.** Every message that is sent is delivered correctly.
- **A2.** The receiver of a message knows who sent it.
- **A3.** The absence of a message can be detected.

A traitor can say that it heard anything, and nobody can check it. The algorithm must give the two interactive consistency conditions of LSP:

- **IC1.** All loyal lieutenants obey the same order.
- **IC2.** If the commander is loyal, then every loyal lieutenant obeys the order it sends.

IC1 is agreement and IC2 is validity. Both are [safety properties](/safety-property/). Termination is not a separate condition in LSP, because each general decides at a fixed round.

## The algorithm

$\text{majority}(w_1, \ldots, w_k)$ is the value that occurs more than $k/2$ times in the list, and RETREAT if no such value exists. Any fixed function works if it gives $v$ when a strict majority of its arguments are $v$. The median is another choice for ordered values. When a general expects a message and none arrives, it uses RETREAT in place of the message. This is possible because of A3.

```pseudo id=main
OM(m, c, v, G)                  ▷ commander c with order v, lieutenants G
L1  c sends v to every lieutenant in G
L2  for each i in G: v_i ← the value i receives from c, or RETREAT if none arrives
L3  if m = 0 then each i in G obeys v_i and stops
L4  for each i in G: i runs OM(m − 1, i, v_i, G \ {i}) as the commander
L5  for each i in G do
L6      for each j in G \ {i}: w_j ← the value i obeys in OM(m − 1, j, v_j, G \ {j})
L7      w_i ← v_i
L8      i obeys majority(w_j for all j in G)
```

The top call is $\text{OM}(m, 0, v, \{1, \ldots, n - 1\})$. In line L4 every lieutenant becomes the commander of a smaller instance with $m - 1$ traitors and $|G| - 1$ lieutenants. A traitor runs whatever code it likes in place of lines L4 to L8.

**Round form.** The recursion is easier to run in rounds. A message carries the path of generals that relayed it, starting with the commander. In round $r$ each general sends, for each path $p$ of length $r - 1$ that it received and that does not contain it, the value it received on $p$, on the path $p$ followed by itself, to each general not on the new path. Round 1 is line L1, and round $r + 1$ is line L1 of all instances at depth $r$ of the recursion, which run at the same time. After round $m + 1$ each lieutenant evaluates lines L6 to L8 bottom up over the paths. This is the exponential information gathering (EIG) form of Lynch, Section 6.3. The implementation on this page uses it.

## Example

The values are 0 (RETREAT), 1 and 2. Take $n = 4$ and $m = 1$, the case of Figure 3 of LSP. The commander is loyal and sends 1, and lieutenant 3 is a traitor that reports 2 to everyone in round 2.

| lieutenant | from commander | report of 1 | report of 2 | report of 3 | majority |
|---|---|---|---|---|---|
| 1 | 1 | (own: 1) | 1 | 2 | 1 |
| 2 | 1 | 1 | (own: 1) | 2 | 1 |

Both loyal lieutenants obey 1, so IC1 and IC2 hold. The run has 2 rounds and 9 messages: 3 in round 1 and 6 in round 2. 7 of the 9 come from loyal generals.

Now let the commander be the traitor, as in Figure 4 of LSP. It sends 1 to lieutenant 1, 2 to lieutenant 2 and 0 to lieutenant 3. The loyal lieutenants report truly, so each of them ends with the list 1, 2, 0 and takes majority(1, 2, 0) = RETREAT. All three obey RETREAT, so IC1 holds, and IC2 does not apply.

With $n = 3$ and $m = 1$ the algorithm fails. The commander is loyal and sends 1, and lieutenant 2 is a traitor that reports 2. Lieutenant 1 has the list 1, 2, so the majority is RETREAT, and IC2 breaks. The implementation also builds the general attack for $n = 3m$: two copies of the system are joined in a ring of six groups (the hexagon of Fischer, Lynch and Merritt), and the traitors replay to the loyal generals what their copies sent in the ring. For $m = 1$ and $m = 2$, the views of the loyal generals in the three runs of the proof match the ring exactly, and at least one of the three runs breaks IC1 or IC2. For $m = 1$ with commander values 0 and 1 in the two copies, the run where the commander and lieutenant 2 are loyal ends with lieutenant 2 obeying 0 while the commander sent 1.

## Correctness

The proof is by induction on $m$, on the recursive form. The round form computes the same values, because the value on the path $0, j_1, \ldots, j_k$ is the order that $j_k$ passes on as commander of an instance at depth $k$.

- **Lemma 1 (LSP).** For all $m$ and $k$, OM(m) satisfies IC2 if there are more than $2k + m$ generals and at most $k$ traitors. A loyal commander sends $v$ to all. By induction, each loyal lieutenant $j$ passes on $v$ correctly in its instance of OM(m - 1), which has $n - 1 > 2k + (m - 1)$ generals. So in line L8 every loyal lieutenant sees $v$ from all loyal lieutenants, and $n - 1 > 2k$ means that they are a strict majority of the $n - 1$ entries.
- **Theorem 1 (LSP).** For all $m$, OM(m) satisfies IC1 and IC2 if there are more than $3m$ generals and at most $m$ traitors. If the commander is loyal, use Lemma 1 with $k = m$. If it is a traitor, at most $m - 1$ lieutenants are traitors and each instance of OM(m - 1) has $n - 1 > 3(m - 1)$ generals. By induction each instance satisfies IC1 and IC2, so all loyal lieutenants get the same entry $w_j$ for each $j$, and so the same majority.

The full proof is below. The algorithm stops after round $m + 1$ in every run, because the depth of the recursion is $m$.

## Complexity

The costs are for the synchronous model, in rounds and messages.

- **Rounds.** Exactly $m + 1$, in every run. This matches the [round lower bound](/byzantine-round-lower-bound/) of $t + 1$ rounds.
- **Messages.** In round $k$ each path of length $k$ carries one message, and there are $(n - 1)(n - 2) \cdots (n - k)$ such paths. When every general sends all its messages, the total is $M(n, m) = \sum_{k=1}^{m+1} (n - 1)(n - 2) \cdots (n - k)$, which is at most $n^{m+1}$. For example $M(4, 1) = 9$, $M(7, 2) = 156$, $M(10, 3) = 3609$ and $M(13, 4) = 108384$. LSP state the count of the last round, $(n - 1)(n - 2) \cdots (n - m - 1)$, in Section 7. With $n = 3m + 1$, each factor is at least $2m$, so the last round alone has at least $(2m)^{m+1}$ messages, and the cost is exponential in $m$.
- **Message size.** Each message holds one value and a path of at most $m + 1$ names.
- **Local space.** Each lieutenant stores one value per path, so $O(n^{m+1})$ values.

The [Dolev-Reischuk lower bound](/dolev-reischuk-lower-bound/) asks for $\Omega(nt)$ messages without signatures, so the exponential count is not needed. The [phase king algorithm](/phase-king-algorithm/) solves the problem with $n > 4t$ and polynomial messages, and Garay and Moses (1998) reach $n > 3t$ and $t + 1$ rounds with polynomial messages.

## Properties

- **Deterministic.** No coins. The only freedom is the choice of the traitors.
- **Optimal resilience.** It works for $n > 3m$, and no algorithm works for $3 \le n \le 3m$ in the oral messages model.
- **Optimal rounds.** $m + 1$ rounds, which no algorithm beats in the worst case.
- **Not early stopping.** It always takes $m + 1$ rounds, also when no general is a traitor.
- **Needs the complete graph.** A2 and A3 are assumed on every link. LSP, Section 5, extend the algorithm to graphs that are $3m$-regular in their sense, as OM(m, 3m) in Theorem 3. Dolev showed that [vertex connectivity](/vertex-connectivity/) $2m + 1$ is needed and enough.

## Variants and improvements

- **Interactive consistency.** Run $n$ copies at the same time, one per commander, to give every loyal general the same vector of all values. This is the form of Pease, Shostak and Lamport 1980. See [interactive consistency](/interactive-consistency/).
- **Lemma 1 resilience.** If only IC2 is needed, $n > 2k + m$ is enough for $k$ traitors. The test of this page runs OM(2) with $n = 5$ and one traitor lieutenant.
- **Signed messages.** With unforgeable signatures, the [signed messages algorithm](/signed-messages-algorithm/) and the [Dolev-Strong algorithm](/dolev-strong-algorithm/) work for any number of traitors.
- **Polynomial algorithms.** The [phase king](/phase-king-algorithm/) and [phase queen](/phase-queen-algorithm/) algorithms send a polynomial number of messages, at the price of more rounds or a lower resilience.

## When to use it

Use OM(m) to learn Byzantine agreement and to see why $n > 3m$ is the right bound, or for $m = 1$, where it costs $n - 1 + (n - 1)(n - 2)$ messages in 2 rounds. For $m \ge 2$ the message count grows too fast for most uses. A system that can use signatures should use them. A system that needs Byzantine fault tolerance in a real network, which is not synchronous, uses a protocol for [partial synchrony](/partial-synchrony/) such as [PBFT](/pbft/) or [HotStuff](/hotstuff/), see [Byzantine fault tolerance](/byzantine-fault-tolerance/).

## Pitfalls

- **Three generals.** With $n = 3$ and one traitor, a lieutenant cannot tell a lying commander from a lying peer. The example above shows a failure, and the [resilience bound](/byzantine-resilience-bound/) shows that no other algorithm does better.
- **Different defaults or majority functions.** All loyal generals must use the same RETREAT default for a missing message and the same majority function. Otherwise the vectors are equal and the decisions still differ.
- **Forgetting the own value.** In line L7 a lieutenant counts the value it got from the commander. Without it, Lemma 1 has one entry fewer and the count $n - 1 > 2k$ no longer gives a strict majority.
- **Trusting the path.** A path only says who claims to have relayed a value. A2 lets the receiver check the last name on the path, but a traitor can invent the earlier part. The proof does not depend on the earlier names being true.
- **Using it with more than $m$ traitors.** The bound is $n > 3m$ for the $m$ in the call. If more traitors exist, IC1 can break even if $n$ is large.

## Implementations

## History

Pease, Shostak and Lamport posed the problem in 1980 during work on the SIFT fault-tolerant computer for aircraft control at SRI, as interactive consistency, and showed that $n \ge 3m + 1$ is necessary and sufficient. The 1982 paper by Lamport, Shostak and Pease gave it the story of the Byzantine generals, the recursive algorithm OM(m) and the proof of Theorem 1. Fischer and Lynch showed in 1982 that $m + 1$ rounds are needed, and Fischer, Lynch and Merritt gave the hexagon proof of $n > 3m$ in 1986. The exponential message count started the search for polynomial algorithms, such as the algorithms of Dolev, Fischer, Fowler, Lynch and Strong, and the phase king algorithm of Berman, Garay and Perry.

## References

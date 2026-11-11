---
tag: XR29FE
kind: algorithm
slug: signed-messages-algorithm
name: Signed messages algorithm
aliases:
- SM(m)
area: distributed/byzantine-agreement
level: core
summary: Byzantine broadcast of Lamport, Shostak and Pease with unforgeable signatures. It tolerates any number m of traitors in m + 1 rounds.
solves: [byzantine-broadcast]
model: signed-messages-model
complexity:
  vars: {n: the number of generals (processes), m: the largest number of traitors (t on the other pages), d: the number of distinct values that the commander signs}
  time: {worst: Θ(m), best: Θ(m)}
  messages: {worst: O(n^2 d), best: Θ(n^2)}
  space: {extra: O(d)}
properties: {deterministic: true, recursive: false}
prereqs: [byzantine-broadcast, signed-messages-model, signature-chain]
see_also: [dolev-strong-algorithm, oral-messages-algorithm, authenticated-resilience-bound, byzantine-round-lower-bound, dolev-reischuk-lower-bound, interactive-consistency, digital-signature]
sources:
  - paper: doi:10.1145/357172.357176
    title: Leslie Lamport, Robert Shostak and Marshall Pease, The Byzantine Generals Problem, ACM Transactions on Programming Languages and Systems 4(3), 1982
    locator: Section 4 (assumption A4, the choice function, Algorithm SM(m) and Theorem 2, pages 390 to 393) and Section 5 (Theorem 4, SM(m + d - 1) on graphs of diameter d, pages 395 to 396)
  - paper: doi:10.1145/322186.322188
    title: Marshall Pease, Robert Shostak and Leslie Lamport, Reaching Agreement in the Presence of Faults, Journal of the ACM 27(2), 1980
    locator: pages 228 to 234 (with authenticated messages, interactive consistency for any n >= m >= 0)
  - paper: doi:10.1137/0212045
    title: Danny Dolev and H. Raymond Strong, Authenticated algorithms for Byzantine agreement, SIAM Journal on Computing 12(4), 1983
    locator: pages 656 to 666 (the t + 1 round authenticated algorithm with polynomial messages)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 6 (Byzantine agreement in synchronous networks; authenticated algorithms are discussed in the notes)
---

The signed messages algorithm SM(m) of Lamport, Shostak and Pease solves [Byzantine broadcast](/byzantine-broadcast/) in the [signed messages model](/signed-messages-model/), where a loyal general's signature cannot be forged. The commander signs its order, and each lieutenant adds its own signature and passes each new order on, so every order travels as a [signature chain](/signature-chain/). A lieutenant collects the set $V_i$ of orders it has seen and obeys one fixed choice from the set. SM(m) tolerates any number $m$ of traitors, with no lower limit on $n$ except that the problem is only interesting when $n \ge m + 2$, and it finishes in $m + 1$ rounds.

## In plain words

A commander sends an order to some generals, and some generals are traitors. This time every general has a signature that nobody else can copy.

The commander signs its order. When a general sees a signed order for the first time, it adds its own signature and sends it to everyone who has not signed it yet. Each general keeps a list of all the different orders it has seen. At the end, if the list has one order, the general obeys it. If the list has two or more orders, the commander must be a traitor, because only the commander can sign an order, and all loyal generals then do the same default thing.

A traitor cannot change an order or make a new one in a loyal name. So the lists of the loyal generals end the same, however many traitors there are.

## The problem

There are $n$ generals $0, \ldots, n - 1$ in the [synchronous model](/synchronous-model/) with a complete network. General 0 is the commander with an order $v$ from a set $V$ that holds the default RETREAT. At most $m$ generals are [Byzantine](/byzantine-failure-model/) traitors. The adversary is static (it fixes the traitors at the start) and rushing (it sees the loyal messages of a round before it sends its own). The traitors share all their keys, so a traitor can sign in the name of any traitor. Lamport, Shostak and Pease use the letter $m$ for the number of traitors. The other pages in this area use $t$.

The messages satisfy A1 to A3 of the [oral messages model](/oral-messages-model/) and also A4:

- **A4 (a).** A loyal general's signature cannot be forged, and any change to the contents of its signed messages can be detected.
- **A4 (b).** Anyone can verify the authenticity of a general's signature.

The goal is IC1 (all loyal lieutenants obey the same order) and IC2 (if the commander is loyal, every loyal lieutenant obeys its order). LSP note that the problem is vacuous when $n < m + 2$, because then at most one general is loyal.

## The algorithm

Write $v{:}0{:}j_1{:}\cdots{:}j_k$ for the order $v$ signed by the commander and then, in turn, by the lieutenants $j_1, \ldots, j_k$. Each signature covers the order and all signatures before it, see [signature chain](/signature-chain/). The function choice must map $\{v\}$ to $v$ and the empty set to RETREAT. For example, choice($W$) can be the single element of $W$ if $|W| = 1$, and RETREAT otherwise, or the median of $W$.

```pseudo id=main
SM(m)                                   ▷ general 0 is the commander; V_i = ∅ at each lieutenant i
L1  the commander signs v and sends v:0 to every lieutenant         ▷ round 1
L2  for r ← 1 to m + 1 do                                              ▷ lock-step rounds
L3      each lieutenant sends the messages it queued in round r − 1
L4      for each message v:0:j_1:…:j_k that lieutenant i receives in round r do
L5          if k ≠ r − 1, or 0, j_1, …, j_k are not distinct, or i is one of them then ignore it
L6          else if a signature on it is not valid then ignore it
L7          else if v ∉ V_i then add v to V_i
L8              if k < m then
L9                  sign it, which gives v:0:j_1:…:j_k:i
L10                 queue it for every lieutenant other than i, j_1, …, j_k
L11 each lieutenant i obeys choice(V_i)
```

LSP state the algorithm without rounds: step (2)(A) is the case $k = 0$ and step (2)(B) the case $k > 0$, and in step (3) a lieutenant decides "when it will receive no more messages", which a timeout or a "will not send" report detects. The round form above is the same algorithm in the synchronous model. A message with $k$ lieutenant signatures arrives in round $k + 1$, so no message can arrive after round $m + 1$. Line L5 also checks that the signers are distinct, which LSP's proof uses without saying it.

## Example

Take $n = 4$ and $m = 2$. The commander 0 and lieutenant 3 are traitors, and lieutenants 1 and 2 are loyal. The values are 0 (RETREAT), 1 and 2, and choice is "the single element, else RETREAT".

| round | what happens | $V_1$ | $V_2$ |
|---|---|---|---|
| 1 | the commander sends $1{:}0$ to 1 and 2. It also signs $2{:}0$ and gives it only to traitor 3 | {1} | {1} |
| 2 | 1 sends $1{:}0{:}1$ to 2 and 3. 2 sends $1{:}0{:}2$ to 1 and 3. Traitor 3 sends $2{:}0{:}3$ to lieutenant 1 only | {1, 2} | {1} |
| 3 | lieutenant 1 has $k = 1 < m$, so it sends $2{:}0{:}3{:}1$ to lieutenant 2 | {1, 2} | {1, 2} |

Both loyal lieutenants end with $\{1, 2\}$ and obey RETREAT. The loyal generals send 5 messages that carry 11 signatures in total, and the traitors send 3 messages. If the run stopped after round 2, lieutenant 1 would obey RETREAT and lieutenant 2 would obey 1. This is why SM(m) needs $m + 1$ rounds, see the [round lower bound](/byzantine-round-lower-bound/).

With no traitors and $n = 4$, $m = 2$, the commander sends 3 messages and each lieutenant relays once to 2 others, so there are $3 + 3 \cdot 2 = 9 = (n - 1)^2$ messages with 15 signatures.

## Correctness

This is Theorem 2 of LSP: for any $m$, SM(m) solves the Byzantine Generals Problem if there are at most $m$ traitors.

- **IC2.** A loyal commander signs only $v$. Each accepted message starts with a valid commander signature, so by A4 it carries $v$. Each loyal lieutenant gets $v{:}0$ in round 1, so $V_i = \{v\}$ and it obeys $v$.
- **IC1.** If the commander is loyal, IC1 follows from IC2. Otherwise, it is enough to show that $v \in V_i$ implies $v \in V_j$ for loyal $i, j$. Suppose $i$ adds $v$ from $v{:}0{:}j_1{:}\cdots{:}j_k$. If $j$ is a signer, $j$ only signs orders it has added. If $k < m$, $i$ relays the order to $j$ in the next round. If $k = m$, the $m$ distinct lieutenant signers cannot all be traitors, because the commander is one of the at most $m$ traitors. A loyal signer $j_l$ relayed $v$ to every lieutenant not yet on the chain, including $j$.

So all loyal lieutenants end with the same set and obey the same order. The full proof is below.

## Complexity

The costs are for the synchronous model.

- **Rounds.** Exactly $m + 1$. The [round lower bound](/byzantine-round-lower-bound/) shows that $t + 1$ rounds are needed in the worst case, also with signatures, when $t \le n - 2$.
- **Messages.** A loyal lieutenant relays each value at most once (line L7) to at most $n - 2$ lieutenants. If the commander signs $d$ distinct values, the loyal generals send at most $(n - 1)(1 + (n - 2)d)$ messages. With a loyal commander, $d = 1$ and the count is at most $(n - 1)^2$, with equality when there are no traitors. LSP, Section 7, give the larger general bound $(n - 1)(n - 2) \cdots (n - m - 1)$ for both OM(m) and SM(m). The count above is for the version that ignores a value already in $V_i$, which LSP's step (2) also does.
- **Signatures.** A message carries at most $m + 1$ signatures, so a message has $O(m)$ signatures and the loyal generals send $O(n^2 d m)$ signatures. Dolev and Reischuk showed that $\Omega(nt)$ signatures are needed by every authenticated algorithm, see the [Dolev-Reischuk lower bound](/dolev-reischuk-lower-bound/).
- **Local space.** Each lieutenant stores $V_i$, at most $d$ values, and the chains it queued in one round.

A traitorous commander can make $d$ large by signing many values. The [Dolev-Strong algorithm](/dolev-strong-algorithm/) removes the factor $d$: a process relays only its first two values, so the loyal processes send $O(n^2)$ messages.

## Properties

- **Deterministic.** No coins.
- **Any number of traitors.** It works for every $m$, while the [oral messages algorithm](/oral-messages-algorithm/) needs $n > 3m$. The [authenticated resilience bound](/authenticated-resilience-bound/) explains why signatures make this possible for broadcast, and why consensus with strong validity still needs $n > 2t$.
- **Not early stopping.** It runs $m + 1$ rounds in every run.
- **Unforgeable signatures assumed.** With real [digital signatures](/digital-signature/) the guarantee holds only against an adversary that cannot break the [signature scheme](/signature-scheme/), and the keys must be distributed before the run.
- **Works on incomplete graphs.** LSP, Theorem 4: if the loyal generals form a connected subgraph of diameter $d$, then SM(m + d - 1), where a general sends only to its neighbors, solves the problem.

## Variants and improvements

- **SM(1) without lieutenant signatures.** LSP note that the last signature in a chain is never relayed, so it is not needed. In SM(1), lieutenants need not sign.
- **Dolev-Strong.** The [Dolev-Strong algorithm](/dolev-strong-algorithm/) is the same idea with the sender among the processes, relays to all processes, and only the first two extracted values relayed. It has $t + 1$ rounds and $O(n^2)$ messages from correct processes.
- **Interactive consistency.** $n$ copies of SM(m), one per sender, give every loyal general the same vector of values, see [interactive consistency](/interactive-consistency/).
- **Fewer signatures.** [Threshold signatures](/threshold-signature/) and [aggregate signatures](/aggregate-signature/) let a chain carry a short proof in place of up to $m + 1$ separate signatures.

## When to use it

Use SM(m) to understand how signatures remove the $n > 3m$ limit of Byzantine broadcast, and as the base of the Dolev-Strong algorithm. In practice, prefer Dolev-Strong, which has the same rounds and a message count that does not depend on what a traitor signs. Real systems are rarely synchronous, so a deployed protocol is usually one for [partial synchrony](/partial-synchrony/), such as [PBFT](/pbft/) or [HotStuff](/hotstuff/), with $n \ge 3t + 1$.

## Pitfalls

- **Repeated signers.** A chain $v{:}0{:}3{:}3$ has two signatures but only one signer. If a lieutenant counts signatures and not distinct signers, a traitorous commander and one traitorous lieutenant can fill a chain with $m$ lieutenant signatures and give a second order to one loyal lieutenant in round $m + 1$, when it can no longer relay. IC1 then breaks with only two traitors. Line L5 checks distinctness.
- **Accepting a chain late.** In the round form a chain with $k$ lieutenant signatures must arrive in round $k + 1$. A loyal lieutenant that accepts a short chain in the last round cannot relay it, so another loyal lieutenant may never see the order.
- **A choice that depends on order of arrival.** choice must be a function of the set $V_i$ only. A lieutenant that obeys the first order it saw breaks IC1 when the commander is a traitor.
- **Treating the signature as the message.** The signature of $j_k$ must cover $v$ and all earlier signatures. If it covers only $v$, a traitor can move signatures from one chain to another.
- **Not distributing keys first.** A4 (b) says that anyone can check anyone's signature. This needs a public key setup before the run, which is a trusted step outside the algorithm.

## Implementations

## History

Pease, Shostak and Lamport noted in 1980 that with authenticated messages, interactive consistency is possible for any number of faults. Lamport, Shostak and Pease gave SM(m) and its proof (Theorem 2) in the 1982 paper, together with the extension to incomplete graphs. Dolev and Strong (1983) gave the authenticated algorithm with $t + 1$ rounds and a polynomial number of messages, and proved that $t + 1$ rounds are needed. Dolev and Reischuk (1985) proved the lower bounds on messages and signatures.

## References

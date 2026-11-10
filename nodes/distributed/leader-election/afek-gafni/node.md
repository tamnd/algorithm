---
tag: 51R5KB
kind: algorithm
slug: afek-gafni
name: Afek-Gafni election algorithm
aliases:
- Afek-Gafni time and message bounds
area: distributed/leader-election
level: research
summary: Election on complete networks by capturing processes in doubling phases. Synchronous, O(n log n) messages and O(log n) time; asynchronous, O(n log n) messages and O(n) time.
solves: [complete-network-leader-election]
model: synchronous-model
complexity:
  vars: {n: the number of processes}
  time: {worst: O(log n)}
  messages: {worst: O(n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1991
  people: [Yehuda Afek, Eli Gafni]
  note: Time and message bounds for election in complete networks, with fast algorithms in both the synchronous and the asynchronous model.
prereqs: [complete-network-leader-election, synchronous-model, korach-kutten-moran, message-complexity]
see_also: [korach-kutten-moran, complete-network-leader-election, hirschberg-sinclair, awerbuch-leader-election, round-complexity, bully-algorithm, ring-election-lower-bound, explicit-leader-election]
sources:
  - paper: doi:10.1137/0220023
    title: Yehuda Afek and Eli Gafni, Time and message bounds for election in synchronous and asynchronous complete networks, SIAM Journal on Computing 20(2), 1991
    locator: pages 376 to 394 (the synchronous algorithm with O(n log n) messages and O(log n) time, the asynchronous algorithm with O(n log n) messages and O(n) time, and lower bounds)
  - paper: doi:10.1016/0304-3975(89)90103-5
    title: Ephraim Korach, Shlomo Moran and Shmuel Zaks, Optimal lower bounds for some distributed algorithms for a complete network of processors, Theoretical Computer Science 64(1), 1989
    locator: pages 125 to 132 (the lower bound of Ω(n log n) messages for election in complete networks)
  - book: isbn:9780471719977
    title: Nicola Santoro, Design and Analysis of Distributed Algorithms, Wiley, 2007
    locator: Chapter 3 (election in complete networks by capture in stages)
---

The Afek-Gafni algorithms elect a leader on a [complete network](/complete-network-leader-election/), where every pair of processes is linked, and they are fast as well as cheap in messages. Each candidate tries to *capture* other processes. A process that is already captured asks its owner, and the stronger of the two candidates goes on. In the synchronous model the candidates double the number of processes they ask in each phase, which gives $O(n \log n)$ messages and $O(\log n)$ rounds. In the asynchronous model the paper gives an algorithm with $O(n \log n)$ messages and $O(n)$ time. The message bound is optimal, by the lower bound of Korach, Moran and Zaks. This page gives a simplified synchronous form in full, with a proof, and describes the asynchronous one in outline.

## In plain words

Some people in a room want to be the leader, and anyone can talk to anyone. In the first step, each candidate asks one other person to join their team. In the next step each candidate who is still in asks two more people, then four, then eight.

A person who is asked by several candidates thinks only about the one with the biggest number. If that person is already in a team, they ask their team boss. A boss with a smaller number, or a boss who has already dropped out, lets them go, and a boss with a smaller number drops out. A candidate who gets a "no" from anybody drops out.

Teams of candidates who are still in never overlap, and they double in size each step. So the number of candidates halves each step, and after about $\log_2 n$ steps one candidate has everybody.

## The problem

There are $n$ processes, and each pair is joined by a link. Each process knows its own identifier and its $n - 1$ links, so it knows $n$, but not the identifiers at the other ends of its links. Identifiers are distinct. The form on this page is [synchronous](/synchronous-model/): the processes run in rounds, and every message sent in a round arrives before the next round. A nonempty set of processes, the *initiators*, start as candidates in the same round. The goal is that exactly one process ends as the leader, and that every process learns it.

## The algorithm

Each process $p$ has an *owner*, at first itself, and a flag *alive*, true for the initiators. The algorithm runs in phases $i = 0, 1, 2, \ldots$, each of 4 rounds.

```pseudo id=main
AFEK-GAFNI at process p, phase i                  ▷ the same code at every process
L1  round 1: if alive then send CAP⟨id(p)⟩ on the next min(2^i, untried) untried links
L2  round 2: take the request ⟨u⟩ with the largest u, from candidate c; if owner = p then
        accept iff not alive or u > id(p); if accepted then alive ← false
L3    else send Q⟨u⟩ to owner
L4  round 3: on each Q⟨u⟩ from x: if not alive or u > id(p) then send YES to x else send NO to x;
        if some YES was sent while alive then alive ← false
L5  round 4: if the chosen request was accepted (by L2 or by YES) then owner ← c; send ACC to c;
        send REJ to every other request
L6  end of phase: if some request of p got REJ then alive ← false
L7  if alive and all n − 1 links are tried then status ← leader; send LEADER⟨id(p)⟩ to all
```

A captured process can be captured again by a stronger candidate, and its owner can be dead. All live candidates are at the same phase, with the same number of captured processes, so identifiers alone decide every conflict.

## Example

Take $n = 8$ processes $p_0, \ldots, p_7$ with identifiers $3, 7, 2, 8, 5, 1, 6, 4$. All start. Process $p_v$ tries its links in the order $p_{v+1}, p_{v+2}, \ldots$, with indices modulo 8.

**Phase 0.** Each $p_v$ asks $p_{v+1}$. A process that owns itself and is alive accepts only a larger identifier. So $p_2, p_4, p_5, p_7, p_0$ are captured by $p_1, p_3, p_4, p_6, p_7$ and die, while $p_1, p_3, p_6$ reject $p_0, p_2, p_5$. The candidates $p_1, p_3, p_6$ got only ACC and are alive. There are 8 requests and 8 answers.

**Phase 1.** $p_1$ asks $p_3, p_4$; $p_3$ asks $p_5, p_6$; $p_6$ asks $p_0, p_1$.

| process | request | owner | outcome |
|---|---|---|---|
| $p_3$ | from $p_1$, 7 | itself, alive, 8 | REJ |
| $p_4$ | from $p_1$, 7 | $p_3$, alive, 8 | NO, REJ |
| $p_5$ | from $p_3$, 8 | $p_4$, dead | YES, ACC, owner $p_3$ |
| $p_6$ | from $p_3$, 8 | itself, alive, 6 | ACC, $p_6$ dies |
| $p_0$ | from $p_6$, 6 | $p_7$, dead | YES, ACC, owner $p_6$ |
| $p_1$ | from $p_6$, 6 | itself, alive, 7 | REJ |

Only $p_3$ is alive after phase 1. **Phase 2.** $p_3$ asks its last 4 links, $p_7, p_0, p_1, p_2$, whose owners $p_6, p_6, p_1, p_1$ are all dead, and gets 4 ACC. It has captured all 7 others and announces itself.

The run sends 18 requests, 6 queries, 6 answers to queries, 12 ACC, 6 REJ and 7 announcements, 55 messages in $3 \cdot 4 + 1 = 13$ rounds. The bound $4n\lceil \log_2 n \rceil = 96$ covers the 48 messages before the announcement.

## Correctness

The [proof of correctness](proofs/correctness/) shows the following.

- **The largest initiator never dies.** Let $m$ be the initiator with the largest identifier. Its request is the largest at every process it asks, every owner is either dead or smaller and answers YES, and no request to $m$ or query to $m$ carries a larger identifier. So it gets only ACC.
- **No other candidate can finish.** To finish, a candidate must capture $m$'s process, and $m$ owns it, is alive and rejects every smaller identifier.
- **Owners stay owners.** If a candidate $c$ is alive at the end of phase $i$, it owns every process it has captured, because a change of owner needs a YES from $c$, which kills it.

So $m$ is the only leader, and it is elected at the end of phase $\lceil \log_2 n \rceil - 1$, when it has tried all its links.

## Complexity

**Messages.** By the third point above, the candidates alive after phase $i$ own disjoint sets of $2^{i+1}$ processes, counting themselves, as long as $2^{i+1} \le n$. So at most $n / 2^{i+1}$ of them remain, and in phase $i + 1$ they send at most $2^{i+1}$ requests each, at most $n$ in all. In phase 0, at most $n$ requests are sent too. Each request causes at most one query, one answer to the query and one ACC or REJ. So each phase sends at most $4n$ messages, and with $\lceil \log_2 n \rceil$ phases the election sends at most

$$4n \lceil \log_2 n \rceil + (n - 1) = O(n \log n)$$

messages, the last term for the announcement.

**Time.** Exactly $4 \lceil \log_2 n \rceil + 1$ rounds for $n \ge 2$, because $m$ needs $\lceil \log_2 n \rceil$ phases to try all $n - 1$ links. This is $O(\log n)$.

**Space.** A process stores its owner, its flag, its phase and a pointer into its list of links. In round 2 it looks at all requests that arrive, at most $n - 1$.

## Properties

- **Deterministic.** The leader is the initiator with the largest identifier.
- **Optimal in messages.** No election on a complete network can use $o(n \log n)$ messages in the asynchronous case, by the lower bound of Korach, Moran and Zaks. The synchronous form matches this bound too.
- **Fast.** $O(\log n)$ rounds, against the $n - 1$ sequential captures of the [traversal method](/korach-kutten-moran/).
- **Explicit.** With the announcement, every process learns the leader.

## Variants and improvements

- **Asynchronous algorithm (outline).** Without rounds, a candidate cannot double its requests in step with the others. The asynchronous algorithm of the paper captures processes one at a time, with a level equal to the number of processes captured, and compares levels before identifiers, as in the complete-network form on the [Korach-Kutten-Moran page](/korach-kutten-moran/). The paper adds rules that keep candidates from waiting for each other for a long time, and it proves $O(n \log n)$ messages and $O(n)$ time. This page does not give those rules.
- **Trade-offs.** The paper also studies how time and messages trade against each other in the synchronous model: with more parallel requests per phase, the time goes down and the messages go up. It proves lower bounds that show its algorithms are close to the best possible. The exact statements are in the paper.
- **Simple broadcast.** If messages do not matter, each process can send its identifier to all others, and the largest wins in one round with $n(n - 1)$ messages. The [bully algorithm](/bully-algorithm/) is a form of this idea with failures.
- **General networks.** On an arbitrary network, [Awerbuch's algorithm](/awerbuch-leader-election/) elects with $O(m + n \log n)$ messages and $O(n)$ time.

## When to use it

Use it when all processes are linked to each other, as in a small cluster with a full mesh, and both the number of messages and the time matter. In the synchronous model it is the standard example of an election with $O(n \log n)$ messages in $O(\log n)$ rounds. If the network is not complete, it does not apply directly.

## Pitfalls

- **Answering every request.** A process must take only the largest request of a phase and reject the others. If it accepts two, two candidates own it, and the domains are no longer disjoint.
- **Trusting a stale owner.** A captured process does not know whether its owner is still alive. It must ask; answering for the owner can let a small candidate survive next to a larger one.
- **Keeping a candidate with a rejected request.** A candidate that got even one REJ in a phase must drop out, or the halving argument fails.
- **Using the synchronous form in an asynchronous network.** The proof needs all live candidates to be in the same phase. Without rounds, identifiers alone do not decide conflicts well, and the number of messages can grow.

## Implementations

## History

Yehuda Afek and Eli Gafni studied election on complete networks in both timing models, after Korach, Moran and Zaks had shown that $\Theta(n \log n)$ messages are needed and enough. Their algorithms keep the optimal number of messages and cut the time to $O(\log n)$ rounds in the synchronous model and to $O(n)$ in the asynchronous one. The journal version appeared in the SIAM Journal on Computing in 1991, after a conference version. The capture technique, with owners and levels, became the standard method for election on complete networks and appears in later work and in textbooks.

## References

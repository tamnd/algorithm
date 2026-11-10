---
tag: KB0GBC
kind: algorithm
slug: korach-kutten-moran
name: Korach-Kutten-Moran algorithm
aliases:
- KKM leader election
- Election by competing traversals
area: distributed/leader-election
level: research
summary: Turns any serial traversal into an election with O((f(n) + n) log n) messages, where f(n) is the cost of the traversal. On a complete network this gives O(n log n), which is optimal.
solves: [complete-network-leader-election]
model: asynchronous-model
complexity:
  vars: {n: the number of processes, f(n): the number of messages of one serial traversal}
  time: {worst: O(n log n)}
  messages: {worst: O(n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1985
  people: [Ephraim Korach, Shay Kutten, Shlomo Moran]
  note: A modular construction of election from traversal, which gives the known O(n log n) bounds for rings and complete networks from one scheme.
prereqs: [complete-network-leader-election, graph-traversal, asynchronous-model, message-complexity]
see_also: [afek-gafni, complete-network-leader-election, hirschberg-sinclair, franklin, awerbuch-leader-election, ring-election-lower-bound, gallager-humblet-spira, eulerian-circuit]
sources:
  - paper: doi:10.1145/77606.77610
    title: Ephraim Korach, Shay Kutten and Shlomo Moran, A modular technique for the design of efficient distributed leader finding algorithms, ACM Transactions on Programming Languages and Systems 12(1), 1990
    locator: pages 84 to 101 (the construction from a serial traversal and the bound (f(n) + n) log n)
  - book: isbn:9780521794831
    title: Gerard Tel, Introduction to Distributed Algorithms, second edition, Cambridge University Press, 2000
    locator: Chapter 7 (election with traversal algorithms, annexing and chasing tokens with levels)
  - paper: doi:10.1016/0304-3975(89)90103-5
    title: Ephraim Korach, Shlomo Moran and Shmuel Zaks, Optimal lower bounds for some distributed algorithms for a complete network of processors, Theoretical Computer Science 64(1), 1989
    locator: pages 125 to 132 (the lower bound of Ω(n log n) messages for election in complete networks)
---

The Korach-Kutten-Moran algorithm is a general way to build a leader election algorithm from a *serial traversal*, an algorithm in which one token visits the processes one after the other. Each candidate starts a traversal of the network, and the traversals compete: when two of them meet, at most one goes on, and the levels of the survivors grow. If one traversal costs $f(n)$ messages, the election costs $O((f(n) + n) \log n)$ messages. On a [complete network](/complete-network-leader-election/) a traversal costs $O(n)$, so the election costs $O(n \log n)$ messages, which matches the lower bound of Korach, Moran and Zaks. On a ring the same scheme gives the $O(n \log n)$ of [Hirschberg and Sinclair](/hirschberg-sinclair/). This page describes the general scheme in outline and then gives one complete-network form in full, with a proof.

## In plain words

Some people in a group want to be the leader. Each of them walks round the group and asks the others, one at a time, to join their team. Each candidate has a score, which is the number of people that have joined their team so far.

If a person already belongs to a team, they ask their team boss to compare the two scores. The candidate with the lower score drops out, and if the two scores are equal, the higher number wins. So a strong candidate grows, and weak candidates stop early.

The first candidate whose team holds everybody is the leader. Big teams cannot overlap, so only a few candidates get far, and the total number of questions stays small.

## The problem

The general scheme works on any network that has a serial traversal. The form on this page is for a complete network: $n$ processes, and a link between every pair. Each process knows its own identifier and its $n - 1$ links, but not the identifiers of the others. Identifiers are distinct. The model is [asynchronous](/asynchronous-model/), channels are reliable and need not be FIFO. Any nonempty set of processes starts on its own; a process that gets a message before it starts does not become a candidate. The goal is that exactly one process ends as the leader.

## The algorithm

**The general scheme, in outline.** This outline follows the abstract of the paper and Tel's account, and it is a paraphrase, not the exact rules. Each initiator starts a traversal token of level 0. A token *annexes* the processes it visits: each process records the origin and the level of the token that annexed it last. A token that reaches a process annexed at a higher level dies. When two tokens of the same level meet, they are both destroyed, and one new traversal of the next level starts. A token that arrives behind the front of another traversal of its level can *chase* that front along the recorded path. Because each token of level $l + 1$ comes from two tokens of level $l$, at most $k / 2^l$ tokens reach level $l$ when $k$ processes start, so there are at most $\lfloor \log_2 k \rfloor + 1$ levels. A token that completes its traversal makes its origin the leader. Korach, Kutten and Moran show that each level costs $O(f(n) + n)$ messages, which gives the bound.

**A complete-network form.** The form below uses the star traversal: a candidate $c$ visits the other processes one link at a time, and each visit is a request and an answer. Every process $x$ has a pair $\mathrm{pair}(x) = (\mathit{lev}_x, \mathrm{id}(x))$, where $\mathit{lev}_x$ is the number of processes $x$ has captured as a candidate, or $-1$ if $x$ never was a candidate. Pairs are compared in lexicographic order. Each process also has an *owner*, at first itself, a flag *alive*, and a flag *busy* with a queue of waiting requests. Conflicts are settled by a direct check with the owner, as in the capture algorithm of [Afek and Gafni](/afek-gafni/), and not by chasing.

```pseudo id=main
KKM-COMPLETE at process p                     ▷ the same code at every process
L1  on start, if no message has arrived: alive ← true; lev ← 0; send CAP⟨pair(p)⟩ on the next untried link
L2  on CAP⟨P⟩ from c, not busy, owner = p: if P > pair(p) then alive ← false; owner ← c; send ACC to c
        else send REJ to c
L3  on CAP⟨P⟩ from c, not busy, owner ≠ p: busy ← (c, P); send Q⟨P⟩ to owner     ▷ a CAP that comes while busy waits in a queue
L4  on Q⟨P⟩ from x: if P > pair(p) then alive ← false; send YES to x else send NO to x
L5  on YES or NO, with busy = (c, P): if YES then owner ← c; send ACC to c; else send REJ to c;
        busy ← none; handle the next waiting CAP, if any
L6  on ACC: if alive then lev ← lev + 1; if lev = n − 1 then status ← leader else send CAP⟨pair(p)⟩ on the next untried link
L7  on REJ: alive ← false
```

A candidate has at most one request in transit. A dead candidate keeps its last pair. A process answers a query at once, even when it is busy itself, and this is why the algorithm cannot block.

## Example

Take $n = 4$ processes $a, b, c, d$ with identifiers $3, 8, 5, 1$. Only $a$ and $c$ start. The untried links of $a$ are in the order $b, c, d$, and those of $c$ in the order $b, d, a$. Every message takes one time unit.

| time | events |
|---|---|
| 0 | $a$ sends $\mathrm{CAP}\langle 0, 3 \rangle$ to $b$, and $c$ sends $\mathrm{CAP}\langle 0, 5 \rangle$ to $b$. |
| 1 | $b$ handles the request of $a$ first. It owns itself and $(0, 3) > (-1, 8)$, so its owner becomes $a$ and it sends ACC to $a$. Then it handles the request of $c$: its owner is $a$, so it sends $\mathrm{Q}\langle 0, 5 \rangle$ to $a$. |
| 2 | $a$ handles the ACC first: its level becomes 1, and it sends $\mathrm{CAP}\langle 1, 3 \rangle$ to $c$. Then the query: $(0, 5) < (1, 3)$, so $a$ sends NO to $b$. |
| 3 | $c$ owns itself and $(1, 3) > (0, 5)$, so $c$ dies, its owner becomes $a$, and it sends ACC to $a$. $b$ gets NO and sends REJ to $c$. |
| 4 | $a$ reaches level 2 and sends $\mathrm{CAP}\langle 2, 3 \rangle$ to $d$. The REJ reaches $c$, which is already dead. |
| 5 | $d$ owns itself and $(2, 3) > (-1, 1)$, so it sends ACC to $a$. |
| 6 | $a$ reaches level $3 = n - 1$ and is the leader. |

The run sends 10 messages. The leader has identifier 3, not the largest one: the level counts first. If $a$ had handled the query before the ACC at time 2, then $(0, 5) > (0, 3)$ and $a$ would have died, and $c$ would have been elected.

## Correctness

The [proof of correctness](proofs/correctness/) shows the following for the complete-network form.

- **Owners only get stronger.** When the owner of a process changes, the new owner's request pair is larger than the old owner's pair at that time, and pairs never decrease. So the request pairs of the successive owners of a process increase.
- **A capture of a live candidate kills it.** While a candidate is alive, it owns its own process, so any capture of that process, or of a process it owns, goes through a comparison with its pair and kills it if it loses.
- **At most one leader.** A leader has captured every other process, including every other candidate's own process. A second leader would have to capture the first one's process, which kills the first one before it is elected or fails against the pair $(n - 1, \cdot)$, the largest level possible.
- **Some leader.** The candidate with the largest final pair can never lose a comparison, so it never dies. No process waits for ever, because queries are answered at once. So this candidate captures all $n - 1$ others and is elected.

## Complexity

**Messages.** Call a candidate's own process and the first $j$ processes that raise its level its *domain at level $j$*. The proof shows that the domains at level $j$ of two different candidates are disjoint. Each has $j + 1$ processes, so at most $n / (j + 1)$ candidates reach level $j$. A candidate that ends at level $L$ sends at most $L + 1$ requests, so the number of requests is at most

$$\sum_{j=0}^{n-1} \#\{c : L_c \ge j\} \le \sum_{j=0}^{n-1} \frac{n}{j + 1} = n H_n \approx n \ln n.$$

Each request causes at most 3 more messages (a query, an answer, and an ACC or REJ), so the run sends at most $4 n H_n = O(n \log n)$ messages. With one candidate, no query is needed and the count is exactly $2(n - 1)$. To make the election [explicit](/explicit-leader-election/), the leader sends $n - 1$ more messages.

**Time.** If every message takes one time unit, at least one message arrives in each time unit until the end, so the time is at most the number of messages, $O(n \log n)$. The tests show times below $4n$ on small networks, but this page does not prove a linear bound. The algorithm of Afek and Gafni gets $O(n)$ time with $O(n \log n)$ messages.

**Space.** A process stores its pair, its owner, a pointer into its list of links and a queue of at most $n - 1$ waiting requests.

## Properties

- **Deterministic and asynchronous.** Correct under every schedule, with or without FIFO channels.
- **Message optimal.** Election in an asynchronous complete network needs $\Omega(n \log n)$ messages, by the lower bound of Korach, Moran and Zaks.
- **Not always the largest identifier.** The leader is the candidate with the largest final pair. A small identifier that grows early can win.
- **Modular.** In the general scheme, the traversal is a parameter. A better traversal on some class of networks gives a better election on that class.

## Variants and improvements

- **Rings.** On a ring, a traversal goes round once, with $f(n) = n$, and the scheme gives $O(n \log n)$ messages, the bound of [Hirschberg and Sinclair](/hirschberg-sinclair/), [Franklin](/franklin/) and [Peterson](/peterson-leader-election/).
- **Traversals of all links.** The paper also gives a form for traversals that pass every link, with $O((f(m) + n) \log n)$ messages for a network with $m$ links. With an [Euler tour](/eulerian-circuit/) in an Eulerian network, $f(m) = m$.
- **Faster complete-network election.** [Afek and Gafni](/afek-gafni/) let a candidate capture many processes at the same time, which gives $O(\log n)$ time in synchronous networks and $O(n)$ time in asynchronous ones, both with $O(n \log n)$ messages.
- **General networks.** On an arbitrary network, [Awerbuch's algorithm](/awerbuch-leader-election/) and [Gallager, Humblet and Spira](/gallager-humblet-spira/) give $O(m + n \log n)$ messages.

## When to use it

Use the general scheme to get an election for a class of networks that already has a cheap serial traversal; the bound then comes for free. Use the complete-network form when every pair of processes is linked, any set of them may start, and messages matter more than time. If time also matters, the algorithm of Afek and Gafni is faster for the same number of messages.

## Pitfalls

- **Comparing identifiers only.** If a request wins only because its identifier is larger, a late candidate with a large identifier can take over the domains of many earlier ones, and the number of messages can grow to $\Theta(n^2)$. The level must count first.
- **Answering for a captured process without its owner.** A captured process does not know whether its owner is still alive or how strong it has become. It must ask the owner, or two candidates could both believe they own it.
- **Handling two requests at once.** A process must check one request with its owner at a time. The bound on messages uses the fact that the captures of one process happen in sequence.
- **Late starters.** A process that has already got a message must not become a candidate. Otherwise it would compete with level 0 against a candidate that already counts it in its domain.
- **Reading the general scheme as exact.** The outline above simplifies the token rules of the paper. A version of the chasing rules made up from it can block with no leader, so take the rules from the paper or from Tel.

## Implementations

## History

Korach, Moran and Zaks proved in 1984 that election in an asynchronous complete network needs $\Omega(n \log n)$ messages and gave an algorithm that meets this bound. Ephraim Korach, Shay Kutten and Shlomo Moran presented their modular technique at PODC in 1985, and the journal version appeared in ACM TOPLAS in 1990. Its point was to explain the many $O(n \log n)$ election algorithms for rings and complete networks as instances of one scheme, with the traversal as the only part that depends on the network. Afek and Gafni later improved the time for complete networks while keeping the number of messages.

## References

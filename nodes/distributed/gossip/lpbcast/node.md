---
tag: DD2C6C
kind: algorithm
slug: lpbcast
name: lpbcast
aliases:
- lightweight probabilistic broadcast
- Lightweight Probabilistic Broadcast
area: distributed/gossip
level: advanced
summary: Gossip broadcast in which each process keeps a fixed size random view and piggybacks subscriptions, unsubscriptions and event ids on the gossip messages, so membership costs no extra traffic.
solves: [probabilistic-broadcast, membership-management]
model: asynchronous-model
complexity:
  vars: {n: the number of processes, l: the view size, F: the fanout}
  rounds: {expected: O(log n)}
  space: {extra: O(l)}
properties: {deterministic: false, recursive: false}
prereqs: [gossip-protocol, gossip-fanout, peer-sampling-service]
see_also: [probabilistic-broadcast, bimodal-multicast, scamp, hyparview, membership-management, gossip-fanout, rumor-mongering, peer-sampling-service]
sources:
  - paper: doi:10.1145/945506.945507
    title: Patrick Th. Eugster, Rachid Guerraoui, Sidath B. Handurukande, Petr Kouznetsov and Anne-Marie Kermarrec, Lightweight probabilistic broadcast, ACM Transactions on Computer Systems 21(4), 2003
    locator: pages 341 to 374 (the view, the subs, unSubs, events and eventIds buffers, gossip emission and reception, the analysis of the infection process with uniform views, and the effect of the view size)
  - paper: "Patrick Th. Eugster, Rachid Guerraoui, Sidath B. Handurukande, Anne-Marie Kermarrec and Petr Kouznetsov, Lightweight probabilistic broadcast, International Conference on Dependable Systems and Networks (DSN), 2001"
    locator: the first version of the protocol
---

lpbcast (lightweight probabilistic broadcast) is a gossip broadcast protocol, from Eugster, Guerraoui, Handurukande, Kouznetsov and Kermarrec (2001, 2003), in which every process knows only a random view of $l$ processes and the membership information travels inside the gossip messages themselves. Once per round each process sends one message to $F$ random members of its view; the message carries the new notifications, recent subscriptions, recent unsubscriptions, and the ids of the notifications that the sender has delivered. The receiver updates its view from the subscriptions, so the views stay random with no separate membership protocol. The paper shows that, with uniform views, the delivery of a notification depends on the fanout $F$ and hardly on the view size $l$.

## In plain words

Every member of a big group knows the names of only a few other members. Once per round, each member writes a short letter and sends a copy to a few names on its list.

The letter holds the news it heard since the last round, the names of members who joined recently, the names of members who left, and a list of all the news it knows about. A reader adds new names to its list, crosses out members who left, and keeps the list short by moving some names out at random.

So the same letters that carry the news also keep the lists fresh, and no member needs to know the whole group. A reader that sees a news item in the list but did not get the item itself can ask the writer for it.

## The problem

[Probabilistic broadcast](/probabilistic-broadcast/) asks that a notification reach almost every process with high probability, with a load per process that does not grow with the group. Flat gossip needs a membership service that gives each process random targets. A full membership list costs $O(n)$ memory and $O(n)$ traffic per change. lpbcast keeps only $O(l)$ state and folds the membership traffic into the gossip, which makes it a [membership management](/membership-management/) protocol as well.

## The algorithm

Each process $p$ keeps:

- view($p$), at most $l$ processes;
- subs($p$) and unSubs($p$), recent subscriptions and unsubscriptions, each with a maximum size;
- events($p$), the notifications received since the last gossip;
- eventIds($p$), the ids of delivered notifications, with a maximum size.

```pseudo id=main
LPBCAST-ROUND(p), once per period T
L1  gossip ← (events(p), subs(p) ∪ {p}, unSubs(p), eventIds(p))
L2  send gossip to F random members of view(p); events(p) ← ∅
ON-GOSSIP(g) at p, from sender
L3  for each u in g.unSubs: remove u from view(p) and subs(p), and add u to unSubs(p)
L4  for each s in g.subs with s ≠ p, s ∉ view(p) and s ∉ unSubs(p): add s to view(p) and to subs(p)
L5  while |view(p)| > l: move a random member of view(p) to subs(p)
L6  trim subs(p) and unSubs(p) to their maximum sizes by removing random elements
L7  for each e in g.events with id(e) ∉ eventIds(p): deliver e, add e to events(p), add id(e) to eventIds(p)
L8  for each id in g.eventIds with id ∉ eventIds(p): note (id, sender) in retrieveBuf(p)
L9  later, for each id in retrieveBuf(p) still not delivered: ask the sender, then other processes, for the notification
```

To broadcast $e$, a process delivers it and puts it into events($p$). Since events($p$) is emptied after each gossip (line L2), each process forwards each notification in only one round. A new process joins by sending its subscription to one member, which adds it to subs and so to its next gossip messages. A leaving process gossips an unsubscription; unsubscriptions carry a time stamp in the paper and are dropped after a while, so that a buffer of old unsubscriptions does not grow.

## Example

**One gossip.** Take $l = 3$. Process $p$ has view $\{a, b, c\}$ and receives from $q$ a gossip with subs $\{q, d\}$, unSubs $\{b\}$, one new notification $e_7$ and eventIds $\{e_5, e_7\}$. Line L3 removes $b$, giving $\{a, c\}$. Line L4 adds $q$ and $d$, giving $\{a, c, q, d\}$. Line L5 moves a random member, say $c$, to subs, so the view is $\{a, q, d\}$. Line L7 delivers $e_7$, which $p$ will forward in its next round. If $p$ has not delivered $e_5$, line L8 notes it, and line L9 fetches it from $q$.

**Delivery against view size.** When every process forwards a notification once to $F$ uniform random processes, the fraction $x$ reached in a large group solves $x = 1 - e^{-F x}$: for $F = 2, 3, 4$ this gives 0.797, 0.941 and 0.980. The implementation runs 500 processes with no message loss, after 3 rounds of view mixing, and measures the fraction that delivers a notification, without retrieval, over 15 notifications:

| $F$ | $l = F$ | $l = 2F$ | $l = 15$ | $l = 30$ | $l = 60$ | $x = 1 - e^{-Fx}$ |
|---|---|---|---|---|---|---|
| 2 | 0.432 | 0.616 | 0.739 | 0.761 | 0.780 | 0.797 |
| 3 | 0.842 | 0.853 | 0.898 | 0.913 | 0.928 | 0.941 |
| 4 | 0.914 | 0.924 | 0.948 | 0.971 | 0.974 | 0.980 |

For $F \ge 3$ the view size matters little: a view four times larger than the fanout gives most of the reliability of a uniform choice over all $n$ processes. The gap to the prediction comes from correlations between views: a gossip carries the sender and its recent subscriptions, so the receiver's view shares entries with the sender's. When $l = F$, a process sends to its whole view, and for $F = 2$ this is clearly worse. With retrieval (lines L8 and L9) every notification reached all 300 processes in the tests. The implementation fetches a missing notification at the end of the round, while the paper first waits some rounds; so here about a third of the deliveries were retrievals, because a process often learns an id from a digest before the notification itself reaches it. The unsubscription of a process removed it from all views within 5 rounds.

## Correctness

The proved claims are: every view holds at most $l$ processes and never its owner; a process delivers each notification at most once; a process that leaves is never added again to a view while its unsubscription is in the receiver's unSubs buffer; and, if the views are independent uniform samples, each round the probability that a given uninfected process is reached by one of the $i$ processes that forward the notification is $1 - (1 - F/(n - 1))^i$, whatever the view size $l$. The full proof is below.

That the views stay close to uniform samples is not proved. The paper argues it from the random replacement in lines L4 to L6 and checks it by simulation.

## Complexity

- **Rounds.** The notification spreads like an infect-and-die rumour with fanout $F$: the number of processes that deliver it grows by a factor of about $F$ per round until most have it, so about $\log_F n$ rounds plus a few.
- **Messages.** $F$ messages per process per period, whatever the number of notifications; each notification is forwarded by each process once, so it costs at most $F n$ sends.
- **Message size.** $|\text{events}| + |\text{subs}| + |\text{unSubs}| + |\text{eventIds}|$ entries, all bounded by their maximum sizes.
- **Space.** $O(l)$ for the view plus the bounded buffers.

## Properties

- **No membership traffic.** Views change only through information carried on gossip messages.
- **Bounded state.** All buffers have a maximum size, and random trimming keeps them unbiased.
- **Reliability set by $F$.** The view size matters little once it is a few times $F$; the fanout and the retrieval of missing ids set the delivery ratio.
- **Uneven in-degree.** In the simulations the number of views that hold a process varies more than in a uniform random graph (variance 54 against a mean of 15 for $l = 15$), because a process puts itself into every gossip it sends.

## Variants and improvements

- **Age-based buffer management.** Kouznetsov, Guerraoui, Handurukande and Kermarrec (SRDS 2001) kept notifications in the buffer for several rounds and purged the oldest first, which raises delivery under buffer limits.
- **Fixed views from a peer sampling service.** Modern designs take $F$ targets from a [peer sampling service](/peer-sampling-service/) such as [Cyclon](/cyclon/), and keep the broadcast and the membership apart.
- **[Bimodal multicast](/bimodal-multicast/)** combines an unreliable multicast with gossip of digests, the same idea as lines L8 and L9.

## When to use it

Use lpbcast for publish and subscribe or event dissemination in large groups where the membership changes all the time and a missed notification now and then is acceptable. With retrieval, it also gives near full delivery. When an always connected overlay with fast repair is needed, [HyParView](/hyparview/) is a better base.

## Pitfalls

- **Fanout too small.** With $F = 2$, a fifth of the processes miss each notification even with uniform views; retrieval or a larger $F$ is needed.
- **Unsubscriptions that never expire.** Without time stamps, the unSubs buffer can keep removing a process that has joined again.
- **Buffers too small.** If events or eventIds are trimmed too early, notifications are lost or delivered twice.
- **Initial views.** The analysis assumes random views from the start; a group that grows from one process must run some rounds before the views are mixed.

## Implementations

## History

Eugster, Guerraoui, Handurukande, Kermarrec and Kouznetsov presented lpbcast at DSN 2001, and published the full version with the analysis in ACM Transactions on Computer Systems in 2003. It came from work on publish and subscribe systems at EPFL and Microsoft Research Cambridge, and its idea of piggybacking membership on gossip messages was taken up by later peer sampling protocols.

## References

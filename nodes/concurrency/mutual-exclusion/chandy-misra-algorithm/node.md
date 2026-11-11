---
tag: 0J7AS3
kind: algorithm
slug: chandy-misra-algorithm
name: Chandy-Misra solution to dining philosophers
aliases:
- Chandy-Misra dining philosophers
- hygienic dining philosophers
- hygienic solution
area: concurrency/mutual-exclusion
level: advanced
summary: Forks passed in messages are clean or dirty, and a philosopher gives up a dirty fork when asked. The precedence graph stays acyclic, so every hungry philosopher eats, on any conflict graph.
model: word-ram
complexity:
  vars: {n: the number of philosophers, d: the degree of a philosopher in the conflict graph}
  time:
    worst: "O(d)"
  space:
    extra: "O(d)"
history:
  year: 1984
  people: [K. Mani Chandy, Jayadev Misra]
  note: Chandy and Misra gave the hygienic solution, for any conflict graph and for drinking philosophers, in 1984. It needs no global order at run time, only an acyclic start.
prereqs: [dining-philosophers-problem]
see_also: [dining-philosophers-problem, lock-ordering, starvation-freedom, directed-acyclic-graph, graph-coloring, wait-for-graph, chandy-misra-bryant, deadlock]
sources:
  - paper: doi:10.1145/1780.1804
    title: K. M. Chandy and J. Misra, The drinking philosophers problem, ACM Transactions on Programming Languages and Systems 6(4), 1984, pages 632 to 646
    locator: the hygienic solution of the dining philosophers (clean and dirty forks, request tokens, the precedence graph and its acyclicity), and the drinking philosophers problem and its solution
  - paper: doi:10.1007/BF00289519
    title: Edsger W. Dijkstra, Hierarchical ordering of sequential processes, Acta Informatica 1(2), 1971, pages 115 to 138
    locator: the five dining philosophers, the problem that Chandy and Misra generalize
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: the chapter on asynchronous network resource allocation, on dining philosophers in a message passing network
---

The Chandy and Misra algorithm, often called the hygienic solution, solves the [dining philosophers problem](/dining-philosophers-problem/) for any conflict graph, by message passing. Each pair of neighbours shares a fork and a request token. A fork is clean or dirty: it becomes dirty when its holder eats, and it is cleaned when it is sent. A philosopher keeps a clean fork, and gives up a dirty fork when the neighbour asks for it. The forks define a precedence graph on the philosophers, and the rules keep that graph acyclic, which gives deadlock freedom and, more, starvation freedom. It appeared in the 1984 paper "The drinking philosophers problem", which also solves that more general problem. It is a different piece of work from the deadlock detection of Chandy, Misra and Haas, outlined on the [wait-for graph](/wait-for-graph/) page, and from the Chandy and Misra simulation algorithm, [Chandy-Misra-Bryant](/chandy-misra-bryant/).

## In plain words

Each pair of neighbours shares one fork, and each fork is either clean or dirty. A fork becomes dirty when someone eats with it. When you are asked for a dirty fork, you must wipe it and hand it over, unless you are eating right now. A clean fork you may keep until you have eaten.

So a person who has just eaten holds only dirty forks and gives way to every neighbour. A person who has just been handed a clean fork keeps it. Taking turns like this means that nobody can wait in a circle, and nobody waits for ever.

At the start, all forks are dirty and each one lies with the lower numbered of its two neighbours. That one choice at the start is the only place where numbers are used.

## The problem

The conflict graph $G$ is an undirected graph whose vertices are $n$ philosophers. A philosopher must hold the forks of all its edges to eat, and two neighbours must never eat at the same time. The model is asynchronous message passing: each philosopher is a process with its own memory, and each edge is a reliable channel in both directions that delivers every message after a finite but unbounded delay. Processes do not crash; a crash of a philosopher that holds a fork would block its neighbours, and this algorithm, like the others for the problem, does not handle that. The primitives are send and receive. Each philosopher may think for ever, but each meal is finite.

| Symbol | Meaning |
|---|---|
| $n$ | the number of philosophers |
| $p, q$ or $u, w$ | philosopher names; $i, j$ are indices |
| $m$ | the number of edges of $G$, which is the number of forks (the shared objects) |
| $d$ | the degree of a philosopher, the number of its forks |
| $k$ | the contention: the number of hungry philosophers |
| $H$ | the precedence graph, an orientation of $G$ |

The properties are exclusion (safety: neighbours never eat together), [deadlock freedom](/deadlock-freedom/), and [starvation freedom](/starvation-freedom/): every hungry philosopher eventually eats.

## The algorithm

Each edge $e = \{u, w\}$ has one fork, which is at one end or in a message on its way, with a bit clean or dirty, and one request token, also at one end or on its way. Philosopher $u$ runs the following rules, one enabled rule per step.

```pseudo id=main
CHANDY-MISRA, the rules of philosopher u
L1  start: for each edge {u, w} with u < w, the fork is at u and dirty, and the token is at w
L2  if u is thinking and wants to eat then u becomes hungry
L3  if u is hungry and holds the token of an edge e but not its fork then send the token to the neighbour on e
L4  if u holds the fork and the token of e, the fork is dirty, and u is not eating then clean the fork and send it to the neighbour on e
L5  a token or a fork that arrives is kept; a fork always arrives clean
L6  if u is hungry, holds all its forks, and each one is clean or has its token away from u then u eats, and all its forks become dirty
L7  when u stops eating, it becomes thinking
```

The token is the request: a philosopher that holds the token of an edge but not the fork may ask for the fork by sending the token (L3). A philosopher that holds both the fork and the token of an edge has a pending request from its neighbour. It must then give up the fork if the fork is dirty and it is not eating (L4); after sending the fork it keeps the token, so if it is still hungry it asks for the fork back at once with L3. A clean fork is never sent, so a philosopher that has received a fork keeps it until it has eaten. The test in L6 stops a hungry philosopher from eating with a dirty fork that a neighbour has asked for; it must send that fork first.

**The precedence graph.** Orient each edge $\{u, w\}$ as $u \to w$ ($u$ has precedence) if the fork is clean on $u$'s side, or dirty on $w$'s side; a fork on its way counts as clean at its receiver. Sending a dirty fork (L4) does not change the direction: before, $w$ had precedence because $u$ held the fork dirty; after, $w$ has precedence because it holds the fork clean. The only rule that changes $H$ is L6: all the forks of the eater become dirty, so all its edges point to it, and it becomes a sink. Making a vertex a sink cannot create a cycle. The start, with all forks dirty at the lower numbered end, makes $H$ acyclic, with every edge from the higher to the lower number. So $H$ is acyclic for ever.

## Example

A triangle $p_0, p_1, p_2$. At the start the forks $\{0, 1\}$ and $\{0, 2\}$ are at $p_0$ and $\{1, 2\}$ is at $p_1$, all dirty; the tokens are at the other ends. So $H$ has $p_1 \to p_0$, $p_2 \to p_0$ and $p_2 \to p_1$: $p_2$ has precedence over everyone. The table is a run of the implementation; a trailing "on the way" means a message.

| step | rule | forks: $\{0,1\}$, $\{0,2\}$, $\{1,2\}$ | tokens | states |
|---|---|---|---|---|
| start | L1 | $p_0$ dirty, $p_0$ dirty, $p_1$ dirty | $p_1$, $p_2$, $p_2$ | all thinking |
| $p_2$ | L2 | same | same | $p_2$ hungry |
| $p_2$ | L3 twice | same | $p_1$, to $p_0$, to $p_1$ | |
| network | L5 twice | same | $p_1$, $p_0$, $p_1$ | |
| $p_1$ | L4 | $p_0$ dirty, $p_0$ dirty, to $p_2$ clean | same | |
| $p_0$ | L4 | $p_0$ dirty, to $p_2$ clean, to $p_2$ clean | same | |
| network | L5 twice | $p_0$ dirty, $p_2$ clean, $p_2$ clean | same | |
| $p_2$ | L6 | $p_0$ dirty, $p_2$ dirty, $p_2$ dirty | same | $p_2$ eats; now a sink |
| $p_0$ | L2, L3 | same | $p_1$, to $p_2$, $p_1$ | $p_0$ hungry |
| network | L5 | same | $p_1$, $p_2$, $p_1$ | $p_2$ eating, keeps the fork |
| $p_2$ | L7, L4 | $p_0$ dirty, to $p_0$ clean, $p_2$ dirty | same | $p_2$ thinking |
| network, $p_0$ | L5, L6 | $p_0$ dirty, $p_0$ dirty, $p_2$ dirty | same | $p_0$ eats |

In the last step $p_0$ eats with the dirty fork $\{0, 1\}$, which is allowed since $p_1$ has not asked for it (its token is at $p_1$). After $p_2$ ate, $H$ has $p_0 \to p_2$ and $p_1 \to p_2$; after $p_0$ eats, $p_1$ has precedence over both.

## Correctness

The full proofs are in the formal proof file. The main steps are these.

1. **A pending request means hunger.** If the token and the fork of $\{u, w\}$ are both on $u$'s side, then $w$ is hungry: the token came from $w$ by L3, and $w$ cannot eat without that fork.
2. **Clean forks belong to hungry philosophers, eaters hold dirty forks.** A fork is cleaned only when it is sent to a neighbour with a pending request, who is hungry by step 1, and it stays clean until that neighbour eats. An eater holds all its forks (L6) and sends none while eating (L4).
3. **Exclusion.** Neighbours share a fork, and an eater holds all its forks.
4. **$H$ stays acyclic.** As shown above: L4 keeps the direction of the edge, and L6 makes the eater a sink.
5. **Every hungry philosopher eats.** Let $\mathit{anc}(u)$ be the set of philosophers with a path to $u$ in $H$. While $u$ is hungry this set never grows, since a philosopher that eats becomes a sink and leaves it. By induction on its size: a hungry neighbour with precedence over $u$ has fewer ancestors, so it eats and leaves; once no neighbour with precedence is hungry, $u$ collects the forks it lacks (they are dirty, so they are sent when asked), keeps them (they are clean), and eats.

The implementation checks steps 2 to 4 in every reachable state: over all interleavings, with arbitrary message delays, of a triangle with one meal each and of a path of three philosophers with two meals each, and over seeded random runs on a ring of five and on 25 random conflict graphs with up to six philosophers. Every run ends with all meals eaten.

## Complexity

| measure | cost |
|---|---|
| messages per meal of $u$ | at most $2d$: one token and one fork per edge |
| local work per rule | $O(d)$ to scan the edges |
| memory per philosopher | $O(d)$ bits: for each edge, fork here, clean or dirty, token here |
| waiting | a hungry philosopher waits only for neighbours with precedence; the chain of waits has length at most the longest path in $H$ |

The time a philosopher waits depends on the longest path in $H$, which can be as long as $n - 1$. Choosing the initial orientation from a proper [graph coloring](/graph-coloring/) with $c$ colours (forks at the end of lower colour) makes the longest path at most $c - 1$ at the start; later meals change $H$.

## Properties

- **Safety:** exclusion between neighbours.
- **Progress:** [starvation freedom](/starvation-freedom/), under weak fairness of the processes and channels and finite meals. Deadlock freedom follows.
- **Symmetric at run time.** All philosophers run the same rules. The only asymmetry is the acyclic start, which the impossibility theorem for deterministic symmetric solutions requires in some form.
- **Local.** A philosopher talks only to its neighbours, and a philosopher far from any conflict never waits for anyone.
- **Neighbours take turns.** After $u$ eats, all its neighbours have precedence over it. Once the request of a hungry neighbour reaches $u$, $u$ must give up the dirty fork when it is not eating, and cannot get it back before that neighbour has eaten.

## Variants and improvements

- **Drinking philosophers.** In the drinking problem, each edge has a bottle, and a thirsty philosopher needs only some of its bottles for each drinking session, possibly a different set each time. Neighbours that need different bottles may drink at the same time. Chandy and Misra solve it by running the dining solution underneath to decide conflicts: the dining layer gives an order between neighbours that want the same bottle, and bottles are passed with request tokens in a way much like forks. This page and its implementation cover only the dining solution.
- **Shared memory.** The same rules work with shared variables per edge instead of messages, as long as each rule runs atomically.
- **Static order.** If the graph is fixed and the philosophers are numbered, [lock ordering](/lock-ordering/) also avoids deadlock, but chains of waits can then be long, and fairness depends on the locks.

## When to use it

Use it when processes in a network compete for resources shared by pairs, the conflict graph is arbitrary, and you want starvation freedom without a central coordinator. It is a good fit for resource allocation in distributed systems, and as a building block for other algorithms that need to schedule neighbours in a graph. On one machine with shared memory, a lock order or a waiter is simpler.

## Pitfalls

- The start must be acyclic. If all forks start clean, or dirty in a cyclic pattern, $H$ can have a cycle and the proof fails.
- A philosopher that sends a fork keeps the token, since the token is how it asks for the fork back.
- A clean fork must not be sent. A version that hands over every requested fork can livelock: two hungry neighbours pass the fork back and forth for ever.
- The test in L6 matters. A philosopher that eats with a dirty fork its neighbour has asked for can take the same fork again and again, which brings back starvation.
- The algorithm does not tolerate crashes. A crashed philosopher that holds a fork blocks its neighbours for ever.
- The name is shared. "Chandy and Misra" also names their distributed deadlock detection (with Haas) and their distributed simulation work; this is neither.

## Implementations

## Formal proof

See the proof file for Lemmas 1 to 3 and Theorems 1 to 3: a pending request means hunger, clean forks belong to hungry philosophers, exclusion, acyclicity of the precedence graph in every reachable state, and starvation freedom under weak fairness.

## History

Dijkstra (1971) stated the dining philosophers for five philosophers in a ring, and Lehmann and Rabin (1981) proved that no deterministic symmetric solution exists. Chandy and Misra (1984), in "The drinking philosophers problem" in ACM TOPLAS, gave the hygienic solution for an arbitrary conflict graph, in which symmetry is broken only by the acyclic start, and used it to solve the drinking philosophers, where each session needs only some of the shared resources. Their precedence graph argument, that a vertex which becomes a sink cannot create a cycle, is now a standard tool for resource allocation in graphs.

## Exercises

1. Show that if all forks start clean at the lower numbered end, the start is still acyclic, and decide whether the algorithm still works.
2. Give a start with a cyclic $H$ on a triangle and a schedule in which no philosopher ever eats.
3. Prove that once the request of a hungry neighbour $w$ has reached $u$, $u$ eats at most once more before $w$ eats. Can $u$ eat twice in a row while $w$ is hungry, if $w$'s request is still on its way?
4. Remove the test in L6 that the token is away, and find a schedule in which a philosopher starves.
5. Bound the number of messages per meal at $u$, and show that $2d$ can be reached.

## References

---
tag: WW2T0H
kind: algorithm
slug: saturation-algorithm
name: Saturation algorithm
aliases:
- Saturation
- Saturation-based state-space generation
area: logic-and-constraints/model-checking
level: research
summary: Build the reachable states of an asynchronous system as an MDD by saturating nodes bottom-up, firing each event only at the top level it touches, instead of doing global breadth-first image steps.
solves: [reachability-problem]
model: word-ram
complexity:
  vars: {K: the number of levels of the MDD, c: "the total cost of the MDD operations that miss the caches, which can be exponential in K", u: the number of MDD nodes created}
  time: {worst: O(c)}
  space: {worst: O(u)}
properties: {deterministic: true, exact: true, online: false, recursive: true, in_place: false}
history:
  year: 2001
  people: [Gianfranco Ciardo, Gerald Lüttgen, Radu Siminiceanu]
  note: Ciardo, Lüttgen and Siminiceanu introduced saturation for MDDs with a Kronecker-consistent next-state function, at TACAS 2001.
prereqs: [symbolic-reachability, multi-valued-decision-diagram, reachability-problem]
see_also: [symbolic-model-checking, petri-net, reduced-ordered-bdd, computed-table, state-explosion-problem, partial-order-reduction, fixed-point]
sources:
  - paper: doi:10.1007/3-540-45319-9_23
    title: Gianfranco Ciardo, Gerald Lüttgen and Radu Siminiceanu, Saturation, an efficient iteration strategy for symbolic state-space generation, TACAS 2001, LNCS 2031
    locator: pages 328 to 342 (saturated nodes, the procedures Saturate and RecFire, and the experiments on Petri net models)
  - paper: doi:10.1007/s10009-005-0188-7
    title: Gianfranco Ciardo, Robert Marmorstein and Radu Siminiceanu, The saturation algorithm for symbolic state-space exploration, International Journal on Software Tools for Technology Transfer 8(1), 2006
    locator: the definitions of Kronecker consistency and of a saturated node, the algorithm with its caches, and the extension to unknown local state spaces
---

Saturation builds the set of reachable states of an asynchronous system as a [multi-valued decision diagram](/multi-valued-decision-diagram/) (MDD). It does not do global breadth-first image steps, as [symbolic reachability](/symbolic-reachability/) does. Instead, it works on the nodes of the MDD from the bottom level up. A node at level $k$ is *saturated* when its set of states is closed under every event that touches only levels $k$ and below. Saturation makes each node saturated as soon as it is created, so each event is fired only on nodes at its top level, and the result of a firing is saturated at once. The method needs an event-based, *Kronecker-consistent* transition relation, as one gets from [Petri nets](/petri-net/) and from systems of communicating components. Ciardo, Lüttgen and Siminiceanu (2001) reported large savings of time and of peak memory over breadth-first iteration on such models. These savings are measured on their benchmarks; there is no worst-case guarantee.

## In plain words

Think of a system as a team of parts, with each part on its own floor of a building. Most moves change only a few nearby floors. A breadth-first search moves the whole team one step at a time, and its working sets grow large in the middle.

Saturation works from the ground floor up. On each floor, it first finishes all the moves that stay on that floor and the floors below. Only then does it go one floor up. When a move from a higher floor changes the lower floors, it again finishes all the local moves there at once. The sets stay complete and small most of the time.

## The problem

The state space is a product $S = S_K \times \cdots \times S_1$ of $K$ finite local state spaces, one per level, with level $K$ at the top. A global state is $s = (s_K, \ldots, s_1)$. The transition relation is a union of events, $\mathcal{N} = \bigcup_{e \in E} \mathcal{N}_e$. The relation must be Kronecker-consistent: each event $e$ has a local relation $\mathcal{N}_{e,k} \subseteq S_k \times S_k$ for each level, and
$$\mathcal{N}_e(s) = \mathcal{N}_{e,K}(s_K) \times \cdots \times \mathcal{N}_{e,1}(s_1).$$
An event does not touch level $k$ when $\mathcal{N}_{e,k}$ is the identity. $\mathrm{Top}(e)$ and $\mathrm{Bot}(e)$ are the highest and the lowest levels that $e$ touches. The task is to compute $\mathcal{N}^*(s^{\mathrm{init}})$, the set of states reachable from a set of initial states, as an MDD. This is the [reachability problem](/reachability-problem/).

An MDD node $p$ at level $k$ has one child $p[i]$ for each $i \in S_k$, and it stands for the set $\mathcal{B}(p) = \{(i, t) : i \in S_k, t \in \mathcal{B}(p[i])\}$ of $k$-tuples. The terminal 0 is the empty set and the terminal 1 is the set holding the empty tuple. Let $\mathcal{N}_{\le k} = \bigcup \{\mathcal{N}_e : \mathrm{Top}(e) \le k\}$, seen as a relation on $k$-tuples. A node $p$ at level $k$ is *saturated* when $\mathcal{N}_{\le k}(\mathcal{B}(p)) \subseteq \mathcal{B}(p)$.

## The algorithm

```pseudo id=main
SATURATE(p)                                   ▷ p is an MDD node at level k
L1  if p is a terminal then return p
L2  if SatCache[p] is set then return it
L3  ch ← (SATURATE(p[i]) for each i in S_k)
L4  r ← FIX(k, ch)
L5  SatCache[p] ← r, return r

FIX(k, ch)                                    ▷ each ch[i] is saturated
L6  repeat
L7      for each event e with Top(e) = k, each i with ch[i] ≠ 0 and N_e,k(i) ≠ ∅ do
L8          f ← REC-FIRE(e, k − 1, ch[i])
L9          for each j in N_e,k(i) do ch[j] ← ch[j] ∪ f
L10 until no ch[j] changed
L11 return NODE(k, ch)                        ▷ look up or add in the unique table

REC-FIRE(e, l, q)                             ▷ q is a saturated node at level l
L12 if l < Bot(e) then return q               ▷ e changes nothing below here
L13 if FireCache[e, q] is set then return it
L14 ch ← (0 for each i in S_l)
L15 for each i with q[i] ≠ 0, each j in N_e,l(i) do
L16     f ← REC-FIRE(e, l − 1, q[i])
L17     ch[j] ← ch[j] ∪ f
L18 r ← FIX(l, ch)                            ▷ saturate the result before it is used
L19 FireCache[e, q] ← r, return r
```

The answer is SATURATE$(p_0)$, where $p_0$ is the MDD of the initial states. In line L15, a level that $e$ does not touch has $\mathcal{N}_{e,l}(i) = \{i\}$. The union in lines L9 and L17 is the usual recursive MDD union, with its own cache. Line L18 is the key step: the result of a firing is saturated before it is stored, so FIX at level $k$ always gets saturated children, and it only has to deal with the events whose top is $k$.

## Example

Three processes in a ring pass one token. Process $k$ sits at level $k$, and its local states are 0 (idle), 1 (has the token) and 2 (working). Event $w_k$ moves process $k$ from 1 to 2. Event $p_k$ makes process $k$ go from 2 to 0 and gives the token to the next process (0 to 1): $p_3$ passes from level 3 to level 2, $p_2$ from level 2 to level 1, and $p_1$ from level 1 back to level 3. So $\mathrm{Top}(p_1) = 3$ and $\mathrm{Bot}(p_1) = 1$, and $p_1$ does not touch level 2. The initial state is $(s_3, s_2, s_1) = (1, 0, 0)$.

Let $a$ be the level-1 node for $\{0\}$ and $A$ the level-2 node for $\{(0, 0)\}$.

1. The initial MDD has the root $(0, A, 0)$ at level 3. SATURATE first saturates $a$ and $A$; no event with top 1 or 2 is enabled there, so they do not change.
2. FIX at level 3 fires $w_3$ on local state 1. As $\mathrm{Bot}(w_3) = 3$, REC-FIRE returns $A$ at once, and the root becomes $(0, A, A)$.
3. It fires $p_3$ on local state 2. REC-FIRE at level 2 moves local state 0 to 1 and gets $(0, a, 0)$. Before it returns, FIX at level 2 saturates this node: $w_2$ adds local state 2, and $p_2$ fires down to level 1, where FIX at level 1 adds the result of $w_1$. The result is $D = (C, a, a)$ with $C$ the level-1 node for $\{1, 2\}$. It is the set $\{(0,1), (0,2), (1,0), (2,0)\}$, and it is closed under all events with top 2 or less. The root becomes $(D, A, A)$.
4. It fires $p_1$ on local state 0. REC-FIRE goes through level 2 without a change and moves level 1 from 2 to 0. The result is $A$, which adds nothing new to child 1.
5. Nothing changes in the next round, and the result is the root $(D, A, A)$.

The final MDD has five inner nodes and holds the six reachable states. Only five firings miss the cache. A breadth-first iteration on the same model needs six image steps, each on the whole relation.

## Correctness

The proof shows by induction on the level that SATURATE$(p)$ returns a node for $\mathcal{N}_{\le k}^*(\mathcal{B}(p))$, and REC-FIRE$(e, l, q)$ a node for $\mathcal{N}_{\le l}^*(\mathcal{N}_e(\mathcal{B}(q)))$, with $\mathcal{N}_e$ cut to levels $l$ and below. Two facts make it work. First, a union of sets that are closed under a relation is closed under it, so a node with saturated children is already closed under all events with top below $k$. Second, FIX at level $k$ repeats until the events with top $k$ add nothing, so at the end the node is closed under them too. Each state that the method adds is reachable, so the result is the least closed set that holds the input. With $k = K$, every event has top at most $K$, and the result is the reachable set. The full proof is below.

## Complexity

The run does at most one SATURATE per input node and one REC-FIRE per pair of an event and a saturated node, by the caches. Each union is cached too. So the total time is linear in the number of cache misses times the work per miss, and space is linear in the number of nodes created. Neither number has a bound polynomial in $K$: reachability for these models is PSPACE-hard in general, and the final MDD itself can be exponential in $K$.

The gain over breadth-first iteration is measured, not proved. Breadth-first iteration builds large intermediate sets, because the BFS layers of an asynchronous system rarely have the structure that makes MDDs small. Saturation keeps most intermediate nodes saturated, so they look like parts of the final MDD, and the peak number of nodes is often close to the final number. Ciardo, Lüttgen and Siminiceanu (2001) report large gains in time and peak memory on Petri net benchmark models, such as the dining philosophers, compared with breadth-first iteration.

## Properties

- **Exact.** The result is the exact reachable set.
- **Not breadth-first.** Saturation does not compute the BFS layers. So it does not give shortest counterexamples directly; a separate pass is needed for them.
- **Local.** Each event is fired only from its top level down to its bottom level. Events that touch few adjacent levels are cheap.
- **Canonical result.** The final MDD is the canonical quasi-reduced (or fully reduced) MDD of the reachable set for the chosen level order.

## Variants and improvements

- **Saturation unbound.** Ciardo, Marmorstein and Siminiceanu (2003) built the local state spaces during the run, so they need not be known in advance.
- **Other relations.** Later work removes the need for Kronecker consistency: the events are kept as MDDs over pairs of levels, and the transition relation is split into conjuncts and disjuncts (Ciardo and Yu, 2005).
- **Saturation for CTL.** The EU and EG operators of [CTL model checking](/ctl-model-checking/) are least and greatest fixed points too, and saturation can compute their backward fixed points.
- **Shortest paths.** A variant computes the distance of each state with edge-valued decision diagrams, for counterexamples of shortest length.
- **Parallel and distributed saturation.** Several papers spread the levels or the cache over processors.

## When to use it

Use saturation for the reachable states of asynchronous systems: [Petri nets](/petri-net/), protocols and systems of processes that each touch few state variables. It is the main engine of the SMART and Meddly tools. For synchronous hardware, where each step changes all latches at once, the events are not local, and the benefit is small; use [symbolic reachability](/symbolic-reachability/), [bounded model checking](/bounded-model-checking/) or [IC3](/ic3-pdr/) there.

## Pitfalls

- **A bad level order.** As for BDDs, the order of the levels decides the size of the MDD. Put components that interact often on adjacent levels, so that events have a small range from Bot to Top.
- **Firing on an unsaturated node.** If REC-FIRE does not saturate its result before it returns (line L18), the cached result is wrong for later uses, and FIX at the level above may stop too early.
- **Caching with node ids that change.** The caches use node identity. Nodes that are modified in place, as FIX does with its child list, must not enter the unique table until they are final.
- **Non-Kronecker events.** An event whose effect on one level depends on another level in a way that is not a product cannot be fired level by level. Split it into several events, or use a relation MDD.

## Implementations

## History

Symbolic state-space generation with BDDs started with Burch, Clarke, McMillan and others around 1990, with breadth-first image steps. Ciardo, Lüttgen and Siminiceanu had used MDDs with a Kronecker encoding of the events of asynchronous systems in 2000. In 2001 they introduced saturation, which replaced the global iteration by the bottom-up saturation of nodes. The 2006 journal paper of Ciardo, Marmorstein and Siminiceanu collects the algorithm and its extensions. Saturation became the main method in the SMART tool and later in the Meddly library.

## References

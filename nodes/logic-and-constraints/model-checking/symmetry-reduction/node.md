---
tag: 2E74AM
kind: technique
slug: symmetry-reduction
name: Symmetry reduction
aliases:
- Symmetry-based state reduction
area: logic-and-constraints/model-checking
level: advanced
summary: Explore one representative state per orbit of a symmetry group of the system. The quotient is bisimilar to the system, so symmetric properties are preserved.
prereqs: [kripke-structure, bisimulation, explicit-state-model-checking]
see_also: [bisimulation, graph-automorphism-group, canonical-labeling, graph-isomorphism-problem, burnside-lemma, partial-order-reduction, state-explosion-problem, explicit-state-model-checking]
sources:
  - paper: "E. Allen Emerson and A. Prasad Sistla, Symmetry and model checking, Formal Methods in System Design 9(1/2), 1996"
    locator: the quotient structure by a group of automorphisms, its correspondence with the original structure for CTL*, and the case of formulas that are not symmetric
  - paper: "Edmund M. Clarke, Reinhard Enders, Thomas Filkorn and Somesh Jha, Exploiting symmetry in temporal logic model checking, Formal Methods in System Design 9(1/2), 1996"
    locator: the orbit relation as a bisimulation, symbolic symmetry reduction, and the hardness of computing orbit representatives (at least as hard as graph isomorphism)
  - paper: "C. Norris Ip and David L. Dill, Better verification through symmetry, Formal Methods in System Design 9(1/2), 1996"
    locator: scalarsets in the Murphi verifier, which make symmetries visible in the syntax, and the search over canonical representatives
  - book: isbn:9780262032704
    title: Edmund M. Clarke, Orna Grumberg and Doron A. Peled, Model Checking, MIT Press, 1999
    locator: Chapter 14 (symmetry)
---

Symmetry reduction shrinks the state space of a system made of identical components. A permutation of the component indices that maps transitions to transitions is a *symmetry*, and the symmetries form a group. States in the same orbit of the group behave in the same way, so a search can store and expand one representative per orbit. The orbit relation is a [bisimulation](/bisimulation/), so the quotient structure satisfies the same CTL* formulas as the original whenever the atomic propositions of the formula are invariant under the group. With $n$ identical processes the gain can be up to a factor of $n!$, but computing a canonical representative is in general as hard as [graph isomorphism](/graph-isomorphism-problem/).

## In plain words

Many systems contain several copies of the same part: five philosophers, ten clients, four caches. A state where client 1 waits and client 2 works behaves just like the state where client 2 waits and client 1 works, with the names swapped. Checking both is wasted effort.

Symmetry reduction treats such states as one. Each time the search finds a state, it renames the copies in a fixed way, for example by sorting them, and stores only the renamed state. States that differ only by a renaming then become the same stored state. The search covers far fewer states, and it still gives the right answer for any property that does not care which copy is which, such as "no two clients are ever in the critical section together".

## When it applies

- The system is built from components that are interchangeable: identical processes, a pool of identical resources, or data values that are only compared for equality. Murphi's *scalarsets* (Ip and Dill 1996) declare such a type, so that the symmetries follow from the syntax.
- The property is symmetric: each atomic proposition it uses has the same value in $s$ and in $\pi(s)$ for every symmetry $\pi$. "Some process is critical" is symmetric; "process 1 is critical" is not.
- A good function from states to representatives is available. Sorting the local states of fully symmetric processes is cheap; rotations of a ring are cheap; general groups need more work.

It does not help a system without symmetry, such as processes with distinct priorities or code, and a property that names a single component reduces the usable group.

## The template

A group $G$ of permutations acts on the states. The holes are in capitals.

```pseudo id=main
SYMMETRIC-SEARCH(INIT, NEXT, P)
L1  Visited ← {REP(s) : s ∈ INIT};  W ← a copy of Visited
L2  while W is not empty do
L3      s ← W.take()
L4      if not P(s) then return a counterexample, mapped back to the original states
L5      for each t ∈ NEXT(s) do
L6          r ← REP(t)                                ▷ one state per orbit
L7          if r ∉ Visited then add r to Visited and to W
L8  return "P holds in every reachable state"
```

The holes:

- **GROUP.** The symmetry group $G$: a group of permutations $\pi$ of the states such that $\pi(I) = I$ and $(s, t) \in R$ iff $(\pi(s), \pi(t)) \in R$. For $n$ identical processes, $\pi$ permutes the process indices in the state vector and in every variable that holds an index. Typical groups are the full symmetric group $S_n$ and the rotations of a ring.
- **REP.** A function with $\mathrm{REP}(t)$ in the orbit $G t$ of $t$. It is *canonical* if moreover $\mathrm{REP}(t) = \mathrm{REP}(u)$ whenever $t$ and $u$ are in the same orbit. For $S_n$ acting on a vector of local states with no index variables, sorting the vector is canonical.
- **P.** A property whose atomic propositions are invariant under $G$.

### Example

Each of $n$ processes is in state $N$ (non-critical), $T$ (trying) or $C$ (critical). A process moves from $N$ to $T$, from $T$ to $C$ if no process is in $C$, and from $C$ back to $N$. The reachable states are those with at most one $C$: $2^n$ states with no $C$ and $n \cdot 2^{n-1}$ with exactly one, all reachable from $N^n$. The full symmetric group $S_n$ permutes the processes, and an orbit is fixed by the number of processes in $T$ and whether one is in $C$, so there are $(n + 1) + n = 2n + 1$ orbits. The canonical representative sorts the vector.

| $n$ | reachable states $2^n + n 2^{n-1}$ | orbits $2n + 1$ |
|---|---|---|
| 3 | 20 | 7 |
| 5 | 112 | 11 |
| 10 | 6144 | 21 |
| 20 | 11534336 | 41 |

The property "at most one process is critical" uses the proposition "the number of processes in $C$", which is invariant, so the search over 7 orbits for $n = 3$ proves it for all 20 states.

### Why it is correct

Let $M = (S, I, R, L)$ and let $G$ be a symmetry group as in the hole GROUP, with $L(\pi(s)) \cap AP_\varphi = L(s) \cap AP_\varphi$ for all $\pi \in G$ and all $s$, where $AP_\varphi$ is the set of propositions of the property.

*The orbit relation is a bisimulation.* Let $s \sim t$ iff $t = \pi(s)$ for some $\pi \in G$. This is an equivalence relation, since $G$ is a group. If $s \sim t$ with $t = \pi(s)$, the labels agree on $AP_\varphi$ by assumption. If $s \to s'$, then $t = \pi(s) \to \pi(s')$ because $\pi$ maps transitions to transitions, and $s' \sim \pi(s')$. The converse condition follows by symmetry of $\sim$.

*The quotient is bisimilar to $M$.* The quotient $M_G$ has the orbits as states, an edge $[s] \to [t]$ iff $s_0 \to t_0$ for some $s_0 \in [s]$ and $t_0 \in [t]$, the orbits of the initial states as initial states, and the label $L(s) \cap AP_\varphi$ of any member. Relate $s$ to $[s]$. If $s \to s'$, then $[s] \to [s']$. If $[s] \to [t]$, pick $s_0 \to t_0$ with $s = \pi(s_0)$; then $s \to \pi(t_0)$ and $\pi(t_0) \in [t]$. So the relation is a bisimulation, and $M$ and $M_G$ satisfy the same CTL* formulas over $AP_\varphi$, by the theorem on the [bisimulation](/bisimulation/) page.

*The search explores the reachable part of $M_G$.* Each stored $r$ is a representative of a reachable orbit, and for each successor orbit $[t]$ of $[s]$ the loop adds $\mathrm{REP}(t)$, as the argument above shows that every successor orbit of $[s]$ contains a successor of the stored representative. With a canonical REP, each orbit is stored once. With a REP that is not canonical, some orbits are stored more than once, which costs space but keeps the answer correct.

*Counterexamples.* A path of representatives $r_0 \to r_1 \to \cdots$ is not a path of $M$, since each step went from $r_i$ to some $t$ with $\mathrm{REP}(t) = r_{i+1}$. Record the permutation $\pi_i$ with $r_{i+1} = \pi_i(t)$, and apply the inverses of the composed permutations to get a real path of $M$.

### Size and time

By the orbit-stabilizer theorem each orbit has at most $|G|$ elements, so the number of orbits is between $|S|/|G|$ and $|S|$; [Burnside's lemma](/burnside-lemma/) gives the exact count as the average number of fixed points. For $S_n$ the reduction is at most a factor of $n!$, and it comes near that factor only when most states give pairwise different local states to the processes. In the example the factor is $(2^n + n 2^{n-1})/(2n + 1)$, which is exponential in $n$ but far below $n!$. The worst case of the [state explosion problem](/state-explosion-problem/) is not changed: $n$ processes with $k$ local states have $\binom{n + k - 1}{k - 1}$ orbits under $S_n$, which is polynomial in $n$ for fixed $k$ but exponential when $k$ grows with $n$; shared variables multiply this count; and a system with a small group gains little. The cost per state is the cost of REP. Sorting costs $O(n \log n)$. For general groups, finding a canonical representative is at least as hard as graph isomorphism (Clarke, Enders, Filkorn and Jha 1996), so tools often use a cheap REP that is not canonical, or try several candidate permutations.

## Classic examples

- **Murphi scalarsets.** Ip and Dill (1996) introduced a data type for symmetric indices. The compiler checks that the model uses scalarset values only in symmetric ways, and the verifier normalizes each state by a permutation of the scalarset values.
- **Cache coherence protocols.** Directory and snooping protocols with $n$ identical caches are the standard application; the reduction makes models with several caches checkable.
- **Mutual exclusion and dining philosophers.** Fully symmetric mutual exclusion is reduced by $S_n$, and the [dining philosophers](/dining-philosophers-problem/) on a ring by the rotation group, with a gain of at most $n$.
- **Symbolic symmetry reduction.** Clarke, Enders, Filkorn and Jha (1996) built the orbit relation as a BDD and computed with the quotient symbolically, though the BDD of the orbit relation can itself be large.

## Variations

- **Multiple representatives.** Allow a few representatives per orbit, which makes REP cheap, at a bounded cost in space.
- **Partial and virtual symmetry.** Systems that are almost symmetric, for example with one distinguished process, can use a subgroup, or a relaxed notion of symmetry that still gives a bisimulation on the reachable part.
- **Non-symmetric formulas.** For a formula that names specific processes, use the subgroup that fixes its propositions, or annotate the quotient with extra information, as Emerson and Sistla (1996) do for formulas that are not invariant under the whole group.
- **Under fairness.** Fairness conditions that name individual processes are not symmetric, and the quotient must keep track of them; Emerson and Sistla studied this case.
- **With partial-order reduction.** The two reductions remove different redundancies, symmetry between components and order between independent steps, and they can be combined with care.

## Pitfalls

- **A property that is not symmetric.** Checking "process 1 never starves" on the quotient by $S_n$ is wrong, because the proposition "process 1 is in $T$" is not invariant.
- **Hidden asymmetry.** Process identifiers used as priorities, an array scanned from index 0, or a tie broken by the smaller index all break symmetry. Then $\pi$ does not map transitions to transitions, and the quotient can miss behaviours.
- **Index variables.** A permutation must also rename the process indices stored in variables, such as a variable that holds the identity of the lock owner. Forgetting this gives a REP that is not in the orbit.
- **Expensive canonical forms.** For complex groups, computing an exact canonical representative can cost more than the states it saves.
- **Counterexamples.** A path in the quotient must be mapped back through the permutations before it is shown to the user.

## Exercises

1. Check the counts $2^n + n 2^{n-1}$ and $2n + 1$ in the example for $n = 2$ by listing all states and orbits.
2. For the [dining philosophers](/dining-philosophers-problem/) with $n$ philosophers on a ring, which group is a symmetry group? Bound the gain.
3. Show that if REP is not canonical, the search still visits a representative of every reachable orbit.
4. Use Burnside's lemma to count the orbits of $\{0, 1\}^n$ under the rotation group of order $n$ for $n = 6$.

## References

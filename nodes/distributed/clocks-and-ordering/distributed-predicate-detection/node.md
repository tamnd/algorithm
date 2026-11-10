---
tag: E1GYTY
kind: problem
slug: distributed-predicate-detection
name: Distributed predicate detection
aliases:
- global predicate detection
area: distributed/clocks-and-ordering
level: research
summary: Given a recorded computation and a predicate on global states, decide if some run passes a consistent cut where it holds (possibly), or if every run does (definitely).
prereqs: [consistent-cut]
see_also: [weak-conjunctive-predicate-detection, global-snapshot, consistent-cut, vector-clocks, happened-before, sat, termination-detection, deadlock-detection]
sources:
  - paper: "Robert Cooper and Keith Marzullo, Consistent detection of global predicates, Proceedings of the ACM/ONR Workshop on Parallel and Distributed Debugging, 1991, pages 167 to 174"
    locator: the modalities possibly and definitely, and their detection by a search of the lattice of consistent global states (page numbers from memory, to be checked)
  - paper: "Craig M. Chase and Vijay K. Garg, Detection of global predicates, techniques and their limitations, Distributed Computing 11(4), 1998, pages 191 to 201"
    locator: the NP-completeness of possibly for general predicates, and the classes of predicates that can be detected fast (volume and pages from memory, to be checked)
  - paper: "Vijay K. Garg and Brian Waldecker, Detection of weak unstable predicates in distributed programs, IEEE Transactions on Parallel and Distributed Systems 5(3), 1994, pages 299 to 307"
    locator: conjunctive predicates and the checker with one queue per process
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: the chapter on global predicate detection (stable and unstable predicates, possibly and definitely, conjunctive predicates)
  - book: isbn:9780471036005
    title: Vijay K. Garg, Elements of Distributed Computing, Wiley, 2002
    locator: the chapters on global predicate detection and the lattice of consistent cuts
---

*Distributed predicate detection* asks whether a condition on the global state of a distributed computation held. No process sees the global state, and different observers can see the events in different orders, so the question has two forms. *Possibly* $\Phi$ asks whether some run of the computation passes through a [consistent cut](/consistent-cut/) where $\Phi$ holds. *Definitely* $\Phi$ asks whether every run does. Cooper and Marzullo (1991) defined both and decided them by a search of the lattice of consistent cuts. For a general predicate the first is NP-complete and the second is coNP-complete, so fast algorithms exist only for special classes, such as [conjunctive predicates](/weak-conjunctive-predicate-detection/).

## In plain words

You want to know whether two processes were ever in their critical sections at the same time. Each process wrote down what it did, and the vector clocks tell you which events came before which. But many events are concurrent: the record does not say which of two concurrent events happened first, and in another run with other delays the order could change.

So you ask two questions. Could the bad state have happened, in at least one order that the record allows? That is *possibly*. Must it have happened, in every order that the record allows? That is *definitely*. A stable property, such as termination, stays true once it is true, and a [snapshot](/global-snapshot/) is enough to see it. A property that can become true and then false again needs this problem.

## Definition

**Computation.** There are $n$ processes. Process $p_i$ runs the events $e_i^1, \dots, e_i^{m_i}$, and $\to$ is the [happened-before](/happened-before/) relation of the computation. A cut is a vector $k$ with $0 \le k_i \le m_i$, and it holds the first $k_i$ events of each process. The [consistent cuts](/consistent-cut/) form a distributive lattice $\mathcal{L}$, from the empty cut $\mathbf{0}$ to the final cut $\mathbf{m} = (m_0, \dots, m_{n-1})$.

**Runs.** A *run* is a sequence of cuts $\mathbf{0} = c_0, c_1, \dots, c_M = \mathbf{m}$ in which each cut is consistent and holds exactly one event more than the one before. A run is an order of all the events that respects $\to$, so it is one way in which the computation could have happened. Every path from $\mathbf{0}$ to $\mathbf{m}$ in $\mathcal{L}$ is a run.

**Predicate.** $\Phi$ is a predicate on global states, that is, on consistent cuts. It is given by an evaluator that computes $\Phi(c)$ in time polynomial in the size of the computation.

**The problem.** Given the computation and $\Phi$:

- $\mathrm{possibly}(\Phi)$ holds if some run passes through a cut $c$ with $\Phi(c)$. Equivalently, some consistent cut satisfies $\Phi$, since every consistent cut is on some run.
- $\mathrm{definitely}(\Phi)$ holds if every run passes through a cut $c$ with $\Phi(c)$.

Definitely implies possibly, because there is at least one run. The converse is false, as the second example shows.

## Variants

- **Stable predicates.** If $\Phi$ stays true once it is true, possibly and definitely are the same, and $\Phi(\mathbf{m})$ decides both. Online, a [global snapshot](/global-snapshot/) detects it.
- **Conjunctive predicates.** $\Phi = l_0 \wedge \dots \wedge l_{n-1}$, where $l_i$ depends only on the state of $p_i$. Possibly is then solved in polynomial time by the [weak conjunctive predicate detection](/weak-conjunctive-predicate-detection/) algorithm of Garg and Waldecker; definitely has a polynomial algorithm too.
- **Linear and regular predicates.** Chase and Garg studied predicates whose true cuts are closed under meet; for them, possibly has a polynomial search that advances one process at a time.
- **Offline or online.** Offline, the whole trace is known. Online, the processes send their events to a checker while they run, and the checker must answer as soon as it can.

## Examples

**Possibly and definitely.** $p_0$ sets $x = 1$ and sends $m_0$ to $p_1$; then it receives $m_1$ and sets $x = 0$. $p_1$ receives $m_0$ and sets $y = 1$; then it sends $m_1$; then it sets $y = 0$. Let $\Phi$ be $x = 1 \wedge y = 1$. Write a cut as $(k_0, k_1)$.

The consistent cuts are $(0,0)$, $(1,0)$, $(1,1)$, $(1,2)$, $(1,3)$, $(2,2)$ and $(2,3)$: seven of the twelve vectors. The receive of $m_0$ needs $k_0 \ge 1$, and the receive of $m_1$ needs $k_1 \ge 2$. $\Phi$ holds at $(1,1)$ and $(1,2)$. From $(1,0)$ the only next cut is $(1,1)$, since $p_0$ must wait for $m_1$. So every run passes through $(1,1)$, and $\mathrm{definitely}(\Phi)$ holds.

**Possibly but not definitely.** Remove the reply: $p_0$ sets $x = 1$, sends $m_0$, and then sets $x = 0$ with an internal event. $p_1$ receives $m_0$, sets $y = 1$, and later sets $y = 0$. The cut $(1,1)$ still satisfies $\Phi$, so possibly holds. But the run $(1,0), (2,0), (2,1), \dots$ lets $p_0$ reset $x$ before $p_1$ sets $y$, and it never passes a cut with $\Phi$. So definitely does not hold.

## Known algorithms

**The lattice search (Cooper and Marzullo).** The consistent cuts with $\ell$ events form level $\ell$ of $\mathcal{L}$. The search goes from level to level.

```pseudo id=main
POSSIBLY(Φ)
L1  level ← {0}
    while level is not empty
L2      if Φ(c) for some c in level then return true
L3      level ← the consistent cuts with one more event than some cut in level
    return false

DEFINITELY(Φ)
    if Φ(0) then return true
L4  level ← {0}                                 ▷ the cuts that a run reaches without meeting Φ
    while level is not empty
L5      if m is in level then return false
L6      level ← the consistent cuts c with one more event than some cut in level, and not Φ(c)
L7  return true
```

A successor of a cut adds event $e_i^{k_i + 1}$; it is consistent if that event is not a receive whose send is outside the cut, by Lemma 1 of the page on [consistent cuts](/consistent-cut/).

*Proof of correctness.* Every consistent cut $c \ne \mathbf{0}$ has an event $e$ on its frontier that happened before no other event of $c$; removing $e$ gives a consistent cut with one event less. So by induction every consistent cut is reached from $\mathbf{0}$ by adding one event at a time, and line L3 makes level $\ell$ exactly the consistent cuts with $\ell$ events. POSSIBLY tests all of them. In DEFINITELY, by induction on $\ell$, level $\ell$ is the set of cuts with $\ell$ events that some path from $\mathbf{0}$ reaches through cuts where $\Phi$ is false. So $\mathbf{m}$ is in a level exactly when some run avoids $\Phi$, and line L5 answers no exactly then. $\square$

The search is exact for every $\Phi$, but $\mathcal{L}$ can have $\prod_i (m_i + 1)$ cuts, for example when no messages are sent. It evaluates $\Phi$ on each cut once, and it keeps two levels in memory.

| Method | Predicates | Cost |
|---|---|---|
| Lattice search (Cooper and Marzullo 1991) | all | the size of $\mathcal{L}$, up to $\prod_i (m_i + 1)$ cuts |
| [Weak conjunctive predicate detection](/weak-conjunctive-predicate-detection/) (Garg and Waldecker 1994) | possibly of a conjunction of local predicates | $O(n^2 m)$ comparisons, $m$ the most candidate states of a process |
| [Global snapshot](/global-snapshot/) | stable predicates | one snapshot |

## Bounds

**Theorem 1.** $\mathrm{possibly}(\Phi)$ is NP-complete for predicates given by a polynomial evaluator.

*Proof.* It is in NP: a certificate is a cut $c$. Its consistency is checked with the vector clock test of the [consistent cut](/consistent-cut/) page, and $\Phi(c)$ by the evaluator. For hardness, reduce [SAT](/sat/). Given a formula $F$ in conjunctive normal form over $x_1, \dots, x_k$, build $k$ processes that send no messages and run one internal event each, and let $x_v$ be true in a cut when $p_{v-1}$ has run its event. With no messages, all $2^k$ cuts are consistent, and they give all $2^k$ assignments. Let $\Phi(c)$ be $F$ under the assignment of $c$. Then $\mathrm{possibly}(\Phi)$ holds exactly when $F$ is satisfiable. $\square$

**Theorem 2.** $\mathrm{definitely}(\Phi)$ is coNP-complete for predicates given by a polynomial evaluator.

*Proof.* It is in coNP: if it fails, a certificate is a run that avoids $\Phi$, a list of $M$ cuts, each checked in polynomial time. For hardness, reduce the complement of SAT. Given $F$ over $x_1, \dots, x_k$, build $2k + 1$ processes that send no messages and run one event each: $T_v$ and $F_v$ for each variable, and a pivot $P$. So every order of the $2k + 1$ events is a run. In a cut, let $\mathrm{done}(X)$ say whether process $X$ has run. Let $\Phi(c)$ be true when one of these holds:

1. $P$ has not run, and $T_v$ and $F_v$ have both run for some $v$;
2. $P$ has run, and neither $T_v$ nor $F_v$ has run for some $v$;
3. $P$ has run, exactly one of $T_v$ and $F_v$ has run for each $v$, and $F$ is false for $x_v = \mathrm{done}(T_v)$.

If $F$ is satisfied by $x$, the run that first runs $T_v$ when $x_v$ is true and $F_v$ when it is false, for each $v$, then $P$, then the rest, avoids $\Phi$. Before $P$, no pair is complete, so rule 1 is false. Just after $P$, each pair has exactly one event and $F(x)$ is true. After the next event, some pair is complete, so rule 3 cannot hold again, and pairs never lose events, so rule 2 stays false. Conversely, let a run avoid $\Phi$. Just before $P$, rule 1 is false, so each pair has at most one event. Just after $P$, rule 2 is false, so each pair has at least one. So each pair has exactly one, and since rule 3 is false, the values $x_v = \mathrm{done}(T_v)$ satisfy $F$. So $\mathrm{definitely}(\Phi)$ holds exactly when $F$ is unsatisfiable. $\square$

The seeded tests check both reductions: possibly against a SAT solver by enumeration on 200 formulas, and definitely against unsatisfiability on 150 formulas and against an enumeration of all runs when $k \le 2$.

**Size of the lattice.** With no messages, all $\prod_i (m_i + 1)$ cuts are consistent, so the lattice search takes exponential time in $n$. Messages only remove cuts.

## Reductions

- **Stable predicates to snapshots.** If $\Phi$ is stable, a run passes a cut with $\Phi$ exactly when $\Phi(\mathbf{m})$ holds, so one [global snapshot](/global-snapshot/) at the end, or repeated snapshots online, decide it.
- **Possibly to SAT.** For a predicate given as a Boolean formula over local variables, possibly asks whether some consistent cut satisfies it; with consistency written as clauses over the cut, a SAT solver can answer.
- **Mutual exclusion to conjunctions.** A violation of mutual exclusion by $p_i$ and $p_j$ is $\mathrm{possibly}(cs_i \wedge cs_j)$, a conjunctive predicate.

## Applications

- **Debugging.** A breakpoint on a global condition stops the program at a consistent cut where the condition could hold.
- **Runtime verification.** A monitor checks a safety property, such as "never two leaders", on every order of the logged events that the vector clocks allow, not only on the order in which the logs arrived.
- **Testing.** A test that found no bad state in the observed order can still report $\mathrm{possibly}(\text{bad})$ from the same trace.

## References

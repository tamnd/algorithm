---
tag: BP947G
kind: algorithm
slug: residual-belief-propagation
name: Residual belief propagation
aliases:
- residual BP
- RBP
- residual scheduling for belief propagation
area: machine-learning/probabilistic-inference
level: research
summary: "Loopy BP that always sends next the message whose new value differs most from its current one, found with a priority queue keyed by this residual."
solves: [marginal-inference]
model: real-ram
complexity:
  vars: {u: the number of committed message updates, d: the largest degree, k: the largest number of states, e: the number of edges}
  time: {worst: "O(e d k^2 + u d (d k^2 + log e))"}
  space: {extra: "O(e k)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2006
  people: [Gal Elidan, Ian McGraw, Daphne Koller]
  note: Elidan, McGraw and Koller (UAI 2006) proposed scheduling the messages of asynchronous belief propagation by their residuals and reported faster and more frequent convergence than synchronous and round-robin schedules.
prereqs: [loopy-belief-propagation, priority-queue]
see_also: [belief-propagation, markov-random-field, binary-heap, indexed-priority-queue, generalized-belief-propagation, tree-reweighted-belief-propagation, gibbs-sampling, ising-model]
sources:
  - paper: "Gal Elidan, Ian McGraw and Daphne Koller, Residual belief propagation: informed scheduling for asynchronous message passing, Proceedings of the 22nd Conference on Uncertainty in Artificial Intelligence (UAI), 2006"
    title: Elidan, McGraw and Koller 2006
    locator: "the residual of a message, the schedule that always updates the message with the largest residual using a priority queue, and the experiments on grids and other networks"
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, MIT Press, 2009
    locator: "Section 11.3 (message scheduling for loopy belief propagation, including residual belief propagation)"
  - paper: "Charles Sutton and Andrew McCallum, Improved dynamic schedules for belief propagation, Proceedings of the 23rd Conference on Uncertainty in Artificial Intelligence (UAI), 2007"
    title: Sutton and McCallum 2007
    locator: schedules that estimate the residuals instead of computing every candidate message
  - paper: "Joseph Gonzalez, Yucheng Low and Carlos Guestrin, Residual splash for optimally parallelizing belief propagation, Proceedings of the 12th International Conference on Artificial Intelligence and Statistics (AISTATS), 2009"
    title: Gonzalez, Low and Guestrin 2009
    locator: the splash variant, which updates a small tree around the node of largest residual, and its parallel version
---

Residual belief propagation is [loopy belief propagation](/loopy-belief-propagation/) with a different order of updates. Instead of updating all messages in rounds, it keeps, for every directed edge, the message it *would* send now, and the *residual*: how far that new message is from the current one. It always sends the message with the largest residual next, and finds it with a [priority queue](/priority-queue/). After each update, only the messages that depend on the changed one get new candidates and residuals. The fixed points are the same as those of loopy BP, but the work goes where the messages still change, so it often needs far fewer updates and converges in more cases. It was introduced by Elidan, McGraw and Koller in 2006.

## In plain words

Loopy belief propagation passes notes between the nodes of a graph until the notes stop changing. The usual way updates every note in each round, even the many that are already settled.

Residual belief propagation is lazier and smarter. For each note it asks: if I rewrote this note now, how much would it change? It always rewrites the note that would change the most. A rewritten note changes the inputs of a few neighbors, so only their scores are refreshed. A priority queue keeps the scores so that the top one is found fast. When even the top score is tiny, nothing would change much any more, and the method stops. The answer is the same kind of answer that loopy belief propagation gives, but it usually comes with fewer note updates.

## The problem

**The model.** A pairwise [Markov random field](/markov-random-field/) on a graph $G = (V, E)$ with positive potentials:

$$p(x) = \frac{1}{Z} \prod_{i \in V} \phi_i(x_i) \prod_{(i, j) \in E} \psi_{ij}(x_i, x_j).$$

The method works the same way on a [factor graph](/factor-graph/); the pairwise form keeps the notation short.

**The messages.** One message $m_{i \to j}$ for each direction of each edge, a positive normalized vector over the states of $x_j$. The loopy BP update of a single message is

$$F_{i \to j}(m)(x_j) \propto \sum_{x_i} \phi_i(x_i)\, \psi_{ij}(x_i, x_j) \prod_{k \in N(i) \setminus j} m_{k \to i}(x_i),$$

and the beliefs are $b_i(x_i) \propto \phi_i(x_i) \prod_{k \in N(i)} m_{k \to i}(x_i)$.

**The residual.** For the current messages $m$, the residual of the directed edge $i \to j$ is

$$r_{i \to j} = \big\| F_{i \to j}(m) - m_{i \to j} \big\|.$$

This page uses the max norm over the states. Other norms, such as a norm of the difference of the log messages, also work. A set of messages is a fixed point of loopy BP exactly when every residual is 0.

**The goal.** The same as loopy BP: approximate marginals from a fixed point. Residual BP only chooses the order of the single-message updates.

## The algorithm

The priority queue holds pairs (residual, edge) with the largest residual on top. When a residual changes, the code pushes a new entry and marks the old one stale, which is simpler than a decrease-key operation on an [indexed priority queue](/indexed-priority-queue/).

```pseudo id=main
RESIDUAL-BP(G, φ, ψ, ε, U)
L1  m_{i→j} ← uniform, for every directed edge
L2  for every directed edge: c_{i→j} ← F_{i→j}(m), r_{i→j} ← ‖c_{i→j} − m_{i→j}‖; insert (r_{i→j}, i→j) into Q
L3  while Q is not empty and fewer than U updates are done do
L4      (r, i→j) ← extract the top of Q, skipping stale entries
L5      if r ≤ ε then stop: "converged"
L6      m_{i→j} ← c_{i→j}; r_{i→j} ← 0
L7      for every k ∈ N(j)∖i: c_{j→k} ← F_{j→k}(m), r_{j→k} ← ‖c_{j→k} − m_{j→k}‖; update the entry of j→k in Q
L8  return the beliefs b_i ∝ φ_i Π_{k ∈ N(i)} m_{k→i}
```

Line L7 is where the method saves work: the new message $m_{i \to j}$ is an input only to the messages $j \to k$ with $k \ne i$, so no other candidate changes. The message $j \to i$ does not use $m_{i \to j}$, and the candidate of $i \to j$ itself is still equal to the new $m_{i \to j}$, so its residual is 0.

## Example

Take the 4-cycle Ising model of the loopy BP page: spins $s_i \in \{-1, +1\}$, $\phi_i(s) = e^{h_i s}$ with $h = (0.3, -0.2, 0.1, 0)$, and $\psi_{ij}(s, t) = e^{0.5 s t}$ on the edges $1 - 2$, $2 - 4$, $4 - 3$, $3 - 1$. There are 8 directed messages.

At the start all messages are uniform. The messages out of spin 1, which has the strongest field, have the largest residuals, so they go first. Each update makes the messages out of the receiving spin out of date, and these then rise in the queue. The changes spread from the strong fields outward, instead of everywhere at once.

| tolerance $\varepsilon$ | residual BP | synchronous BP |
|---|---|---|
| $10^{-6}$ | 56 updates | 120 updates (15 rounds of 8) |
| $10^{-10}$ | 102 updates | 208 updates (26 rounds of 8) |

Both end at the same fixed point, with $b_1(+1) = 0.6315$, while the exact marginal is $0.6211$. Residual BP is no more accurate than loopy BP; it gets to the same place with about half the updates.

On ten seeded $3 \times 3$ Ising grids with fields uniform in $[-0.5, 0.5]$ and couplings uniform in $[-0.5, 0.5]$, residual BP needed between 138 and 193 updates to reach $\varepsilon = 10^{-10}$, while synchronous BP needed between 336 and 648. With couplings in $[-2, 2]$, residual BP converged on all ten grids, with between 219 and 764 updates, while synchronous BP needed up to 19032 updates and did not converge on one grid in 5000 rounds. These are observations on these seeds, not a theorem.

## Correctness

The main fact is an invariant: before each execution of line L3, for every directed edge $e$,

$$c_e = F_e(m) \quad \text{and} \quad r_e = \| c_e - m_e \|.$$

It holds after line L2. Line L6 changes only $m_{i \to j}$. The candidates that depend on $m_{i \to j}$ are exactly those of the edges $j \to k$ with $k \ne i$, which line L7 recomputes. The candidate of $i \to j$ does not depend on $m_{i \to j}$, so it still equals $F_{i \to j}(m) = m_{i \to j}$, and its residual is 0. All other candidates have unchanged inputs.

So when line L5 stops, the top of the queue is the largest residual, and every residual is at most $\varepsilon$: the messages are a fixed point of loopy BP up to $\varepsilon$, and with $\varepsilon = 0$ an exact fixed point. Everything that is known about loopy BP fixed points, such as the link to the [Bethe free energy](/bethe-free-energy/), then applies.

On a tree with $\varepsilon = 0$, the method stops after a finite number of updates with the exact marginals. The proof is by induction on the height of a directed edge: the inputs of an edge change only a finite number of times, and between two changes the edge is updated at most once, because an update makes its residual 0.

On a graph with cycles, there is no guarantee that the loop stops; the bound $U$ on the number of updates is needed. The output must report whether it converged. The proofs are in the correctness proof.

## Complexity

The costs are in the [real RAM](/real-ram/) model, with $e$ edges, largest degree $d$, and at most $k$ states per variable.

- **Start.** Line L2 computes $2e$ candidates. One candidate costs $O(d k + k^2)$, so the start costs $O(e (d k + k^2))$, which is within $O(e d k^2)$.
- **One update.** Line L7 recomputes up to $d - 1$ candidates, at $O(d k + k^2)$ each, and pushes $d - 1$ entries into a [binary heap](/binary-heap/) at $O(\log(\text{heap size}))$ each. With lazy deletion the heap holds $O(e + u d)$ entries; with an indexed queue it holds $2e$. So one update costs $O(d (d k + k^2 + \log e))$, if the heap is rebuilt when stale entries pile up.
- **Total.** $O(e d k^2 + u\, d (d k^2 + \log e))$, where $u$ is the number of updates. A round of synchronous BP does $2e$ message updates at $O(d k + k^2)$ each, so residual BP pays an extra factor of about $d$ per update, plus the queue. It wins when it needs far fewer updates, as in the example.
- **Memory.** Messages, candidates and residuals: $O(e k)$, plus the queue.

## Properties

- **Same fixed points as loopy BP.** Only the order changes. If both converge to a unique fixed point, they give the same beliefs.
- **Asynchronous.** Each update uses the newest messages, like a [Gauss-Seidel method](/gauss-seidel-method/), not the old ones of the last round, like a [Jacobi method](/jacobi-method/).
- **Greedy.** The next update is chosen by a local score. There is no proof that this order is best, and a different order can reach a different fixed point when there are several.
- **Deterministic.** With a fixed rule for ties, the run is the same each time.
- **Sequential.** One message at a time, which is hard to run in parallel.

## Variants and improvements

- **Estimated residuals.** Computing the candidates of line L7 costs as much as the update itself. Sutton and McCallum (2007) estimate the residuals instead, and update a candidate only when it reaches the top.
- **Residual splash.** Gonzalez, Low and Guestrin (2009) update a small tree of messages around the variable of largest residual, in the order of a tree schedule, and run several splashes in parallel.
- **Residual tree-reweighted and generalized BP.** The same schedule applies to any message-passing method with a fixed point equation per message, such as [tree-reweighted BP](/tree-reweighted-belief-propagation/) and [generalized BP](/generalized-belief-propagation/).
- **Damping.** Each committed message can be damped, as in loopy BP; the invariant then uses the damped candidate.

## When to use it

Use residual BP when loopy BP is slow or fails to converge in rounds, on graphs where the messages settle at very different speeds, for example with strong fields in a few places or long chains. It is a drop-in change of schedule: the model, the messages and the result stay the same. If the model is so frustrated that no schedule converges, a different approximation such as [Gibbs sampling](/gibbs-sampling/) or tree-reweighted BP is needed.

## Pitfalls

- **A max that is out of date.** If the residuals of the edges $j \to k$ are not refreshed in line L7, the queue no longer holds the true largest residual, and the stop test of line L5 is wrong.
- **Forgetting the zero residual.** After line L6, the residual of $i \to j$ must be set to 0; otherwise the same message is sent again and again.
- **Stale entries.** With lazy deletion, an entry must be checked against the current version of its edge before use, or a stale large residual will trigger a needless update.
- **Assuming convergence.** On a frustrated $K_4$ with $J = -2$, residual BP fails to converge just as synchronous BP does. Keep the bound $U$ and report failure.
- **Counting rounds instead of updates.** Compare residual and synchronous BP by message updates, not by rounds or by time alone.

## Implementations

## History

Synchronous and round-robin schedules for loopy BP were common in practice when Elidan, McGraw and Koller proposed residual belief propagation at UAI 2006. Their idea was to treat the order of the message updates as a choice to be made from the messages themselves. Their experiments showed faster and more frequent convergence than synchronous and round-robin schedules. Sutton and McCallum (2007) made the scheduling cheaper by estimating the residuals, and Gonzalez, Low and Guestrin (2009) combined it with tree updates and parallel execution in residual splash.

## References

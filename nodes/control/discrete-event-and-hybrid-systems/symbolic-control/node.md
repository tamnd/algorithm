---
tag: W6XGE3
kind: technique
slug: symbolic-control
name: Symbolic control
aliases:
- abstraction-based controller synthesis
area: control/discrete-event-and-hybrid-systems
level: research
summary: Builds a finite abstraction of a continuous system related by approximate bisimulation, synthesizes a controller on it, and refines it back.
prereqs: [bisimulation, reactive-synthesis, reachable-set-computation]
see_also: [bisimulation, simulation-relation, reactive-synthesis, games-on-graphs, control-invariant-set, reachable-set-computation, ltl-model-checking, curse-of-dimensionality]
sources:
  - book: isbn:978-1-4419-0223-8
    title: "P. Tabuada, Verification and Control of Hybrid Systems: A Symbolic Approach, Springer, 2009"
    locator: the chapters on symbolic models, approximate symbolic models for control, and controller synthesis on finite models
  - paper: doi:10.1109/TAC.2007.895849
    title: "A. Girard and G. J. Pappas, Approximation metrics for discrete and continuous systems, IEEE Transactions on Automatic Control 52(5), 2007, pages 782 to 798"
    locator: approximate simulation and bisimulation relations with a precision, and bisimulation functions
  - paper: doi:10.1016/j.automatica.2008.02.021
    title: "G. Pola, A. Girard and P. Tabuada, Approximately bisimilar symbolic models for nonlinear control systems, Automatica 44(10), 2008, pages 2508 to 2516"
    locator: finite models on a grid that are approximately bisimilar to incrementally stable nonlinear control systems
  - paper: doi:10.1109/TAC.2016.2593947
    title: "G. Reissig, A. Weber and M. Rungger, Feedback refinement relations for the synthesis of symbolic controllers, IEEE Transactions on Automatic Control 62(4), 2017, pages 1781 to 1796"
    locator: abstractions built from over-approximated reachable sets of cells, and refinement of the controller by a quantizer only
  - paper: doi:10.1109/5.871304
    title: "R. Alur, T. A. Henzinger, G. Lafferriere and G. J. Pappas, Discrete abstractions of hybrid systems, Proceedings of the IEEE 88(7), 2000, pages 971 to 984"
    locator: classes of hybrid systems with exact finite bisimulation quotients
  - paper: doi:10.1145/2883817.2883834
    title: "M. Rungger and M. Zamani, SCOTS: A tool for the synthesis of symbolic controllers, Hybrid Systems: Computation and Control (HSCC 2016), 2016, pages 99 to 104"
    locator: a tool that builds grid abstractions with growth bounds and solves safety and reachability games
---

Symbolic control designs a controller for a continuous or hybrid system in three steps. It replaces the system by a finite transition system, the abstraction, whose states are cells of a grid and whose transitions over-approximate the dynamics. It solves the control problem on the finite system as a game on a graph, which is exact and automatic for safety, reachability and temporal logic goals. Then it refines the finite controller into a controller for the real system: measure the state, find its cell, and apply an input that the finite controller allows in that cell. A relation between the two systems, an approximate [bisimulation](/bisimulation/) (Girard and Pappas 2007; Pola, Girard and Tabuada 2008) or a feedback refinement relation (Reissig, Weber and Rungger 2017), makes the refined controller correct by construction. Tabuada (2009) presents the approach in a book.

## In plain words

Draw a grid over the space of states. For each square and each allowed input, work out, with a safe margin, which squares the system can move into in one step. Now you have a finite map: squares, and arrows labeled with inputs. A computer can solve control questions on such a map exactly, the way it solves a game on a board: which squares can stay away from the bad ones for ever, or reach a goal.

To use the answer, look at which square the real state is in, and apply an input that the map allows there. Because the arrows include every real move, the real system does what the map promises. The price is the grid: it grows very fast with the number of state components.

## When it applies

- **Discrete-time or sampled dynamics.** The system is $x_{k+1} = f(x_k, u_k)$, or a continuous system sampled with a period $\tau$ and inputs held constant, on a bounded set of states, with finitely many input values or a quantized input set.
- **A way to over-approximate one step.** For each cell and input, the program needs a set that contains all successors: from monotonicity, a Lipschitz or growth bound, or an interval or [zonotope](/zonotope-reachability/) enclosure. This is a small [reachable set computation](/reachable-set-computation/).
- **Specifications for finite systems.** Safety, reachability, reach-avoid and linear temporal logic goals, which have exact algorithms on finite graphs; see [reactive synthesis](/reactive-synthesis/) and [games on graphs](/games-on-graphs/).
- **Low dimension.** In practice, about up to five or six state variables with current tools, because the number of cells is exponential in the dimension (a rule of thumb, not a theorem).

## The template

The cells $q$ partition the bounded state set, each cell is a set $[q]$, and $\mathrm{Post}(q, u)$ is the set of cells that meet an over-approximation of $f([q], u)$. The goal here is safety: keep the state in the safe set $S$ for ever.

```pseudo id=template
SYMBOLIC-SAFETY(cells, inputs, f, S)
L1  for each cell q and input u do Post(q, u) ← the cells that meet an over-approximation of f([q], u)
L2  W ← the cells q with [q] inside S
L3  repeat
L4      W' ← the cells q in W that have an input u with Post(q, u) nonempty and inside W
L5      if W' = W then stop;  W ← W'
L6  C(q) ← the inputs u with Post(q, u) inside W, for each q in W
L7  refined controller: at the state x, find the cell q with x in [q], and apply any u in C(q)
```

Lines L3 to L5 compute the largest fixed point of a safety game on the finite graph, the finite analogue of the [control invariant set](/control-invariant-set/) iteration. With a counter of the good successors per pair $(q, u)$, it takes time linear in the number of transitions.

**Theorem (soundness of the refinement).** Suppose that for every cell $q$, input $u$ and state $x \in [q]$, the successor $f(x, u)$ lies in a cell of $\mathrm{Post}(q, u)$. Then every solution of the closed loop of line L7 that starts in a cell of $W$ stays in the union of the cells of $W$, and so in $S$.

*Proof.* Let $x_k \in [q]$ with $q \in W$, and let $u \in C(q)$ be the applied input. Then $x_{k+1}$ lies in a cell of $\mathrm{Post}(q, u)$, and $\mathrm{Post}(q, u) \subseteq W$ by line L6, which is nonempty by line L4 at the fixed point. By induction the state stays in cells of $W$, and these lie in $S$ by line L2. $\blacksquare$

The converse fails: a state from which a safe controller exists can be outside $W$, because the abstraction adds behaviors. Approximate bisimulation gives a bound on this loss, for incrementally stable systems.

## Classic examples

**An unstable scalar plant.** Take $x_{k+1} = 2x_k + u_k$ with $u \in \{-0.5, 0, 0.5\}$ and the safe set $S = [-1, 1]$. With cells $[-1, -0.5)$, $[-0.5, 0)$, $[0, 0.5)$ and $[0.5, 1]$, a cell $[a, b)$ maps exactly to $[2a + u, 2b + u)$.

| cell | best input | image | kept in round 1 | kept in round 2 |
|---|---|---|---|---|
| $[-1, -0.5)$ | $0.5$ | $[-1.5, -0.5)$ | no | |
| $[-0.5, 0)$ | $0.5$ | $[-0.5, 0.5)$ | yes | yes |
| $[0, 0.5)$ | $-0.5$ | $[-0.5, 0.5)$ | yes | yes |
| $[0.5, 1]$ | $-0.5$ | $[0.5, 1.5]$ | no | |

The fixed point is $W = \{[-0.5, 0), [0, 0.5)\}$, with $C = 0.5$ on the left cell and $C = -0.5$ on the right one. From $x_0 = 0.3$, the closed loop visits $0.1, -0.3, -0.1, 0.3$ and repeats, so it stays safe. The largest set from which some input sequence keeps the state in $S$ is $[-0.5, 0.5]$: for $x > 0.5$, $2x - 0.5 - 0.5 = 2(x - 0.5)$, so the distance above $0.5$ at least doubles at every step. The abstraction finds this set except the point $0.5$. With the coarser cells $[-1, 0)$ and $[0, 1]$, the images are $[-1.5, 0.5)$ and $[-0.5, 1.5]$ at best, both leave $S$, and $W$ is empty: the coarse abstraction proves nothing, although the plant can be kept safe.

**Exact abstractions of hybrid systems.** For timed automata, the [region graph](/region-graph/) is a finite bisimulation quotient. Alur, Henzinger, Lafferriere and Pappas (2000) describe other classes of hybrid systems with finite bisimulation quotients. For general continuous dynamics such quotients do not exist, and symbolic control uses approximate ones.

**Incrementally stable systems.** Pola, Girard and Tabuada (2008) built grid abstractions of nonlinear control systems that are incrementally globally asymptotically stable. For such systems, the finite model is approximately bisimilar to the sampled system, with a precision that a fine enough grid and a long enough sampling time make as small as wanted. A controller found on the finite model then has a guaranteed precision on the real system.

**Tools.** SCOTS (Rungger and Zamani 2016) builds abstractions with growth bounds, in the setting of feedback refinement relations, and solves safety and reachability games.

## Variations

- **Reachability and reach-avoid.** Replace the greatest fixed point by a least fixed point: start from the target cells and add the cells that have an input whose successors all lie in the set so far. The number of rounds bounds the number of steps to the target.
- **Temporal logic goals.** Turn an LTL formula into an automaton, take the product with the abstraction, and solve the resulting game, for example a [parity game](/parity-game/); see [reactive synthesis](/reactive-synthesis/) and [LTL model checking](/ltl-model-checking/).
- **Feedback refinement relations.** Reissig, Weber and Rungger (2017) require the abstraction to over-approximate the reachable sets of cells, and refine the controller by a quantizer only, without incremental stability.
- **Nonuniform and lazy abstractions.** Refine the grid only where the synthesis needs it, or compute transitions only for the cells that the fixed point visits.
- **Abstraction of hybrid systems.** The same steps apply to switched and [piecewise affine](/piecewise-affine-system/) systems, with the modes as inputs or as part of the state.

## Pitfalls

- **An abstraction that under-approximates (line L1).** If $\mathrm{Post}(q, u)$ misses a cell that a real successor enters, for example because the program sampled a few points of the cell, the theorem fails. Use a sound enclosure of the successors of the whole cell.
- **Cells that overlap, or a state between cells (line L7).** The refinement needs each state in exactly one cell. Use half-open cells, and treat the edge of the domain as unsafe.
- **Empty answer from a coarse grid (lines L3 to L5).** The method is sound but not complete: an empty $W$ means only that this abstraction found no controller, as in the example. Refine the grid or shorten the sampling period.
- **Dimension.** With $k$ cells per axis there are $k^n$ cells, the [curse of dimensionality](/curse-of-dimensionality/). Exploit structure (monotone dynamics, decomposition) before refining.
- **Sampled-data effects.** For a continuous plant, the abstraction is about the sampling instants. Safety between samples needs an enclosure of the flow over the whole sampling interval.
- **Measurement errors.** The refinement assumes that the cell of the true state is known. With measurement errors, enlarge the over-approximation by the error, or the theorem no longer applies.

## Exercises

1. In the example, use the cells of width $0.25$ on $[-1, 1]$. Which cells are in $W$, and how close is $W$ to $[-0.5, 0.5]$?
2. Replace the inputs by $u \in \{-1, 0, 1\}$ in the example and compute $W$ with cells of width $0.5$. Compare with the largest set that some input sequence can keep in $S$.
3. Write the least fixed point for the goal "reach $[-0.1, 0.1]$ while staying in $S$" and run it on the example with cells of width $0.1$.
4. Show that the iteration of lines L3 to L5 stops after at most as many rounds as there are cells.
5. For $x_{k+1} = 0.5x_k + u_k$ with $|u| \le 0.1$, show that cells of any width $\eta$ give an abstraction in which the images of a cell have width $\eta / 2$, and explain why such a contracting system is easy to abstract.

## References

---
tag: 9AA5EW
kind: technique
slug: analytical-placement
name: Analytical placement
aliases:
- nonlinear placement
area: cad/partitioning-floorplanning-and-placement
level: core
summary: Places cells by minimizing a smooth wire length model plus a density penalty with gradient methods, then legalizing.
prereqs: [placement-problem, half-perimeter-wirelength, penalty-method, gradient-descent]
see_also: [quadratic-placement, force-directed-placement, simpl-placement, electrostatics-based-placement, log-sum-exp-wirelength, placement-legalization, detailed-placement, min-cut-placement]
sources:
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 4, Global and Detailed Placement (analytical global placement, quadratic placement with spreading, and the flow of global placement, legalization and detailed placement; general locator)
  - paper: doi:10.1109/TCAD.2008.923063
    title: Tung-Chieh Chen, Zhe-Wei Jiang, Tien-Chang Hsu, Hsin-Chen Chen and Yao-Wen Chang, NTUplace3, an analytical placer for large-scale mixed-size designs with preplaced blocks and density constraints, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 27(7), 1228 to 1240, 2008
    locator: the objective of log-sum-exp wirelength plus a smoothed bin density penalty, the conjugate gradient solver, and the growing penalty weight
  - paper: doi:10.1145/2699873
    title: Jingwei Lu, Pengwen Chen, Chin-Chih Chang, Lu Sha, Dennis Jen-Hsin Huang, Chin-Chi Teng and Chung-Kuan Cheng, ePlace, electrostatics-based placement using fast Fourier transform and Nesterov's method, ACM Transactions on Design Automation of Electronic Systems 20(2), article 17, 2015
    locator: the electrostatic density penalty, Nesterov's method and the schedule of the penalty weight
  - paper: doi:10.1109/TCAD.2011.2170567
    title: Myung-Chul Kim, Dong-Jin Lee and Igor L. Markov, SimPL, an effective placement algorithm, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 31(1), 50 to 60, 2012
    locator: the quadratic branch of the technique, with spreading by anchors in place of a density penalty
---

Analytical placement is the main technique for global placement of standard cells today. It treats the cell positions as real variables and replaces the hard parts of the [placement problem](/placement-problem/) with smooth ones. The total [HPWL](/half-perimeter-wirelength/) is not differentiable, so a smooth model such as a quadratic or [log-sum-exp](/log-sum-exp-wirelength/) wirelength takes its place. The rule that cells must not overlap is not smooth either, so a density penalty takes its place: it grows where the cells are crowded. A gradient method minimizes the sum of the two, while the weight of the penalty grows step by step, as in a [penalty method](/penalty-method/). When the cells are spread enough, a [legalizer](/placement-legalization/) puts them on rows and sites, and a [detailed placer](/detailed-placement/) improves the result. Quadratic placers with spreading forces or anchors belong to the same family; they keep a quadratic wirelength and spread the cells by other means.

## In plain words

Think of the cells as beads on rubber bands that may slide anywhere on the board. Pulling only on the bands makes all the beads clump. So add a second push: every crowded spot pushes beads away, and the push gets stronger each round.

Let the beads settle under both pulls, make the push a bit stronger, and let them settle again. After some rounds the beads are spread out and the bands are still short. Then snap each bead to a nearby legal place.

## When it applies

- The cells are many and small, so a continuous model of their positions is accurate; a few large macros need extra care.
- The cost can be written as a sum over nets of a function of the pin positions, so a smooth model exists and its gradient is cheap.
- The overlap rule can be relaxed to a density limit per region, so that a smooth penalty can measure it.
- A later legalizer can turn a well-spread placement into a legal one with small moves.

## The template

```pseudo id=main
ANALYTICAL-PLACE(netlist, rows, smooth wirelength WL_γ, density penalty D, target overflow τ*)
L1  start from a quadratic solve or with all cells near the center
L2  λ ← a small weight, chosen so that the gradient of λ D is small next to the gradient of WL_γ
L3  repeat
L4      from the current point, minimize WL_γ(x, y) + λ D(x, y) with a gradient method and a preconditioner
L5      λ ← λ · β with β > 1, and lower γ to sharpen the wirelength model
L6  until the density overflow is at most τ*
L7  legalize: put each cell on a site of a row with no overlap
L8  detailed placement: improve the legal placement by local moves
L9  return the placement
```

The holes of the template are:

- **The wirelength model $\mathrm{WL}_\gamma$.** The quadratic model of [quadratic placement](/quadratic-placement/), with the clique, star or bound to bound net model; or a smooth model of HPWL such as [log-sum-exp](/log-sum-exp-wirelength/) or the weighted average model, both with a smoothing parameter $\gamma$.
- **The density penalty $D$.** A sum over bins of the squared excess of a smoothed bin density, as in APlace and NTUplace; the energy of an electric field whose charges are the cells, as in [electrostatics-based placement](/electrostatics-based-placement/); or, in quadratic placers, no penalty at all but forces or anchors that move the cells, as in [force-directed placement](/force-directed-placement/) and [SimPL](/simpl-placement/).
- **The optimizer.** The [conjugate gradient method](/conjugate-gradient-method/) for a quadratic or nonlinear objective, or [Nesterov's accelerated gradient](/nesterov-accelerated-gradient/) with a step from a Lipschitz estimate.
- **The schedule.** The start value and growth factor $\beta$ of $\lambda$, the schedule of $\gamma$, and the stop rule.
- **The finish.** A legalizer such as [Tetris](/tetris-legalization/) or [Abacus](/abacus-legalization/), and a detailed placer such as [independent set matching](/independent-set-matching/).

What is proved and what is not: a smooth model with a parameter $\gamma$ is within a known bound of HPWL (for log-sum-exp, at most $2 \gamma \ln p$ above it per net of $p$ pins and per coordinate), and the gradient methods have known rates on convex, smooth objectives. The density penalty makes the objective nonconvex, so nothing proves that the loop finds a good placement; the quality of analytical placers is measured on benchmarks.

## Classic examples

- **[Quadratic placement](/quadratic-placement/).** The objective is quadratic and $D$ is absent; one sparse linear solve per coordinate gives a placement with the cells clumped near the center, the start point of most of the others.
- **[Force-directed placement](/force-directed-placement/).** The quadratic solve with added forces that push cells out of crowded regions; Kraftwerk and FastPlace are of this kind.
- **[SimPL](/simpl-placement/).** The quadratic solve alternates with lookahead legalization, and anchors at the spread positions take the role of $\lambda D$; the anchor weight grows like $\lambda$.
- **APlace and NTUplace3.** The [log-sum-exp](/log-sum-exp-wirelength/) wirelength plus a penalty on smoothed bin densities, minimized by conjugate gradients with a growing $\lambda$.
- **[Electrostatics-based placement](/electrostatics-based-placement/).** ePlace and RePlAce take the cells as charges and use the field energy as $D$, the weighted average wirelength as $\mathrm{WL}_\gamma$, and Nesterov's method as the optimizer; DREAMPlace runs the same method on GPUs.

## Variations

- **Multilevel analytical placement.** mPL and NTUplace cluster the netlist, place the coarse netlist, and refine level by level, as in [multilevel hypergraph partitioning](/multilevel-hypergraph-partitioning/).
- **Mixed-size placement.** Large macros enter the same objective with their area, then are legalized first and fixed.
- **Timing and routability.** Net weights from timing analysis, as in [timing-driven placement](/timing-driven-placement/), and inflated cells in congested regions enter the same loop.
- **Augmented Lagrangian forms.** Some placers update a multiplier per bin instead of one global $\lambda$, as in the [augmented Lagrangian method](/augmented-lagrangian-method/).

## Pitfalls

- **Growing $\lambda$ too fast.** The cells then spread before the wirelength has pulled connected cells together, and the result is close to a random spreading. Growing it too slowly costs many solves.
- **A $\gamma$ that is too small early.** The smooth model becomes nearly as rough as HPWL and the gradient method takes tiny steps; lower $\gamma$ as the cells spread.
- **Stopping at a high overflow.** If many cells still overlap at line L6, the legalizer must move them far, and the wirelength gain of global placement is lost.
- **Trusting the smooth value.** The objective is a model. Report HPWL after legalization and detailed placement, not the smooth wirelength.
- **Large macros.** Treating a macro as one more charge or one more bin load causes poor spreading near it; mixed-size designs need their own handling.

## References

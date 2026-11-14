---
tag: Q680V7
kind: problem
slug: cmm-probe-path-planning
name: CMM probe path planning
aliases:
- inspection path planning
- coordinate measuring machine path planning
area: cad/reverse-engineering-and-inspection
level: advanced
summary: Choose probe orientations for the measurement points of a coordinate measuring machine, order the points and find collision-free moves between them, to cut measuring time.
prereqs: [traveling-salesman-problem, accessibility-cone]
see_also: [nearest-neighbor-heuristic, two-opt, christofides-algorithm, euclidean-tsp, configuration-space, motion-planning, hammersley-sampling-for-cmm, cad-based-inspection]
sources:
  - paper: doi:10.1080/00207549408956955
    title: C. P. Lim and C. H. Menq, CMM feature accessibility and path generation, International Journal of Production Research 32(3), 1994, 597 to 618
    locator: the accessibility of features to the probe, the choice of probe orientations, and the generation of collision-free probe paths
  - paper: doi:10.1109/70.782025
    title: S. N. Spitz, A. J. Spyridi and A. G. Requicha, Accessibility analysis for planning of dimensional inspection with coordinate measuring machines, IEEE Transactions on Robotics and Automation 15(4), 1999, 714 to 727
    locator: the accessibility of measurement points as sets of probe directions computed in configuration space, and the selection of a small set of probe orientations
  - paper: doi:10.1016/0304-3975(77)90012-3
    title: Christos H. Papadimitriou, The Euclidean travelling salesman problem is NP-complete, Theoretical Computer Science 4(3), 1977, 237 to 244
    locator: the NP-completeness of the traveling salesman problem for points in the plane with Euclidean distances, used here for the hardness of sequencing
  - paper: doi:10.1109/70.134279
    title: C.-H. Menq, H.-T. Yau and G.-Y. Lai, Automated precision measurement of surface profile in CAD-directed inspection, IEEE Transactions on Robotics and Automation 8(2), 1992, 268 to 278
    locator: the planning of measurement points from the CAD model and the automatic measurement of surface profiles
---

CMM probe path planning is the problem of turning a list of points to be measured on a part into a program for a coordinate measuring machine. Each point must be touched along its surface normal by a probe that reaches it without hitting the part or the fixture. The planner chooses for each point a probe orientation from which it is accessible, keeps the number of orientation changes small, orders the points, and finds collision-free moves between consecutive points, so that the total time is least. The ordering part contains the [traveling salesman problem](/traveling-salesman-problem/), so the problem is NP-hard, and planners use heuristics. Where the points come from is [Hammersley sampling](/hammersley-sampling-for-cmm/) or another sampling plan, and the place of the planning in the whole process is [CAD-based inspection](/cad-based-inspection/).

## In plain words

A measuring machine checks a part by touching it with a small ball on a thin rod, one point at a time. Between touches it moves through the air, and moving takes most of the time. The rod can be turned to a few fixed angles, and turning it is slow too.

So we must decide three things. For each point, which angle of the rod can reach it without the rod hitting the part. In which order to visit the points, so that the moves are short. And how to move from one point to the next without a crash, often by going up to a safe height, across, and down. Finding the very best order is as hard as the famous problem of a salesman who wants the shortest trip through many towns, so we use good orders, not perfect ones.

## Definition

The input is:

- the part and fixture as solids $P$, in the coordinates of the machine after the part is localized (see [localization for inspection](/inspection-localization/));
- measurement points $p_1, \dots, p_n$ on $\partial P$ with outer unit normals $\nu_1, \dots, \nu_n$, each to be touched by a straight approach along $-\nu_i$ from a pre-touch point $p_i + \varepsilon \nu_i$;
- a set $\Omega$ of probe orientations: a finite set for an indexable head, or a region of the unit sphere for a continuous head;
- the probe geometry (stylus ball, stem, head), and a time model: the time of a move along a path, and the time $c$ of an orientation change.

For a point $p_i$ the set $A_i \subseteq \Omega$ of orientations from which the stylus can touch it without collision is its [accessibility cone](/accessibility-cone/). A plan is an orientation $\omega_i \in A_i$ for every point, an order $\pi$ of the points, and for each pair of consecutive points a collision-free path of the probe between their pre-touch points, in the [configuration space](/configuration-space/) of the probe. The objective is to minimize the total time: the sum of the move times, plus $c$ times the number of orientation changes along the order, plus the touch times, which are fixed.

## Variants

- **Orientation selection.** Choose a smallest set of orientations $W \subseteq \Omega$ such that every point is accessible from some $\omega \in W$. Each orientation covers the points whose accessibility cones contain it, so this is a [set cover](/set-cover/) problem over the points. Spitz, Spyridi and Requicha compute the accessibility of points as sets of directions and use them to select a small set of orientations.
- **Sequencing with one orientation.** With all points measured from one orientation and moves of known cost, the order is a traveling salesman tour or path on the pre-touch points.
- **Clearance-plane moves.** Every move goes up to a safe plane at height $h$ above the part, across, and down. Between two points at the same depth the cost is $2h$ plus the distance in the plane, so every order pays $2h$ per move and the best order is the best planar tour.
- **Direct moves.** A straight move is used when the segment is free of the part, and a path from a [motion planning](/motion-planning/) method otherwise. Lim and Menq generate such collision-free paths around the part.
- **Grouping by feature.** Points of one feature, such as a hole or a face, are measured together, and the order is a tour of features with a tour inside each feature.
- **Choice of orientation per point.** When a point is accessible from several orientations, the problem is a generalized traveling salesman problem, in which one copy of each point must be visited.

## Examples

**A short tour on a line.** The probe starts at $x = 0$ and must touch points at $x = 1, -2, 4$ on one edge of a part, then return. The [nearest neighbor heuristic](/nearest-neighbor-heuristic/) goes to $1$, then to $-2$, then to $4$, then home: $1 + 3 + 6 + 4 = 14$. The best tour goes to the left end and the right end once each, for example $0, -2, 1, 4, 0$: $2 + 3 + 3 + 4 = 12$. With clearance-plane moves at height $h$, both tours add $8h$, so the comparison is the same.

**Orientations.** A block with a vertical bore and a side hole: the top face and the bore are accessible from the vertical orientation, the side hole only from a horizontal one, and the side face from both. Two orientations cover all points, and the plan measures the top face, the bore and the side face first, changes the orientation once, then measures the side hole. A plan that switched for the side face would pay a second change.

## Known algorithms

- **Accessibility.** The accessibility cone of a point is computed from the part and the stylus, exactly for simple shapes and on a discretized sphere of directions in general, as on the [accessibility cone](/accessibility-cone/) page. Lim and Menq and Spitz, Spyridi and Requicha give methods for measuring machines.
- **Orientation selection.** [Greedy set cover](/greedy-set-cover/): repeatedly take the orientation that covers the most points not yet covered. It uses at most $H_d$ times the least number of orientations, with $d$ the largest number of points accessible from one orientation and $H_d$ the harmonic number.
- **Sequencing.** Construction by the [nearest neighbor heuristic](/nearest-neighbor-heuristic/), improvement by [2-opt](/two-opt/) moves, and the [Christofides algorithm](/christofides-algorithm/) with its factor $3/2$ when the move times form a metric, which clearance-plane moves do. In the plane with straight moves, the [Euclidean TSP](/euclidean-tsp/) has a polynomial-time approximation scheme.
- **Collision-free moves.** Clearance planes for prismatic parts, and general [motion planning](/motion-planning/) in the space of probe positions for complex parts.

## Bounds

**NP-hardness.** Deciding whether a plan of time at most $L$ exists is NP-hard. *Proof.* Take an instance of the Euclidean traveling salesman problem: points $x_1, \dots, x_n$ in the plane and a bound $L$, which is NP-complete by Papadimitriou (1977). Build a flat plate whose top face contains the points, with nothing above it, one vertical probe orientation, normals $\nu_i$ pointing up, and a move time equal to the length of the path of the probe tip. All pre-touch points lie in the plane at height $\varepsilon$ above the plate, in free space, so the shortest move between two of them is the straight segment, of length $\lvert x_i - x_j \rvert$. With no orientation changes and fixed touch times, a plan of total move time at most $L$ exists exactly when a tour of length at most $L$ exists. $\square$

The proof uses the simplest time model. Real machines accelerate, so the time of a move is not proportional to its length, but every model that agrees with the length on such instances gives the same hardness.

- **Heuristic guarantees.** For move times that satisfy the triangle inequality, the nearest neighbor tour is within a factor $\frac12(\lceil \lg n \rceil + 1)$ of the best, Christofides within $3/2$, and 2-opt local optima within $O(\sqrt n)$, as proved on those pages.
- **Collision checking.** A path is checked against the part and the fixture for every move, which dominates the time of planning for complex parts.

## Reductions

- **From the Euclidean traveling salesman problem**, as above, which shows the hardness.
- **To the traveling salesman problem**, when the orientations are fixed: the cost of a move is the time of the shortest collision-free path, and an orientation change between two points adds $c$ to the cost of the edge.
- **To set cover**, for the selection of the fewest orientations.
- **To motion planning**, for each move between consecutive points.

## Applications

- **Measuring machine programs.** Offline programming from the CAD model replaces the teaching of points by hand on the machine.
- **Free-form surfaces.** Many points on a blade or a die, where the order and the orientation changes decide most of the measuring time.
- **Scanning probes and robots.** The same planning, with continuous scanning paths in place of single touches, and with arm robots that carry optical sensors.

## References

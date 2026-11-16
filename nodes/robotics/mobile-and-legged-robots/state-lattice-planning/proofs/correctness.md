---
title: State lattice search is feasible, complete and optimal with respect to its lattice and control set
proves: [correctness]
status: full
---

Line numbers refer to the pseudocode on the [state lattice planning](/state-lattice-planning/) page. Lengths are in lattice units ($r = 1$); the costs in meters are $r$ times these. The lattice states are $(i, j, k)$ with integers $i, j$ and a heading $k\pi/4$, $k \in \{0, \dots, 7\}$. The radius of every arc is $R = 1 + \sqrt 2$.

**Lemma 1 (primitives join lattice states).** Each primitive of the control set, driven from $(0, 0, k)$, ends exactly at the lattice state given in the table of the page.

*Proof.* Start with the left turn from heading 0. An arc of radius $R$ through the angle $\pi/4$ from $(0, 0, 0)$ ends at $(R\sin\frac\pi4,\ R(1 - \cos\frac\pi4)) = (R/\sqrt2,\ R(1 - 1/\sqrt2))$ with heading $\pi/4$. The straight part of length $\sqrt2 - 1$ along $\pi/4$ adds $(1 - 1/\sqrt2,\ 1 - 1/\sqrt2)$. With $R = 1 + \sqrt2$, $R/\sqrt2 = 1 + 1/\sqrt2$ and $R(1 - 1/\sqrt2) = 1 - 1/\sqrt2 + \sqrt2 - 1 = 1/\sqrt2$. So the end point is $(2, 1)$, with heading $\pi/4$, the state $(2, 1, 1)$. The right turn is its mirror image in the $x$ axis and ends at $(2, -1, 7)$. The straight primitives end at $(1, 0, 0)$ and $(1, 1, 1)$ by inspection. The turn from $(0, 0, 1)$ to $(2, 1, 0)$ is the left turn above driven backward in time and rotated by $\pi$: reversing it gives a path from $(2, 1)$ with heading $5\pi/4$ to $(0, 0)$ with heading $\pi$, and the rotation by $\pi$ about the origin after the shift by $(-2, -1)$ maps it to a path from $(0, 0, \pi/4)$ to $(2, 1, 0)$, made of a straight part of length $\sqrt2 - 1$ and then a right arc through $\pi/4$. The turn to $(1, 2, 2)$ is its mirror image in the line $y = x$. A rotation by $\pi/2$ maps lattice points to lattice points and adds 2 to $k$, so the primitives of the other six headings also join lattice states. $\square$

The test `test_primitives_end_on_lattice_states` drives all 24 primitives in floating point and finds every end within $10^{-12}$ of its lattice state.

**Lemma 2 (primitives are paths of the car).** Each primitive is a $C^1$ curve with curvature $0$ or $\pm 1/R$, driven forward. So it is a path of the forward car with minimum turning radius $R r$ meters, and a sequence of primitives that joins states is again such a path.

*Proof.* Each piece is an arc of radius $R$ or a line, both driven forward. Inside a primitive, the arc and the line meet with the same heading, because the line starts in the direction where the arc ends. Two consecutive primitives meet at a lattice state whose heading both of them use, the end heading of the first and the start heading of the second, so the heading is continuous there too. $\square$

**Lemma 3 (the collision test).** Line L6 accepts a primitive from $(i, j, k)$ only if every sample of the primitive, at spacing at most $1/8$, lies in a free cell inside the map, where a sample on a cell border counts for the cells on both sides.

*Proof.* The swath of a primitive is the set of cells hit by its samples from $(0, 0, k)$, computed once. A shift by the integer vector $(i, j)$ moves each sample and its cell by the same vector, so the cells hit from $(i, j, k)$ are the swath shifted by $(i, j)$, and line L6 checks exactly those. $\square$

As for every sampled check, an arc can clip the corner of a blocked cell between two samples. The test `test_path_is_continuous_and_collision_free` samples every returned path four times more densely than the swath and finds no sample in a blocked cell.

**Theorem (optimal and complete with respect to the lattice).** Let $\mathcal G$ be the directed graph whose vertices are the lattice states in the map and whose edges are the primitives that pass the test of line L6, weighted by their lengths. The search of lines L1 to L8 returns a path of least weight in $\mathcal G$ from the start to the goal if one exists, and failure otherwise.

*Proof.* $\mathcal G$ is finite: it has $8(n_x + 1)(n_y + 1)$ vertices and at most three edges per vertex, all with positive weight. The heuristic of line L2 is $h(s) = |(i, j) - (i_g, j_g)|$. A primitive from $s$ to $t$ has length at least the distance between its end points, so $h(s) \le |(i_s, j_s) - (i_t, j_t)| + h(t) \le w(s, t) + h(t)$, and $h = 0$ at the goal: $h$ is consistent. A\* with a consistent heuristic on a finite graph with positive weights expands each vertex at most once, with its least distance from the start, and stops at the goal with a shortest path, or empties the open list exactly when the goal cannot be reached; see [A\* search](/a-star-search/) and [consistent heuristic](/consistent-heuristic/). $\square$

The test `test_a_star_matches_dijkstra` compares the cost with [Dijkstra's algorithm](/dijkstra/) on the same graph on random maps and finds them equal to $10^{-9}$, with A\* expanding no more states.

**What the theorem does not say.** The optimality and the completeness are relative to the lattice and to the control set. A path of the continuous car can exist where $\mathcal G$ has none, and the continuous optimum can be shorter than the best lattice path; the page gives examples of both. Pivtoraiko, Knepper and Kelly call this resolution completeness and optimality with respect to the lattice.

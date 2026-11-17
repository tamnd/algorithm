---
tag: P1VHW8
kind: algorithm
slug: shock-propagation
name: Shock propagation
aliases:
- stacking by shock propagation
- shock propagation sweep
area: graphics-and-signals/rigid-body-simulation
level: advanced
summary: Make tall stacks stable by solving contacts from the ground up in a contact graph and freezing each lower level when solving the one above.
solves: [rigid-body-simulation-problem]
model: real-ram
complexity:
  vars: {n: the number of bodies, e: the number of edges of the contact graph, c: the number of contacts, S: the number of contact sweeps, I: the passes per level}
  time: {graph_and_levels: O(n + e), sweeps: O((S + 1) I c)}
  space: {total: O(n + e + c)}
properties: {deterministic: true, online: false, recursive: false, in_place: true}
history:
  year: 2003
  people: [Eran Guendelman, Robert Bridson, Ronald Fedkiw]
  note: Guendelman, Bridson and Fedkiw introduced the contact graph, its levels and the shock propagation sweep for stacks of nonconvex rigid bodies. Erleben (2007) built a velocity-based time stepping scheme around shock propagation.
prereqs: [projected-gauss-seidel, collision-impulse, strongly-connected-components, topological-sort, depth-first-search]
see_also: [impulse-based-simulation, baumgarte-stabilization, contact-manifold, tarjan-scc, stewart-trinkle-time-stepping, rigid-contact-complementarity, baraff-contact-force-algorithm]
sources:
  - paper: doi:10.1145/882262.882358
    title: "Eran Guendelman, Robert Bridson and Ronald Fedkiw, Nonconvex rigid bodies with stacking, ACM Transactions on Graphics 22(3), 871-878, 2003 (SIGGRAPH 2003)"
    locator: "Section 6 (the time step and the predicted positions), Section 8 (contact processing), Section 8.1 (the contact graph and its strongly connected components) and Section 8.2 (shock propagation), Figures 6 and 7"
  - paper: doi:10.1145/1243980.1243986
    title: "Kenny Erleben, Velocity-based shock propagation for multibody dynamics animation, ACM Transactions on Graphics 26(2), article 12, 2007"
    locator: the fixed time stepping scheme with shock propagation for velocity-based complementarity formulations
  - url: https://box2d.org/files/ErinCatto_IterativeDynamics_GDC2005.pdf
    title: "Erin Catto, Iterative Dynamics with Temporal Coherence, Game Developers Conference, 2005"
    locator: "Section 9.1 (box stacking with and without contact caching)"
---

Shock propagation is a heuristic that makes stacks of rigid bodies come to rest. An iterative contact solver such as [projected Gauss-Seidel](/projected-gauss-seidel/) needs many sweeps before the weight of a tall stack reaches the ground, so with a fixed budget the stack sinks into itself. Shock propagation builds a graph of which body rests on which, sorts the bodies into levels from the ground up, and then makes one last sweep over the levels. After it handles a level, it gives the bodies of that level infinite mass, so the levels above cannot push them down again. This stops a stack in one sweep. It also changes the physics, because a body of finite mass is treated as if it could not move: the method does not conserve momentum, and it is tuning for stable stacks, not a solution of the contact problem.

## In plain words

Think of a tower of boxes on the floor. A simple solver fixes one touching pair at a time. When it stops a box, it pushes the box below down a little. The push needs many rounds to reach the floor, and with few rounds the tower sinks.

Shock propagation first finds out which box sits on which. Then it fixes the floor contacts, and it nails the bottom boxes in place for the rest of the round. Next it fixes the boxes on top of them, and nails those. It goes up the tower in this way. A box can only be pushed up by what is below it, never down by what is above it. So the whole tower stops in one round. The price is that the upper boxes cannot press the lower ones, which real boxes do.

## The problem

The input is one time step of a [rigid body simulation](/rigid-body-simulation-problem/): bodies with velocities after gravity, and contacts $(A, B)$ with normal $n$ from $B$ to $A$, as on the [collision impulse](/collision-impulse/) page. A contact approaches when $v_{rel} = n \cdot (v_A(p) - v_B(p)) < 0$. The aim is velocities for which no contact approaches, found with a small, fixed amount of work, also for stacks of many bodies. This page uses $y$ up and gravity $(0, -9.81)$.

## The algorithm

Guendelman, Bridson and Fedkiw (2003) define the levels by a contact graph (Section 8.1). Each body is moved for a short time $\Delta\tau$ under gravity alone, with the others fixed. If the moved body $A$ then touches $B$, the graph gets the edge $B \to A$: $A$ would fall onto $B$. In the code of this page, static bodies do not move, so they get no incoming edges. Bodies in a cycle of the graph, such as dominoes leaning on each other in a ring, are merged into one strongly connected component, found by two depth-first searches. The condensation is acyclic, and the level of a component is 0 if no edge enters it, and otherwise one more than the largest level of a component with an edge into it. A contact belongs to the higher level of its two bodies.

```pseudo id=main
SHOCK-PROPAGATION-STEP(bodies, contacts, Δτ, S, I)
L1  G ← edges B → A where A, moved under gravity for Δτ, touches B
L2  C_0, C_1, ... ← strongly connected components of G in topological order
L3  level(C) ← 0 if no edge enters C, else 1 + max level of a predecessor of C
L4  repeat S times                                  ▷ contact sweeps
L5    for each level ℓ, from 0 upward
L6      repeat I times: resolve each contact of level ℓ
L7  for each level ℓ, from 0 upward                 ▷ the shock sweep
L8    repeat I times: resolve each contact of level ℓ
L9    give every body of level ℓ infinite mass (inverse mass 0)
```

RESOLVE applies the [collision impulse](/collision-impulse/) of one contact if it approaches. The infinite masses of line L9 last only until the end of the sweep; the bodies keep their real masses in the next step. In the paper, the contact sweeps of lines L4 to L6 use the coefficient of restitution with a value of $\epsilon$ ramped from $-0.9$ up to $0$ over the sweeps (Section 8), and the shock sweep is run on the last of them (Section 8.2). The code of this page uses plastic impulses throughout ($e = 0$) and a separate shock sweep, which is the same structure in a simpler form.

Inside one level the contacts are solved $I$ times, and the bodies of that level are not given infinite mass while it is solved (Section 8.2). This is how a ring of dominoes in one component is still solved by the ordinary iteration.

## Example

Three boxes of mass 1 and side 1 stand on the ground and all move down at $1$ m/s, for example after a gravity step. The contact graph is ground $\to$ box 1 $\to$ box 2 $\to$ box 3, with levels 0, 1, 2 and 3. The contacts are ground with box 1 (level 1), box 1 with box 2 (level 2), and box 2 with box 3 (level 3).

One contact sweep from the bottom up, with plastic impulses:

| contact | before | after |
|---|---|---|
| ground and box 1 | $v_1 = -1$ | $v_1 = 0$ |
| box 1 and box 2 | $v_1 = 0$, $v_2 = -1$ | $v_1 = v_2 = -1/2$ |
| box 2 and box 3 | $v_2 = -1/2$, $v_3 = -1$ | $v_2 = v_3 = -3/4$ |

The velocities are $(-1/2, -3/4, -3/4)$: the stack still sinks. Plain sweeps need 17 sweeps until every box is slower than 1% of its start speed. A shock sweep after the first sweep handles level 1 (box 1 stops) and freezes box 1, then level 2 (box 2 stops against the frozen box 1) and freezes it, then level 3. The result is $(0, 0, 0)$ after one sweep.

**Momentum.** A lower box of mass 1 moves up at $1$ m/s, and an upper box of mass 3 on it moves down at $1$ m/s. The total momentum is $1 - 3 = -2$. A plastic collision of the two gives both $-1/2$ m/s and keeps the momentum. The shock sweep freezes the lower box at level 0 first, so the upper box takes the velocity of the lower box: both move at $1$ m/s, and the momentum is $4$. The lower box is not slowed by the heavy box on top of it. This is the change of physics: the result is not what a collision of these two bodies would give.

**Stacks over time.** A column of $N$ boxes of mass 1 and side 1 starts at rest on the ground. Each step adds gravity, runs 4 contact sweeps with one pass per level, and moves the boxes by symplectic Euler, at $\Delta t = 1/60$ for 120 steps. The numbers are measurements from the code of this page:

| boxes $N$ | 5 | 10 | 20 |
|---|---|---|---|
| top box height at rest | 4.5 | 9.5 | 19.5 |
| without shock: top box height | 3.81 | 6.31 | 10.32 |
| without shock: largest overlap | 0.262 | 0.557 | 0.768 |
| with shock: top box height | 4.5 | 9.5 | 19.5 |
| with shock: largest overlap | 0 | 0 | 0 |

Without shock propagation, the boxes overlap and the stack loses about half of its height for $N = 20$. With it, the stack stays exactly at rest.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It uses the model of the code: boxes that translate only, with vertical normals. It shows:

- **Termination.** Every loop is finite, so the step ends after $O(n + e + (S + 1) I c)$ work once the graph is built.
- **Levels respect the graph.** Bodies in one component share a level, and every edge between components goes to a strictly higher level, because the components come out in a topological order.
- **Stacks give an acyclic graph.** For boxes with disjoint interiors, an edge $B \to A$ means that the bottom of $A$ lies above the top of $B$, so the graph has no cycle, and every contact has its upper body at a strictly higher level.
- **After the shock sweep, no contact approaches.** When level $\ell$ is solved, the bodies below are frozen, so each impulse only raises the velocity of a body of level $\ell$, and later levels cannot change it again. This holds for any number of contact sweeps before.
- **Nothing changes if nothing approaches.** The sweep then applies no impulse.

Not proved: the result for bodies that rotate, where another contact of the same body can lower the relative velocity again; any error bound for the contacts inside one strongly connected component; and any property of the contact sweeps before the shock sweep. The momentum example shows that the result is not the solution of the contact problem.

## Complexity

The strongly connected components and the levels take $O(n + e)$ time with [depth-first search](/depth-first-search/) for $n$ bodies and $e$ edges. Building the graph needs a collision query per moved body; the code of this page tests all pairs in $O(n^2)$, and an engine uses its broad phase. Each sweep resolves every contact $I$ times, so $S$ contact sweeps and one shock sweep cost $O((S + 1) I c)$ for $c$ contacts. Memory is $O(n + e + c)$.

## Properties

- A heuristic: it changes the physics by giving lower levels infinite mass (Guendelman, Bridson and Fedkiw 2003, Section 8.2).
- Stops a stack in one sweep, whatever its height, in the model of the proof.
- Does not conserve momentum, and the upper bodies do not press on the lower ones during the shock sweep.
- Depends on the direction of gravity, through the contact graph.
- The levels depend on the choice of $\Delta\tau$; a value that is too large finds edges between bodies that are not about to touch.

## Variants and improvements

- **Ramped restitution.** Guendelman, Bridson and Fedkiw run the contact sweeps with $\epsilon$ from $-0.9$ up to $0$, and the shock sweep on the last one (Section 8).
- **Propagation sweeps first.** In the paper, a large box dropped onto a plank resting on other bodies needs the ordinary sweeps to pass its weight down before the shock sweep; with shock propagation alone, the plank does not react as expected (Figure 6). Similarly, a see-saw with shock propagation alone sits still or tips slowly (Figure 7).
- **Velocity-based shock propagation.** Erleben (2007) uses shock propagation in a fixed time stepping scheme for velocity-based complementarity formulations, with an iterative solver tuned for multibody dynamics.
- **Warm starting instead.** Catto (2005) keeps the impulses of the last step, which also lets a stack of ten boxes stand with 10 iterations (Section 9.1). This changes the start of the iteration, not the masses.

## When to use it

Use it when stacks and piles must come to rest with a small budget of sweeps, in animation and games, and when a plausible result matters more than the forces between the bodies. Do not use it when the forces or the momentum must be right, for example for a see-saw, a balance, or a heavy body landing on a light one, or when there is no clear direction of support.

## Pitfalls

- **Freeze every level.** A level with no contacts of its own must still be frozen, or a body below can be pushed down by a contact above it. The code loops over all levels for this reason.
- **Restore the masses.** The infinite masses belong to one sweep only. Keep them in a separate list, as the code does, so that the next step uses the real masses.
- **Penetration breaks the graph.** If the bodies overlap, moving one down can touch a body above it, which adds edges in both directions and merges the stack into one component. In the run without shock propagation above, the largest level fell to 2 after the boxes sank.
- **Same level, no freezing.** Bodies in one component are solved only by the $I$ passes; a large ring of leaning bodies behaves like plain iteration.
- **Robotics conventions.** Pages such as [Stewart-Trinkle time stepping](/stewart-trinkle-time-stepping/) and [rigid contact complementarity](/rigid-contact-complementarity/) use $z$ up; this page uses $y$ up.

## Implementations

## History

Guendelman, Bridson and Fedkiw (2003) introduced the contact graph, its levels and shock propagation in their method for nonconvex rigid bodies with stacking, which separates collision, contact and the position update in each time step. They collapsed cycles of the graph into strongly connected components with two depth-first searches, the method of [Tarjan](/tarjan-scc/) being another way to find them. Erleben (2007) made shock propagation part of a velocity-based time stepping method for multibody animation.

## References

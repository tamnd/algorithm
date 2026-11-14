---
tag: 34KRY7
kind: algorithm
slug: soukup-algorithm
name: Soukup's algorithm
aliases:
- Soukup fast maze router
area: cad/routing
level: core
summary: A maze router that goes depth first toward the target and falls back to a breadth-first wave when blocked. It finds a path if one exists, but not always a shortest one.
solves: [graph-reachability]
model: word-ram
complexity:
  vars: {M: the number of rows of the routing grid, N: the number of columns}
  time: {worst: Θ(M N), best: Θ(1)}
  space: {extra: Θ(M N)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1978
  people: [J. Soukup]
  note: Soukup presented the fast maze router at the 15th Design Automation Conference in 1978. It mixes a depth-first run toward the target with Lee's breadth-first wave.
prereqs: [lee-maze-routing, depth-first-search]
see_also: [lee-maze-routing, hadlock-algorithm, line-probe-routing, breadth-first-search, depth-first-search, a-star-search, detailed-routing, rip-up-and-reroute]
sources:
  - paper: doi:10.1109/DAC.1978.1585154
    title: J. Soukup, Fast maze router, Proceedings of the 15th Design Automation Conference, 100 to 102, 1978
    locator: the search that runs toward the target until it is blocked and then expands a breadth-first wave (general locator)
  - paper: "C. Y. Lee, An algorithm for path connections and its applications, IRE Transactions on Electronic Computers EC-10(3), 346 to 365, 1961"
    locator: the breadth-first wave that Soukup's router uses when the direct run is blocked
  - paper: "Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, 3rd edition, Kluwer, 1999"
    locator: the section on Soukup's algorithm in the chapter on maze routing (general locator)
---

Soukup's algorithm is a fast maze router for electronic design automation (EDA). Like [Lee's algorithm](/lee-maze-routing/), it connects two cells of a routing grid around blocked cells, but it first runs straight at the target, depth first, and uses a breadth-first wave only to get around obstacles. Each cell is reached once. The router always finds a path when one exists, and on open grids it reaches the target after visiting little more than the cells of the path. The price is that the path need not be shortest.

## In plain words

Lee's router spreads out in all directions at once. That is safe, but slow when the goal is far away. Soukup's router walks straight at the goal and keeps going in the same direction as long as each step brings it nearer.

When the walk hits a wall, the router does not give up. It writes down all the squares next to the walk that go sideways or back, and it starts new walks from them. These new walks start one ring farther out, like the rings in Lee's router.

A square is never visited twice. So the router does a small amount of work and always finds a way when one exists. But the first walk that reaches the goal may have gone the wrong way around a wall, so the wire can be longer than needed.

## The problem

The input is a grid of $M$ rows and $N$ columns, where each cell is free or blocked, and two free cells $s$ and $t$. Moves go between free cells that share a side. The output is some path from $s$ to $t$, or the answer that no path exists. Unlike [Lee's algorithm](/lee-maze-routing/), Soukup's router does not promise a shortest path. For cells $u, v$ write $\mathrm{md}(u, v)$ for the Manhattan distance of their coordinates. A neighbor $v$ of $u$ is *toward* $t$ if $\mathrm{md}(v, t) < \mathrm{md}(u, t)$.

## The algorithm

```pseudo id=main
SOUKUP(grid, s, t)
L1  mark s as reached;  wave ← [s]
L2  while wave is not empty do
L3      next ← []
L4      for each cell c of wave do
L5          stack ← [c]
L6          while stack is not empty do
L7              u ← pop stack
L8              for each free neighbor v of u that is not reached do
L9                  mark v as reached;  parent(v) ← u
L10                 if v = t then return the path from s to t by the parent links
L11                 if v is toward t then push v on stack (the neighbor in the direction of the last step last, so it is popped first)
L12                 else add v to next
L13     wave ← next
L14 return "no path"
```

Lines L5 to L12 are the depth-first part: from a cell of the current wave, the search follows toward steps as far as it can, keeping its direction when possible. Line L12 is the breadth-first part: every neighbor that is not toward $t$ waits for the next wave. Textbook accounts describe the toward part as a run that keeps its direction until it reaches the target or an obstacle, and the fallback as Lee's expansion. This page gives the router in the form above, which keeps both parts and reaches each cell once.

## Example

Take a grid of 5 rows and 2 columns, rows and columns numbered from 0, with one blocked cell at $(1, 0)$. Let $s = (4, 1)$ and $t = (0, 0)$, so $\mathrm{md}(s, t) = 5$.

```
t .
# .
. .
. .
. s
```

The neighbors are tried in the order up, right, down, left. The search runs like this.

| step | cell popped | new neighbors | toward $t$ | next wave |
| --- | --- | --- | --- | --- |
| 1 | (4,1) | (3,1), (4,0) | both | |
| 2 | (4,0) | (3,0) | yes | |
| 3 | (3,0) | (2,0) | yes | |
| 4 | (2,0) | (2,1) | no, $\mathrm{md}$ grows from 2 to 3 | (2,1) |
| 5 | (3,1) | none | | |
| 6 | (2,1) | (1,1) | yes | |
| 7 | (1,1) | (0,1) | yes | |
| 8 | (0,1) | (0,0) = $t$ | stop | |

In step 1 both neighbors of $s$ are toward $t$. They are pushed in the order found, so $(4, 0)$ is popped first. The run goes up the left column until the blocked cell $(1, 0)$ stops it. The only way on is the step right to $(2, 1)$, which is not toward $t$, so it waits for the next wave. The cell $(3, 1)$ is then popped, but its only new neighbor would be $(2, 1)$, which is already reached. In the second wave, the run from $(2, 1)$ goes up the right column and left to $t$. The path found is

$(4,1), (4,0), (3,0), (2,0), (2,1), (1,1), (0,1), (0,0)$,

with 7 steps. The shortest path, straight up the right column and then left, has 5 steps. The search reached $(2, 1)$ first from $(2, 0)$, and since each cell is reached only once, the shorter way through $(3, 1)$ was lost.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Each cell once.** A cell is marked when it is first found and never again, so the parent links form a tree rooted at $s$.
- **Every reached cell is expanded.** A reached cell goes either on the stack, which is emptied before the wave ends, or into the next wave. So every reached cell is popped exactly once, unless the search stops at $t$.
- **Completeness.** If $t$ is reachable from $s$, it is reached: the reached set is closed under free neighbors when the waves run out, so it is the whole component of $s$.
- **Valid path.** The parent links of $t$ lead back to $s$ through neighbors, so the router returns a path.
- **Not shortest.** The example above has a path of 7 steps where 5 suffice.

## Complexity

- **Time.** Each cell is reached once and popped once, and each pop looks at 4 neighbors. So the time is $O(MN)$, and a maze that forces the search to visit every cell gives $\Theta(MN)$.
- **Space.** The marks and parents take $\Theta(MN)$ memory. The stack and the waves hold each cell at most once.
- **Open grid.** With no blockage, every step on a monotone path is toward $t$, and the search walks straight to $t$, visiting about $\mathrm{md}(s, t)$ cells and their neighbors.

## Properties

- **What is proved.** The router finds a path whenever one exists, and it visits each cell at most once. It does not promise a shortest path, and no bound on the extra length is known for general grids. The extra length can be large: a wall that the toward run follows into a dead end makes the path go around it.
- **What is measured.** On 16466 random grids with a path from $s$ to $t$ (sizes 2 to 8 on each side, 10 to 40 percent blocked cells, Python `random.Random(43)`), the path was longer than the shortest in 87 grids, with a mean ratio of 1.0015 and a worst ratio of 1.4. The search visited fewer cells than Lee's wave labeled in 15346 grids. These are toy inputs, not benchmark results.
- **Deterministic.** The result depends on the order of the neighbors and on the rule that keeps the direction of the last step.

## Variants and improvements

- **Straight runs only.** The toward part can be a straight run that never turns until it is blocked. The form on this page lets the depth-first part turn to another toward direction when the first one is blocked.
- **Keep the direction.** Preferring the neighbor in the direction of the last step gives paths with few bends, which matter for vias in two-layer routing.
- **Hadlock's order.** If a shortest path is needed, order the cells by detour number as in [Hadlock's algorithm](/hadlock-algorithm/). This costs a little more work but restores the guarantee.
- **Line probes.** [Line-probe routing](/line-probe-routing/) works with whole free segments instead of cells, and it trades the shortest path for less memory as well.

## When to use it

- To route many short connections quickly on a grid that is mostly open, where a short path is good enough.
- As a first try in a router, with Lee's or Hadlock's search kept for the nets where the path is too long.

When the length of each net matters, use [Lee's algorithm](/lee-maze-routing/) or [Hadlock's algorithm](/hadlock-algorithm/), which find shortest paths.

## Pitfalls

- **Claiming a shortest path.** The router is complete but not exact. Do not use its length as the distance between the pins.
- **Marking too late.** A cell must be marked when it is first found, on line L9, not when it is popped. Otherwise a cell can be put on the stack or in a wave many times, and the time bound is lost.
- **Forgetting the waves.** A depth-first run toward the target alone gets stuck behind a wall. The cells that are not toward the target must be kept for the next wave, or the router can fail on a grid that has a path.
- **Stopping at a label.** The search stops when it finds $t$ on line L10. There is no backtrace by labels, as in Lee's router, so the parent links must be kept.

## Implementations

## History

J. Soukup presented the "fast maze router" at the 15th Design Automation Conference in 1978. Lee's router (1961) was reliable but slow on large printed circuit boards, and Hadlock (1977) had sped it up while keeping shortest paths. Soukup gave up the shortest path and ran straight toward the target, using Lee's wave only when the direct run was blocked. The idea of a fast directed search with a breadth-first fallback appears in many later grid routers.

## References

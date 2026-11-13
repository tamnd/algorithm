---
tag: X5ZAVD
kind: algorithm
slug: d-star
name: "D*"
aliases:
- D star
- "Dynamic A*"
area: games-and-search/heuristic-search
level: advanced
summary: "Stentz's replanner for robots in unknown terrain: a backward search from the goal that, when arc costs change, sends RAISE and LOWER waves only through the states whose costs change."
solves: [single-pair-shortest-path]
model: word-ram
complexity:
  vars: {n: the number of states, m: the number of arcs, d: the largest number of neighbours of a state}
  time: {first-phase: "O((n + m) log n)", per-process-state: "O(d log n)"}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
prereqs: [dijkstra]
see_also: [d-star-lite, lifelong-planning-a-star, replanning, dynamic-single-source-shortest-paths, motion-planning, bug-algorithms, a-star-search, dijkstra]
sources:
  - paper: doi:10.1109/ROBOT.1994.351061
    title: Anthony Stentz, Optimal and efficient path planning for partially-known environments, Proceedings of the IEEE International Conference on Robotics and Automation (1994)
    locator: vol. 4, pp. 3310 to 3317; the functions PROCESS-STATE, MODIFY-COST and INSERT, the RAISE and LOWER states, Properties 1 to 3, and the experiments on a 50 by 50 eight-connected grid
  - paper: Anthony Stentz, The focussed D* algorithm for real-time replanning, Proceedings of the International Joint Conference on Artificial Intelligence (IJCAI 1995)
    title: Anthony Stentz, The focussed D* algorithm for real-time replanning, IJCAI 1995
    locator: pp. 1652 to 1659 (focussed D*, with a heuristic toward the robot and biased keys)
  - paper: Sven Koenig and Maxim Likhachev, D* Lite, Proceedings of the Eighteenth National Conference on Artificial Intelligence (AAAI 2002)
    title: Sven Koenig and Maxim Likhachev, D* Lite, AAAI 2002
    locator: pp. 476 to 483 (the comparison of D* Lite with focussed D*, and the uses of D* on outdoor robots)
---

D* moves a robot to a goal through terrain that is only partly known, and replans quickly each time the robot finds that an arc costs more or less than its map says. It computes the costs to the goal with a search that starts at the goal, as [Dijkstra's algorithm](/dijkstra/) does. When costs change, it does not search again. It puts the affected states back on the OPEN list and lets two kinds of waves run: RAISE waves carry cost increases to the states whose paths got worse, and LOWER waves carry cost decreases and new paths. The robot stops waiting as soon as its own state is correct. Anthony Stentz introduced it in 1994. The name means "dynamic A*".

## In plain words

You stand at the goal and write on every corner of the map how far it is from there, and an arrow that points to the next corner on the way. The robot reads its corner and follows the arrows.

When the robot finds a closed street, the numbers that used the street are now too small. You do not wipe the map. You take the corner at the end of the closed street and tell every corner whose arrow points into it that its number went up. Those corners tell the corners that point to them, and so on. Each corner that went up also looks around for a neighbour with a better number, and if it finds one, it turns its arrow to it. You do the corners in order of their old numbers, and you stop when the corner of the robot is right again.

## The problem

The map is a finite directed graph of *states*, usually the cells of a grid, with a goal state $G$ and the state $R$ of the robot. Each arc $Y \to X$ has a cost $c(Y, X)$, which is positive or $\infty$ for a blocked arc. The robot knows a map of the costs, and the costs of unknown arcs are set to an optimistic value. While it moves, its sensors give the true costs of arcs near it. The task is to move the robot to $G$, at each step along a shortest path of the current map, or to report that the map shows no path.

This page writes $c(Y, X)$ for the cost of moving from $Y$ to $X$. The 1994 paper writes $c(X, Y)$ for the cost of the arc from $Y$ to $X$, so its formulas have the arguments in the other order. On an undirected grid the two are the same.

## The algorithm

Each state $X$ has a tag $t(X)$, which is NEW, OPEN or CLOSED, a value $h(X)$, the cost of the path from $X$ to $G$ through the back pointers, a back pointer $b(X)$, and, while it is OPEN, a key $k(X)$. The key is the least value of $h(X)$ since $X$ was put on OPEN. An OPEN state with $k(X) < h(X)$ is a *RAISE* state: its cost went up, and it must pass this on. An OPEN state with $k(X) = h(X)$ is a *LOWER* state. OPEN is a priority queue ordered by $k$. MIN-STATE returns the state of least key, GET-KMIN returns the least key, and both return $-1$ when OPEN is empty.

```pseudo id=main
PROCESS-STATE()
L1  X ← MIN-STATE()
L2  if X = NULL then return −1
L3  k_old ← GET-KMIN(), DELETE(X)
L4  if k_old < h(X) then
L5      for each neighbour Y of X do
L6          if h(Y) ≤ k_old and h(X) > h(Y) + c(X, Y) then
L7              b(X) ← Y, h(X) ← h(Y) + c(X, Y)
L8  if k_old = h(X) then
L9      for each neighbour Y of X do
L10         if t(Y) = NEW or (b(Y) = X and h(Y) ≠ h(X) + c(Y, X)) or (b(Y) ≠ X and h(Y) > h(X) + c(Y, X)) then
L11             b(Y) ← X, INSERT(Y, h(X) + c(Y, X))
L12 else
L13     for each neighbour Y of X do
L14         if t(Y) = NEW or (b(Y) = X and h(Y) ≠ h(X) + c(Y, X)) then
L15             b(Y) ← X, INSERT(Y, h(X) + c(Y, X))
L16         else if b(Y) ≠ X and h(Y) > h(X) + c(Y, X) then
L17             INSERT(X, h(X))
L18         else if b(Y) ≠ X and h(X) > h(Y) + c(X, Y) and t(Y) = CLOSED and h(Y) > k_old then
L19             INSERT(Y, h(Y))
L20 return GET-KMIN()

INSERT(X, h_new)
L21 if t(X) = NEW then k(X) ← h_new
L22 else if t(X) = OPEN then k(X) ← min(k(X), h_new)
L23 else k(X) ← min(h(X), h_new)
L24 h(X) ← h_new, t(X) ← OPEN

MODIFY-COST(Y, X, c_new)
L25 c(Y, X) ← c_new
L26 if t(X) = CLOSED then INSERT(X, h(X))
L27 return GET-KMIN()

MAIN(R, G)
L28 t(X) ← NEW for every state X, INSERT(G, 0)
L29 repeat k_min ← PROCESS-STATE() until t(R) = CLOSED or k_min = −1
L30 while R ≠ G do
L31     if h(R) = ∞ then return "no known path"
L32     R ← b(R), and move the robot to R
L33     for each arc (Y, X) whose sensed cost c_new differs from the map do k_min ← MODIFY-COST(Y, X, c_new)
L34     while k_min ≠ −1 and k_min < h(R) do k_min ← PROCESS-STATE()
```

Lines L1 to L27 are the three functions of the 1994 paper, with the cost arguments in the order of this page. A neighbour is a state with an arc to $X$ or from $X$, and a missing arc has cost $\infty$.

- **The first phase** (line L29) is Dijkstra's algorithm from the goal: every state is NEW or LOWER, and it stops when the robot state is CLOSED.
- **A cost change** (line L26) puts the head $X$ of the changed arc back on OPEN with key $h(X)$. When $X$ comes off OPEN, it is a LOWER state, and lines L10 and L11 give each state that points to $X$ its new value. A state whose value goes up becomes a RAISE state with its old value as key.
- **A RAISE state** first tries to lower its value through a neighbour whose value is not more than its key (lines L5 to L7). These neighbours are final for now, because no state with a smaller key is on OPEN. If it is still RAISE, it passes the increase to its children (line L15). If a neighbour could get a better path through it, it goes back on OPEN as a LOWER state (line L17), so that the better path is sent later, in key order. If it could get a better path through a CLOSED neighbour, the neighbour goes back on OPEN (line L19).
- **The stop rule** (line L34). After a change, the robot processes states only until $k_{min} \ge h(R)$. States far from the robot can stay wrong. They are fixed later, when they matter.

## Example

The map is a 4-connected grid of 5 columns and 3 rows, with every move costing 1. The goal is $G = (4, 1)$ and the robot starts at $(0, 1)$. The cell $(2, 1)$ is blocked, but the robot does not know this.

**First phase.** D* processes 12 states in the order of their distance to $G$: $(4, 1)$ with key 0, then $(4, 0)$, $(3, 1)$ and $(4, 2)$ with key 1, $(3, 0)$, $(2, 1)$ and $(3, 2)$ with key 2, $(2, 0)$, $(1, 1)$ and $(2, 2)$ with key 3, and $(1, 0)$ and $(0, 1)$ with key 4. Now the robot state is CLOSED with $h = 4$, and its back pointers go straight along the middle row.

**The robot moves** to $(1, 1)$ and sees that $(2, 1)$ is blocked. The 8 arcs into and out of $(2, 1)$ get cost $\infty$. Line L26 puts the heads of these arcs on OPEN: $(3, 1)$ with key 1, $(2, 1)$ with key 2, and $(1, 1)$, $(2, 0)$ and $(2, 2)$ with key 3. The states $(1, 2)$, $(0, 0)$ and $(0, 2)$ are still on OPEN from the first phase, with keys 4, 5 and 5.

**Replanning.** D* processes 8 states.

| order | state | key | kind | what happens |
| --- | --- | --- | --- | --- |
| 1 | $(3, 1)$ | 1 | LOWER | $(2, 1)$ points to it through a blocked arc: $h(2, 1) \leftarrow \infty$, its key stays 2 |
| 2 | $(2, 1)$ | 2 | RAISE | its children $(1, 1)$ and $(2, 2)$ get $h = \infty$ |
| 3 | $(1, 1)$ | 3 | RAISE | its children $(0, 1)$ and $(1, 2)$ get $h = \infty$ |
| 4 | $(2, 2)$ | 3 | RAISE | finds $(3, 2)$ with $h = 2 \le 3$, points to it and lowers itself to 3; it is now LOWER and gives $(1, 2)$ the value 4 and a pointer to $(2, 2)$ |
| 5 | $(2, 0)$ | 3 | LOWER | no change |
| 6 | $(1, 2)$ | 4 | LOWER | gives $(1, 1)$ the value 5 and a pointer to $(1, 2)$ |
| 7 | $(0, 1)$ | 4 | RAISE | no neighbour helps; its child $(0, 2)$ gets $h = \infty$ |
| 8 | $(1, 0)$ | 4 | LOWER | no change |

Now the least key is 5 and $h(1, 1) = 5$, so line L34 stops. The back pointers from the robot give $(1, 1)$, $(1, 2)$, $(2, 2)$, $(3, 2)$, $(3, 1)$, $(4, 1)$, a shortest path of cost 5. Three states are still on OPEN with key 5: $(0, 0)$, $(0, 2)$ and $(1, 1)$ itself. The state $(0, 1)$, where the robot was, keeps the wrong value $\infty$ (its distance is now 6). D* fixes such values only if a later phase needs them.

**A measured experiment.** The grid is 50 by 50 and 8-connected, with each move to one of the 8 neighbours costing 1 and a diagonal move needing only its end cell to be free. Each cell is blocked with probability 0.3 (`random.Random(seed)` of Python), the robot starts at $(0, 0)$, the goal is $(49, 49)$, the robot knows nothing at the start and sees the 8 cells around it. At each position where it sees a change, D* replans, and for comparison Dijkstra's algorithm searches from scratch from the goal until it reaches the robot.

| seed | first phase | replanning phases | states processed in them | Dijkstra pops at the same points | moves | shortest true path |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2,500 | 46 | 203 | 34,986 | 58 | 57 |
| 2 | 2,500 | 47 | 246 | 37,743 | 63 | 57 |

These are measurements on two random maps, not bounds. The first phase processes all 2,500 cells, because D* without the focussing heuristic is a Dijkstra search, and the robot is in the far corner. After that, each replanning phase processes about 5 states on average. On the same maps, [D* Lite](/d-star-lite/), which searches with a heuristic, expands 50 states in its first call. The moves differ from those of D* Lite because ties are broken in another way.

## Correctness

The [proof](proofs/correctness.md) shows three invariants and derives the results from them.

- **Relaxed arcs.** For an arc $Y \to X$ into a CLOSED state, $h(Y) \le h(X) + c(Y, X)$ if $Y$ is CLOSED, and $k(Y) \le h(X) + c(Y, X)$ if $Y$ is OPEN.
- **Back pointers.** If $b(Y) = X$, then $h(Y) = h(X) + c(Y, X)$ when $X$ is CLOSED, and $k(X) < h(Y)$ when $X$ is OPEN. The back pointers never form a cycle. This is Property 1 of the paper, which calls such a chain monotonic.
- **The stop rule.** When $k_{min} \ge h(R)$, or OPEN is empty, the back pointers from $R$ give a path of cost $h(R)$, and the first invariant shows that no path is shorter. So $h(R)$ is the distance of the robot on the current map. This is Property 2 of the paper.
- **Termination.** In a phase, the keys taken from OPEN do not go down and a state comes back only with a larger key. The values are sums of arc costs, so the keys cannot stay bounded in an endless phase, and a count to infinity is not possible because the back pointers stay fixed once the keys pass the largest finite distance. So every phase stops. With an optimistic first map, the robot reaches the goal when it can be reached (Property 3 of the paper).

## Complexity

The model is the [word RAM](/word-ram/) with $n$ states, $m$ arcs and $d$ the largest number of neighbours of a state. OPEN is a [binary heap](/binary-heap/). One call of PROCESS-STATE looks at at most $d$ neighbours and does at most $d + 1$ insertions, so it takes $O(d \log n)$ time. In the first phase each state is processed at most once, so the phase takes $O((n + m) \log n)$ time, as Dijkstra's algorithm does. The space is $O(n)$ for the tags, values, keys and pointers, besides the map.

For a replanning phase, the proof shows that it stops, but it gives no polynomial bound on the number of PROCESS-STATE calls, and the paper gives none either. A state can be processed more than once in a phase. The gain over searching again is measured: in the experiment above, the replanning phases processed less than 1 percent of the states that Dijkstra's algorithm popped from scratch. The experiments of the 1994 paper also compare D* with replanning from scratch.

## Properties

- **Exact on the map.** When a phase stops, $h(R)$ is the distance of the robot on the current map and the back pointers give a shortest path.
- **Backward search.** The values are costs to the goal, so they stay valid when the robot moves. A move along a back pointer needs no work.
- **Lazy repair.** A phase stops when the robot state is right. Wrong values far from the robot wait on OPEN.
- **Increases and decreases.** RAISE states carry increases and LOWER states carry decreases, both in the same queue.
- **Not optimal in the true terrain.** The robot is optimal on the map it knows, but the walk can be longer than the shortest true path.
- **No heuristic in the basic version.** The first phase is a Dijkstra search. Focussed D* adds a heuristic toward the robot.

## Variants and improvements

- **Focussed D*.** Stentz (1995) adds a heuristic $g(X, R)$ from each state to the robot to the keys, so that the search focuses toward the robot as A* does. When the robot moves, the keys are biased by an accrued amount instead of being computed again. This is the version that is usually called D* in later papers.
- **D* Lite.** Koenig and Likhachev (2002) get the same robot behaviour from LPA* run backward, with one key and no RAISE and LOWER cases. They measured that it is at least as efficient as focussed D* on random grids. See [D* Lite](/d-star-lite/).
- **Field D*.** Ferguson and Stentz interpolate the values along cell edges, so that paths are not tied to the grid directions.
- **Large finite costs for obstacles.** Many uses of D* give an obstacle a large finite cost instead of $\infty$. Then every state stays reachable on the map, and a path through an obstacle means that there is no path.

## When to use it

D* is the historical starting point for replanning in robot navigation. For new code, [D* Lite](/d-star-lite/) gives the same moves of the robot with less code, one key and proofs that build on [LPA*](/lifelong-planning-a-star/). Use the D* family when a robot or a game unit must reach a fixed goal through terrain that it learns while it moves. When nothing changes, use [A*](/a-star-search/) once. When the start and the goal are fixed and only arc costs change, use LPA* or an algorithm for [dynamic shortest paths](/dynamic-single-source-shortest-paths/). Other uses of replanning are described in [replanning](/replanning/).

## Pitfalls

- **The order of the cost arguments.** The paper writes $c(X, Y)$ for the arc from $Y$ to $X$. On a directed map, a copy that reads it the usual way puts the wrong state on OPEN in MODIFY-COST. Put the head of the changed arc on OPEN.
- **Stopping too early or too late.** The first phase stops when the robot state is CLOSED. A replanning phase stops when $k_{min} \ge h(R)$. Running a replanning phase until OPEN is empty is correct but wastes the main gain.
- **Treating a RAISE state as LOWER.** Line L8 must test $k_{old} = h(X)$ after lines L4 to L7, because these lines can lower $h(X)$ to $k_{old}$.
- **Forgetting the tests on NEW states.** Lines L10 and L14 start with $t(Y) = $ NEW. Without them, the states that the first phase never reached stay unknown after a change.
- **Comparing $\infty$ values.** With $\infty$ costs, $\infty \ne \infty + c$ must be false. Floating point infinity does this right. A large integer for $\infty$ must be large enough that sums do not wrap.
- **Expecting the true shortest path.** D* is optimal for the map. The walk in unknown terrain can be longer.

## Implementations

## History

Stentz introduced D* at ICRA 1994 for robots that move through terrain that is partly known, and he chose the name because the algorithm is like A* except that it is dynamic: arc costs can change while it solves the problem. The paper tests it on 50 by 50 grids and gives short proofs of its three properties. In 1995, at IJCAI, he added focussing with a heuristic toward the robot. As the D* Lite paper states, D* was used on outdoor HMMWVs and on prototypes of Mars rovers. Koenig and Likhachev noted that focussed D* is complex and hard to analyze and extend, and in 2002 they gave D* Lite, which has the same behaviour and a simpler proof.

## References

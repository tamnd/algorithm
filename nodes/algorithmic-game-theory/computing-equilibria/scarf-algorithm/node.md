---
tag: E57190
kind: algorithm
slug: scarf-algorithm
name: Scarf's algorithm
aliases:
- Scarf simplicial algorithm
- simplicial fixed-point algorithm
area: algorithmic-game-theory/computing-equilibria
level: advanced
summary: Finds an approximate fixed point of a continuous map, or an approximate equilibrium, by path following on a simplicial subdivision.
solves: [nash-equilibrium-computation]
model: real-ram
complexity:
  vars: {d: the dimension of the simplex, N: the number of grid steps on each edge, M: "the number of grid points, binomial(N + d, d)", T: the number of pivots}
  time: {pivot: O(d M), worst: O(T d M)}
  space: {extra: O(d M)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1967
  people: [Herbert Scarf]
  note: Published in the SIAM Journal on Applied Mathematics as the first constructive method for approximate Brouwer fixed points, with a complementary pivot rule in the style of Lemke and Howson.
prereqs: [brouwer-fixed-point-theorem, sperner-lemma, nash-equilibrium, mixed-strategy]
see_also: [end-of-the-line-problem, ppad, lemke-howson-algorithm, ppad-completeness-of-nash, nash-existence-theorem, triangulation, homotopy-continuation, nash-equilibrium-computation]
sources:
  - paper: doi:10.1137/0115116
    title: "Herbert Scarf, The approximation of fixed points of a continuous mapping, SIAM Journal on Applied Mathematics 15(5) (1967), 1328-1343"
    locator: primitive sets, the replacement step and the approximate fixed point of a continuous map of the simplex
  - paper: doi:10.1137/0112033
    title: "C. E. Lemke and J. T. Howson, Jr., Equilibrium points of bimatrix games, Journal of the Society for Industrial and Applied Mathematics 12(2) (1964), 413-423"
    locator: the complementary pivot path that Scarf's method follows in a different setting
  - paper: doi:10.1145/1379759.1379761
    title: "Xi Chen and Xiaotie Deng, Matching algorithmic bounds for finding a Brouwer fixed point, Journal of the ACM 55(3) (2008), 13:1-13:26"
    locator: upper and lower bounds on the number of function values that any method of this kind needs, for each fixed dimension
  - paper: doi:10.1137/070699652
    title: "Constantinos Daskalakis, Paul W. Goldberg and Christos H. Papadimitriou, The complexity of computing a Nash equilibrium, SIAM Journal on Computing 39(1) (2009), 195-259"
    locator: the path-following argument behind Scarf's method as the defining problem of PPAD, and the hardness of approximate fixed points
---

Scarf's algorithm finds a point of the simplex that a continuous map moves only a little. By the [Brouwer fixed-point theorem](/brouwer-fixed-point-theorem/), such a map has a fixed point, and Scarf (1967) gave the first method that computes an approximation of it. The method puts a grid on the simplex, gives each grid point a label from the map, and follows a path of small sets of grid points from a fixed start until it reaches a set that carries every label. A set with every label is small, so the map moves all its points by a small amount. The same path argument proves the [Sperner lemma](/sperner-lemma/), and it is the model of the [END OF THE LINE](/end-of-the-line-problem/) problem that defines the class [PPAD](/ppad/). With labels from best responses, the method gives an approximate [Nash equilibrium](/nash-equilibrium/) of any finite game.

## In plain words

Think of a triangle covered by a fine grid of points. A rule moves each point to a new point of the triangle, and we want a point that stays almost where it is. Give each grid point a color: the color names a corner that the point does not move away from. A small group of points with all colors at once must sit next to a point that hardly moves. To find such a group, start in a corner with a group that misses one color. Trade one member of the group at a time, so that the group always keeps the other colors. Each trade has only one way forward, and the walk can never come back to a group that it saw before. So the walk must stop, and it stops at a group with all colors.

## The problem

Let $d \ge 1$ and let $\Delta_d = \{p \in \mathbb{R}^{d+1} : p \ge 0, \sum_i p_i = 1\}$ be the standard simplex, with coordinates $0, \dots, d$. The input is a map $f : \Delta_d \to \Delta_d$ that we can evaluate at any point, with a Lipschitz bound $\|f(p) - f(q)\|_\infty \le \lambda \|p - q\|_\infty$, and a target accuracy. The output is a point $p^*$ with $\|f(p^*) - p^*\|_\infty$ at most the target. On this page $N$ is the number of grid steps on each edge, so the grid points are the points $v/N$ where $v$ has $d + 1$ nonnegative integer entries with sum $N$.

For a finite game the same method gives an $\varepsilon$-Nash equilibrium. For a symmetric two-player game with a $k \times k$ payoff matrix $C$ with entries in $[0, 1]$, the row player gets $C_{rc}$ and the column player gets $C_{cr}$. A pair $(q, q)$ is an $\varepsilon$-Nash equilibrium if $\max_r (Cq)_r - q^{\mathsf T} C q \le \varepsilon$. Pure deviations are enough, because a mixed strategy is a [best response](/best-response/) if and only if its support is inside the set of pure best responses. Any finite game reduces to a fixed point of a continuous map, and a bimatrix game reduces to a symmetric game, so the symmetric case shows the main idea.

## The algorithm

The code uses the ordinal form of the method, with Scarf's primitive sets. There are $d + 1$ slack vectors $s_0, \dots, s_d$ and the grid points, and there is one strict order for each coordinate $i$:

- $s_i$ is the lowest vector in order $i$;
- next come all grid points, by the value of $p_i$, with ties broken by a fixed index;
- the slacks $s_j$ with $j \ne i$ come last, in the order of $j$.

A set $S$ of $d + 1$ vectors is **primitive** if no vector is above the lowest member of $S$ in every order at the same time. The member that is lowest in order $i$ **holds** order $i$, and in a primitive set each member holds exactly one order. Primitive sets play the part of the small simplices of a triangulation: their grid points differ by less than $(d + 1)/N$ in each coordinate. The slack $s_j$ has label $j$. A grid point $p$ has the least label $i$ with $f_i(p) \ge p_i$, and such an $i$ exists because $f(p)$ and $p$ both sum to 1. For a game, the label of $q$ is the least pure best response to $q$.

```pseudo id=main
SCARF(d, N, label)                    ▷ label maps each grid point to 0..d
L1  z ← e_0 ; P ← {s_1, ..., s_d, z}       ▷ e_0 is the grid point with p_0 = 1
L2  while label(z) ≠ 0
L3      y ← the member of P other than z with label(y) = label(z)
L4      Q ← P minus y ; a ← the order that y holds in P
L5      w ← the lowest member of Q in order a ; b ← the order that w holds in P
L6      z ← the highest vector in order b among the vectors u not in Q that are above the lowest member of Q in every order i ≠ b
L7      P ← Q plus z
L8  return P
```

Every set $P$ on the path has the labels $1, \dots, d$. If the new vector $z$ has label 0, then $P$ has all the labels and the loop ends. If not, the label of $z$ appears twice, and line L3 removes the old member with that label. Lines L4 to L6 compute the only vector $z \ne y$ that makes $Q$ plus $z$ primitive again. This is the replacement step: the member $w$ loses order $a$ to the new vector or keeps it, and the new member takes the order $b$ that $w$ held. It is the ordinal form of a pivot of the [Lemke-Howson algorithm](/lemke-howson-algorithm/).

## Example

Take $d = 2$, $N = 4$ and the cyclic map $f(p_0, p_1, p_2) = (p_1, p_2, p_0)$, which has the fixed point $(1/3, 1/3, 1/3)$ and Lipschitz constant 1. We write a grid point by its integer vector $v$, so $(3, 1, 0)$ means $(3/4, 1/4, 0)$. The point $(3, 1, 0)$ has $f = (1, 0, 3)$, so coordinates 0 and 1 go down and coordinate 2 goes up, and its label is 2.

| step | $P$ | labels | new vector $z$ | removed $y$ |
|---|---|---|---|---|
| 0 | $s_1, s_2, (4, 0, 0)$ | 1, 2, 1 | $(4, 0, 0)$ | $s_1$ |
| 1 | $s_2, (4, 0, 0), (3, 1, 0)$ | 2, 1, 2 | $(3, 1, 0)$ | $s_2$ |
| 2 | $(4, 0, 0), (3, 1, 0), (2, 1, 1)$ | 1, 2, 1 | $(2, 1, 1)$ | $(4, 0, 0)$ |
| 3 | $(3, 1, 0), (2, 1, 1), (1, 2, 1)$ | 2, 1, 0 | $(1, 2, 1)$ | stop |

After 3 pivots the set has the labels $\{0, 1, 2\}$. Its points $(3/4, 1/4, 0)$, $(1/2, 1/4, 1/4)$ and $(1/4, 1/2, 1/4)$ lie around the fixed point. On this coarse grid the bound of the theorem below, $2 \cdot 2 \cdot 3/4 = 3$, says nothing, but it goes to 0 as $N$ grows.

For a game, take rock-paper-scissors with payoff 1 for a win, $1/2$ for a tie and 0 for a loss. With $N = 6, 12, 24, 48$ the code returns the points $(1/6, 1/2, 1/3)$, $(1/4, 5/12, 1/3)$, $(7/24, 3/8, 1/3)$ and $(5/16, 17/48, 1/3)$ after 13, 25, 49 and 97 pivots. The gains are $1/6$, $1/12$, $1/24$ and $1/48$, so each time the grid doubles, the gain goes down by half.

## Correctness

Call a set of $d$ vectors a **door** if its labels are exactly $1, \dots, d$. The replacement step shows that every door lies in exactly two primitive sets, except the door $\{s_1, \dots, s_d\}$, which lies only in the start set. A primitive set with all labels has one door, and any other primitive set that has a door has two. So the primitive sets with a door form a graph in which every node has degree at most 2. The start set has degree 1 (or it is complete already), so the walk from it is a path. It cannot repeat a set, and there are finitely many sets, so it ends at a set with all labels. The same count shows that the number of completely labeled primitive sets is odd. This is the Sperner argument, and it is the reason why the search problem is in PPAD.

Next, every primitive set is small. Let $\delta = (d + 1)/N$. Any two grid points of a primitive set differ by less than $\delta$ in every coordinate, and if $s_j$ is in the set, its grid points have $p_j < \delta$. Now take any grid point $p^*$ of the output and let $g = f(p^*) - p^*$. For each $i$, label $i$ comes either from a grid point $q$ with $f_i(q) \ge q_i$, or from $s_i$ with $p^*_i < \delta$. In both cases $g_i > -(1 + \lambda)\delta$. Since the entries of $g$ sum to 0, also $g_i < d(1 + \lambda)\delta$. So

$$\|f(p^*) - p^*\|_\infty < \frac{d(1 + \lambda)(d + 1)}{N}.$$

For a symmetric game with labels from best responses, the same lemma gives that $(p^*, p^*)$ is a $2k^2/N$-Nash equilibrium. The [proof file](proofs/correctness.md) has the full proofs of the replacement step, the path, the size lemma and both bounds.

## Complexity

There are $M = \binom{N + d}{d}$ grid points. The code stores one rank array for each of the $d + 1$ orders, so the extra space is $O(d M)$. One pivot finds $a$, $w$ and $b$ in $O(d^2)$ steps, and it finds the new vector in one scan over all vectors with $O(d)$ comparisons each, so a pivot costs $O(d M)$. With $T$ pivots the time is $O(T d M)$. A real implementation does not scan: with the standard triangulations of Kuhn or Freudenthal, a pivot is a reflection of one vertex and costs $O(d)$ steps.

The number of pivots $T$ is the problem. The path visits only primitive sets, but it can visit a large part of them, and $M$ is exponential in $d$ for fixed accuracy. To reach accuracy $\varepsilon$ the grid needs $N$ of order $d^2(1 + \lambda)/\varepsilon$. Hirsch, Papadimitriou and Vavasis (1989) showed that every method that only evaluates the map needs a number of evaluations that is exponential in the dimension for some maps, and Chen and Deng (2008) gave matching upper and lower bounds for each fixed dimension. For games, the problem that the path solves is PPAD-complete ([PPAD-completeness of Nash](/ppad-completeness-of-nash/)), so no polynomial method is expected.

## Properties

- **Deterministic.** The path depends only on the orders and the labels, and the ties are broken by index.
- **Exact arithmetic is enough.** The code uses rational numbers, and a pivot needs only comparisons of coordinates and labels.
- **Only labels matter.** The walk uses the map only through the label of each new grid point, one evaluation for each pivot.
- **Approximate, not exact.** The output is a set of nearby grid points, and none of them needs to be close to an actual fixed point. It only satisfies $f(p^*) \approx p^*$.
- **Odd number of solutions.** The number of completely labeled primitive sets is odd, as in the Sperner lemma.

## Variants and improvements

- **Simplicial form.** Kuhn (1968) and Hansen and Scarf (1973) used a triangulation of the simplex and integer labels in place of primitive sets. The pivot then replaces one vertex of a small simplex by the reflection of that vertex, in $O(d)$ time.
- **Vector labels.** Each grid point can get a vector label in place of an integer, and the pivot is then a linear-programming pivot. The output is then a fixed point of a piecewise linear approximation of $f$.
- **Restarts and homotopy.** Eaves (1972) and Merrill (1972) started the path from a coarse grid and refined it on the way, or restarted from the last answer on a finer grid. This is the idea of [homotopy continuation](/homotopy-continuation/) on a grid.
- **Lemke-Howson.** For a bimatrix game the [Lemke-Howson algorithm](/lemke-howson-algorithm/) follows the same kind of path on the [best-response polytopes](/best-response-polytope/) and finds an exact equilibrium.
- **Scarf's lemma.** In the same year Scarf used primitive sets to prove that balanced games have a nonempty core, with the same pivot.

## When to use it

Use it when the map has no structure apart from continuity, and the dimension is small: a few coordinates, and a grid of moderate size. It is a good choice to teach the path argument, to test claims about Sperner labelings, and to find an approximate equilibrium of a small game with any number of players. For two-player games use Lemke-Howson or [support enumeration](/support-enumeration/), which give exact answers. For large dimensions use a method that exploits the structure of the map, because no method that only evaluates the map can be fast in general.

## Pitfalls

- **Ties in the orders.** The orders must be strict. If two grid points have the same coordinate and no tie rule, the replacement step is not unique and the walk can split or loop.
- **Labels on the boundary in the simplicial form.** The ordinal form with slacks accepts any labeling, because the slacks cover the faces. The simplicial form needs a Sperner labeling, in which a point with $p_i = 0$ never has label $i$. The rule "least $i$ with $f_i(p) \ge p_i$" does not have this property. There, use an $i$ with $p_i > 0$ and $f_i(p) \le p_i$, which exists because both vectors sum to 1.
- **Wrong member removed.** Line L3 must remove the old member with the repeated label, not the new one. Removing the new vector walks back along the path.
- **Grid too coarse.** The bound has the factor $d(d + 1)(1 + \lambda)/N$. With a small $N$ the output can be far from a fixed point, as in the example.
- **Reading the output as an exact fixed point.** A point with small $\|f(p) - p\|$ can be far from every fixed point when the map is nearly flat. Use a finer grid, or an exact method, if a point near a true fixed point is needed.

## Implementations

The Python code builds the orders of the grid as rank arrays and runs lines L1 to L8 in exact rational arithmetic. `approximate_fixed_point` labels points by the Brouwer rule, and `approximate_symmetric_equilibrium` labels points by the least pure best response. The tests list all primitive sets of small grids by brute force and check that each member holds one order, that each door lies in two primitive sets except the start door, and that random labelings give an odd number of complete sets with a path that stays primitive. They also check the cyclic example above, random stochastic linear maps against the bound, and rock-paper-scissors and chicken against the bound $2k^2/N$, with the shared exact checker for the gains.

## History

Lemke and Howson (1964) found the complementary pivot path for bimatrix games. Scarf (1967) used a path of the same kind to approximate fixed points of continuous maps, and in the same year to prove his lemma on the core of balanced games. Kuhn (1968) gave the simplicial form with integer labels, and Hansen and Scarf (1973) wrote it up for economic equilibrium models. Restart and homotopy methods followed in the 1970s. Hirsch, Papadimitriou and Vavasis (1989) showed exponential lower bounds for methods that only evaluate the map. Papadimitriou (1994) defined PPAD from the parity argument of this path, and Daskalakis, Goldberg and Papadimitriou (2006, 2009) and Chen, Deng and Teng (2006, 2009) showed that the problems it solves for games are PPAD-complete.

## References

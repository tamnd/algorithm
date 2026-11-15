---
tag: 19214B
kind: algorithm
slug: polyhedral-scanning
name: Polyhedral scanning
aliases:
- Quillere-Rajopadhye-Wilde algorithm
- polyhedral code generation
area: compilers-and-program-analysis/loop-transformations
level: research
summary: Generates loop nests that visit the integer points of a union of polyhedra in schedule order, by separating and projecting the polyhedra.
model: word-ram
complexity:
  vars: {n: the number of scanning dimensions, s: the number of statements, m: the largest number of constraints of a polyhedron the generator builds, P: the largest number of pieces at one level, L: the cost of one emptiness or implication test}
  time: {worst: O(s m P^(n+1) L)}
  space: {extra: O(m P^n)}
properties: {deterministic: true, recursive: true}
prereqs: [lexicographic-order, polyhedron, linear-programming-problem, simplex-method, fourier-motzkin-elimination, polyhedral-model]
see_also: [feautrier-scheduling, pluto-algorithm, loop-tiling, loop-fusion, loop-skewing, loop-interchange, unimodular-transformations, omega-test]
sources:
  - paper: doi:10.1145/109625.109631
    title: Corinne Ancourt and François Irigoin, Scanning polyhedra with DO loops, PPoPP 1991, 39-50
    locator: loop bounds for one polyhedron by Fourier-Motzkin elimination, as maxima and minima of rounded affine expressions
  - paper: doi:10.1023/A:1007554627716
    title: Fabien Quilleré, Sanjay Rajopadhye and Doran Wilde, Generation of efficient nested loops from polyhedra, International Journal of Parallel Programming 28(5), 2000, 469-498
    locator: the recursive algorithm for a union of polyhedra, with projection, separation into disjoint pieces and sorting at each level
  - paper: doi:10.1109/PACT.2004.1342537
    title: Cédric Bastoul, Code generation in the polyhedral model is easier than you think, PACT 2004, 7-16
    locator: scanning with scattering functions (schedules), the CLooG tool, and the control of code size by limiting separation
  - paper: doi:10.1145/2743016
    title: Tobias Grosser, Sven Verdoolaege and Albert Cohen, Polyhedral AST generation is more than scanning polyhedra, ACM TOPLAS 37(4), 2015
    locator: the AST generator of isl, with options for separation, unrolling and isolation of full tiles
---

Polyhedral scanning turns a set of polyhedra back into loops. A polyhedral compiler describes each statement by the integer points of its iteration domain and by a schedule that gives each point a time vector. After it changes the schedule, it must produce code that runs every point exactly once, in the lexicographic order of the time vectors. For one polyhedron, Ancourt and Irigoin (1991) found the loop bounds by [Fourier-Motzkin elimination](/fourier-motzkin-elimination/). For a union of polyhedra, one per statement, Quilleré, Rajopadhye and Wilde (2000) gave a recursive method: at each depth, project the polyhedra, split the projections into disjoint pieces, sort the pieces, and make one loop per piece. The CLooG tool of Bastoul (2004) and the code generator of isl are built on this method. It is the last step of every polyhedral compiler, after a scheduler such as [Feautrier's](/feautrier-scheduling/) or [Pluto](/pluto-algorithm/).

## In plain words

Picture each statement as a set of dots on graph paper, and the schedule as the order in which we must touch the dots: row by row, and left to right inside each row. To write a loop for the rows, we need the lowest and highest row that has a dot. To get them, we flatten the shape onto one axis, like a shadow. When several shapes overlap, some rows have dots of one statement and some rows have dots of both. So we cut the rows into stretches where the same statements are present. Each stretch gets its own loop, and the stretches run from left to right. Inside each loop we do the same for the next axis. The result has no tests inside the loops, and every dot is touched once, in the right order.

## The problem

**Input.** Integer parameters $N$ in a context $K$, and statements $S_1, \dots, S_s$. Statement $S$ has a domain $D_S$, a polyhedron given by affine inequalities in its loop counters $\vec{i}$ and $N$, bounded for each $N \in K$, and an affine schedule $\theta_S(\vec{i}) \in \mathbb{Z}^{m}$.

**Scanning space.** Each instance $S(\vec{i})$ becomes the point $x = (\theta_S(\vec{i}), \vec{i}, 0, \dots, 0)$ of $\mathbb{Z}^n$, with the counters padded to the largest depth. The set of these points is a polyhedron $Q_S$ in $(x, N)$: the domain, plus the equalities $x_k = \theta_{S,k}(\vec{i})$ and the zero padding. The schedule order is the lexicographic order of $(x, S)$, where the text position of $S$ breaks ties.

**Output.** A loop nest that, for every $N \in K$, runs every instance $S(\vec{i})$ with $\vec{i} \in D_S$ exactly once, in the [lexicographic order](/lexicographic-order/) of $(x, S)$, and nothing else.

**Loop bounds.** A constraint $a x_k + r(x_1, \dots, x_{k-1}, N) \ge 0$ with $a > 0$ is a lower bound $x_k \ge \lceil -r / a \rceil$, and with $a < 0$ an upper bound $x_k \le \lfloor r / (-a) \rfloor$. A loop runs $x_k$ from the maximum of its lower bounds to the minimum of its upper bounds.

## The algorithm

The generator is a recursive function of a list of polyhedra (each with the set of statements it stands for), a level $k$ and a context $C$, the constraints that hold at that depth of the code. It starts with the polyhedra $Q_S$, level 1 and the context $K$.

```pseudo id=main
SCAN(polyhedra Q_1..Q_s, context C, level k)
L1  for each Q_i: Q'_i <- the shadow of Q_i on (x_1..x_k, N), by Fourier-Motzkin elimination of x_n down to x_(k+1); drop the empty ones
L2  separate the Q'_i into disjoint pieces R_1..R_r, each labeled with the set of statements whose Q'_i contains it
L3  sort the pieces so that, of two pieces that exist for the same outer values, the one with the smaller x_k comes first
L4  if no such order exists then make one loop over x_k from the least lower bound to the largest upper bound, and run inside it the part of each piece that contains x_k
L5  for each piece R in this order do
L6      guards <- the constraints of R without x_k that C does not imply
L7      bounds <- the constraints of R with x_k, minus those that the others and C imply
L8      if k = n then body <- the statements of the label of R, in text order
L9      else body <- SCAN({Q_i intersect R : i in the label of R}, C and R, k + 1)
L10     emit "if guards then for x_k = max(lower bounds) to min(upper bounds): body"
```

**Fourier-Motzkin elimination.** To remove $x_j$, keep the constraints without $x_j$ and add, for each pair of a lower bound $a x_j + r \ge 0$ and an upper bound $-b x_j + q \ge 0$ (with $a, b > 0$), the combination $b r + a q \ge 0$. If $x_j$ appears in an equality, substitution is enough. The result is the rational shadow of the polyhedron. Each new constraint is divided by the greatest common divisor of its coefficients, and the constant is rounded down, which keeps the same integer points.

**Separation.** The pieces are built one polyhedron at a time. A new polyhedron $Q$ splits each old piece $R$ into $R \cap Q$ and the pieces of $R \setminus Q$, and what is left of $Q$ after all the old pieces becomes new pieces. The difference of two polyhedra is a union of polyhedra. With the constraints $q_1, \dots, q_t$ of $Q$, it is the disjoint union of

$$R \cap \{q_1 \ge 0, \dots, q_{j-1} \ge 0, q_j \le -1\}, \qquad j = 1, \dots, t,$$

where $q_j \le -1$ is the integer complement of $q_j \ge 0$. Empty pieces are dropped. The emptiness tests and the tests "does $C$ imply $g \ge 0$" are linear programs, solved here with an exact [simplex method](/simplex-method/) over integer rows.

**Sorting.** Two pieces always differ by one constraint $g$: one has $g \ge 0$ and the other $g \le -1$. If $g$ contains $x_k$, this fixes their order along $x_k$ for all outer values. If it does not, the two pieces never exist for the same outer values. So pairs are either ordered or independent, and the test of line L3 is a pair of linear programs: "is there a point of $A$ and a point of $B$ with the same outer values and $a_k \ge b_k$?". A topological sort of this relation gives the order. Line L4 is a safety net of this implementation in case the relation has a cycle. It never fires on the tests.

## Example

**A triangle, interchanged.** The nest `for i = 0 to N: for j = 0 to i: S(i, j)` with the schedule $(j, i)$ has $t_1 = j$ and $t_2 = i$, so its points satisfy $0 \le t_1 \le t_2 \le N$. Eliminating $t_2$ pairs the lower bound $t_2 \ge t_1$ with the upper bound $t_2 \le N$, and gives $0 \le t_1 \le N$. The generator prints

```
for t1 = 0 to N:
  for t2 = t1 to N:
    i1 = t2
    i2 = t1
    S(i1, i2)
```

The last two lines are loops with a single iteration, from the equalities $i_1 = t_2$ and $i_2 = t_1$.

**Two statements, fused.** Let $S_1$ run on $0 \le i \le N$ and $S_2$ on $2 \le i \le N + 2$, with the schedules $(i, 0)$ and $(i, 1)$, a [fusion](/loop-fusion/) of two loops. At level 1 the shadows are the two ranges. Separation gives three pieces: $S_1$ alone on $0 \le t_1 \le \min(N, 1)$, both on $2 \le t_1 \le N$, and $S_2$ alone on $\max(2, N + 1) \le t_1 \le N + 2$. Inside the middle piece, level 2 separates $t_2 = 0$ from $t_2 = 1$. The output is

```
for t1 = 0 to min(N, 1):
  t2 = 0
  i1 = t1
  S1(i1)
for t1 = 2 to N:
  t2 = 0
  i1 = t1
  S1(i1)
  t2 = 1
  i1 = t1
  S2(i1)
for t1 = max(2, N + 1) to N + 2:
  t2 = 1
  i1 = t1
  S2(i1)
```

There is no test inside any loop. For $N = 0$ the middle loop is empty and the last one runs $t_1 = 2$, as it should.

**A skewed stencil.** For `for t = 0 to N: for i = 1 to N: S(t, i)` with the [skewed](/loop-skewing/) schedule $(t, t + i)$, the generator gives `for t1 = 0 to N: for t2 = t1 + 1 to t1 + N:` with $i_2 = t_2 - i_1$ inside, under the guard $N - 1 \ge 0$, which the context $N \ge 0$ does not imply.

## Correctness

The full proof is in [the proof page](proofs/correctness.md). It rests on four facts about the pieces at one level, for fixed values of the outer dimensions and the parameters.

- **Cover.** Every integer point of every $Q_S$ has its first $k$ coordinates in the shadow $Q'_S$, and so in some piece. Separation keeps every integer point of the union, because a point outside $Q$ breaks some $q_j \ge 0$ and so has $q_j \le -1$.
- **Disjointness.** Two pieces have no integer point in common, so no point is visited twice.
- **Labels.** If a point of $Q_S$ lies in the piece $R$, then $S$ is in the label of $R$, so the body of $R$ contains $S$.
- **Order.** Inside one loop $x_k$ grows, and the sorted pieces visit increasing $x_k$ for the same outer values. By induction on $k$, the whole nest visits the points in lexicographic order.

At the last level, a piece lies inside $Q_S$ for each $S$ of its label, so a statement runs only at points of its domain.

## Complexity

Fourier-Motzkin elimination of one variable can square the number of constraints, so $m$ can grow doubly exponentially with $n$ in the worst case. The implementation removes redundant constraints with linear programs to keep $m$ small. Separation of $s$ polyhedra can make a number of pieces $P$ that is exponential in $s$. The generator calls itself at most $P$ times per piece and level, so it makes $O(P^{n-1})$ calls. Each call separates at most $s$ shadows against at most $P$ pieces, with $O(P m)$ tests each, and sorts with $O(P^2)$ tests. The total is $O(s m P^{n+1})$ tests of cost $L$, and the code holds $O(P^n)$ loops of $O(m)$ constraints each. In practice, for the loops of real programs, $P$ and $m$ stay small, and the size of the code is the main concern.

## Properties

- **No tests inside the loops.** Each loop has exact bounds. Guards appear only where a piece does not exist for all outer values, and they sit outside the loop they guard.
- **Rational shadows.** The shadow from Fourier-Motzkin elimination is the rational one. For a polyhedron with a non-unimodular schedule, such as $t = 2i$, the loop over $t$ also visits odd values, where the inner loop over $i$ is empty. The output is still correct, but it does wasted work.
- **Code size.** Separation can duplicate a statement many times, once per piece that contains it.
- **Deterministic.** The pieces and their order depend only on the input order of the statements and constraints.

## Variants and improvements

- **Strides.** CLooG and isl detect equalities such as $t = 2i$ and turn them into loop steps, `for t = 0 to 2N step 2`, instead of empty iterations.
- **Limits on separation.** Bastoul's CLooG can stop separation below a given depth and use guards there, which trades a few tests for much smaller code. isl lets the user choose separation, isolation of full tiles, or unrolling per loop.
- **Exact integer shadows.** The projection of the [omega test](/omega-test/) is exact on integers, as a union of polyhedra, and so avoids the empty iterations of rational shadows at the cost of more pieces.
- **Tiled code.** A tiled schedule uses $\lfloor \phi / \tau \rfloor$, which is not affine. Code generators add a tile counter $T$ with $\tau T \le \phi \le \tau T + \tau - 1$ and scan the larger polyhedron.

## When to use it

Use polyhedral scanning whenever loops must be produced from a polyhedral description: after an affine scheduler, for [loop tiling](/loop-tiling/) with parametric bounds, or to rewrite a nest under a [unimodular transformation](/unimodular-transformations/). For one perfect nest and a unimodular change, Fourier-Motzkin bounds alone are enough. For many statements with different domains, separation avoids tests in the inner loops.

## Pitfalls

- **Affine programs only.** The domains, schedules and context must be affine in the counters and the parameters. Data-dependent bounds or subscripts leave the model.
- **A legal schedule can still give slow code.** Scanning makes the code follow the schedule, but separation can blow up the code size, and many small pieces near the borders cost branch and loop overhead.
- **Integer holes.** A rational shadow can contain integer values with no integer point above them. Without stride detection, the code runs empty loops there.
- **Context matters.** If the context of the parameters is too weak, the generator emits guards and pieces for parameter values that never occur, as in the guard $N - 1 \ge 0$ of the stencil example.
- **Ties.** Points of two statements with the same time vector run in text order. If the schedule is not one to one, the counters themselves decide the order, which must then be legal too.

## Implementations

## History

Ancourt and Irigoin (1991) gave a general method to scan one polyhedron with DO loops, using Fourier-Motzkin elimination for the bounds. Quilleré, Rajopadhye and Wilde (2000) gave the recursive separation algorithm, which produces code with no redundant tests inside loops. Bastoul (2004) extended it to general schedules and made it practical in CLooG, used by many polyhedral tools, including Pluto. Grosser, Verdoolaege and Cohen (2015) described the AST generator of isl, which handles the same problem with more options for code size.

## References

---
tag: CVQVJX
kind: algorithm
slug: arora-euclidean-tsp-ptas
name: Arora's PTAS for Euclidean TSP
aliases:
- Arora PTAS for Euclidean TSP
- Arora's TSP scheme
- Arora's approximation scheme
- Arora-Mitchell PTAS
area: approximation/tsp-approximation
level: advanced
summary: A randomized scheme with expected ratio 1 + 1/c for Euclidean TSP; a shifted quadtree, portals and patching reduce the problem to a dynamic program over the squares.
solves: [euclidean-tsp]
model: real-ram
complexity:
  vars: {n: the number of points, c: "the accuracy parameter (the ratio is 1 + 1/c)"}
  time: {expected: n (log n)^O(c)}
  space: {extra: n (log n)^O(c)}
properties: {deterministic: false, recursive: true, online: false}
history:
  year: 1996
  people: [Sanjeev Arora]
  note: Arora gave the scheme at FOCS 1996 and a nearly linear version at FOCS 1997; the journal paper of 1998 has both, and Mitchell found a scheme independently.
prereqs: [euclidean-tsp, quadtree, ptas, linearity-of-expectation]
see_also: [portal-based-dissection, mitchell-euclidean-tsp-ptas, mitchell-guillotine-ptas, euclidean-tsp, quadtree, arora-euclidean-k-median-ptas, ptas, christofides-algorithm]
sources:
  - paper: doi:10.1145/290179.290180
    title: Sanjeev Arora, Polynomial time approximation schemes for Euclidean traveling salesman and other geometric problems, Journal of the ACM 45(5), 1998
    locator: pages 753 to 782 (the perturbation, the shifted dissection, portals, the patching lemma, the structure theorem and the dynamic program)
  - title: Satish B. Rao and Warren D. Smith, Approximating geometrical graphs via spanners and banyans, Proceedings of the 30th ACM Symposium on Theory of Computing, 1998
    locator: the O(n log n) scheme for fixed c and fixed dimension
  - title: Yair Bartal and Lee-Ad Gottlieb, A linear time approximation scheme for Euclidean TSP, Proceedings of the 54th IEEE Symposium on Foundations of Computer Science, 2013
    locator: the linear time randomized scheme
---

Arora's scheme is a [PTAS](/ptas/) for the [Euclidean TSP](/euclidean-tsp/): for each fixed $c > 1$ it finds a tour of expected length at most $(1 + 1/c) \cdot$ OPT in time $n (\log n)^{O(c)}$ in the plane. It moves the points to a grid, cuts the plane by a [quadtree](/quadtree/) with a random shift, and puts $m = O(c \log n)$ *portals* on each side of each square. The structure theorem says that some tour that crosses each side only at portals, and at most $r = O(c)$ times, is within $1 + 1/c$ of OPT in expectation over the shift. A dynamic program over the squares then finds the best such tour. The method is called [portal-based dissection](/portal-based-dissection/), and it works for many other geometric problems.

## In plain words

Draw a big square around the cities. Cut it into four squares, and each of those into four, until each small square holds at most one city. Move the whole grid of cuts by a random amount first.

On each side of each square, mark a few gates. Now look only at tours that pass from one square into the next through gates, and only a few times per side.

The best tour of that kind is a little longer than the best tour, because it must bend to the gates. The random move makes it unlikely that a long road meets a big cut, where the gates are far apart. Then a table of best partial tours for each square and each way of using its gates, built from the small squares up, finds the best tour of that kind.

## The problem

The input is a set $P$ of $n$ points in the plane with the Euclidean distance and a number $c > 1$. The output is a tour of $P$. OPT is the length of a shortest tour and ALG is the length of the returned tour. The convention is ALG $\le \rho \cdot$ OPT for a minimization problem, and here $\rho = 1 + 1/c$ for the expected value of ALG over the random shift. The same scheme works in $\mathbb{R}^d$ for fixed $d$.

## The algorithm

```pseudo id=main
ARORA-TSP(P, c)
L1  move the points to a grid of spacing δ = L0 / (8cn), scale by 1 / δ; L = a power of 2 above every coordinate
L2  pick a shift (a, b) uniformly from {0, ..., L - 1}^2
L3  build the quadtree of the shifted square of side 2L until each square holds at most one point
L4  put m = O(c log L) portals on each side of each square, and allow r = O(c) crossings per side
L5  find the best portal-respecting tour with at most r crossings per side by dynamic programming over the squares
L6  shortcut the tour to an order of the points and return it
```

Here $L_0$ is the larger side of the bounding box. On line L5, a subproblem is a square together with an *interface*: at most $r$ portals on each side and a pairing of them. Its value is the least cost of a set of paths inside the square that visits all its points and joins the portals as the pairing says. The value of a square comes from the values of its four children whose interfaces agree on the shared sides.

**What the code covers.** The code implements lines L1 to L4 and L6, with $m$ the least power of 2 with $m \ge 2\sqrt{2}\, c \log_2(2L)$. It does not implement the dynamic program, and it does not limit the crossings to $r$. In their place it takes, by brute force over all orders, the order with the least grid length plus the cost of moving its crossings to portals. This keeps the expected ratio $1 + 1/c$, proved in the proof file, but takes exponential time. The tests check the lemmas on which the ratio rests, exactly over all $L^2$ shifts.

## Example

Take the seven cities of the [3-opt](/three-opt/) page, $A(1,2)$, $B(0,5)$, $C(3,3)$, $D(1,0)$, $E(0,0)$, $F(3,4)$ and $G(2,6)$, and $c = 1$. OPT is the tour $A\,E\,D\,C\,F\,G\,B$ of length 15.476.

1. **The grid.** $L_0 = 6$, so $\delta = 6/56 = 0.107$. The points become $(9, 19)$, $(0, 47)$, $(28, 28)$, $(9, 0)$, $(0, 0)$, $(28, 37)$ and $(19, 56)$, so $L = 64$ and the dissection square has side 128 and depth 7.
2. **The portals.** $2\sqrt{2} \cdot 7 = 19.8$, so $m = 32$ portals per side.
3. **The quadtree.** For the shift $(0, 0)$ it has 12 non-empty squares and depth 4.
4. **Moving to portals.** In grid units, OPT has length 144.32 and crosses 186 grid lines. For the shift $(0, 0)$, moving its crossings to portals costs 8.62. Over all 4096 shifts the average cost is 11.02, which is 7.6 percent of its length. The proved bound is $186 \cdot 7/32 = 40.69$.
5. **The choice.** The tour $A\,C\,F\,G\,B\,E\,D$ has grid length 147.07 but portal cost only 5.65, so its sum 152.72 is less than $144.32 + 8.62 = 152.94$. The code returns it. Its true length 15.708 is 1.015 times OPT, well inside the ratio 2.

**Measured behavior.** The portal cost on these small inputs is much smaller than the bound, as in step 4. The scheme is of theoretical interest: the constants in $(\log n)^{O(c)}$ make it slower than [2-opt](/two-opt/) or [Lin-Kernighan](/lin-kernighan/) in practice, and those local searches give better tours on typical inputs. These are observations, not bounds.

## Correctness

**Theorem.** In the plane, for each $c > 1$, the tour of the scheme has expected length at most $(1 + 1/c) \cdot$ OPT, and the running time is $n (\log n)^{O(c)}$.

The proof has three steps.

1. **The grid step.** Moving each point by at most $\delta / \sqrt{2}$ changes each tour by at most $\sqrt{2}\, n \delta \le \frac{\sqrt{2}}{16c}$ OPT, because OPT $\ge 2 L_0$.
2. **The portal lemma.** A grid line has level $i$, the depth of the largest square whose side it holds, with probability at most $2^{i-1} / L$, and at that level the portals are $2L / (2^i m)$ apart. So moving one crossing to a portal costs at most $\log_2(2L) / m$ in expectation. A tour crosses grid lines at most $\sqrt{2}$ times its length, so the total is at most $|H| / (2c)$.
3. **Patching and the dynamic program.** If a side is crossed more than $r$ times, adding segments of length at most 3 times the side cuts the crossings to 2. The expected cost of this over all sides is $O(\text{OPT}/r)$. The dynamic program then has $(\log n)^{O(c)}$ interfaces per square.

The full proof is in the proof file. Steps 1 and 2, which give the ratio of the code, and the patching lemma are proved in full. The rest of step 3, the bound on the cost of patching and the count of interfaces, is a sketch of Arora's proof.

**With high probability.** By [Markov's inequality](/markov-inequality/) the extra cost is at most twice its mean with probability at least 1/2. So repeating the scheme with fresh shifts gives ratio $1 + 2/c$ with high probability. Trying all $L^2$ shifts gives a deterministic scheme.

**Lower bounds.** The Euclidean TSP has no FPTAS unless P = NP, by the reduction from Hamiltonian cycles in grid graphs on the [Euclidean TSP](/euclidean-tsp/) page. So no scheme has a time polynomial in both $n$ and $c$ unless P = NP. When the dimension grows like $\log n$, the problem is APX-hard (Trevisan 2000).

**Hardness.** For general metric costs no polynomial algorithm has a ratio below $123/122$ unless P = NP (Karpinski, Lampis and Schmied 2015; see [metric TSP inapproximability](/metric-tsp-inapproximability/)), so the geometry is what makes a PTAS possible. Without the triangle inequality no constant ratio is possible unless P = NP ([general TSP inapproximability](/general-tsp-inapproximability/)).

## Complexity

- **The grid and the quadtree.** $O(n \log n)$ time; the quadtree has depth $O(\log n)$ and $O(n \log n)$ non-empty squares.
- **Interfaces.** At most $r$ of the $m + 4$ portals per side and a non-crossing pairing give $(m + 4)^{4r} \cdot 2^{O(r)} = (\log n)^{O(c)}$ interfaces per square.
- **The dynamic program.** $(\log n)^{O(c)}$ time per square, so $n (\log n)^{O(c)}$ in total.
- **Dimension $d$.** Arora gives $n (\log n)^{(O(\sqrt{d}\, c))^{d-1}}$.
- **Faster schemes.** Rao and Smith (1998) gave $O(n \log n)$ time for fixed $c$ and $d$, and Bartal and Gottlieb (2013) a linear time randomized scheme.
- **The code.** $O(n! \cdot n L)$ time, for checking only.

## Properties

- **Randomized.** The ratio holds in expectation over the shift, for every input; no input is bad for most shifts.
- **Only the geometry matters.** The proof uses the quadtree, the fact that a segment crosses few grid lines, and the patching lemma. The same plan gives schemes for the Steiner tree, $k$-median and other problems; see [Arora's $k$-median scheme](/arora-euclidean-k-median-ptas/).
- **Time in $c$.** The factor $(\log n)^{O(c)}$ grows very fast with $c$, so the scheme is of use only for small $c$, even in theory. The schemes of Rao and Smith separate the dependence on $c$ from the factor $n \log n$.

## Variants and improvements

- **[Mitchell's scheme](/mitchell-euclidean-tsp-ptas/).** Found at the same time, it uses [guillotine subdivisions](/mitchell-guillotine-ptas/) instead of portals, and it is deterministic, with time $n^{O(c)}$.
- **The first version.** Arora's FOCS 1996 paper had time $n^{O(c)}$. The FOCS 1997 paper reached $n (\log n)^{O(c)}$.
- **Rao and Smith.** Spanners and banyans give $O(n \log n)$ time for fixed $c$ and $d$.
- **Other norms and problems.** Other fixed $\ell_p$ norms, the Steiner tree, $k$-TSP, $k$-MST and min-cost $k$-connected subgraphs.

## When to use it

Use the scheme when you need a proof that a Euclidean instance can be approximated within any fixed factor, or as a pattern for a new geometric scheme. For real tours use [Lin-Kernighan](/lin-kernighan/) or [LKH](/lin-kernighan-helsgaun/), which are faster and give better tours in practice without a guarantee, or [Christofides](/christofides-algorithm/) for a guarantee of 1.5.

## Pitfalls

- **Forgetting the grid step.** Without it, the quadtree can be very deep and $L$ is not bounded by a polynomial in $n$.
- **No random shift.** A fixed dissection fails: a tour edge can cross the middle line, where portals are far apart, many times. The shift makes such lines rare.
- **Portals that do not nest.** If the portals of a square are not portals of its children, a tour cannot pass through them consistently. Choose $m$ and the sides as powers of 2.
- **Mixing the ratio.** The ratio is $1 + 1/c$ in expectation; one run can be worse.
- **Counting pairings.** All pairings give $(4r)!$ per interface; the bound $(\log n)^{O(c)}$ needs the non-crossing pairings.

## Implementations

## History

Arora found the scheme in 1996, with time $n^{O(1/\varepsilon)}$, and in 1997 a version in nearly linear time. The journal paper of 1998 gives both. Mitchell found a scheme independently with guillotine subdivisions, and the two shared the Gödel Prize in 2010. Rao and Smith (1998) improved the time to $O(n \log n)$, and Bartal and Gottlieb (2013) to linear time.

## References

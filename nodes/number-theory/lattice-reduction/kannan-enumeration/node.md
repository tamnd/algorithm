---
tag: NY4D49
kind: algorithm
slug: kannan-enumeration
name: Kannan enumeration
aliases:
- Kannan's SVP algorithm
- Kannan's algorithm
- Kannan's HKZ algorithm
- Kannan-Helfrich enumeration
area: number-theory/lattice-reduction
level: research
summary: Enumeration with preprocessing that solves SVP in n^O(n) time.
solves: [shortest-vector-problem]
model: word-ram
complexity:
  vars: {n: the rank of the lattice, m: the length of the vectors, s: the size of the input basis, e: the base of the natural logarithm, about 2.718}
  time: {worst: n^(n/(2e) + o(n)) s^(O(1)), kannan_1983_analysis: n^(O(n)) s^(O(1)), cvp_variant: n^(n/2 + o(n)) s^(O(1))}
  space: {extra: O(n^2 + n m)}
properties: {deterministic: true, recursive: true, exact: true, polynomial_space: true}
history:
  year: 1983
  people: [Ravi Kannan, Bettina Helfrich, Guillaume Hanrot, Damien Stehlé]
  note: Kannan gave the algorithm in 1983 for integer programming; Helfrich improved the analysis to n^(n/2) in 1985, and Hanrot and Stehlé to n^(n/(2e)) in 2007.
prereqs: [hkz-reduction, fincke-pohst-enumeration, lll-algorithm, shortest-vector-problem]
see_also: [lattice-enumeration, schnorr-euchner-enumeration, bkz-algorithm, gauss-sieve, closest-vector-problem, hermite-constant, gram-schmidt-orthogonalization, lattice-sieving]
sources:
  - paper: "R. Kannan, Improved algorithms for integer programming and related lattice problems, Proceedings of the 15th ACM Symposium on Theory of Computing (STOC 1983)"
    locator: pages 193 to 206 (the recursive HKZ algorithm with enumeration and its use for integer programming)
  - paper: "R. Kannan, Minkowski's convex body theorem and integer programming, Mathematics of Operations Research 12(3) (1987)"
    locator: pages 415 to 440 (the full version, with the n^(O(n)) analysis)
  - paper: "B. Helfrich, Algorithms to construct Minkowski reduced and Hermite reduced lattice bases, Theoretical Computer Science 41 (1985)"
    locator: pages 125 to 139 (the improved bound n^(n/2 + o(n)))
  - paper: "G. Hanrot and D. Stehlé, Improved analysis of Kannan's shortest lattice vector algorithm, CRYPTO 2007, LNCS 4622"
    locator: the bound n^(n/(2e) + o(n)) for SVP and n^(n/2 + o(n)) for CVP, through the number of enumeration nodes on a quasi-HKZ basis
  - paper: "G. Hanrot and D. Stehlé, Worst-case Hermite-Korkine-Zolotarev reduced lattice bases, arXiv:0801.3331 (2008)"
    locator: HKZ-reduced bases on which enumeration needs n^(n/(2e) - o(n)) nodes, so the analysis is tight
---

Kannan's algorithm finds a shortest vector of a [lattice](/lattice/), and more: an [HKZ-reduced](/hkz-reduction/) basis. It is [enumeration](/lattice-enumeration/) of the lattice points in a ball, run on a basis that was first made almost HKZ-reduced by calling the algorithm recursively on the projected lattice of rank $n - 1$. That preprocessing makes the enumeration tree small: Kannan proved a bound $n^{O(n)}$ in 1983, and Hanrot and Stehlé sharpened it in 2007 to $n^{n/(2e) + o(n)}$ operations, times a polynomial in the input size, which remains the reference bound for polynomial-space algorithms for the [shortest vector problem](/shortest-vector-problem/).

## In plain words

To find the shortest arrow of a grid, one can list every grid point inside a ball and keep the shortest. That listing is fast when the arrows that describe the grid are already good, and very slow when they are bad.

Kannan's idea is to make the arrows good first, and to use the same method for it. Flatten the grid along the first arrow, so that one dimension disappears. Solve the smaller problem completely, by the same method, to get the best possible arrows for the flattened grid. Then the first arrow is either already fine, or it is much too long, and swapping it with the second arrow halves it. Once the first arrow is no more than twice the second, list the ball. Its radius is now small compared to the arrows, so the list is short.

## The problem

**Input.** Linearly independent rows $b_1, \ldots, b_n \in \mathbb{Q}^m$ of a lattice $L$.

**Output.** An **HKZ-reduced** basis of $L$: size-reduced, $|\mu_{ij}| \le 1/2$, and $\|b_k^*\| = \lambda_1(\pi_k(L))$ for every $k$, where $\pi_k$ projects orthogonally to $b_1, \ldots, b_{k-1}$. In particular $\|b_1\| = \lambda_1(L)$, so the first row solves SVP.

**Notation and cost model.** As on the other pages of this area, basis vectors are rows $b_1, \ldots, b_n$, $b_i^*$ and $\mu_{ij}$ are the [Gram-Schmidt](/gram-schmidt-orthogonalization/) data, $N_i = \|b_i^*\|^2$, $\lambda_1$ is the first minimum, $\det(L)$ is the determinant and $\delta$ is the LLL parameter, here $\delta = 3/4$. The reference implementation uses exact rational arithmetic. Time counts arithmetic operations; the bounds $n^{O(n)}$, $n^{n/2 + o(n)}$ and $n^{n/(2e) + o(n)}$ are proved for this count, and the operands have size polynomial in the input size, so the bit complexity is the same times a polynomial. Nothing on this page is heuristic except the remarks on practice.

## The algorithm

The algorithm is recursive on the projected lattices $\pi_k(L)$. The reference implementation runs the recursion on an explicit stack of tasks: $(k, \text{start})$ begins the HKZ reduction of $\pi_k(L)$, and $(k, \text{check})$ continues it after $\pi_{k+1}(L)$ was HKZ-reduced.

```pseudo id=main
KANNAN(B)                           ▷ independent rows b_1..b_n; returns an HKZ-reduced basis
L1  T ← a stack holding the task (1, start)
L2  while T ≠ ∅
L3      (k, phase) ← pop(T); if k = n then go to L2
L4      if phase = start then LLL-reduce π_k(b_k), ..., π_k(b_n); push (k, check), then (k+1, start); go to L2
L5      size-reduce b_{k+1} against b_k
L6      if N_k > 4 N_{k+1} then swap b_k and b_{k+1}; push (k, check), then (k+1, start); go to L2
L7      x ← a shortest nonzero vector of π_k(L(b_k, ..., b_n)), by enumeration with radius N_k
L8      if ‖π_k(Σ x_i b_i)‖² < N_k then put Σ x_i b_i at position k, keeping the lattice; push (k+1, start)
L9  size-reduce B; return B
```

In recursive form, one call at $k$ does: LLL on the projected rows (line L4), HKZ-reduce $\pi_{k+1}(L)$ by a recursive call, and repeat with a swap while $N_k > 4 N_{k+1}$ (lines L5 and L6). A basis in this state, with $\pi_{k+1}$ part HKZ-reduced and $\|b_k^*\| \le 2 \|b_{k+1}^*\|$, is called **quasi-HKZ**. Then it enumerates a shortest vector of $\pi_k(L)$ (line L7), puts it at position $k$ with a sweep of $2 \times 2$ unimodular steps from the [extended Euclidean algorithm](/extended-euclidean-algorithm/), and HKZ-reduces $\pi_{k+1}(L)$ once more by a second recursive call (line L8). The enumeration of line L7 is [Fincke-Pohst enumeration](/fincke-pohst-enumeration/) with a radius that shrinks to the best length found.

## Example

The basis $b_1 = (4, 0, 0)$, $b_2 = (-2, 3, 0)$, $b_3 = (1, 1, 3)$, with $N = (16, 9, 9)$, $\mu_{21} = -\tfrac12$, $\mu_{31} = \tfrac14$, $\mu_{32} = \tfrac13$.

| Task | Line | Action |
|------|------|------|
| $(1, \text{start})$ | L4 | the basis is LLL-reduced, unchanged; push $(1, \text{check})$, $(2, \text{start})$ |
| $(2, \text{start})$ | L4 | $\pi_2(b_2), \pi_2(b_3)$ LLL-reduced, unchanged; push $(2, \text{check})$, $(3, \text{start})$ |
| $(3, \text{start})$ | L3 | $k = n$, nothing to do |
| $(2, \text{check})$ | L5 to L8 | $\mu_{32} = \tfrac13$, no size reduction; $9 \le 4 \cdot 9$; enumeration gives $x = (1, 0)$ with length $9 = N_2$: no insertion |
| $(1, \text{check})$ | L5 to L8 | $\mu_{21} = -\tfrac12$ rounds to 0; $16 \le 4 \cdot 9$; enumeration gives $x = (0, 0, -1)$, length $11 < 16$: insert $-b_3$, rows $(-1, -1, -3), (-4, 0, 0), (-2, 3, 0)$; push $(2, \text{start})$ |
| $(2, \text{start})$ | L4 | LLL on $\pi_2$ gives rows $(-1, -1, -3), (2, 3, 0), (-2, 3, 0)$; push $(2, \text{check})$, $(3, \text{start})$ |
| $(3, \text{start})$ | L3 | nothing to do |
| $(2, \text{check})$ | L5 to L8 | $N = (11, \tfrac{118}{11}, \tfrac{648}{59})$; $\tfrac{118}{11} \le 4 \cdot \tfrac{648}{59}$; $x = (1, 0)$ with length $\tfrac{118}{11} = N_2$: no insertion; the stack is empty |

Line L9 changes nothing, and the output is $(-1, -1, -3), (2, 3, 0), (-2, 3, 0)$, with $N = (11, \tfrac{118}{11}, \tfrac{648}{59})$ and $\|b_1\|^2 = 11 = \lambda_1^2$.

Line L6 swaps only when the Gram-Schmidt norms fall fast. For the rows $(80, 0, 0, 0, 0)$, $(40, 58, 0, 0, 0)$, $(0, 29, 42, 0, 0)$, $(0, 0, 21, 30, 0)$, $(0, 0, 0, 15, 22)$, whose $N_i$ fall by a factor of about $0.53$ at each step, it swaps twice: at $k = 2$ with $N_2 = 3364 > 4 \cdot 709$, and at $k = 1$ with $N_1 = 6400 > 4 \cdot 709$. The output starts with $(0, 0, 0, 15, 22)$, of squared length $709 = \lambda_1^2$. The test file checks both runs.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Each step is a unimodular operation on rows at positions $\ge k$, so it keeps the lattice and the rows before $k$, and therefore keeps $\pi_k$ and the projected lattice $\pi_k(L)$. The proof goes by downward induction on $k$: a call at $k$ ends with $\pi_k(b_k), \ldots, \pi_k(b_n)$ HKZ-reduced. At $k = n$ this is trivial. For $k < n$, the recursive call makes the part from $k + 1$ HKZ-reduced; the enumeration is exact, so after line L8 the vector $b_k^*$ is a shortest vector of $\pi_k(L)$; the inserted vector has coprime coefficients, because a common factor would give a shorter vector; and the second recursive call does not touch $b_k$.

For termination, a swap on line L6 happens when $N_k > 4 N_{k+1}$ and $|\mu_{k+1,k}| \le \tfrac12$, so the new $N_k = N_{k+1} + \mu_{k+1,k}^2 N_k < \tfrac14 N_k + \tfrac14 N_k$ is less than half the old one. Since $N_k \ge \lambda_1(\pi_k(L))^2$, there are at most $\log_2(N_k / \lambda_1(\pi_k(L))^2) + 1$ swaps at each level, and every recursive call ends by induction.

## Complexity

- **Number of calls.** The swaps at a level are at most $\log_2(N_k / \lambda_1(\pi_k(L))^2) + 1$, which is $O(n)$ after LLL, and each swap costs one recursive call. Since every level can call the next one several times, bounding the total takes care; the analyses below bound the whole algorithm, preprocessing included, and the top-level enumeration is the dominant term.
- **The enumeration on a quasi-HKZ basis.** Enumerating the ball of radius $\|b_1\|$ visits at most $\sum_{k} \prod_{i \ge k} \big(2 \sqrt{N_1 / N_i} + 1\big)$ nodes, roughly. The HKZ property of $\pi_2(L)$ bounds each ratio $N_2 / N_i$ through [Hermite's constant](/hermite-constant/) of the projected lattices, and $N_1 \le 4 N_2$. Kannan derived $n^{O(n)}$, Helfrich $n^{n/2 + o(n)}$, and Hanrot and Stehlé, by a volume argument on the number of points in each projected ball, $n^{n/(2e) + o(n)}$.
- **Tightness.** Hanrot and Stehlé also built HKZ-reduced bases on which the enumeration needs $n^{n/(2e) - o(n)}$ nodes, so the exponent $1/(2e)$ cannot be improved for this algorithm.
- **CVP.** Enumerating around a target on the HKZ-reduced basis solves the [closest vector problem](/closest-vector-problem/) in $n^{n/2 + o(n)}$ operations.
- **Space.** The recursion depth is $n$ and the enumeration needs $O(n)$ numbers, so the space is polynomial, unlike sieving, which needs $2^{\Theta(n)}$ memory.
- **Comparison.** Enumeration after LLL alone costs $2^{O(n^2)}$ in the worst case. Proved single exponential algorithms run in time $2^{n + o(n)}$ but with exponential space; heuristic [sieves](/gauss-sieve/) run in $2^{0.292 n + o(n)}$ time.

## Properties

- **Exact and deterministic.** The output is HKZ-reduced, and its first vector is a shortest vector, with no heuristic and no randomness.
- **Polynomial space.** Its bound is among the best proved for SVP algorithms that use polynomial space.
- **Output not unique.** HKZ-reduced bases are not unique: signs, ties between shortest vectors and the size-reduction choices can differ.
- **Self-reducing.** The preprocessing of each level is the same algorithm one dimension lower.

## Variants and improvements

- **Helfrich's version.** A different balance of preprocessing and enumeration, with the bound $n^{n/2 + o(n)}$.
- **Schnorr-Euchner enumeration with BKZ preprocessing.** Practical SVP solvers replace the recursive HKZ preprocessing by [BKZ](/bkz-algorithm/) with a moderate block size and use [Schnorr-Euchner](/schnorr-euchner-enumeration/) zigzag order; this has no comparable proved bound but is much faster in practice.
- **Pruned enumeration.** Gama, Nguyen and Regev's extreme pruning cuts the tree by heuristic bounds and repeats with rerandomized bases; it gives up the guarantee for a large speedup.
- **Micciancio and Walter (2015).** An enumeration algorithm with Kannan-style preprocessing whose cost is $n^{n/(2e) + o(n)}$ with only a small overhead over the enumeration itself.
- **Integer programming.** Kannan's original use: with this algorithm, integer programming in $n$ variables takes $n^{O(n)}$ operations times a polynomial in the input size, against $2^{O(n^3)}$ for Lenstra's algorithm of 1983.

## When to use it

- When a proved shortest vector or an HKZ-reduced basis is needed in moderate dimension, up to about 40 to 60, and memory is limited.
- As a subroutine with a proved bound, for example inside a BKZ variant or slide reduction when proofs about the whole algorithm are needed.
- Not in high dimension for speed: pruned enumeration with BKZ preprocessing, and sieving above dimension about 70, are faster in practice.

## Pitfalls

- **The second recursive call.** After inserting the shortest vector at position $k$, the projected lattice $\pi_{k+1}(L)$ changes, and it must be HKZ-reduced again; skipping that call leaves a basis that starts with a shortest vector but is not HKZ-reduced.
- **Size reduction before the swap test.** The halving argument needs $|\mu_{k+1,k}| \le \tfrac12$; without line L5 the swap can make $N_k$ larger.
- **Recursion depth.** A literal recursive implementation has depth $n$ and recomputes Gram-Schmidt data at every level; keep the data updated or use a stack as here.
- **Inserting without the gcd.** Prepending the vector without removing the linear dependence gives $n + 1$ rows; use the gcd sweep or LLL on the extended set.
- **Floating point.** The enumeration radius must not be rounded down, or a shortest vector can be missed; use exact arithmetic or a proved error bound.

## Implementations

## History

Ravi Kannan presented the algorithm at STOC 1983 as part of an improved algorithm for integer programming, with the full version in Mathematics of Operations Research in 1987; it was the first algorithm to compute shortest vectors and HKZ-reduced bases in $n^{O(n)}$ operations. Bettina Helfrich improved the exponent to $n/2$ in 1985. The analysis stayed there for two decades, until Guillaume Hanrot and Damien Stehlé proved $n/(2e)$ in 2007 and showed in 2008 that it is tight. Practical SVP solvers moved instead to pruned Schnorr-Euchner enumeration with BKZ preprocessing and then to sieving, but Kannan's algorithm remains the reference for proved polynomial-space bounds.

## References

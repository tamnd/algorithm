---
tag: JER2FD
kind: algorithm
slug: clarksons-algorithm
name: Clarkson's algorithm
aliases:
- Clarkson's random sampling algorithm
- Clarkson's LP-type algorithm
- Clarkson's Las Vegas linear programming algorithm
- Clarkson's reweighting algorithm
area: geometry/geometric-optimization
level: advanced
summary: Las Vegas algorithm for linear programming and LP-type problems of small dimension. Random samples of about d sqrt(n) constraints and reweighting of violators give expected O(n) time.
solves: [linear-programming-problem, minimum-enclosing-circle, minimum-enclosing-ball]
model: real-ram
complexity:
  vars: {n: the number of constraints, d: the combinatorial dimension (a constant)}
  time: {expected: O(d^2 n + d^4 sqrt(n) log n)}
  space: {extra: O(n)}
properties: {online: false, deterministic: false, recursive: false}
history:
  year: 1988
  people: [Kenneth L. Clarkson]
  note: Clarkson gave the sampling algorithm with sample size d sqrt(n), the iterative reweighting algorithm and their combination at FOCS 1988; the journal version appeared in 1995.
prereqs: [lp-type-problem, linear-programming-problem, random-sampling, welzls-algorithm]
see_also: [seidel-linear-programming, megiddo-fixed-dimension-lp, minimum-enclosing-circle, minimum-enclosing-ball, chans-randomized-optimization, coreset, multiplicative-weights-update, las-vegas-algorithm]
sources:
  - paper: doi:10.1145/201019.201036
    title: Kenneth L. Clarkson, Las Vegas algorithms for linear and integer programming when the dimension is small, Journal of the ACM 42(2), 1995
    locator: abstract (the expected bound), Section 2 (Figure 1, the recursive algorithm with r = d sqrt(n) and the test |V| ≤ 2 sqrt(n); Figure 2, the iterative algorithm with the test V(V) ≤ 2V(S)/(9d − 1) and doubling), Lemma 3.1, Lemma 3.2, Theorems 3.3 to 3.5
  - paper: "Kenneth L. Clarkson, Las Vegas algorithms for linear and integer programming when the dimension is small, Proceedings of the 29th IEEE Symposium on Foundations of Computer Science (FOCS), 1988"
    locator: the conference version of the algorithm
  - paper: doi:10.1007/BF01940877
    title: Jiří Matoušek, Micha Sharir and Emo Welzl, A subexponential bound for linear programming, Algorithmica 16, 1996
    locator: the subexponential base solver and its combination with Clarkson's algorithm
  - paper: "Bernd Gärtner and Emo Welzl, A simple sampling lemma, analysis and applications in geometric optimization, Discrete and Computational Geometry 25(4), 2001"
    locator: the sampling lemma for LP-type problems and its use in the analysis of Clarkson's algorithm
  - paper: "Bernard Chazelle and Jiří Matoušek, On linear-time deterministic algorithms for optimization problems in fixed dimension, Journal of Algorithms 21(3), 1996"
    locator: the derandomization of Clarkson's algorithm for LP-type problems
---

Clarkson's algorithm solves [linear programming](/linear-programming-problem/) with $n$ constraints in a small number $d$ of variables, and in the same form every [LP-type problem](/lp-type-problem/) of small combinatorial dimension, such as the [minimum enclosing circle](/minimum-enclosing-circle/) and the [minimum enclosing ball](/minimum-enclosing-ball/). It is a [Las Vegas algorithm](/las-vegas-algorithm/): the answer is always exact, and only the running time is random. It solves a [random sample](/random-sampling/) of about $d\sqrt{n}$ constraints, finds the constraints that the sample's optimum violates, and adds them to the next sample if they are few. The small subproblems go to a second loop that samples $9d^2$ constraints by weight and doubles the weights of the violators, a form of the [multiplicative weights](/multiplicative-weights-update/) method. For fixed $d$ the expected time is $O(n)$ on the [real RAM](/real-ram/), and the slow part of the work is done only on sets of $O(d^2)$ constraints.

## In plain words

You must find the best answer that obeys a very long list of rules, and only a few rules really matter. You do not know which ones.

Pick a random handful of rules and find the best answer for the handful. Then check this answer against all the rules. If it obeys all of them, you are done. If it breaks some rules, there are usually only a few, and at least one of them is a rule that really matters. Keep those rules and add them to every later handful. After a few rounds you hold all the rules that matter, and the answer obeys the whole list.

Each handful is solved the same way with even smaller samples. There, a broken rule gets more likely to be picked next time, until the important rules are almost sure to be picked.

## The problem

Notation: $H$ is the set of constraints, with $n = |H|$; $w$ is the value function of an LP-type problem $(H, w)$ with combinatorial dimension $\delta$ (for linear programming in $d$ variables $\delta = d$, for the smallest ball in $\mathbb{R}^d$ $\delta = d + 1$, for the smallest disk $\delta = 3$). A constraint $h$ violates a set $G$ if $w(G \cup \{h\}) > w(G)$. A basis of $G$ is a minimal subset $B \subseteq G$ with $w(B) = w(G)$, so $|B| \le \delta$. The task is to compute $w(H)$, together with the object that attains it (the optimal point, or the disk).

The algorithm needs two primitives:

- a violation test: given the optimum of a set $G$ and a constraint $h$, decide whether $h$ violates $G$;
- a base solver $\mathrm{BASE}(G)$ that returns the optimum of a set of at most $C = 9\delta^2$ constraints. For linear programming it is the [simplex method](/simplex-method/); for the disk it is [Welzl's algorithm](/welzls-algorithm/).

**Clarkson's hypotheses.** Clarkson (1995) states the method for the linear program $\min c^\top x$ subject to $Ax \le b$ with $n$ constraints in $d$ variables, under these assumptions. (1) Every subset $S$ of the constraints has a unique optimum $x^*(S)$: unbounded problems are bounded by extra constraints, and among several optimal points the one of minimum norm is taken. (2) The optimum is determined by at most $d$ constraints: there is $S^* \subseteq S$ with $|S^*| \le d$ and $x^*(S^*) = x^*(S)$. (3) For the bound on the number of violators (his Lemma 3.2), the problem is nondegenerate; perturbation removes degeneracies. (4) A base algorithm, the simplex method, solves small instances. In the LP-type form below, (1) and (2) are the axioms and the combinatorial dimension, and (3) is not needed, because the [sampling lemma](/lp-type-problem/) of Gärtner and Welzl holds without it.

**Degeneracies.** For the disk no general position is assumed. Duplicate points, collinear points and many points on one circle are allowed, because the smallest disk of a nonempty set is unique, and the implementation tests containment with exact rational arithmetic.

## The algorithm

CLARKSON is the outer algorithm, Clarkson's mixed algorithm $x^*_m$. ITERATIVE is his iterative algorithm $x^*_i$; it gives every constraint a weight $\mu(h)$, draws $C$ times without replacement from the multiset in which $h$ has $\mu(h)$ copies, and doubles the weights of the violators. $V^*$ is the set of constraints that the outer loop keeps, and $\mu(V)$ is the total weight of a set $V$.

```pseudo id=main
CLARKSON(H)                       ▷ n = |H|, δ = combinatorial dimension, C = 9δ²
L1  if n ≤ C then return ITERATIVE(H)
L2  r ← ⌈δ √n⌉;  V* ← ∅
L3  repeat
L4      R ← a uniformly random r-subset of H \ V*
L5      x ← ITERATIVE(R ∪ V*)
L6      V ← the constraints of H that violate x
L7      if V = ∅ then return x
L8      if |V| ≤ 2 √n then
L9          V* ← V* ∪ V

ITERATIVE(G)                      ▷ μ(h) = 1 for every h in G
L10 if |G| ≤ C then return BASE(G)
L11 repeat
L12     R ← the constraints drawn in C weighted draws from G
L13     x ← BASE(R)
L14     V ← the constraints of G that violate x
L15     if V = ∅ then return x
L16     if μ(V) ≤ 2δ μ(G) / (C − δ) then
L17         μ(h) ← 2 μ(h) for every h in V
```

A round of either loop is successful when it returns or passes the test on L8 or L16. A failed round changes nothing and is repeated with fresh random choices.

## Example

Take the $300$ lattice points $(x, y)$ with $0 \le x \le 29$ and $0 \le y \le 9$, the smallest disk ($\delta = 3$, $C = 81$), and the implementation's generator with seed 0. Here $r = \lceil 3\sqrt{300} \rceil = 52$, and L8 accepts $|V| \le 2\sqrt{300}$, that is $|V| \le 34$. Each set passed to ITERATIVE has at most 81 points, so ITERATIVE calls Welzl's algorithm directly. Disks are given as center and squared radius.

| phase | points solved | disk | violators $V$ | action |
|---|---|---|---|---|
| 1 | 52 | $(29/2, 4)$, $905/4$ | $(0, 9)$, $(29, 9)$ | add 2 to $V^*$ |
| 2 | 54 | $(29/2, 13/2)$, $433/2$ | $(0,0)$, $(0,1)$, $(0,2)$, $(0,3)$, $(1,0)$, $(28,0)$, $(29,0)$, $(29,1)$, $(29,2)$, $(29,3)$ | add 10 to $V^*$ |
| 3 | 64 | $(29/2, 9/2)$, $461/2$ | none | return |

The first sample missed the top corners, and its disk passes through the bottom corners $(0, 0)$ and $(29, 0)$. The second sample holds the two top corners but neither bottom corner. The third holds all four corners, which form the basis: the answer is the circle through the corners, with center $(29/2, 9/2)$ and squared radius $(29/2)^2 + (9/2)^2 = 461/2$. The phases solved $52 + 54 + 64 = 170$ points and made $3 \cdot 300$ containment tests.

## Correctness

The full proof is in [proofs/correctness](proofs/correctness.md). It uses three facts about LP-type problems.

1. **A certificate.** If $R \subseteq G$ is nonempty and no constraint of $G$ violates $R$, then $w(R) = w(G)$. Locality lets us add the constraints one at a time without a change of value. So both loops return only the optimum: L7 returns $w(H)$ and L15 returns $w(G)$.
2. **Violators meet every basis** (Clarkson's Lemma 3.1). If some constraint of $G$ violates $R \subseteq G$, then for every basis $B$ of $G$, some constraint of $B$ violates $R$. Otherwise $w(R) = w(R \cup B) \ge w(B) = w(G)$, and nothing could violate $R$.
3. **The sampling lemma.** For a uniformly random $r$-subset $R$ of an $N$-element multiset, the expected number of elements outside $R$ that violate $R$ is at most $\delta(N - r)/(r + 1)$. An element that violates $R$ is extreme in $R \cup \{h\}$, and a set has at most $\delta$ extreme elements.

By fact 3 and [Markov's inequality](/markov-inequality/), each round of each loop is successful with probability at least $1/2$. In the outer loop, a successful round that does not return adds to $V^*$ a constraint of a fixed basis of $H$ that was not there before (fact 2, and $V$ is disjoint from $R \cup V^*$). So after at most $\delta$ such rounds the basis lies in $V^*$, and the next round returns. In ITERATIVE, a successful round that does not return doubles the weight of a constraint of a fixed basis $B$ of $G$ (fact 2), but raises the total weight by a factor of at most $1 + 2\delta/(C - \delta)$. After $k$ such rounds $2^{k/\delta} \le \mu(B) \le |G|\, e^{2\delta k/(C - \delta)}$, which bounds $k$ by $O(\delta \log |G|)$ when $C > \delta + 2\delta^2/\ln 2$; the choice $C = 9\delta^2$ satisfies this.

## Complexity

Let $T_v$ be the cost of a violation test and $T_b$ the cost of one call of BASE on $C = 9\delta^2$ constraints.

- **Outer loop.** At most $\delta + 1$ successful rounds, so at most $2(\delta + 1)$ rounds in expectation. Each makes $n$ violation tests and calls ITERATIVE on at most $r + 2\delta\sqrt{n} \le 3\delta\sqrt{n} + 1$ constraints.
- **ITERATIVE on $m$ constraints.** At most $2(2.3\,\delta \ln m + 1)$ rounds in expectation, each with $m$ violation tests and one call of BASE. Sampling by prefix sums and binary search adds $O(m + C \log m)$ per round.
- **Total.** In expectation $O(\delta n + \delta^3 \sqrt{n} \log n)$ violation tests and $O(\delta^2 \log n)$ calls of BASE, so

$$O\bigl((\delta n + \delta^3 \sqrt{n} \log n)\, T_v + \delta^2 \log n \cdot T_b\bigr)$$

expected time. For linear programming, $T_v = O(d)$, and Clarkson's bound is $O(d^2 n) + (\log n)\, O(d)^{d/2 + O(1)} + O(d^4 \sqrt{n} \log n)$ expected arithmetic operations, where the middle term is the simplex method on $O(d^2)$ constraints. For the disk all of $\delta$, $T_v$ and $T_b$ are constants, and the time is $O(n)$ expected.

**Space.** $O(n)$ for the input, the weights, the sets $V^*$ and the samples.

**Lower bound.** Every algorithm must look at every constraint, since an unread constraint could be the one that changes the optimum, so $\Omega(n)$ time is needed, and the algorithm is optimal in $n$ for fixed $\delta$.

**Worst case.** A Las Vegas algorithm has no finite worst-case bound here: with tiny probability, every sample fails. The number of rounds has an exponentially decreasing tail, since each round succeeds with probability at least $1/2$ whatever happened before.

## Properties

- **Exact output.** The output is checked against every constraint before it is returned, so it is always correct; randomness affects only the time.
- **Few expensive calls.** BASE runs $O(\delta^2 \log n)$ times in expectation, on $O(\delta^2)$ constraints. This is why a slow exact solver, or one whose cost is exponential in $\delta$, is good enough.
- **Few passes over the data.** All access to the full set $H$ is the violation scan on L6, which is $O(\delta)$ passes in expectation. The scans parallelize, and $H$ may be on disk or given only by a violation oracle.
- **Generic.** Only the two primitives depend on the problem, so the same code solves linear programming, smallest balls, polytope distance and the other [LP-type problems](/lp-type-problem/).
- **A basis as a core set.** The kept set $V^*$ together with the last sample contains a basis of $H$, a set of at most $\delta$ constraints with the optimum of all $n$: an exact [core set](/coreset/).

## Variants and improvements

- **Recursive algorithm $x^*_r$.** Clarkson's first algorithm calls itself on $R \cup V^*$ instead of ITERATIVE, and calls the simplex method when $n \le 9d^2$.
- **Iterative algorithm $x^*_i$ alone.** ITERATIVE on all of $H$ takes $O(d^2 n \log n) + (d \log n)\, O(d)^{d/2 + O(1)}$ expected arithmetic operations (Clarkson's Theorem 3.4), more in $n$ but simpler.
- **Subexponential base solver.** With the algorithm of Matoušek, Sharir and Welzl as BASE, linear programming takes $O(d^2 n + e^{O(\sqrt{d \log d})})$ expected time, the best known bound that is linear in $n$ and subexponential in $d$.
- **Deterministic.** Chazelle and Matoušek (1996) derandomized the sampling for LP-type problems with a further condition on the range space, and got deterministic $O(n)$ time for fixed $\delta$, with a constant that grows faster in $\delta$.
- **Integer programming.** Clarkson's paper also applies the scheme to integer programming in fixed dimension, where bases are larger but still bounded.
- **Implicit and distributed problems.** Because only violation tests touch $H$, the method suits problems whose constraints are given implicitly, and it is a common pattern for optimization over data spread over many machines.

## When to use it

- **Large $n$, small $\delta$, slow base solver.** When $n$ is in the millions and the exact solver for small sets is expensive, as for linear programming in 10 to 50 variables, Clarkson's algorithm keeps the solver on small inputs.
- **Data that is cheap to scan but costly to hold.** Each round is one pass; only $O(\delta \sqrt{n})$ constraints are kept in memory.
- **Not for the plane.** For the smallest disk or two-variable linear programming, [Welzl's algorithm](/welzls-algorithm/) or [Seidel's algorithm](/seidel-linear-programming/) alone is simpler and faster in practice; Clarkson's layer pays off as $\delta$ grows, because Seidel's bound has a factor $\delta!$ in front of $n$.
- **Deterministic needs.** If a fixed time bound is required, use [Megiddo's method](/megiddo-fixed-dimension-lp/) by [prune and search](/prune-and-search/), or the derandomized versions.

## Pitfalls

- **Inexact violation tests.** The algorithm returns only after a scan with no violators. With floating-point tests a point on the circle may test as outside forever, and the loop never ends, or a violator may be missed and a wrong answer returned. Use exact arithmetic or a tolerance with a stated error bound.
- **Non-unique optimum.** The axioms need one value per set. For linear programming, break ties, for example by the minimum-norm or the lexicographically smallest optimal point, and bound unbounded problems; otherwise fact 2 fails.
- **Too small a sample in ITERATIVE.** The weight argument needs $C > \delta + 2\delta^2/\ln 2$, about $29$ for $\delta = 3$. A smaller $C$ can still terminate, but without the $O(\delta \log n)$ bound.
- **Drawing with replacement.** The $C$ draws of L12 are without replacement from the multiset of copies. Repeated draws of one constraint are fine; the sample is the set of distinct constraints drawn.
- **Counting violators by weight.** The test on L16 compares the total weight of $V$, not its size; using $|V|$ breaks the Markov bound.
- **Keeping old violators.** $V^*$ grows only in successful rounds. Adding the violators of a failed round, with $|V| > 2\sqrt{n}$, makes later subproblems too large.

## Implementations

## History

Linear programming in fixed dimension became a linear-time problem with Megiddo (1984), whose deterministic prune and search method takes $O(2^{2^d} n)$ time; Dyer (1986) and Clarkson (1986) reduced the constant to $3^{d^2}$. Clarkson presented the Las Vegas algorithm at FOCS 1988 and published the journal version in 1995. It was the first algorithm whose dependence on $n$ is $O(d^2 n)$, with the exponential cost in $d$ moved to subproblems of size $O(d^2)$. Its reweighting loop is an early example of the multiplicative weights method. Seidel (1991) gave a simpler randomized incremental algorithm with $O(d!\, n)$ expected time. Sharir and Welzl (1992) stated LP-type problems, and Matoušek, Sharir and Welzl (1996), together with Kalai (1992), gave subexponential bounds; combined with Clarkson's algorithm they give the best known randomized bound for linear programming in the unit-cost model. Gärtner and Welzl (2001) gave the simple sampling lemma that now drives the analysis.

## References

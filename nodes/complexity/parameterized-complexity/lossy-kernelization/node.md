---
tag: 5NEZGB
kind: technique
slug: lossy-kernelization
name: Lossy kernelization
aliases:
- lossy kernel
area: complexity/parameterized-complexity
level: research
summary: "Shrink an instance to size g(k) so that a c-approximate solution of the small instance lifts to a (c times alpha)-approximate one of the original. It gives small kernels where exact ones fail."
prereqs: [kernelization, approximation-ratio]
see_also: [kernel-lower-bounds, fpt-approximation, polynomial-compression, cross-composition, nemhauser-trotter-theorem, vertex-cover-2-approximation, parameterized-inapproximability, polynomial-kernel]
sources:
  - paper: doi:10.1145/3055399.3055456
    title: "Daniel Lokshtanov, Fahad Panolan, M. S. Ramanujan and Saket Saurabh, Lossy kernelization, Proceedings of the 49th ACM Symposium on Theory of Computing (STOC 2017), 224-237"
    locator: Definitions 3.1 to 3.6 (parameterized optimization problems, approximate preprocessing, approximate kernels), the capped vertex cover objective, and the results on connected vertex cover, cycle packing, longest path and set cover
  - book: isbn:9781107057760
    title: Fedor V. Fomin, Daniel Lokshtanov, Saket Saurabh and Meirav Zehavi, Kernelization, Theory of Parameterized Preprocessing, Cambridge University Press, 2019
    locator: Part IV, Beyond kernelization (lossy kernels)
  - paper: doi:10.1016/j.jcss.2010.06.007
    title: "Lance Fortnow and Rahul Santhanam, Infeasibility of instance compression and succinct PCPs for NP, Journal of Computer and System Sciences 77(1), 91-106 (2011)"
    locator: the distillation theorem behind the lower bounds for lossy kernels
---

Lossy kernelization joins [kernelization](/kernelization/) with approximation. An $\alpha$-approximate kernel shrinks an instance with parameter $k$ to size $g(k)$, and comes with a lifting step that turns any $c$-approximate solution of the small instance into a $(c \cdot \alpha)$-approximate solution of the original. Lokshtanov, Panolan, Ramanujan and Saurabh set up the theory in 2017. Some problems with no polynomial kernel, such as connected vertex cover, have polynomial $\alpha$-approximate kernels for every $\alpha > 1$, while others, such as longest path, have none for any $\alpha$.

## In plain words

An ordinary kernel shrinks a big problem to a small one with exactly the same answer. Sometimes this is not possible at a small size. A lossy kernel accepts a small loss: the small problem only needs to keep the answer up to a fixed factor.

The method has two steps. The first step shrinks the input. You then solve the small problem in any way you like, well or badly. The second step turns your answer back into an answer for the big problem. The promise is that the final answer is at most a fixed factor worse than your answer was for the small problem.

## When it applies

- The problem is an optimization problem with a parameter $k$, and the interesting solutions have value about $k$.
- Exact kernels are too large or are ruled out by [kernel lower bounds](/kernel-lower-bounds/).
- There are reduction rules that are safe up to a small loss: for example, a rule may throw away a structure whose best use costs at most a factor $1 + \varepsilon$.
- The goal is an [FPT approximation](/fpt-approximation/), or a preprocessing step that a heuristic solver can use.

## The template

**Parameterized optimization problem.** A function $\Pi(I, k, S)$ gives the value of a solution $S$ for instance $I$ with parameter $k$. Let $\mathrm{OPT}(I, k)$ be the best value. The parameter enters through a *cap*: for vertex cover, $\mathrm{VC}(G, k, S) = \min(|S|, k + 1)$ when $S$ is a vertex cover and $\infty$ otherwise. So all solutions with more than $k$ vertices are equally bad.

**Approximate preprocessing.** For a minimization problem, an *$\alpha$-approximate polynomial-time preprocessing algorithm* is a pair of polynomial-time algorithms. The reduction algorithm maps $(I, k)$ to $(I', k')$. The solution lifting algorithm takes $(I, k)$, $(I', k')$ and a solution $S'$ of $(I', k')$, and returns a solution $S$ of $(I, k)$ with

$$\frac{\Pi(I, k, S)}{\mathrm{OPT}(I, k)} \le \alpha \cdot \frac{\Pi(I', k', S')}{\mathrm{OPT}(I', k')}.$$

It is an *$\alpha$-approximate kernel* of size $g$ if $|I'| + k' \le g(k)$, and a *polynomial* one if $g$ is a polynomial. A *polynomial-size approximate kernelization scheme* (PSAKS) is a family that gives a $(1 + \varepsilon)$-approximate polynomial kernel for every $\varepsilon > 0$.

The template applies rules one by one and lifts in the reverse order. It has four holes: CAP, the capped objective; RULES, the list of reduction rules, each with a ratio; LIFT, the lifting step of each rule; and SIZE, the size bound when no rule applies.

```pseudo id=main
LOSSY-KERNEL(I, k)
L1  T ← empty stack
L2  while some rule ρ in RULES applies to (I, k) do
L3      (I', k') ← ρ.REDUCE(I, k)                ▷ ρ has ratio α_ρ under CAP
L4      push (ρ, I, k) on T; (I, k) ← (I', k')
L5  return (I, k), T                             ▷ |I| + k ≤ SIZE(k) by the analysis

LIFT(T, S')
L6  while T is not empty do
L7      pop (ρ, I, k) from T; S' ← ρ.LIFT(I, k, S')
L8  return S'
```

If the chain uses rules with ratios $\alpha_1, \ldots, \alpha_r$, the lifted solution has ratio at most $c \cdot \alpha_1 \cdots \alpha_r$, by the definition applied once per rule. So the analysis must bound the product. Exact rules have ratio 1 and cost nothing; LPRS also define a *strict* form of the bound, with $\max(c, \alpha)$ in place of $c \cdot \alpha$, which stays $\alpha$ along a chain of any length.

## Classic examples

**An approximation algorithm is a lossy kernel of constant size.** If a problem has a polynomial-time $\alpha$-approximation, then it has an $\alpha$-approximate kernel of constant size: the reduction outputs a fixed tiny instance, and the lifting step ignores $S'$ and runs the approximation algorithm on $(I, k)$. The converse also holds, because a kernel of constant size can be solved exactly in constant time and the solution lifted. For vertex cover, the cover from a maximal matching is a 2-approximation; see [vertex cover 2-approximation](/vertex-cover-2-approximation/). On the Petersen graph a scratch script found an optimum cover of 6 vertices and a greedy maximal matching with 5 edges, which gives a cover of 10 vertices, a ratio of $10/6 \le 2$.

**Vertex cover between exact and 2-approximate.** The [Nemhauser-Trotter](/nemhauser-trotter-theorem/) kernel has $2k$ vertices and ratio 1, and the constant-size kernel above has ratio 2. The table of LPRS lists an $\alpha$-approximate kernel with $2(2 - \alpha)k$ vertices for $1 < \alpha < 2$, which fills the range between the two ends.

**Connected vertex cover.** Find a vertex cover of size at most $k$ that induces a connected subgraph. This problem is FPT but has no polynomial kernel unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$. LPRS give a PSAKS: for every $\varepsilon > 0$, a $(1 + \varepsilon)$-approximate kernel whose size is a polynomial in $k$ with an exponent that depends on $\varepsilon$. So a small loss in the ratio buys a polynomial size that no exact kernel can reach.

**Cycle packing.** Find $k$ vertex-disjoint cycles. This problem has no polynomial kernel unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$, and LPRS give a PSAKS for it.

**No lossy kernel at all.** LPRS showed that longest path, and set cover parameterized by the size of the universe, have no $\alpha$-approximate kernel of polynomial size for any $\alpha \ge 1$, unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$. The proofs use a *gap creating cross-composition*, a [cross-composition](/cross-composition/) that also keeps a gap between the values of yes- and no-instances.

## Variations

- **Maximization problems.** The ratio is turned over: the lifted solution has value at least $1/\alpha$ times the value the small solution has relative to its optimum.
- **Efficient schemes.** A PSAKS is *efficient* when the size is $f(\varepsilon) \cdot \mathrm{poly}(k)$, with the dependence on $\varepsilon$ only in the constant factor.
- **Earlier notions.** Fellows and coauthors studied *$\alpha$-fidelity kernels* before LPRS. The LPRS definition asks that every approximate solution of the small instance lifts, with the loss factor $\alpha$.
- **Lossy compression.** The output may be in another problem, with a transformation that keeps the ratio, as with [polynomial compression](/polynomial-compression/) for exact kernels.

## Pitfalls

- **Without a cap the definition says little.** If $k$ does not limit the objective, a "kernel" for vertex cover could have to keep every vertex. The cap $\min(|S|, k + 1)$ makes all large solutions equally bad, so the kernel only has to keep the solutions of size at most $k$.
- **Ratios multiply.** A chain of $r$ rules that each lose a factor $1 + \varepsilon$ loses up to $(1 + \varepsilon)^r$. Use strict rules or bound $r$.
- **Lifting must be fast.** The lifting step has to run in polynomial time; a step that solves the original problem would make the kernel useless.
- **An approximate kernel is not an approximation algorithm.** The small instance still has to be solved. Solving it exactly in time that depends on $k$ gives an $\alpha$-approximation in FPT time, and solving it with a $c$-approximation gives ratio $c \cdot \alpha$ in polynomial time.
- **Lower bounds need gaps.** A plain cross-composition rules out exact polynomial kernels only. To rule out lossy ones, the composition must keep a gap.

## Exercises

1. Show that the composition of an $\alpha_1$-approximate and an $\alpha_2$-approximate preprocessing algorithm is $\alpha_1 \alpha_2$-approximate.
2. Prove that a problem with a polynomial-time $\alpha$-approximation has an $\alpha$-approximate kernel of constant size, and that the converse holds.
3. For capped vertex cover, show that deleting an isolated vertex and taking a vertex of degree more than $k$ into the solution are rules with ratio 1.
4. Explain why the capped objective is needed for the claim in Exercise 3.

## References

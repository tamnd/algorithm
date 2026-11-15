---
tag: 2DG6NT
kind: definition
slug: strong-np-hardness
name: Strong NP-hardness
aliases:
- NP-hard in the strong sense
- strongly NP-hard
area: complexity/np-completeness
level: advanced
summary: NP-hardness that holds even when all numbers in the input are bounded by a polynomial in the input length, so no pseudo-polynomial algorithm exists unless P = NP.
prereqs: [np-hard, pseudo-polynomial-time, unary-encoding]
see_also: [weak-np-hardness, three-partition, bin-packing-np-hardness, no-fptas-for-strongly-np-hard-problems, scheduling-with-release-times-and-deadlines, garey-johnson-compendium, traveling-salesman-problem, makespan-minimization]
sources:
  - paper: doi:10.1145/322077.322090
    title: M. R. Garey and D. S. Johnson, "Strong" NP-completeness results, motivation, examples, and implications, Journal of the ACM 25(3), 499 to 508 (1978)
    locator: the definition of strong NP-completeness, the pseudo-polynomial transformation, and the consequences for pseudo-polynomial algorithms and fully polynomial approximation schemes
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 4.2 (number problems, strong NP-completeness, pseudo-polynomial transformations and 3-PARTITION), Theorem 4.5 (SEQUENCING WITHIN INTERVALS is NP-complete in the strong sense), and the appendix, problems SP15, SP16, SR1 and SS1
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms, Springer, 2001
    locator: Chapter 8 (strong NP-hardness and the existence of an FPTAS)
---

A problem with numbers in its input is strongly NP-hard, or NP-hard in the strong sense, when it stays [NP-hard](/np-hard/) on the instances whose numbers are bounded by a polynomial in the input length. On those instances a [pseudo-polynomial](/pseudo-polynomial-time/) algorithm runs in polynomial time. So a strongly NP-hard problem has no pseudo-polynomial algorithm unless P = NP. The idea and the name are from Garey and Johnson (1978). [3-partition](/three-partition/), [bin packing](/bin-packing-np-hardness/), [scheduling with release times and deadlines](/scheduling-with-release-times-and-deadlines/) and the traveling salesman problem are strongly NP-hard. [Subset sum](/subset-sum-problem/), [partition](/partition-problem/) and knapsack are NP-hard but not strongly NP-hard unless P = NP; they are [weakly NP-hard](/weak-np-hardness/).

## Definition

**Length, Max and restrictions.** Fix a decision problem $\Pi$ and a reasonable encoding with numbers in binary. For an instance $I$, $\mathrm{Length}(I)$ is the length of its encoding and $\mathrm{Max}(I)$ is the magnitude of its largest integer. For a polynomial $p$, let $\Pi_p$ be the restriction of $\Pi$ to the instances $I$ with $\mathrm{Max}(I) \le p(\mathrm{Length}(I))$.

**Definition (Garey and Johnson).** $\Pi$ is *NP-hard in the strong sense* if $\Pi_p$ is NP-hard for some polynomial $p$. If, in addition, $\Pi$ is in NP, then $\Pi$ is *NP-complete in the strong sense*, or strongly NP-complete. An optimization problem is strongly NP-hard when its decision version is.

**Problems without large numbers.** If $\Pi$ is not a number problem, that is, if $\mathrm{Max}(I) \le q(\mathrm{Length}(I))$ for a polynomial $q$ and all $I$, then $\Pi_q = \Pi$. So each NP-complete problem without large numbers, such as [3-SAT](/3-sat/), [clique](/clique-problem/) or the [Hamiltonian cycle problem](/hamiltonian-cycle-problem/), is strongly NP-complete. The definition is of interest only for number problems.

**Main consequence.** If $\Pi$ is strongly NP-hard and has a pseudo-polynomial algorithm, then P = NP. Proof: let the algorithm take at most $r(\mathrm{Length}(I), \mathrm{Max}(I))$ steps for a polynomial $r$. On an instance of $\Pi_p$ this is at most $r(\mathrm{Length}(I), p(\mathrm{Length}(I)))$, a polynomial in the length. So $\Pi_p$ is in P. Since $\Pi_p$ is NP-hard, P = NP.

**Unary form.** If $\Pi$ is strongly NP-hard, then $\Pi$ stays NP-hard when its numbers are written in [unary](/unary-encoding/). Proof: an instance $I$ of $\Pi_p$ has a unary encoding of length $O(\mathrm{Length}(I) \cdot (p(\mathrm{Length}(I)) + 1))$, which is polynomial, and it is computed in polynomial time. Composing with a reduction to $\Pi_p$ gives a reduction to the unary form. Many authors use "NP-hard in unary" as the working definition. It is enough for the consequence above, because a pseudo-polynomial algorithm is a polynomial-time algorithm on unary input.

**Pseudo-polynomial transformations.** Strong NP-hardness is usually proved by a reduction from a strongly NP-hard problem that keeps the numbers small. A *pseudo-polynomial transformation* from $\Pi$ to $\Pi'$ is a function $f$ such that:

1. $I$ is a yes-instance of $\Pi$ if and only if $f(I)$ is a yes-instance of $\Pi'$;
2. $f$ is computable in time polynomial in $\mathrm{Length}(I)$ and $\mathrm{Max}(I)$;
3. $\mathrm{Length}(I) \le q_1(\mathrm{Length}'(f(I)))$ for a polynomial $q_1$;
4. $\mathrm{Max}'(f(I)) \le q_2(\mathrm{Max}(I), \mathrm{Length}(I))$ for a polynomial $q_2$.

If $\Pi$ is strongly NP-hard and there is a pseudo-polynomial transformation from $\Pi$ to $\Pi'$, then $\Pi'$ is strongly NP-hard (Garey and Johnson, Section 4.2). An ordinary [polynomial-time reduction](/polynomial-time-reduction/) whose output numbers are polynomially bounded is a special case.

## Examples and non-examples

**3-partition.** The input is $3m$ positive integers $a_i$ and a bound $B$ with $B/4 < a_i < B/2$ and $\sum_i a_i = mB$; the question is whether the numbers split into $m$ triples, each with sum $B$. Garey and Johnson proved it NP-complete in the strong sense by reductions from [three-dimensional matching](/three-dimensional-matching/) that produce numbers polynomial in the size of the matching instance. It is the standard source of strong NP-hardness; see [3-partition](/three-partition/).

**Bin packing.** Map a 3-partition instance to $m$ bins of size $B$ with item sizes $a_i$. The numbers do not change, so this is a pseudo-polynomial transformation, and bin packing is strongly NP-hard. For example, $a = (6, 7, 7, 6, 6, 8)$ with $B = 20$ and $m = 2$ splits as $\{6, 7, 7\}$ and $\{6, 6, 8\}$, so the six items fit into two bins of size 20. The instance $a = (6, 6, 6, 6, 7, 9)$ with $B = 20$ has no such split. See [bin packing NP-hardness](/bin-packing-np-hardness/).

**Scheduling.** One-machine scheduling with release times and deadlines is strongly NP-complete (Garey and Johnson, Theorem 4.5), by a reduction from 3-partition that adds $m - 1$ unit jobs to cut the time line into $m$ gaps of length $B$. See [scheduling with release times and deadlines](/scheduling-with-release-times-and-deadlines/). Makespan minimization on $m$ identical machines, with $m$ part of the input, is also strongly NP-hard; see [makespan minimization](/makespan-minimization/).

**Traveling salesman.** The reduction from the Hamiltonian cycle problem gives distance 1 to edges and 2 to non-edges, so $\mathrm{Max}(I) = 2$. The [traveling salesman problem](/traveling-salesman-problem/) is therefore strongly NP-hard.

**Non-example: subset sum.** The $O(nt)$ dynamic program is pseudo-polynomial, so [subset sum](/subset-sum-problem/) is not strongly NP-hard unless P = NP. The reduction from 3-SAT shows the reason: it writes numbers with one decimal digit for each variable and each clause, so their values grow exponentially with the size of the formula. [Partition](/partition-problem/) and the [knapsack problem](/knapsack-problem/) are non-examples for the same reason.

**Non-example: two machines.** Makespan minimization on two machines is NP-hard by a reduction from partition, but it has a pseudo-polynomial algorithm. So it is only weakly NP-hard. The number of machines is what changes the kind of hardness.

## Related definitions

- **Weak NP-hardness.** An NP-hard problem with a pseudo-polynomial algorithm is [weakly NP-hard](/weak-np-hardness/). Unless P = NP, no problem is both weakly and strongly NP-hard.
- **Pseudo-polynomial time.** The class of algorithms that strong NP-hardness rules out; see [pseudo-polynomial time](/pseudo-polynomial-time/).
- **FPTAS.** A strongly NP-hard optimization problem whose optimum is an integer bounded by a polynomial in the length and the largest number has no [FPTAS](/fptas/) unless P = NP; see [no FPTAS for strongly NP-hard problems](/no-fptas-for-strongly-np-hard-problems/). Weakly NP-hard problems such as knapsack can have one; see the [knapsack FPTAS](/knapsack-fptas/).
- **Unary encoding.** Strong NP-hardness implies NP-hardness for the [unary encoding](/unary-encoding/) of the problem.
- **Lists of problems.** The [Garey and Johnson compendium](/garey-johnson-compendium/) marks the number problems that are NP-complete in the strong sense.

## References

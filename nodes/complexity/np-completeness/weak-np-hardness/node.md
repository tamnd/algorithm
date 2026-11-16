---
tag: R8MN80
kind: definition
slug: weak-np-hardness
name: Weak NP-hardness
aliases:
- weakly NP-hard
area: complexity/np-completeness
level: advanced
summary: A problem is weakly NP-hard when it is NP-hard but has a pseudo-polynomial algorithm, so its hardness needs numbers with many bits.
prereqs: [np-hard, pseudo-polynomial-time, subset-sum-problem]
see_also: [strong-np-hardness, partition-problem, knapsack-problem, subset-sum-fptas, knapsack-fptas, weighted-tardy-jobs, total-tardiness-minimization, three-partition]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 4.2 (number problems, pseudo-polynomial algorithms, and NP-completeness in the strong sense)
  - paper: doi:10.1145/322077.322090
    title: M. R. Garey and D. S. Johnson, "Strong" NP-completeness results, motivation, examples, and implications, Journal of the ACM 25(3), 499 to 508 (1978)
    locator: the discussion of number problems that have pseudo-polynomial algorithms
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 34.5.5, The subset-sum problem (the reduction from 3-CNF-SAT)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 6.4 (the pseudo-polynomial algorithm for subset sum) and Section 8.8 (subset sum is NP-complete)
---

A problem is weakly NP-hard when it is [NP-hard](/np-hard/) and also has a [pseudo-polynomial](/pseudo-polynomial-time/) algorithm, one whose time is polynomial in the input length and in the largest number of the input. The hardness of such a problem needs numbers that are exponentially large in the input length: when the numbers are small, the pseudo-polynomial algorithm is fast. The standard examples are [subset sum](/subset-sum-problem/), [partition](/partition-problem/) and the [knapsack problem](/knapsack-problem/). Unless P = NP, a weakly NP-hard problem is not [strongly NP-hard](/strong-np-hardness/), so the two terms name disjoint groups of NP-hard number problems; the groups need not cover all of them. Some authors call these problems NP-hard in the ordinary sense.

## Definition

**Definition.** A decision or optimization problem $\Pi$ with numbers in its input, written in binary, is *weakly NP-hard* if

1. $\Pi$ is NP-hard under polynomial-time reductions, and
2. $\Pi$ has an algorithm whose time on each instance $I$ is at most a polynomial in $\mathrm{Length}(I)$ and $\mathrm{Max}(I)$, the length of the encoding and the largest number.

If $\Pi$ is also in NP, it is *weakly NP-complete*.

**A second usage.** Some texts call a problem weakly NP-hard, or NP-hard in the ordinary sense, as soon as it is shown NP-hard by a reduction that uses large numbers, for example from partition, and no proof of strong NP-hardness is known. In that usage a pseudo-polynomial algorithm is not required, and the label can change when a strong NP-hardness proof is found. This page uses the first definition, which states a property of the problem and not of the current proofs.

**Relation to strong NP-hardness.** If P $\neq$ NP, no problem is both weakly and strongly NP-hard, because a strongly NP-hard problem has no pseudo-polynomial algorithm unless P = NP. If P = NP, every problem in NP has a polynomial algorithm and the distinction is empty.

**Why the reductions do not contradict the algorithm.** A reduction that proves a weakly NP-hard problem NP-hard must produce numbers whose values are exponential in the input length. The reduction from 3-SAT to subset sum (CLRS, Section 34.5.5) writes numbers with one decimal digit for each variable and each clause. For a formula with $v$ variables and $c$ clauses it makes $2v + 2c$ numbers with $v + c$ digits:

| variables $v$ | clauses $c$ | numbers | digits | bits for each number |
|---|---|---|---|---|
| 3 | 2 | 10 | 5 | about 17 |
| 10 | 40 | 100 | 50 | about 167 |
| 100 | 400 | 1000 | 500 | about 1661 |

The output length grows only quadratically, but the target is about $10^{v+c}$, so the $O(nt)$ dynamic program on the output takes time exponential in the size of the formula.

## Examples and non-examples

**Subset sum and partition.** Both are NP-complete under Karp reductions (Karp 1972), and both are decided by the $O(nt)$ dynamic program. They are weakly NP-complete.

**Knapsack.** The decision version is NP-complete, and the dynamic program over capacities takes $O(nW)$ time. Knapsack is weakly NP-hard; see the [knapsack problem](/knapsack-problem/).

**Two-machine scheduling.** Minimizing the makespan on two identical machines is NP-hard by the reduction from partition, and a subset sum table over the loads of the first machine solves it in pseudo-polynomial time. It is weakly NP-hard. With the number of machines part of the input, the problem becomes strongly NP-hard; see [makespan minimization](/makespan-minimization/).

**Weighted tardy jobs and total tardiness.** Minimizing the weighted number of late jobs on one machine, and minimizing the total tardiness on one machine, are NP-hard and have pseudo-polynomial algorithms. See [weighted tardy jobs](/weighted-tardy-jobs/) and [total tardiness minimization](/total-tardiness-minimization/).

**Non-example: 3-partition and bin packing.** [3-partition](/three-partition/) and [bin packing](/bin-packing-np-hardness/) are strongly NP-hard, so they are not weakly NP-hard unless P = NP. The pair partition and 3-partition shows how a small change in the question moves a problem from one group to the other.

**Non-example: problems without numbers.** 3-SAT and the Hamiltonian cycle problem have no large numbers, so a pseudo-polynomial algorithm for them would be a polynomial-time algorithm. They are strongly NP-complete, not weakly NP-complete, unless P = NP.

## Related definitions

- **Pseudo-polynomial time.** The class of algorithms in condition 2; see [pseudo-polynomial time](/pseudo-polynomial-time/).
- **Strong NP-hardness.** NP-hardness that holds on instances with polynomially bounded numbers; see [strong NP-hardness](/strong-np-hardness/).
- **Unary encoding.** A weakly NP-hard problem is in P when its numbers are written in [unary](/unary-encoding/), because the pseudo-polynomial algorithm is then polynomial in the input length.
- **FPTAS.** Many weakly NP-hard optimization problems have an [FPTAS](/fptas/), often made from the pseudo-polynomial dynamic program by [rounding and scaling](/rounding-and-scaling/), as for [subset sum](/subset-sum-fptas/) and [knapsack](/knapsack-fptas/). This does not follow from weak NP-hardness alone. An FPTAS does not contradict NP-hardness, because it finds an approximate optimum, not an exact one.
- **Weakly polynomial.** A different use of the word "weak": an algorithm is weakly polynomial when its time is polynomial in the bit length but not bounded by a polynomial in the number of input numbers alone, as for the [ellipsoid method](/ellipsoid-method/). This is a property of algorithms, not of hardness.

## References

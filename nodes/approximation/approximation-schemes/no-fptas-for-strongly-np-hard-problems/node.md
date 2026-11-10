---
tag: BZTN2P
kind: theorem
slug: no-fptas-for-strongly-np-hard-problems
name: No FPTAS for strongly NP-hard problems
aliases:
- strong NP-hardness rules out FPTAS
- Garey-Johnson theorem on FPTAS
- FPTAS implies pseudo-polynomial algorithm
area: approximation/approximation-schemes
level: advanced
summary: Unless P=NP, a strongly NP-hard optimization problem with polynomially bounded objective values admits no FPTAS.
prereqs: [fptas, strong-np-hardness, pseudo-polynomial-time]
see_also: [weak-np-hardness, knapsack-fptas, multiple-knapsack-problem, bin-packing, three-partition, makespan-minimization, eptas, rounding-and-scaling]
sources:
  - paper: doi:10.1145/322077.322090
    title: Michael R. Garey and David S. Johnson, "Strong" NP-completeness results, motivation, examples, and implications, Journal of the ACM 25(3), 1978
    locator: pages 499 to 508 (the definition of strong NP-completeness and the theorem on fully polynomial approximation schemes)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 4.2 (number problems and strong NP-completeness) and Chapter 6 (approximation algorithms)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms, Springer, 2001
    locator: Chapter 8, Section 8.3 (strong NP-hardness and the existence of an FPTAS)
  - book: isbn:9783540654315
    title: Giorgio Ausiello, Pierluigi Crescenzi, Giorgio Gambosi, Viggo Kann, Alberto Marchetti-Spaccamela and Marco Protasi, Complexity and Approximation, Springer, 1999
    locator: Chapter 3 (the class FPTAS and pseudo-polynomial algorithms)
---

This theorem of Garey and Johnson (1978) says that a fully polynomial-time approximation scheme can be turned into an exact pseudo-polynomial algorithm, when the optimal value is an integer bounded by a polynomial in the size of the instance and the largest number in it. A [strongly NP-hard](/strong-np-hardness/) problem has no [pseudo-polynomial](/pseudo-polynomial-time/) algorithm unless P = NP. So such a problem, with such an objective, has no [FPTAS](/fptas/) unless P = NP. This is why [bin packing](/bin-packing/), makespan minimization on $m$ machines with $m$ in the input, and the [multiple knapsack problem](/multiple-knapsack-problem/) have no FPTAS, while the [0/1 knapsack problem](/knapsack-problem/), which is only [weakly NP-hard](/weak-np-hardness/), has one. The proof is short: run the scheme with $\varepsilon$ smaller than $1/\mathrm{OPT}$, and the integer answer must be exact.

## Statement

For an instance $I$, let $|I|$ be its length in a binary encoding, and let $\mathrm{Max}(I)$ be the largest absolute value of a number in $I$ (and 1 if there is none). An algorithm is pseudo-polynomial when its time is bounded by a polynomial in $|I|$ and $\mathrm{Max}(I)$. A problem is NP-hard in the strong sense when there is a polynomial $r$ such that the problem restricted to the instances with $\mathrm{Max}(I) \le r(|I|)$ is still NP-hard.

**Theorem (Garey and Johnson, 1978).** Let $\Pi$ be an optimization problem in [NPO](/npo-class/), a minimization or a maximization problem, with these properties:

1. the value of each feasible solution is a non-negative integer, and
2. there is a polynomial $q$ in two variables with $\mathrm{OPT}(I) \le q(|I|, \mathrm{Max}(I))$ for each instance $I$.

If $\Pi$ has an FPTAS, then $\Pi$ has a pseudo-polynomial algorithm that finds an optimal solution.

**Corollary.** If, in addition, $\Pi$ is NP-hard in the strong sense, then $\Pi$ has no FPTAS unless P = NP.

**Corollary (polynomially bounded optimum).** If $\mathrm{OPT}(I) \le q(|I|)$ for a polynomial $q$ in one variable, and $\Pi$ is NP-hard, then $\Pi$ has no FPTAS unless P = NP. Strong NP-hardness is not needed in this case.

## In plain words

An FPTAS can be asked for any accuracy, and it pays only a polynomial price for it. Ask for so much accuracy that the allowed error is less than 1. If the answer is a whole number, an error less than 1 means no error at all, so the scheme now gives the exact optimum.

How much does that cost? The accuracy needed is about one over the optimum. If the optimum is at most a polynomial in the size and the largest number, the cost is polynomial in the size and the largest number. That is a pseudo-polynomial exact algorithm. Strongly NP-hard problems stay hard even when all the numbers are small, so for them such an algorithm would solve an NP-hard problem fast, and P would equal NP.

## Proof

*Proof of the theorem.* Let $A$ be an FPTAS for $\Pi$ with time at most $p(|I|, 1/\varepsilon)$ for a polynomial $p$. We may take $p$ and $q$ with non-negative coefficients, so that both are non-decreasing in each variable. Given an instance $I$:

1. Compute $M = \mathrm{Max}(I)$ by one pass over $I$, and $Q = q(|I|, M)$. This takes time polynomial in $|I|$ and $M$.
2. Run $A$ on $I$ with $\varepsilon = 1 / (Q + 1)$, and return its solution $S$.

*Time.* Step 2 takes at most $p(|I|, Q + 1) = p(|I|, q(|I|, M) + 1)$ steps. This is a polynomial in $|I|$ and $M$, so the algorithm is pseudo-polynomial.

*Correctness, minimization.* The value of $S$ satisfies $\mathrm{OPT} \le c(S) \le (1 + \varepsilon)\,\mathrm{OPT}$. By hypothesis 2, $\varepsilon \cdot \mathrm{OPT} = \mathrm{OPT} / (Q + 1) \le Q / (Q + 1) < 1$. So $\mathrm{OPT} \le c(S) < \mathrm{OPT} + 1$. Both $c(S)$ and $\mathrm{OPT}$ are integers by hypothesis 1, so $c(S) = \mathrm{OPT}$.

*Correctness, maximization.* Here $(1 - \varepsilon)\,\mathrm{OPT} \le c(S) \le \mathrm{OPT}$, and in the same way $\varepsilon \cdot \mathrm{OPT} < 1$, so $\mathrm{OPT} - 1 < c(S) \le \mathrm{OPT}$, and $c(S) = \mathrm{OPT}$. $\blacksquare$

*Proof of the first corollary.* Let $r$ be the polynomial of strong NP-hardness, and let $\Pi_r$ be $\Pi$ restricted to the instances with $\mathrm{Max}(I) \le r(|I|)$. On these instances, the algorithm of the theorem runs in time polynomial in $|I|$ and $r(|I|)$, which is a polynomial in $|I|$. It finds an optimal solution, so it decides the decision form of $\Pi_r$ (is there a solution of value at most, or at least, a bound $B$?) in polynomial time. That decision problem is NP-hard, so P = NP. $\square$

*Proof of the second corollary.* With $\mathrm{OPT}(I) \le q(|I|)$, the same algorithm runs with $\varepsilon = 1/(q(|I|) + 1)$ in time $p(|I|, q(|I|) + 1)$, which is polynomial in $|I|$, and it solves the NP-hard problem $\Pi$ exactly. $\square$

*A check by code.* The [knapsack FPTAS](/knapsack-fptas/) satisfies the hypotheses with $q(|I|, M) = nM$, since $\mathrm{OPT} \le \sum_j p_j \le n \cdot \max_j p_j$. On the instance with profits $56, 22, 12, 45, 58, 53$, weights $2, 7, 3, 8, 9, 6$ and capacity 15, we have $Q = 6 \cdot 58 = 348$, and the run with $\varepsilon = 1/349$ returns profit 131, the optimum found by brute force. With $\varepsilon = 1/2$ the same scheme returns 126. A script with a fixed seed ran the conversion on 300 random instances with $n \le 7$ and numbers up to 60, and the result was equal to the brute-force optimum each time. On the same instances, the run with $\varepsilon = 1/2$ lost up to 4.

## Consequences

- **Bin packing.** [Bin packing](/bin-packing/) is strongly NP-hard, by a reduction from [3-partition](/three-partition/), and $\mathrm{OPT} \le n$. So it has no FPTAS unless P = NP. (It has no PTAS either, by the $3/2$ gap from [partition](/partition-problem/), but it has an [AFPTAS](/asymptotic-ptas/).)
- **Makespan on identical machines.** For $P \| C_{\max}$ with $m$ in the input, the problem is strongly NP-hard, also from 3-partition, and $\mathrm{OPT} \le \sum_j p_j \le n \cdot \mathrm{Max}(I)$. So it has no FPTAS unless P = NP. It has an [EPTAS](/eptas/), so it separates FPTAS from EPTAS. For a fixed $m$, the problem is only weakly NP-hard, and it has an FPTAS.
- **Multiple knapsack.** The [multiple knapsack problem](/multiple-knapsack-problem/) with $m$ in the input is strongly NP-hard. With only two knapsacks it is weakly NP-hard, but with unit profits $\mathrm{OPT} \le n$, and the second corollary shows that it has no FPTAS unless P = NP.
- **Graph problems.** Maximum independent set, minimum vertex cover, graph coloring and max cut have $\mathrm{OPT} \le n$ or $\mathrm{OPT} \le n^2$ and are NP-hard, so by the second corollary none of them has an FPTAS. Most of them have stronger lower bounds from the PCP theorem.
- **Knapsack is consistent with the theorem.** The 0/1 knapsack problem has an FPTAS and a pseudo-polynomial algorithm, the [knapsack dynamic program](/knapsack-dynamic-programming/). It is weakly NP-hard, so the theorem says nothing against it.
- **Design advice.** Before looking for an FPTAS, check whether the problem is strongly NP-hard. If it is, look for an EPTAS or a PTAS instead.

## Tightness

Each hypothesis is needed, and the converse is false.

**The polynomial bound on OPT.** Take [bin packing](/bin-packing/), with $n$ items of integer sizes and a capacity $B$, and change only the objective: a packing with $k$ bins has value $2^{n^2} + k$. The new problem is still NP-hard in the strong sense: the instances and the solutions are those of bin packing, and the optimum of the new problem is $2^{n^2}$ plus the optimum of bin packing. But it has an FPTAS. On input $\varepsilon$:

- If $\varepsilon \ge n / 2^{n^2}$, return the next fit packing. It uses at most $n$ bins, and $\mathrm{OPT} \ge 2^{n^2}$, so its value is at most $2^{n^2} + n \le 2^{n^2}(1 + \varepsilon) \le (1 + \varepsilon)\,\mathrm{OPT}$.
- If $\varepsilon < n / 2^{n^2}$, then $1 / \varepsilon > 2^{n^2} / n$, and we may try all $n^n = 2^{n \log_2 n}$ assignments of items to at most $n$ bins, in time $O(n^{n+1}) \le \mathrm{poly}(1 / \varepsilon)$. This returns the optimum.

So both cases take time polynomial in $|I|$ and $1/\varepsilon$. The theorem does not apply, because $\mathrm{OPT} \ge 2^{n^2}$ is not bounded by a polynomial in $|I|$ and $\mathrm{Max}(I)$. A script checked the first case against the brute-force optimum on 50 random instances with $n \le 5$.

**Integer values.** The proof needs that two different values differ by at least 1. If the values are rationals with a common denominator $D$ bounded by a polynomial, multiply by $D$ and the theorem applies. With arbitrary real values, two values can differ by less than any fixed amount, and the step from $c(S) < \mathrm{OPT} + 1$ to $c(S) = \mathrm{OPT}$ fails. Then the theorem gives no conclusion, and a different argument is necessary.

**The converse is false.** A pseudo-polynomial algorithm does not give an FPTAS. The multiple knapsack problem with two knapsacks has a pseudo-polynomial dynamic program over the pair of loads, in $O(n W_1 W_2)$ time for capacities $W_1$ and $W_2$, but by the second corollary it has no FPTAS unless P = NP.

**Strong NP-hardness alone is not enough.** Strongly NP-hard problems can have a PTAS, and even an EPTAS, such as $P \| C_{\max}$. The theorem rules out only the polynomial dependence on $1/\varepsilon$.

## History

Garey and Johnson introduced strong NP-completeness in their 1978 paper in the Journal of the ACM, to tell apart number problems such as [partition](/partition-problem/), which have pseudo-polynomial algorithms, from problems such as [3-partition](/three-partition/), which stay NP-complete with numbers in unary. In the same paper they proved that a strongly NP-hard optimization problem with a suitably bounded integer objective has no fully polynomial approximation scheme unless P = NP. The first FPTAS, for knapsack and subset sum, was given by Ibarra and Kim in 1975, and the theorem explained why the method did not extend to bin packing and scheduling with many machines. The result is in the book of Garey and Johnson (1979) and in the textbooks of Vazirani (Section 8.3) and Ausiello et al.

## References

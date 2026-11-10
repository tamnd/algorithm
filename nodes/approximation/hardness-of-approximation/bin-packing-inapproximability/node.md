---
tag: 9SGJ55
kind: theorem
slug: bin-packing-inapproximability
name: Bin packing inapproximability
aliases:
- 3/2 bin packing hardness
- no absolute ratio below 3/2 for bin packing
area: approximation/hardness-of-approximation
level: advanced
summary: Unless P = NP, no polynomial algorithm always uses fewer than 3/2 times the optimal number of bins (a gap reduction from partition). Asymptotic schemes are not ruled out.
prereqs: [bin-packing, partition-problem, gap-problem, approximation-ratio]
see_also: [bin-packing-np-hardness, first-fit-decreasing, bin-packing-aptas, karmarkar-karp-bin-packing, asymptotic-ptas, fernandez-de-la-vega-lueker-aptas, no-fptas-for-strongly-np-hard-problems, scheduling-makespan-inapproximability]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Appendix A3.2, problem SP12 (Partition), and A4.1, problem SR1 (Bin packing)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 3.3 (bin packing, the 3/2 hardness from partition and the asymptotic scheme)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 9 (bin packing, the 3/2 hardness and the asymptotic PTAS)
  - paper: doi:10.1007/BF02579456
    title: "W. Fernandez de la Vega and G. S. Lueker, Bin packing can be solved within 1 + ε in linear time, Combinatorica 1(4), 1981"
    locator: the asymptotic scheme with (1 + ε) OPT + 1 bins
  - paper: "N. Karmarkar and R. M. Karp, An efficient approximation scheme for the one-dimensional bin-packing problem, Proceedings of the 23rd IEEE Symposium on Foundations of Computer Science (FOCS), 1982"
    locator: the algorithm with OPT + O(log² OPT) bins
  - paper: "R. Hoberg and T. Rothvoss, A logarithmic additive integrality gap for bin packing, Proceedings of the 28th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2017"
    locator: the algorithm with OPT + O(log OPT) bins
  - paper: "N. Bansal, J. R. Correa, C. Kenyon and M. Sviridenko, Bin packing in multiple dimensions: inapproximability results and approximation schemes, Mathematics of Operations Research 31(1), 2006"
    locator: no asymptotic PTAS for two-dimensional geometric bin packing unless P = NP
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: "R. M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, 1972"
    locator: the NP-completeness of partition
---

The bin packing inapproximability theorem says that, unless P = NP, no polynomial-time algorithm packs every list into fewer than $\frac32 \mathrm{OPT}$ bins. The proof is a [gap reduction](/gap-problem/) from [partition](/partition-problem/): deciding whether $\mathrm{OPT} = 2$ or $\mathrm{OPT} \ge 3$ is already NP-hard. The bound holds only for absolute ratios. It says nothing against an asymptotic bound of the form $(1 + \varepsilon)\mathrm{OPT} + 1$, and such [asymptotic schemes](/bin-packing-aptas/) exist.

## Statement

Notation is as on [bin packing](/bin-packing/): $n$ items with integer sizes $a_1, \ldots, a_n$, bins of integer capacity $C$ with $a_i \le C$, and $\mathrm{OPT}$ the least number of bins. $\mathrm{ALG}$ is the number of bins an algorithm uses. For this minimization problem, an absolute ratio $\rho \ge 1$ means $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every list, and an asymptotic guarantee means $\mathrm{ALG} \le \rho \cdot \mathrm{OPT} + c$ for a constant $c$.

**Theorem.**

1. For every fixed integer $k \ge 2$, the problem "is $\mathrm{OPT} \le k$?" is NP-complete.
2. Let $\rho < \frac32$. If a polynomial-time algorithm satisfies $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every list, then P = NP.
3. More generally, let $\rho \ge 1$ and $c \ge 0$ satisfy $(\rho - 1) k + c < 1$ for some integer $k \ge 2$. If a polynomial-time algorithm satisfies $\mathrm{ALG} \le \rho \cdot \mathrm{OPT} + c$ on every list, then P = NP.

Part 2 is part 3 with $k = 2$ and $c = 0$. Part 3 with $\rho = 1$ says that a polynomial algorithm with $\mathrm{ALG} \le \mathrm{OPT} + c$ needs $c \ge 1$.

## In plain words

Suppose you could always tell, fast, whether a pile of objects fits into two boxes. Then you could tell whether a list of numbers splits into two halves with equal sums, which is a famous hard question. So the box question is hard already for two boxes.

A fast method that always used less than one and a half times the best number of boxes would use two boxes whenever two are enough, because three is too many. So it would answer the hard question. Adding full boxes moves the same question to any number of boxes. The hardness is always about one box more or less. For large inputs, one extra box is a tiny fraction, so fast methods can come very close to the best in proportion.

## Proof

*Membership in NP.* A certificate maps each item to one of $k$ bins. Checking the $k$ loads takes $O(n + k)$ additions.

*The reduction.* An instance of [partition](/partition-problem/) is a list of positive integers $a_1, \ldots, a_n$ with $n \ge 2$, and the question is whether a subset has sum exactly half of the total. Partition is NP-complete (Karp 1972; Garey and Johnson, problem SP12). Fix $k \ge 2$.

- If the total is odd, or some $a_i$ is more than half of the total, the answer is no. Map the instance to $k + 1$ items of size 1 with capacity 1, which needs exactly $k + 1$ bins.
- Otherwise let the total be $2B$, so $a_i \le B$ for each $i$. Map the instance to capacity $C = B$ and the list $a_1, \ldots, a_n$ followed by $k - 2$ items of size $B$.

The new list has $n + k - 2$ items, each at most $C$, and the numbers do not grow. So the map takes polynomial time.

*Completeness.* If a subset $T$ has sum $B$, then $T$ and its complement fill two bins exactly, and each item of size $B$ fills one more bin. So $\mathrm{OPT} \le k$.

*Soundness.* Suppose $k$ bins suffice. The total size is $2B + (k - 2) B = kB$, and each bin holds at most $B$, so each of the $k$ bins holds exactly $B$. An item of size $B$ fills its bin alone. So the $k - 2$ items of size $B$ fill $k - 2$ bins, and the original items fill the other two bins exactly. The items of one of these bins are a subset with sum $B$, and the partition instance is a yes-instance.

The total size $kB$ forces $\mathrm{OPT} \ge k$ in all cases. So the partition instance is a yes-instance if and only if $\mathrm{OPT} = k$, and a no-instance if and only if $\mathrm{OPT} \ge k + 1$. This proves part 1.

*Part 3.* Run the algorithm on the list for the integer $k$ of the hypothesis. On a yes-instance, $\mathrm{ALG} \le \rho k + c < k + 1$, and $\mathrm{ALG}$ is an integer, so $\mathrm{ALG} \le k$. On a no-instance, $\mathrm{ALG} \ge \mathrm{OPT} \ge k + 1$. So the test "$\mathrm{ALG} \le k$" decides partition in polynomial time, and P = NP. $\blacksquare$

### Example

The list $5, 6, 7, 8, 9, 11$ has total 46, so $B = 23$, and $\{5, 7, 11\}$ and $\{6, 8, 9\}$ show $\mathrm{OPT} = 2$. [First fit decreasing](/first-fit-decreasing/) packs $[11\ 9]$, $[8\ 7\ 6]$, $[5]$ and uses 3 bins, which is $\frac32 \mathrm{OPT}$. The list $2, 2, 3, 5$ has total 12 and $B = 6$, but no subset sums to 6, so $\mathrm{OPT} = 3$ with capacity 6. With $k = 4$, the first list gets two more items of size 23, and then $\mathrm{OPT} = 4$; the second list gets two items of size 6, and then $\mathrm{OPT} = 5$.

## Consequences

- **No absolute PTAS.** Part 2 rules out an algorithm with $\mathrm{ALG} \le (1 + \varepsilon)\mathrm{OPT}$ for $\varepsilon < \frac12$. With $\mathrm{OPT} \le n$, the general theorem on [strongly NP-hard problems](/no-fptas-for-strongly-np-hard-problems/) also rules out an FPTAS, using the [strong NP-hardness](/bin-packing-np-hardness/) of bin packing.
- **Asymptotic schemes are not ruled out.** Part 3 applies only when $(\rho - 1)k + c < 1$ for some $k \ge 2$, so only when $c < 1$ and $\rho$ is close to 1. The [asymptotic scheme](/fernandez-de-la-vega-lueker-aptas/) of Fernandez de la Vega and Lueker (1981) uses at most $(1 + \varepsilon)\mathrm{OPT} + 1$ bins for each fixed $\varepsilon > 0$. With $c = 1$, the condition reads $(\rho - 1)k < 0$, which no $k$ meets. So bin packing has an [asymptotic PTAS](/asymptotic-ptas/), and the hardness of part 2 is a statement about small optima.
- **Additive guarantees.** [Karmarkar and Karp](/karmarkar-karp-bin-packing/) (1982) use $\mathrm{OPT} + O(\log^2 \mathrm{OPT})$ bins, and Hoberg and Rothvoss (2017) use $\mathrm{OPT} + O(\log \mathrm{OPT})$. Part 3 says that $\mathrm{OPT} + c$ with $c < 1$ is impossible unless P = NP. Whether $\mathrm{OPT} + 1$ is possible in polynomial time is open.
- **Related problems.** "Is $\mathrm{OPT} \le 2$?" for bin packing is the same question as "is the makespan on two machines at most $B$?", so the reduction also shows that $P2 \mid\mid C_{\max}$ is NP-hard. It does not give a constant gap there, because the makespan is not an integer count; see [scheduling makespan inapproximability](/scheduling-makespan-inapproximability/).

## Tightness

The constant $\frac32$ is tight for the absolute ratio: [first fit decreasing](/first-fit-decreasing/) satisfies $\mathrm{FFD} \le \frac32 \mathrm{OPT}$ on every list, and the example above shows that this is reached. So the absolute approximation threshold of bin packing is exactly $\frac32$, unless P = NP.

The condition of part 3 is the exact reach of this reduction. On the lists of the reduction, $\mathrm{OPT}$ is $k$ or $k + 1$, and an algorithm that always uses $\mathrm{OPT} + 1$ bins would return $k + 1$ in both cases, so it would not separate them. For more than one dimension the picture changes: two-dimensional geometric bin packing has no asymptotic PTAS unless P = NP (Bansal, Correa, Kenyon and Sviridenko 2006), so there the hardness holds also for large optima.

## History

The reduction from partition is the standard textbook argument; Garey and Johnson list bin packing as problem SR1 and partition as SP12. Vazirani (Chapter 9) and Williamson and Shmoys (Section 3.3) use it to motivate asymptotic ratios. Fernandez de la Vega and Lueker (1981) gave the first asymptotic scheme, Karmarkar and Karp (1982) the first additive $O(\log^2 \mathrm{OPT})$ bound, and Hoberg and Rothvoss (2017) improved it to $O(\log \mathrm{OPT})$.

## References

---
tag: KVD1F4
kind: theorem
slug: scheduling-makespan-inapproximability
name: Makespan scheduling inapproximability
aliases:
- P||Cmax hardness
- makespan hardness by machine model
- integer gap lemma for scheduling
area: approximation/hardness-of-approximation
level: advanced
summary: Makespan hardness by machine model. Identical machines have a PTAS but no FPTAS, unrelated machines have no ratio below 3/2, and unit jobs with precedence have none below 4/3.
prereqs: [makespan-minimization, scheduling-notation, gap-problem, strong-np-hardness]
see_also: [unrelated-makespan-inapproximability, precedence-constrained-scheduling, no-fptas-for-strongly-np-hard-problems, hochbaum-shmoys-ptas, lenstra-shmoys-tardos, bin-packing-inapproximability, restricted-assignment-scheduling, machine-environments]
sources:
  - paper: doi:10.1287/opre.26.1.22
    title: J. K. Lenstra and A. H. G. Rinnooy Kan, Complexity of scheduling under precedence constraints, Operations Research 26(1), 1978
    locator: makespan 3 for unit jobs with precedence is NP-complete
  - paper: doi:10.1007/BF01585745
    title: J. K. Lenstra, D. B. Shmoys and É. Tardos, Approximation algorithms for scheduling unrelated parallel machines, Mathematical Programming 46, 1990
    locator: makespan 2 for unrelated machines is NP-complete, and the 2-approximation
  - paper: doi:10.1145/322077.322090
    title: M. R. Garey and D. S. Johnson, "Strong" NP-completeness results, motivation, examples, and implications, Journal of the ACM 25(3), 1978
    locator: strong NP-hardness and the absence of fully polynomial schemes
  - paper: doi:10.1145/7531.7535
    title: D. S. Hochbaum and D. B. Shmoys, Using dual approximation algorithms for scheduling problems, theoretical and practical results, Journal of the ACM 34(1), 1987
    locator: the PTAS for P||Cmax
  - paper: "D. P. Williamson, L. A. Hall, J. A. Hoogeveen, C. A. J. Hurkens, J. K. Lenstra, S. V. Sevast'janov and D. B. Shmoys, Short shop schedules, Operations Research 45(2), 1997"
    locator: makespan 4 is NP-complete to decide for flow, job and open shops, so no ratio below 5/4
  - paper: "O. Svensson, Conditional hardness of precedence constrained scheduling on identical machines, Proceedings of the 42nd ACM Symposium on Theory of Computing (STOC), 2010"
    locator: no ratio 2 - ε for P|prec|Cmax under a variant of the unique games conjecture
  - paper: "T. Ebenlendr, M. Krčál and J. Sgall, Graph balancing: a special case of scheduling unrelated parallel machines, Algorithmica 68(1), 2014"
    locator: the 3/2 bound holds when each job may run on only two machines
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Sections 3.2 and 11.1 (the PTAS for identical machines and the 3/2 bound for unrelated machines)
---

The hardness of makespan scheduling depends on the machine model. For identical machines, $P \mid\mid C_{\max}$, the problem is strongly NP-hard, so it has no FPTAS, but it has a PTAS, so no constant ratio above 1 is ruled out. For [unrelated machines](/unrelated-makespan-inapproximability/), $R \mid\mid C_{\max}$, no ratio below $\frac32$ is possible unless P = NP. For unit jobs with [precedence constraints](/precedence-constrained-scheduling/), no ratio below $\frac43$ is possible, and for shop scheduling none below $\frac54$. All the constant bounds come from one simple lemma: when the makespan is an integer and deciding "makespan at most $t$" is NP-hard, every ratio below $\frac{t+1}{t}$ is NP-hard. This page proves the lemma and collects the results; the reductions are on the linked pages.

## Statement

Notation is the three-field notation of [scheduling](/scheduling-notation/). $\mathrm{OPT}$ is the least makespan, and a ratio $\rho \ge 1$ means a schedule of makespan at most $\rho \cdot \mathrm{OPT}$ on every instance, with the number of machines part of the input.

**Lemma (integer gap).** Let a scheduling problem have integer makespans, and let deciding $\mathrm{OPT} \le t$ be NP-hard for a fixed integer $t \ge 1$. Then for each $\rho < \frac{t + 1}{t}$, a polynomial algorithm with ratio $\rho$ gives P = NP.

**Theorem.** Unless P = NP, the following hold.

| problem | hardness | proved on | best known ratio |
|---|---|---|---|
| $P \mid\mid C_{\max}$ | strongly NP-hard, no FPTAS | [makespan minimization](/makespan-minimization/) | PTAS (Hochbaum and Shmoys 1987) |
| $Q \mid\mid C_{\max}$ | strongly NP-hard, no FPTAS | contains $P \mid\mid C_{\max}$ | PTAS (Hochbaum and Shmoys 1988) |
| $Pm \mid\mid C_{\max}$, $Rm \mid\mid C_{\max}$, fixed $m$ | NP-hard in the weak sense | partition | FPTAS |
| $R \mid\mid C_{\max}$ and $P \mid M_j \mid C_{\max}$ | no ratio below $\frac32$ | [unrelated makespan inapproximability](/unrelated-makespan-inapproximability/) | 2 (Lenstra, Shmoys and Tardos) |
| $P \mid \mathrm{prec}, p_j = 1 \mid C_{\max}$ | no ratio below $\frac43$ | [precedence-constrained scheduling](/precedence-constrained-scheduling/) | $2 - \frac1m$ (Graham) |
| $F \mid\mid C_{\max}$, $J \mid\mid C_{\max}$, $O \mid\mid C_{\max}$ | no ratio below $\frac54$ | Williamson et al. (1997), cited | depends on the shop |

## In plain words

Schedule lengths here are whole numbers. Suppose it is hard to tell whether a set of jobs can finish by time 3. A fast method that always comes within less than one third over the best length would answer the question: when the best is 3, the method gives less than 4, so 3; when the best is 4 or more, it gives at least 4. So hardness at a small time gives a fixed hardness ratio.

For identical machines, the hard questions need large times, because a fast method can come as close to the best as you want. Here the hardness only rules out the fastest kind of scheme. For machines with different speeds per job, and for jobs that must wait for others, the hard questions are at times 2 and 3. This gives the ratios one and a half and four thirds.

## Proof

*The lemma.* Let $A$ have ratio $\rho < \frac{t+1}{t}$. If $\mathrm{OPT} \le t$, then $A$ returns a makespan at most $\rho \, \mathrm{OPT} \le \rho t < t + 1$, and the makespan is an integer, so it is at most $t$. If $\mathrm{OPT} \ge t + 1$, then $A$ returns at least $t + 1$. So "is the makespan of $A$ at most $t$?" decides the NP-hard question in polynomial time. $\blacksquare$

*Unrelated machines.* Lenstra, Shmoys and Tardos show that deciding $\mathrm{OPT} \le 2$ is NP-complete, with times in $\{1, 2, \infty\}$, by a reduction from three-dimensional matching. The lemma with $t = 2$ gives $\frac32$. The reduction is proved on the [unrelated makespan inapproximability](/unrelated-makespan-inapproximability/) page. Ebenlendr, Krčál and Sgall (2014) showed that the bound holds even when each job may run on only two machines.

*Unit jobs with precedence.* Lenstra and Rinnooy Kan (1978) reduce from clique. For a graph with $n_V$ vertices and $n_E$ edges and an integer $k$, there is a job for each vertex and each edge, with an arc from each vertex to each edge on it, and three layers of filler jobs that force the three time slots to hold exactly $k$, $\binom{k}{2} + n_V - k$ and $n_E - \binom{k}{2}$ graph jobs. A schedule of makespan 3 exists if and only if the graph has a clique on $k$ vertices. The full proof is on the [precedence-constrained scheduling](/precedence-constrained-scheduling/) page, and the code for this page checks the equivalence by brute force on small graphs. The lemma with $t = 3$ gives $\frac43$.

*Shops.* Williamson et al. (1997) show that deciding makespan at most 4 is NP-complete for flow shops, job shops and open shops with integer times, while makespan at most 3 is decidable in polynomial time. The lemma with $t = 4$ gives $\frac54$. This reduction is cited.

*Identical machines.* Here the lemma gives nothing. Deciding $\mathrm{OPT} \le t$ for a fixed $t$ is polynomial: jobs with $p_j > t$ make the answer no, and the others have at most $t$ distinct times, so the machine configurations can be counted by a dynamic program, which is the core of the [PTAS](/hochbaum-shmoys-ptas/). What remains is the strong NP-hardness from [3-partition](/three-partition/), proved on the [makespan minimization](/makespan-minimization/) page. With $\mathrm{OPT} \le \sum_j p_j$, an FPTAS run with $\varepsilon < 1 / \sum_j p_j$ would solve the problem exactly in pseudo-polynomial time, which rules out an FPTAS ([no FPTAS for strongly NP-hard problems](/no-fptas-for-strongly-np-hard-problems/)).

### Example

On the triangle with $k = 3$, the instance has $m = \max(3, 3, 0) + 1 = 4$ machines and $12$ unit jobs, and a schedule of makespan 3 exists. On the path with two edges and $k = 3$, the same construction has no schedule of makespan 3, but has one of makespan 4. An algorithm with ratio below $\frac43$ would return 3 on the first instance and at least 4 on the second.

## Consequences

- **Where the thresholds are known.** For $P \mid\mid C_{\max}$ and $Q \mid\mid C_{\max}$ the threshold is 1, reached by PTASs, and the question is how fast the scheme can be. Under the exponential time hypothesis, the time of a PTAS for $P \mid\mid C_{\max}$ must grow like $2^{(1/\varepsilon)^{1 - \delta}}$ (Chen, Jansen and Zhang 2014). For fixed $m$ the threshold is 1 with an FPTAS.
- **Where they are open.** For $R \mid\mid C_{\max}$ the gap is between $\frac32$ and 2. For $P \mid \mathrm{prec} \mid C_{\max}$ it is between $\frac43$ and 2, and Svensson (2010) showed that $2 - \varepsilon$ is hard under a variant of the [unique games conjecture](/unique-games-conjecture/) due to Bansal and Khot.
- **Bin packing.** The [bin packing](/bin-packing-inapproximability/) bound $\frac32$ uses the same lemma, with the number of bins as the integer objective and $t = 2$. For $P \mid\mid C_{\max}$ the same reduction from partition does not give a gap, because the makespan, not the number of machines, is the objective.

## Tightness

The lemma is tight for the reductions it uses: an instance family with $\mathrm{OPT} \in \{t, t + 1\}$ cannot give a gap larger than $\frac{t+1}{t}$. To get larger bounds one needs instances with $\mathrm{OPT}$ at most $t$ against a much larger value, as in Svensson's conditional result. The bound $\frac32$ for unrelated machines is not known to be tight, and the best ratio is $2 - \frac1m$, or 2 for the LP rounding.

## History

Garey and Johnson (1978) introduced strong NP-hardness and showed that it rules out fully polynomial schemes. Lenstra and Rinnooy Kan (1978) proved the $\frac43$ bound for unit jobs with precedence, one of the first hardness results for approximation. Hochbaum and Shmoys gave the PTAS for identical machines in 1987 and for uniform machines in 1988. Lenstra, Shmoys and Tardos (1990) proved the $\frac32$ bound and the 2-approximation for unrelated machines. Williamson et al. (1997) proved the $\frac54$ bound for shops, and Svensson (2010) the conditional $2 - \varepsilon$ for precedence constraints.

## References

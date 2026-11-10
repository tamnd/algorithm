---
tag: JHS8TD
kind: definition
slug: fptas
name: Fully polynomial-time approximation scheme (FPTAS)
aliases:
- FPTAS
- fully polynomial approximation scheme
- fully polynomial time approximation scheme
area: approximation/approximation-schemes
level: core
summary: A PTAS whose running time is also polynomial in 1/ε, the strongest approximation scheme for optimization problems.
prereqs: [ptas, approximation-ratio, pseudo-polynomial-time]
see_also: [eptas, knapsack-fptas, subset-sum-fptas, rounding-and-scaling, trimming-technique, no-fptas-for-strongly-np-hard-problems, strong-np-hardness, asymptotic-ptas]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 3, Section 3.1 (the definition of an FPTAS and the knapsack scheme)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms, Springer, 2001
    locator: Chapter 8 (Knapsack), Sections 8.2 and 8.3 (the FPTAS and strong NP-hardness)
  - book: isbn:9783540654315
    title: Giorgio Ausiello, Pierluigi Crescenzi, Giorgio Gambosi, Viggo Kann, Alberto Marchetti-Spaccamela and Marco Protasi, Complexity and Approximation, Springer, 1999
    locator: Chapter 3 (the classes PTAS and FPTAS)
  - paper: doi:10.1145/321906.321909
    title: Oscar H. Ibarra and Chul E. Kim, Fast approximation algorithms for the knapsack and sum of subset problems, Journal of the ACM 22(4), 1975
    locator: pages 463 to 468
  - paper: doi:10.1145/322077.322090
    title: Michael R. Garey and David S. Johnson, "Strong" NP-completeness results, motivation, examples, and implications, Journal of the ACM 25(3), 1978
    locator: pages 499 to 508
  - title: Noga Alon, Yossi Azar, Gerhard J. Woeginger and Tal Yadid, Approximation schemes for scheduling on parallel machines, Journal of Scheduling 1(1), 1998
    locator: the linear-time approximation scheme for makespan on identical machines
---

A fully polynomial-time approximation scheme, or FPTAS, is an algorithm that takes an instance and an accuracy $\varepsilon > 0$, and returns a solution within a factor $1 + \varepsilon$ of the optimum (or $1 - \varepsilon$ for a maximization problem), in time polynomial in both the size of the instance and $1 / \varepsilon$. It is the strongest kind of approximation scheme: the cost of more accuracy grows only polynomially. The [knapsack FPTAS](/knapsack-fptas/) of Ibarra and Kim, in $O(n^3 / \varepsilon)$ time, is the standard example. An FPTAS gives an exact [pseudo-polynomial](/pseudo-polynomial-time/) algorithm, so [strongly NP-hard](/strong-np-hardness/) problems with polynomially bounded integer objectives have no FPTAS unless P = NP. With P ≠ NP, the class FPTAS is strictly smaller than the class [EPTAS](/eptas/).

## Definition

Let $\Pi$ be an optimization problem in [NPO](/npo-class/), with the ratio conventions of [the approximation ratio](/approximation-ratio/) page: $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ with $\rho \ge 1$ for minimization, and $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha \le 1$ for maximization.

An algorithm $A$ is a **fully polynomial-time approximation scheme** for $\Pi$ when, on input an instance $I$ and a rational number $0 < \varepsilon \le 1$, it returns a feasible solution of $I$ with

$$
\mathrm{ALG}(I, \varepsilon) \le (1 + \varepsilon) \cdot \mathrm{OPT}(I) \ \ \text{(minimization)}, \qquad \mathrm{ALG}(I, \varepsilon) \ge (1 - \varepsilon) \cdot \mathrm{OPT}(I) \ \ \text{(maximization)},
$$

and its running time is bounded by a polynomial in $|I|$ and $1 / \varepsilon$. The class **FPTAS** is the set of NPO problems that have such an algorithm.

Notes on the definition:

- **The time is polynomial in 1/ε, not in log(1/ε).** The bound $1 / \varepsilon$ is the value, as if $\varepsilon$ were given in unary. A time such as $O(n^2 / \varepsilon^3)$ is allowed, and a time $O(n \cdot 2^{1/\varepsilon})$ is not.
- **The guarantee is absolute.** It holds on every instance, not only for large optima. The asymptotic form is the AFPTAS, on the [asymptotic PTAS](/asymptotic-ptas/) page.
- **ε up to 1.** The restriction $\varepsilon \le 1$ is only for comfort. For a maximization problem the bound $1 - \varepsilon$ means nothing for $\varepsilon \ge 1$, and for a minimization problem a larger $\varepsilon$ can be replaced by 1.
- **Some books write the maximization bound as OPT/(1 + ε).** Since $1/(1 + \varepsilon) \ge 1 - \varepsilon$ and $1 - \varepsilon/2 \ge 1/(1 + \varepsilon)$ for $\varepsilon \le 1$, the two forms differ only by a factor 2 in $\varepsilon$, and they define the same class.
- **An FPTAS is a PTAS.** For each fixed $\varepsilon$, the time is a polynomial in $|I|$, so an FPTAS is a [PTAS](/ptas/), and also an EPTAS, because $\mathrm{poly}(|I|, 1/\varepsilon) \le \mathrm{poly}(1/\varepsilon) \cdot \mathrm{poly}(|I|)$.

**The conversion to an exact algorithm.** Let the values be integers, and let $\mathrm{OPT}(I) \le q(|I|, \mathrm{Max}(I))$ for a polynomial $q$, where $\mathrm{Max}(I)$ is the largest number in $I$. Run the FPTAS with $\varepsilon = 1 / (q + 1)$. For minimization, $\mathrm{ALG} \le \mathrm{OPT} + \varepsilon \, \mathrm{OPT} < \mathrm{OPT} + 1$, so $\mathrm{ALG} = \mathrm{OPT}$; maximization is the same. The time is polynomial in $|I|$ and $\mathrm{Max}(I)$, so this is a pseudo-polynomial exact algorithm. This is the theorem of Garey and Johnson (1978); its full proof, with the hypotheses, is on the page [no FPTAS for strongly NP-hard problems](/no-fptas-for-strongly-np-hard-problems/).

## Examples and non-examples

**The 0/1 knapsack problem.** The [knapsack FPTAS](/knapsack-fptas/) divides the profits by $K = \varepsilon P / n$, where $P$ is the largest profit of an item that fits alone, rounds down, and solves the rounded instance by the [profit-indexed dynamic program](/profit-indexed-dynamic-programming/). It returns a set of profit at least $(1 - \varepsilon) \cdot \mathrm{OPT}$ in $O(n^3 / \varepsilon)$ time. With a greedy lower bound in place of $P$, the time is $O(n^2 / \varepsilon)$. This is the general method of [rounding and scaling](/rounding-and-scaling/).

**Subset sum.** The [subset sum FPTAS](/subset-sum-fptas/) keeps the sorted list of reachable sums and [trims](/trimming-technique/) it with the factor $1 + \varepsilon / (2n)$. It returns a sum of at least $\mathrm{OPT} / (1 + \varepsilon)$ in $O(n^2 \log t / \varepsilon)$ time, where $t$ is the target.

**Other problems with an FPTAS.** The [bounded](/bounded-knapsack/) and [unbounded knapsack](/unbounded-knapsack/) problems, the [constrained shortest path](/constrained-shortest-path/) problem (Hassin, 1992), and [makespan minimization](/makespan-minimization/) on a fixed number $m$ of identical machines (Sahni, 1976) all have one. In each case the exact algorithm is pseudo-polynomial, and rounding or trimming makes it polynomial.

**What the polynomial in 1/ε buys.** For a knapsack instance with $n = 100$ and $\varepsilon = 0.1$, the FPTAS does about $n^3 / \varepsilon = 10^7$ steps. A PTAS with time $n^{1/\varepsilon}$, such as the partial enumeration scheme on the [PTAS](/ptas/) page, does about $100^{10} = 10^{20}$ steps. The difference is the reason to look for an FPTAS first.

**Non-example: strongly NP-hard problems.** [Bin packing](/bin-packing/), [makespan minimization](/makespan-minimization/) with the number of machines in the input, and the [3-partition](/three-partition/) based problems are strongly NP-hard, and their optimal values are integers bounded by a polynomial in the size and the largest number. By the conversion above, an FPTAS for any of them would give a pseudo-polynomial algorithm for a strongly NP-hard problem, which implies P = NP. So none of them has an FPTAS unless P = NP.

**Non-example: multiple knapsack with two knapsacks.** The [multiple knapsack problem](/multiple-knapsack-problem/) with only two knapsacks of the same capacity is not strongly NP-hard, but it still has no FPTAS unless P = NP (Chekuri and Khanna). Give each item profit 1. Then $\mathrm{OPT} \le n$, and an FPTAS with $\varepsilon = 1/(n + 1)$ would be exact in polynomial time, so it would decide the [partition problem](/partition-problem/): all items fit exactly when the numbers split into two halves of equal sum. The conversion needs only a polynomial bound on $\mathrm{OPT}$ in terms of the size, and here the bound is $n$.

**Non-example: a PTAS with time n^(1/ε).** A scheme with time $O(n^{\lceil 1/\varepsilon \rceil})$ is a PTAS but not an FPTAS, because the exponent of $n$ grows with $1/\varepsilon$.

**The separation FPTAS ⊊ EPTAS (if P ≠ NP).** Makespan minimization on identical machines, $P \| C_{\max}$, has an EPTAS: Alon, Azar, Woeginger and Yadid (1998) gave a scheme with time $f(1/\varepsilon) + O(n)$, by integer programming in fixed dimension. The problem is strongly NP-hard, from 3-partition, and its makespan is an integer of at most $\sum_j p_j \le n \cdot \max_j p_j$. So it has no FPTAS unless P = NP. The multiple knapsack problem gives a second separation: it has an EPTAS (Jansen, 2010) and, as above, no FPTAS.

## Related definitions

- **PTAS and EPTAS.** A [PTAS](/ptas/) only needs time polynomial in $|I|$ for each fixed $\varepsilon$, and an [EPTAS](/eptas/) needs time $f(1/\varepsilon) \cdot \mathrm{poly}(|I|)$. Under P ≠ NP, $\mathrm{FPTAS} \subsetneq \mathrm{EPTAS} \subsetneq \mathrm{PTAS}$, where the second step needs the stronger assumption [FPT ≠ W[1]](/fpt-w1-conjecture/).
- **AFPTAS.** An asymptotic FPTAS guarantees $\mathrm{ALG} \le (1 + \varepsilon)\mathrm{OPT} + c$, in time polynomial in $|I|$ and $1/\varepsilon$, where $c$ may be a polynomial in $1/\varepsilon$. The [Karmarkar and Karp algorithm](/karmarkar-karp-bin-packing/) for bin packing gives one. See the [asymptotic PTAS](/asymptotic-ptas/) page.
- **Pseudo-polynomial time and strong NP-hardness.** A problem is [weakly NP-hard](/weak-np-hardness/) when it is NP-hard but has a [pseudo-polynomial](/pseudo-polynomial-time/) algorithm. Most problems with an FPTAS are of this kind. A [strongly NP-hard](/strong-np-hardness/) problem stays NP-hard when the numbers are written in unary.
- **Approximate Pareto sets.** For problems with several objectives, the analog of an FPTAS is an algorithm that builds an [approximate Pareto set](/approximate-pareto-set/) in time polynomial in the size and $1/\varepsilon$.

## References

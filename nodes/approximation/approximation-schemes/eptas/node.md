---
tag: K5VFG3
kind: definition
slug: eptas
name: Efficient polynomial-time approximation scheme (EPTAS)
aliases:
- EPTAS
- efficient PTAS
- efficient polynomial time approximation scheme
area: approximation/approximation-schemes
level: advanced
summary: A PTAS whose running time has the form f(1/ε)·poly(n) with the dependence on n separated from ε.
prereqs: [ptas, fixed-parameter-tractable, w-hierarchy]
see_also: [ptas, fptas, fpt-w1-conjecture, fpt-approximation, parameterized-inapproximability, baker-technique, chekuri-khanna-ptas, epstein-levin-eptas-bin-packing]
sources:
  - title: Marco Cesati and Luca Trevisan, On the efficiency of polynomial time approximation schemes, Information Processing Letters 64(4), 1997
    locator: pages 165 to 171 (the definition of an EPTAS and the link to fixed-parameter tractability)
  - title: Dániel Marx, Parameterized complexity and approximation algorithms, The Computer Journal 51(1), 2008
    locator: the section on efficient approximation schemes
  - title: Dániel Marx, Efficient approximation schemes for geometric problems?, Proceedings of ESA 2005, Lecture Notes in Computer Science 3669
    locator: the W[1]-hardness of independent set in unit disk graphs
  - paper: doi:10.1137/080731207
    title: Klaus Jansen, Parameterized approximation scheme for the multiple knapsack problem, SIAM Journal on Computing 39(4), 2010
    locator: pages 1392 to 1412
  - title: Noga Alon, Yossi Azar, Gerhard J. Woeginger and Tal Yadid, Approximation schemes for scheduling on parallel machines, Journal of Scheduling 1(1), 1998
    locator: the linear-time approximation scheme for makespan on identical machines
---

An efficient polynomial-time approximation scheme, or EPTAS, is a [PTAS](/ptas/) whose running time has the form $f(1/\varepsilon) \cdot \mathrm{poly}(n)$: the accuracy may cost any amount, but it must not appear in the exponent of $n$. A PTAS with time $n^{1/\varepsilon}$ is not efficient in this sense, and one with time $2^{1/\varepsilon} \cdot n$ is. The notion comes from parameterized complexity. An EPTAS for a problem with integer values gives a [fixed-parameter tractable](/fixed-parameter-tractable/) algorithm for its standard parameterization, so a W[1]-hard parameterized problem has no EPTAS unless FPT = W[1]. This is how one shows that a problem with a PTAS has no EPTAS. Under P ≠ NP and [FPT ≠ W[1]](/fpt-w1-conjecture/), $\mathrm{FPTAS} \subsetneq \mathrm{EPTAS} \subsetneq \mathrm{PTAS}$.

## Definition

Let $\Pi$ be an optimization problem in [NPO](/npo-class/), with the conventions of [the approximation ratio](/approximation-ratio/) page.

An algorithm $A$ is an **efficient polynomial-time approximation scheme** for $\Pi$ when it is a PTAS for $\Pi$ (on input $I$ and $\varepsilon > 0$ it returns a solution with $\mathrm{ALG} \le (1 + \varepsilon)\mathrm{OPT}$ for minimization, or $\mathrm{ALG} \ge (1 - \varepsilon)\mathrm{OPT}$ for maximization) and its running time is at most

$$
f(1/\varepsilon) \cdot |I|^{c}
$$

for a computable function $f$ and a constant $c$ that does not depend on $\varepsilon$. The class **EPTAS** is the set of NPO problems that have such an algorithm.

Notes on the definition:

- **Product or sum.** The forms $f(1/\varepsilon) \cdot |I|^c$ and $f(1/\varepsilon) + |I|^c$ define the same class: the sum is at most the product when both are at least 1, and $ab \le a^2 + b^2$ turns the product into a sum with $f^2$ and $|I|^{2c}$.
- **The degree is fixed.** A time such as $n^{\log(1/\varepsilon)}$ or $n^{O(1/\varepsilon)}$ is not of this form, because the degree grows with $1/\varepsilon$. A time such as $(\log n)^{1/\varepsilon} \cdot n$ is of this form, because $(\log_2 n)^{k} \le k^{2k} + 2n$ for all $k \ge 1$ and $n \ge 2$. To see this, let $L = \log_2 n$. If $L \le k^2$, then $L^k \le k^{2k}$. If $L > k^2$, then $k < \sqrt{L}$ and $L^k < 2^{\sqrt{L} \log_2 L} \le 2^{L + 1} = 2n$, because $\sqrt{L} \log_2 L \le L + 1$ for all $L \ge 1$.
- **Where it sits.** Each FPTAS is an EPTAS, since $\mathrm{poly}(|I|, 1/\varepsilon) \le \mathrm{poly}(1/\varepsilon) \cdot \mathrm{poly}(|I|)$, and each EPTAS is a PTAS.
- **Origin.** Cesati and Trevisan (1997) defined the notion and proved the link with fixed-parameter tractability below. Bazgan (1995) found the same link independently.

**The standard parameterization.** For a maximization problem $\Pi$ with integer values, the [parameterized problem](/parameterized-problem/) $\Pi_{\ge}$ asks, for an instance $I$ and an integer $k$, whether $\mathrm{OPT}(I) \ge k$, with parameter $k$. For a minimization problem, $\Pi_{\le}$ asks whether $\mathrm{OPT}(I) \le k$.

**Theorem (Bazgan; Cesati and Trevisan).** If an NPO problem $\Pi$ with integer values has an EPTAS, then its standard parameterization is fixed-parameter tractable.

*Proof.* Let $A$ be an EPTAS with time $f(1/\varepsilon) \cdot |I|^c$. Given $(I, k)$ with $k \ge 1$, run $A$ with $\varepsilon = 1/(k + 1)$. The time is $f(k + 1) \cdot |I|^c$, which is an FPT time.

*Maximization.* If $\mathrm{OPT} \ge k$, then $\mathrm{ALG} \ge (1 - \frac{1}{k+1})\mathrm{OPT} \ge \frac{k}{k+1} \cdot k = k - \frac{k}{k+1} > k - 1$, and $\mathrm{ALG}$ is an integer, so $\mathrm{ALG} \ge k$. If $\mathrm{OPT} < k$, then $\mathrm{ALG} \le \mathrm{OPT} < k$. So $\mathrm{OPT} \ge k$ exactly when $\mathrm{ALG} \ge k$.

*Minimization.* If $\mathrm{OPT} \le k$, then $\mathrm{ALG} \le (1 + \frac{1}{k+1})\mathrm{OPT} \le k + \frac{k}{k+1} < k + 1$, so $\mathrm{ALG} \le k$. If $\mathrm{OPT} > k$, then $\mathrm{ALG} \ge \mathrm{OPT} > k$. So $\mathrm{OPT} \le k$ exactly when $\mathrm{ALG} \le k$. For $k \le 0$ the answer can be read off a single run with $\varepsilon = 1$, since then the value is an integer in a known range. $\square$

The same proof with a PTAS of time $|I|^{g(1/\varepsilon)}$ gives only time $|I|^{g(k + 1)}$, which is the class XP, not FPT. So a PTAS says nothing about FPT, but an EPTAS does.

**Corollary.** If the standard parameterization of $\Pi$ is W[1]-hard, then $\Pi$ has no EPTAS unless FPT = W[1].

## Examples and non-examples

**Makespan on identical machines.** For $P \| C_{\max}$, the [Hochbaum and Shmoys PTAS](/hochbaum-shmoys-makespan-ptas/) has time $n^{O(1/\varepsilon^2)}$, which is not an EPTAS. Alon, Azar, Woeginger and Yadid (1998) replaced its dynamic program by an integer program in fixed dimension, solved by the [algorithm of Lenstra](/lenstra-algorithm/), and got time $f(1/\varepsilon) + O(n)$. So $P \| C_{\max}$ has an EPTAS.

**Planar graphs.** [Baker's technique](/baker-technique/) splits a [planar graph](/planar-graph/) into pieces of treewidth $O(1/\varepsilon)$ and solves each piece exactly. For maximum independent set, the time is $2^{O(1/\varepsilon)} \cdot n$, which is an EPTAS. By the theorem, the parameterized independent set problem on planar graphs is FPT, which is also known directly.

**Multiple knapsack.** The [Chekuri and Khanna PTAS](/chekuri-khanna-ptas/) for the [multiple knapsack problem](/multiple-knapsack-problem/) has time $n^{O(\log(1/\varepsilon) / \varepsilon^8)}$, as Jansen states it. Jansen (2010) gave an EPTAS with time $2^{O(\log(1/\varepsilon)/\varepsilon^5)} \cdot \mathrm{poly}(n) + O(m)$. The problem has no FPTAS unless P = NP, even with two knapsacks, so it separates EPTAS from FPTAS.

**Bin packing.** Asymptotic schemes for bin packing can also be efficient in this sense. See [the Epstein and Levin EPTAS for bin packing](/epstein-levin-eptas-bin-packing/).

**Non-example: a PTAS with ε in the exponent.** The partial enumeration scheme for knapsack on the [PTAS](/ptas/) page has time $O(n^{\lceil 1/\varepsilon \rceil + 1})$. It is a PTAS and not an EPTAS. Knapsack still has an EPTAS, because it has an [FPTAS](/fptas/): the class is a property of the problem, and this scheme is just a slow one.

**The separation EPTAS ⊊ PTAS (if FPT ≠ W[1]): independent set in unit disk graphs.** A unit disk graph has a vertex for each of $n$ disks of diameter 1 in the plane, and an edge between two disks that meet. Maximum independent set in unit disk graphs has a PTAS by the [shifting technique](/shifting-technique/) (Hunt, Marathe, Radhakrishnan, Ravi, Rosenkrantz and Stearns, 1998): cut the plane into strips of width $k = \lceil 1/\varepsilon \rceil$, drop the disks on one class of strip borders for each of the $k$ shifts, and solve each square of side $k$ exactly. A square of side $k$ holds an independent set of $O(k^2)$ disks, so each square is solved in $n^{O(k^2)}$ time. Marx (2005) showed that deciding whether a unit disk graph has an independent set of size $k$ is W[1]-hard with parameter $k$. By the corollary, the problem has no EPTAS unless FPT = W[1]. The PTAS above has time $n^{O(1/\varepsilon^2)}$, and the hardness says that the exponent of $n$ in any PTAS for this problem must grow with $1/\varepsilon$.

**Non-example: the converse fails.** FPT does not imply an EPTAS. Minimum [vertex cover](/vertex-cover/) has an FPT algorithm with time $O(1.2738^k + kn)$ (Chen, Kanj and Xia), but it is APX-hard, so it has no PTAS at all unless P = NP.

## Related definitions

- **PTAS and FPTAS.** A [PTAS](/ptas/) allows any polynomial for each fixed $\varepsilon$. An [FPTAS](/fptas/) needs time polynomial in $n$ and $1/\varepsilon$. The separations of the chain are summarized on the PTAS page.
- **Fixed-parameter tractability.** A [parameterized problem](/parameterized-problem/) is [fixed-parameter tractable](/fixed-parameter-tractable/) when it has an algorithm with time $f(k) \cdot n^{O(1)}$. The [W hierarchy](/w-hierarchy/) classifies the problems that are likely not FPT, starting from [clique](/clique-w1-completeness/), and [FPT ≠ W[1]](/fpt-w1-conjecture/) is the standard assumption.
- **FPT approximation.** An [FPT approximation](/fpt-approximation/) algorithm runs in FPT time and approximates the optimum. It turns the question around: it uses a parameter to gain accuracy, while an EPTAS uses the accuracy as a parameter. The limits of such algorithms are on the page [parameterized inapproximability](/parameterized-inapproximability/).

## References

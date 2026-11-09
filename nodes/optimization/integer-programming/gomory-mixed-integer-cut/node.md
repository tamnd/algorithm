---
tag: 6XS6G3
kind: concept
slug: gomory-mixed-integer-cut
name: Gomory mixed-integer cut
aliases:
- GMI cut
- Gomory fractional cut
- Gomory mixed-integer inequality
area: optimization/integer-programming
level: advanced
summary: Cut derived from a row of the optimal simplex tableau whose basic integer variable is fractional.
prereqs: [gomory-cutting-plane-algorithm, chvatal-gomory-cut, simplex-method]
see_also: [mixed-integer-rounding-inequality, disjunctive-cut, chvatal-gomory-cut, gomory-cutting-plane-algorithm, branch-and-cut, lift-and-project, subadditive-duality, cutting-plane-method-integer-programming]
sources:
  - paper: "Ralph E. Gomory, An algorithm for the mixed integer problem, Research Memorandum RM-2597, The RAND Corporation, 1960"
    locator: the mixed-integer cut from a tableau row
  - paper: "Egon Balas, Sebastián Ceria, Gérard Cornuéjols and N. Natraj, Gomory cuts revisited, Operations Research Letters 19 (1996), 1 to 9"
    locator: the computational study that brought the cuts into branch and cut
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 5 (Gomory's mixed-integer inequalities, split inequalities and the equivalence with MIR)
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming, Wiley, 1998
    locator: Chapter 8 (cutting plane algorithms, the mixed-integer cut)
  - paper: "Gérard Cornuéjols, Valid inequalities for mixed integer linear programs, Mathematical Programming 112 (2008), 3 to 44"
    locator: the survey sections on Gomory mixed-integer cuts, split cuts and MIR
---

A Gomory mixed-integer (GMI) cut is a valid inequality read from one row of an optimal simplex tableau in which a basic integer variable has a fractional value. It applies when some variables are continuous, it is never weaker than Gomory's earlier fractional cut, and it is the same inequality as a [mixed-integer rounding](/mixed-integer-rounding-inequality/) cut and a split cut for the disjunction "the basic variable is at most its floor or at least its ceiling". After Balas, Ceria, Cornuéjols and Natraj (1996) showed that these cuts work well inside [branch and cut](/branch-and-cut/), they became one of the most effective cut families in MIP solvers.

## In plain words

When a solver relaxes an integer program and gets an answer with a fractional value, say $x = 2.4$, it knows that the true answer has $x \le 2$ or $x \ge 3$. The simplex method also gives a formula that shows how $x$ changes when the other variables move away from zero.

The GMI cut combines the two facts. To bring $x$ down to 2 or up to 3, the other variables must move by a total amount that the formula fixes. The cut says: "move them at least that much". The current fractional answer has them all at zero, so it breaks the cut, while every true answer keeps it.

## The idea

**The row.** Take a mixed-integer program in the form $Ax = b$, $x \ge 0$, with $x_j \in \mathbb{Z}$ for $j \in I$. At an optimal basis of the [LP relaxation](/lp-relaxation/), a row of the tableau reads

$$x_i + \sum_{j \in N} \bar a_j x_j = \bar b,$$

where $N$ is the set of nonbasic variables, $x_i$ is a basic integer variable and $\bar b$ is fractional. Let $f_0 = \bar b - \lfloor \bar b \rfloor \in (0, 1)$ and $f_j = \bar a_j - \lfloor \bar a_j \rfloor$. The page on [Gomory's algorithm](/gomory-cutting-plane-algorithm/) uses the form $Ax \le b$; its slacks are the extra variables here, and they are integer when $A$ and $b$ are integral.

**The cut.** Every feasible point satisfies

$$\sum_{\substack{j \in N \cap I \\ f_j \le f_0}} \frac{f_j}{f_0}\, x_j + \sum_{\substack{j \in N \cap I \\ f_j > f_0}} \frac{1 - f_j}{1 - f_0}\, x_j + \sum_{\substack{j \in N \setminus I \\ \bar a_j > 0}} \frac{\bar a_j}{f_0}\, x_j + \sum_{\substack{j \in N \setminus I \\ \bar a_j < 0}} \frac{-\bar a_j}{1 - f_0}\, x_j \ \ge\ 1.$$

The current LP vertex has $x_j = 0$ for all $j \in N$, so the left side is 0 there, and the cut cuts it off.

*Proof of validity.* Let $x$ be feasible. For $j \in N \cap I$, let $g_j = f_j$ if $f_j \le f_0$ and $g_j = f_j - 1$ otherwise; in both cases $\bar a_j - g_j$ is an integer. Then

$$\sum_{j \in N \cap I} g_j x_j + \sum_{j \in N \setminus I} \bar a_j x_j = \bar b - x_i - \sum_{j \in N \cap I} (\bar a_j - g_j) x_j = f_0 + k$$

for some integer $k$, because $x_i$ and $x_j$, $j \in I$, are integers. Let $S^+$ be the sum of the positive terms on the left and $S^-$ the sum of the absolute values of the negative terms, so $S^+ - S^- = f_0 + k$ with $S^+, S^- \ge 0$. If $k \ge 0$, then $S^+ \ge f_0$. If $k \le -1$, then $S^- \ge 1 - f_0$. In both cases

$$\frac{S^+}{f_0} + \frac{S^-}{1 - f_0} \ge 1,$$

and this is the cut: $S^+$ collects the terms $f_j x_j$ with $f_j \le f_0$ and $\bar a_j x_j$ with $\bar a_j > 0$, and $S^-$ collects $(1 - f_j) x_j$ with $f_j > f_0$ and $-\bar a_j x_j$ with $\bar a_j < 0$. $\square$

**Comparison with the fractional cut.** For a pure integer row, Gomory's fractional cut is $\sum_j f_j x_j \ge f_0$, that is, $\sum_j (f_j / f_0) x_j \ge 1$. The GMI coefficient of $x_j$ is $\min\{f_j / f_0,\ (1 - f_j)/(1 - f_0)\}$, which is never larger. So the GMI cut dominates the fractional cut, strictly when some $f_j > f_0$. The fractional cut is a [Chvátal-Gomory cut](/chvatal-gomory-cut/), and the GMI cut is a split cut, which can be of higher Chvátal rank.

**Three views of one inequality.**

- *Split cut.* The proof is the disjunction $x_i \le \lfloor \bar b \rfloor$ or $x_i \ge \lceil \bar b \rceil$, written in the space of the nonbasic variables. The GMI cut is the intersection cut of the LP cone with this split, so it is a [disjunctive cut](/disjunctive-cut/).
- *MIR.* Applying the [mixed-integer rounding](/mixed-integer-rounding-inequality/) inequality to the tableau row gives the same cut.
- *Group relaxation.* For one row with integer nonbasics, the GMI coefficient function $\pi(f) = \min\{f / f_0,\ (1 - f)/(1 - f_0)\}$ is an extreme valid function of the Gomory-Johnson infinite group relaxation, the best known case of [subadditive](/subadditive-duality/) valid functions.

**Practical use.** Solvers generate GMI cuts from the rows of the optimal tableau at the root node, and sometimes in the tree. Rows with $f_0$ close to 0 or 1 give weak and numerically risky cuts, so they are skipped. Cuts with very dense rows or a large ratio between the largest and smallest coefficients are scaled or rejected. The cuts are computed in floating point, so solvers make the right side slightly weaker to keep them safe. Many rounds of GMI cuts, each from the tableau of the previous round, tend to give unstable bases, which is why solvers limit the number of rounds.

## Examples

**A mixed row.** Take the row

$$x_0 + \tfrac34 x_1 + \tfrac14 x_2 + \tfrac12 y_1 - \tfrac12 y_2 = \tfrac{12}{5},$$

with $x_0, x_1, x_2 \ge 0$ integer and $y_1, y_2 \ge 0$ continuous. Here $f_0 = 2/5$, $f_1 = 3/4 > f_0$ and $f_2 = 1/4 \le f_0$. The GMI cut is

$$\tfrac{5}{12} x_1 + \tfrac58 x_2 + \tfrac54 y_1 + \tfrac56 y_2 \ge 1.$$

It holds with equality at the feasible points $(x_0, x_1, x_2, y_1, y_2) = (2, 0, 0, \tfrac45, 0)$, $(3, 0, 0, 0, \tfrac65)$, $(2, 1, 0, 0, \tfrac{7}{10})$, $(2, 0, 1, \tfrac{3}{10}, 0)$ and $(1, 2, 0, 0, \tfrac15)$, so it cannot be moved without cutting off a feasible point. If $y_1$ and $y_2$ were integer too, the fractional cut would give the coefficient $15/8$ for $x_1$ instead of $5/12$.

**The running example.** For $\max x_2$ subject to $3x_1 + 2x_2 + s_1 = 6$, $-3x_1 + 2x_2 + s_2 = 0$, $x, s \ge 0$, the optimal tableau row of $x_2$ is $x_2 + \tfrac14 s_1 + \tfrac14 s_2 = \tfrac32$. With $f_0 = 1/2$ and $f_1 = f_2 = 1/4$, the GMI cut is $\tfrac12 s_1 + \tfrac12 s_2 \ge 1$. Substituting $s_1 = 6 - 3x_1 - 2x_2$ and $s_2 = 3x_1 - 2x_2$ gives $x_2 \le 1$. This holds whether $x_1$ is integer or continuous, and here it equals the fractional cut, since no $f_j$ exceeds $f_0$.

## Where it is used

- **Branch and cut.** Every major MIP solver separates GMI cuts at the root, and they are among the cut families with the largest effect on solve times.
- **Benchmarks of cut strength.** The gap closed by one round of GMI cuts is a standard baseline for new cut families, such as [lift-and-project](/lift-and-project/) cuts and multi-row cuts.
- **Theory.** GMI cuts started the study of split closures, of corner polyhedra and of the infinite group relaxation, which describe which cuts a single tableau row or several rows can give.
- **Exact and safe MIP.** Solvers that must certify their answers derive GMI cuts in exact or interval arithmetic, since a cut that is slightly wrong can remove the optimum.

## References

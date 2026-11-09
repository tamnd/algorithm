---
tag: NBQNPG
kind: concept
slug: mixed-integer-rounding-inequality
name: Mixed-integer rounding inequality
aliases:
- MIR inequality
- Nemhauser-Wolsey inequality
- MIR cut
area: optimization/integer-programming
level: advanced
summary: Valid inequality for one constraint with integer and continuous variables.
prereqs: [chvatal-gomory-cut, mixed-integer-programming, lp-relaxation]
see_also: [gomory-mixed-integer-cut, chvatal-gomory-cut, flow-cover-inequality, cover-inequality, disjunctive-cut, branch-and-cut, cutting-plane-method-integer-programming, integer-hull]
sources:
  - book: isbn:9780471828198
    title: George L. Nemhauser and Laurence A. Wolsey, Integer and Combinatorial Optimization, Wiley, 1988
    locator: Part II, the chapter on strong valid inequalities for mixed-integer sets (mixed-integer rounding)
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming, Wiley, 1998
    locator: Chapter 8 (the basic mixed-integer inequality and MIR)
  - paper: "Hugues Marchand and Laurence A. Wolsey, Aggregation and mixed integer rounding to solve MIPs, Operations Research 49 (2001), 363 to 371"
    locator: the c-MIR separation heuristic (aggregation, bound substitution and the choice of the divisor)
  - paper: "Gérard Cornuéjols and Yanjun Li, Elementary closures for integer programs, Operations Research Letters 28 (2001), 1 to 8"
    locator: the equality of the MIR closure and the split closure
  - paper: "Sanjeeb Dash, Oktay Günlük and Andrea Lodi, MIR closures of polyhedral sets, Mathematical Programming 121 (2010), 33 to 60"
    locator: optimizing over the MIR closure in computations
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 5 (MIR inequalities and their equivalence with Gomory mixed-integer and split inequalities)
---

A mixed-integer rounding (MIR) inequality is a valid inequality for one linear constraint in nonnegative integer and continuous variables. It is the mixed-integer form of the rounding step in a [Chvátal-Gomory cut](/chvatal-gomory-cut/): the right side is rounded down, and the continuous variables pay for the rounding with a larger coefficient. Nemhauser and Wolsey made it the base of a general theory of cuts for mixed-integer sets. Applied to a row of the simplex tableau, it gives the [Gomory mixed-integer cut](/gomory-mixed-integer-cut/). Applied to rows that a solver first adds together and scales, it gives most of the cuts that modern MIP solvers use.

## In plain words

Suppose a whole number $x$ must stay below $2.5$ plus some amount $y$ that can be any nonnegative real number. If $y$ is zero, $x$ can be at most 2. To reach 3, $y$ must be at least $0.5$. To reach 4, $y$ must be at least $1.5$. The MIR inequality is the straight line that joins the cheapest ways to reach 2 and 3. It removes the fractional corner where $x = 2.5$ and $y = 0$, and it keeps every point where $x$ is a whole number.

The general MIR inequality reduces any single constraint to this small case. It puts the whole-number parts of the constraint on one side and the fractional parts and the continuous variables on the other.

## The idea

**The basic MIR inequality.** Let $X = \{(x, y) \in \mathbb{Z} \times \mathbb{R} : x - y \le b,\ y \ge 0\}$, with $f = b - \lfloor b \rfloor > 0$. Then

$$x - \frac{y}{1 - f} \le \lfloor b \rfloor$$

is valid for $X$, and

$$\operatorname{conv}(X) = \left\{(x, y) : y \ge 0,\ x - y \le b,\ x - \frac{y}{1 - f} \le \lfloor b \rfloor\right\}.$$

*Proof.* Validity: if $x \le \lfloor b \rfloor$, the inequality holds because $y \ge 0$. If $x \ge \lfloor b \rfloor + 1$, then $y \ge x - b = (x - \lfloor b \rfloor - 1) + (1 - f)$, so $y/(1 - f) \ge (x - \lfloor b \rfloor - 1)/(1 - f) + 1 \ge x - \lfloor b \rfloor$. For the hull, call the right side $Q$. It contains $\operatorname{conv}(X)$ by validity. Its vertices are $(\lfloor b \rfloor, 0)$ and $(\lfloor b \rfloor + 1, 1 - f)$, both in $X$, and its recession cone is spanned by $(-1, 0)$ and $(1, 1)$, both directions of $X$. So $Q \subseteq \operatorname{conv}(X)$. $\square$

**The MIR inequality.** Let

$$X = \Big\{(x, y) \in \mathbb{Z}^n_+ \times \mathbb{R}^p_+ : \sum_{j=1}^n a_j x_j + \sum_{k=1}^p c_k y_k \le b\Big\},$$

with $f = b - \lfloor b \rfloor > 0$ and $f_j = a_j - \lfloor a_j \rfloor$. The MIR inequality is

$$\sum_{j=1}^n \Big(\lfloor a_j \rfloor + \frac{\max(0,\ f_j - f)}{1 - f}\Big) x_j + \frac{1}{1 - f} \sum_{k : c_k < 0} c_k y_k \le \lfloor b \rfloor.$$

*Proof.* Let $J = \{j : f_j > f\}$. Write $a_j = \lfloor a_j \rfloor + f_j$ for $j \notin J$ and $a_j = \lceil a_j \rceil - (1 - f_j)$ for $j \in J$. Drop the terms $f_j x_j$ for $j \notin J$ and $c_k y_k$ for $c_k > 0$, which are nonnegative. This gives $z - w \le b$, where

$$z = \sum_{j \notin J} \lfloor a_j \rfloor x_j + \sum_{j \in J} \lceil a_j \rceil x_j \in \mathbb{Z}, \qquad w = \sum_{j \in J} (1 - f_j) x_j - \sum_{k : c_k < 0} c_k y_k \ge 0.$$

The basic MIR inequality gives $z - w/(1 - f) \le \lfloor b \rfloor$. Since $\lceil a_j \rceil - (1 - f_j)/(1 - f) = \lfloor a_j \rfloor + (f_j - f)/(1 - f)$, this is the MIR inequality. $\square$

**Relation to other cuts.**

- *Chvátal-Gomory.* Each integer coefficient is at least $\lfloor a_j \rfloor$, so for $x \ge 0$ the MIR inequality is at least as strong as the Chvátal-Gomory cut $\sum_j \lfloor a_j \rfloor x_j \le \lfloor b \rfloor$, and it also applies when continuous variables are present.
- *Gomory mixed-integer cut.* The MIR inequality of a simplex tableau row is the [GMI cut](/gomory-mixed-integer-cut/) of that row.
- *Split cuts.* The proof uses only the disjunction $z \le \lfloor b \rfloor$ or $z \ge \lfloor b \rfloor + 1$, so each MIR inequality is a split cut, a kind of [disjunctive cut](/disjunctive-cut/). The other direction also holds: the MIR closure, which applies MIR to every nonnegative combination of the rows, equals the split closure (Nemhauser and Wolsey; Cornuéjols and Li, 2001).
- *Covers and flow covers.* After the right aggregation and complementing of variables, [flow cover](/flow-cover-inequality/) inequalities and some lifted [cover inequalities](/cover-inequality/) are MIR inequalities.

**The c-MIR heuristic.** Solvers separate MIR cuts with the procedure of Marchand and Wolsey (2001). They add a few rows of the problem together, replace bounded variables by their bounds or by their complements $u_j - x_j$, divide the row by a number $\delta$ from a short list (for example, the coefficients of the integer variables with fractional LP values), and apply the MIR formula. Each choice gives a different cut, and the solver keeps the most violated ones. The choice of $\delta$ matters a lot, as the example below shows.

## Examples

**The basic case.** For $x - y \le 5/2$, $f = 1/2$ and the MIR inequality is $x - 2y \le 2$. It joins $(2, 0)$ and $(3, 1/2)$, the two vertices of the hull, and it cuts off the LP vertex $(5/2, 0)$.

**The choice of the divisor.** Take $7x_1 + 3x_2 - y \le 10$ with $x_1, x_2 \in \mathbb{Z}_+$ and $y \ge 0$. With $\delta = 1$ the right side is integral, so there is no cut. Other divisors give these inequalities, scaled to integer coefficients:

| $\delta$ | $f$ | MIR inequality | Integer points where it is tight | Value at $(10/7, 0, 0)$ |
|---|---|---|---|---|
| 3 | 1/3 | $4x_1 + 2x_2 - y \le 6$ | $(0, 3, 0)$, $(1, 1, 0)$, $(0, 4, 2)$ | $40/7 \le 6$ |
| 4 | 1/2 | $3x_1 + x_2 - y \le 4$ | $(1, 1, 0)$ only | $30/7 > 4$ |
| 7 | 3/7 | $4x_1 - y \le 4$ | $(1, 0, 0)$, $(1, 1, 0)$, $(2, 0, 4)$ | $40/7 > 4$ |

For $\delta = 3$ and $\delta = 7$, the tight points are affinely independent, so the inequality defines a facet of the 3-dimensional hull. The cut for $\delta = 4$ is valid but touches the hull in one point only. The point $(10/7, 0, 0)$ is a vertex of the LP relaxation. Only the cuts for $\delta = 4$ and $\delta = 7$ remove it, and only $\delta = 7$ gives a facet that does so.

## Where it is used

- **MIP solvers.** The c-MIR procedure is a standard separator in [branch and cut](/branch-and-cut/) codes. With different aggregations, one implementation finds cuts of the GMI, flow cover and several other families.
- **Lot sizing and network design.** MIR inequalities on aggregated flow balance rows give many of the strong cuts known for these problems.
- **Theory of closures.** The MIR closure is the split closure, so results on one apply to the other. Dash, Günlük and Lodi (2010) optimized over the MIR closure to measure how much of the [integrality gap](/integrality-gap/) split cuts can close.
- **Multi-row and lifted cuts.** Many stronger cut families start from an MIR inequality and lift it, or apply the MIR function to two or more rows in turn.

## References

---
tag: M6S753
kind: concept
slug: bounds-consistency
name: Bounds consistency
aliases:
- interval consistency
- bound consistency
- bounds propagation
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Weaker propagation for ordered domains that only enforces consistency at the lower and upper bounds.
prereqs: [arc-consistency, constraint-propagation]
see_also: [interval-constraint-propagation, numeric-constraint-satisfaction, all-different-constraint, regin-all-different-filtering, global-constraint, simple-temporal-problem, singleton-arc-consistency, constraint-programming]
sources:
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 3, Constraint propagation, by Christian Bessière (bounds consistency and its variants)
  - paper: "Chiu Wo Choi, Warwick Harvey, Jimmy H. M. Lee and Peter J. Stuckey, Finite domain bounds consistency revisited, Advances in Artificial Intelligence (AI 2006), Lecture Notes in Computer Science 4304, Springer, 2006, pages 49 to 58"
    locator: the definitions bounds(D), bounds(Z) and bounds(R), and the relations between them and with range and domain consistency
  - paper: "Jean-François Puget, A fast algorithm for the bound consistency of alldiff constraints, Proceedings of AAAI 1998, pages 359 to 366"
    locator: bounds consistency for all-different in O(n log n) time by Hall intervals
  - paper: "Olivier Lhomme, Consistency techniques for numeric CSPs, Proceedings of IJCAI 1993, pages 232 to 238"
    locator: arc B-consistency, which checks only the bounds of interval domains of real variables
---

Bounds consistency is a local consistency for a [constraint satisfaction problem](/constraint-satisfaction-problem/) whose domains are ordered, such as sets of integers. It asks only that the smallest and the largest value of each domain have a support, a tuple that satisfies the constraint, with the other variables taking values between their own bounds. Values inside a domain are not checked. It is weaker than [arc consistency](/arc-consistency/), or generalized arc consistency for constraints of more than two variables, but it is much cheaper for arithmetic and many [global constraints](/global-constraint/), and it lets a solver store each domain as an interval. It is the default propagation for linear constraints in finite domain solvers.

## In plain words

For a number unknown, keep only a lowest and a highest possible value. Bounds consistency asks: can the lowest value really occur? To check, look for values of the other unknowns, each between its own lowest and highest value, that make the rule true. If there are none, raise the lowest value by one, and try again. Do the same for the highest value.

This is cheap for rules like "$x + y \le 10$", where simple arithmetic on the ends gives the answer. It misses holes inside a range: if only even values can work, bounds consistency still keeps the odd values in the middle.

## The idea

**Notation.** $n$ variables, $m$ constraints of arity at most $r$, domains $D_x$ of integers with $|D_x| \le d$. For a domain, $\min D_x$ and $\max D_x$ are its bounds, and $[D_x]$ is the integer interval $\{\min D_x, \ldots, \max D_x\}$.

**Definitions.** Let $C$ be a constraint on the variables $x_1, \ldots, x_r$. A *support* of a value $a$ of $x_i$ is a tuple in $C$ with $x_i = a$. There are several versions of bounds consistency in the literature, and Choi, Harvey, Lee and Stuckey (2006) gave them names:

- **bounds(D).** For each $i$, $\min D_{x_i}$ and $\max D_{x_i}$ have a support with $x_j \in D_{x_j}$ for each $j \ne i$.
- **bounds(Z).** For each $i$, the two bounds have a support with $x_j \in [D_{x_j}]$, an integer between the bounds, for each $j \ne i$.
- **bounds(R).** For each $i$, the two bounds have a support in the real intervals $[\min D_{x_j}, \max D_{x_j}]$, where $C$ is read as a constraint over the reals.
- **Range consistency.** Every value of $D_{x_i}$, not only the bounds, has a support with $x_j \in [D_{x_j}]$.

The word *interval consistency* is used for bounds(Z) and for bounds(R) by different authors. Generalized arc consistency asks that every value have a support in the domains. Each of these is a property of the domains, and each comes with a propagator that deletes values that fail it, at the ends only for the bounds versions.

**The order of strength.** A support in the domains is also a support in the integer intervals, and an integer support is also a real one. So if a value has no real support, it has no integer support, and if it has no integer support, it has no support in the domains. Hence, on the deleted values: generalized arc consistency deletes at least what bounds(D) deletes, bounds(D) at least what bounds(Z) deletes, and bounds(Z) at least what bounds(R) deletes; range consistency lies between generalized arc consistency and bounds(Z). For interval domains, $[D_x] = D_x$, so bounds(D) and bounds(Z) are the same, and range consistency is generalized arc consistency.

**A unique closure.** A bounds propagator is monotone: on smaller domains, fewer supports exist, so it deletes at least as much. It is contracting, since it only deletes. By the fixpoint theorem of [constraint propagation](/constraint-propagation/), running the propagators of all constraints in any order until nothing changes gives the same domains, the bounds consistency closure, and it keeps every solution.

**Linear inequalities.** Take $\sum_i a_i x_i \le c$ with integer coefficients. The smallest value of the sum of the terms other than $j$ is $L_j = \sum_{i \ne j} \min(a_i \min D_{x_i}, a_i \max D_{x_i})$. If $a_j > 0$, a support for the value $v$ of $x_j$ exists in the integer intervals exactly when $a_j v + L_j \le c$, because the other variables can take their minimizing bounds. So bounds(Z) consistency is

$$\max D_{x_j} \le \left\lfloor \frac{c - L_j}{a_j} \right\rfloor \quad (a_j > 0),$$

and the symmetric rule raises $\min D_{x_j}$ when $a_j < 0$. Keeping the total of the minima, a propagator updates all $r$ variables in $O(r)$ arithmetic operations. Here bounds(Z) and bounds(R) agree, apart from rounding.

**Linear equations are harder.** For $\sum_i a_i x_i = c$ with domains $\{0, 1\}$, bounds consistency is generalized arc consistency, because each domain has only its two bounds. A support for $x_1 = 1$ exists exactly when some subset of $a_2, \ldots, a_r$ sums to $c - a_1$. This is the subset sum problem, a special case of the [knapsack problem](/knapsack-problem/), which is NP-complete, so enforcing bounds(Z) on linear equations is NP-hard. Solvers apply the two inequalities $\le c$ and $\ge c$ separately, which gives bounds(R) consistency in $O(r)$ time and misses some integer deletions.

**Cost per constraint.** A propagation of bounds(R) on a linear constraint costs $O(r)$. Each bound of each variable moves at most $d$ times, so all propagations of a fixpoint computation trigger at most $O(n d)$ changes, and each change wakes up the constraints on that variable. This is why bounds propagation scales to long linear sums with large domains, where generalized arc consistency would cost time exponential in $r$ or pseudo-polynomial in the coefficients.

## Examples

**Holes are kept.** Let $x \in \{1, 2, 3\}$, $y \in \{1, \ldots, 6\}$ and $y = 2x$. The bound $y = 1$ has no support, since $2x = 1$ has no integer solution, so $\min D_y$ becomes 2. The bound $y = 6$ has the support $x = 3$, and the bounds $x = 1$ and $x = 3$ have the supports $y = 2$ and $y = 6$. So bounds(Z) leaves $y \in \{2, \ldots, 6\}$. Generalized arc consistency leaves $y \in \{2, 4, 6\}$. Bounds(R) gives the same result here: the only real support of $y = 1$ is $x = 1/2$, which lies outside $[1, 3]$.

**A linear chain.** $x, y, z \in \{0, \ldots, 10\}$ with $x + y \le 8$, $y + z \ge 15$. The first constraint gives $x \le 8$ and $y \le 8$. The second then gives $y \ge 15 - 10 = 5$ and $z \ge 15 - 8 = 7$. The first again gives $x \le 8 - 5 = 3$, and nothing changes after that. The closure is $x \in [0, 3]$, $y \in [5, 8]$, $z \in [7, 10]$, and each of the six bounds has a support.

**All-different.** For $x_1, x_2 \in \{1, 2\}$ and $x_3 \in \{1, 2, 3\}$ with all values different, the interval $[1, 2]$ holds two variables in two values, a *Hall interval*, so $x_3$ cannot take 1 or 2, and its lower bound rises to 3. Bounds consistency for [all-different](/all-different-constraint/) finds all Hall intervals in $O(n \log n)$ time (Puget 1998), while full generalized arc consistency needs a matching algorithm ([Régin's filtering](/regin-all-different-filtering/)). On $x_1, x_2 \in \{1, 3\}$ and $x_3 \in \{1, 2, 3\}$, generalized arc consistency gives $x_3 = 2$, while bounds consistency on the intervals $[1, 3]$ deletes nothing.

**Real variables.** For real intervals, $x \in [0, 10]$, $y \in [0, 10]$ and $y = x^2$, bounds reasoning gives $y \in [0, 10]$ and $x \in [0, \sqrt{10}]$. Solvers for [numeric CSPs](/numeric-constraint-satisfaction/) do this with outward rounding; see [interval constraint propagation](/interval-constraint-propagation/).

## Where it is used

- **Finite domain solvers.** Linear constraints, products and many arithmetic constraints use bounds propagation by default, and domains are often stored as intervals with an optional set of holes.
- **Global constraints.** Bounds consistency algorithms exist for all-different, global cardinality and sorting constraints, at lower cost than generalized arc consistency; see [global constraints](/global-constraint/).
- **Scheduling.** Start times are integers with large ranges, so precedence and resource constraints are propagated on bounds. Precedences $x_j - x_i \ge b$ alone form a [simple temporal problem](/simple-temporal-problem/), for which bounds propagation reaches the earliest and latest start times. *Shaving*, which tests a bound by a trial as in [singleton arc consistency](/singleton-arc-consistency/), adds strength on hard instances.
- **Continuous domains.** Interval solvers apply the same idea to real variables as hull or box consistency, through [interval constraint propagation](/interval-constraint-propagation/).
- **Linear programming and integer programming.** Bound tightening in mixed integer programming presolve uses the same rule as for linear inequalities above.

## References

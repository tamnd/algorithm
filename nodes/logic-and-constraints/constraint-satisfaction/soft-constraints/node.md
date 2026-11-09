---
tag: MYPV8J
kind: concept
slug: soft-constraints
name: Soft constraints
aliases:
- weighted constraints
- preferences
- semiring-based CSP
- SCSP
- valued CSP
- VCSP
- weighted CSP
- cost function network
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Constraints that give each tuple a level of preference or a cost instead of yes or no. The semiring (SCSP) and valued (VCSP) frameworks define how levels combine and which assignment is best.
prereqs: [constraint-satisfaction-problem, maximum-csp, depth-first-branch-and-bound]
see_also: [maximum-csp, weighted-max-sat, bounding-function, arc-consistency, bucket-elimination, incumbent-solution, partial-max-sat, max-sat]
sources:
  - paper: doi:10.1145/256303.256306
    title: Stefano Bistarelli, Ugo Montanari and Francesca Rossi, Semiring-based constraint satisfaction and optimization, Journal of the ACM 44(2), 1997
    locator: pages 201 to 236 (c-semirings, soft constraints, combination and projection, and the instances classical, fuzzy, probabilistic and weighted)
  - paper: "Thomas Schiex, Hélène Fargier and Gérard Verfaillie, Valued constraint satisfaction problems, hard and easy problems, Proceedings of IJCAI-95, 1995, pages 631 to 637"
    locator: valuation structures, valued CSPs, and the effect of a strictly monotone or idempotent operator on local consistency
  - paper: doi:10.1023/A:1026441215081
    title: Stefano Bistarelli, Hélène Fargier, Ugo Montanari, Francesca Rossi, Thomas Schiex and Gérard Verfaillie, Semiring-based CSPs and valued CSPs, frameworks, properties, and comparison, Constraints 4(3), 1999
    locator: pages 199 to 240 (the mappings between SCSPs and VCSPs, and the result that totally ordered SCSPs and VCSPs have the same power)
  - paper: doi:10.1016/j.artint.2004.05.004
    title: Javier Larrosa and Thomas Schiex, Solving weighted CSP by maintaining arc consistency, Artificial Intelligence 159(1-2), 2004
    locator: pages 1 to 26 (the zero-arity cost as a lower bound, node and arc consistency for weighted CSPs, and their use in depth-first branch and bound)
  - paper: doi:10.1016/j.artint.2003.09.002
    title: Martin C. Cooper and Thomas Schiex, Arc consistency for soft constraints, Artificial Intelligence 154(1-2), 2004
    locator: pages 199 to 227 (equivalence-preserving moves of cost between constraints, soft arc consistency)
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 9, Soft constraints, by Pedro Meseguer, Francesca Rossi and Thomas Schiex
---

A soft constraint does not say only "allowed" or "forbidden". It gives each combination of values a *level*: a cost, a degree of preference, or a probability. A problem with soft constraints asks for the assignment whose combined level is best. This models over-constrained problems, where no assignment meets every wish, and problems with preferences, where many assignments are allowed but some are better. Two general frameworks define what "combined" and "best" mean. The *semiring-based CSP* (SCSP) of Bistarelli, Montanari and Rossi (1997) uses an algebraic structure called a c-semiring. The *valued CSP* (VCSP) of Schiex, Fargier and Verfaillie (1995) uses a totally ordered valuation structure. Bistarelli and colleagues (1999) showed that VCSPs are exactly the SCSPs whose order is total. [Maximum CSP](/maximum-csp/) is one special case: each violated constraint costs 1, or its weight.

## In plain words

In an ordinary CSP each rule is strict. With soft constraints each rule says how much you like each choice. A meeting at 9 is fine, at 8 is bad, and at 7 is very bad. A solver adds up, or otherwise combines, the scores of all the rules, and looks for the choice with the best total.

Different problems combine scores in different ways. With costs you add them. With "how happy is the least happy person" you take the minimum. With probabilities you multiply. The two frameworks on this page give one theory for all of these, so that one search method works for all of them.

## The idea

**Semiring-based CSPs.** A *c-semiring* is a tuple $S = \langle A, +, \times, \mathbf{0}, \mathbf{1} \rangle$ with these properties:

- $+$ is commutative, associative and idempotent ($a + a = a$), $\mathbf{0}$ is its unit, and $\mathbf{1}$ is absorbing for it ($a + \mathbf{1} = \mathbf{1}$);
- $\times$ is commutative and associative, distributes over $+$, $\mathbf{1}$ is its unit, and $\mathbf{0}$ is absorbing for it.

The relation $a \le_S b \iff a + b = b$ is a partial order, read "$b$ is at least as good as $a$". Then $\mathbf{0}$ is the worst level, $\mathbf{1}$ the best, $+$ gives the least upper bound, and $\times$ combines levels and never makes them better. A soft constraint is a pair $\langle \mathit{def}, \mathit{con} \rangle$, where $\mathit{con}$ is a tuple of variables and $\mathit{def} : D^{|\mathit{con}|} \to A$. For a complete assignment $t$, the level of $t$ is

$$\mathit{val}(t) = \prod_{c \in C} \mathit{def}_c(t\!\downarrow_{\mathit{con}_c}) ,$$

with the product taken by $\times$. The task is to find the best level $\sum_t \mathit{val}(t)$, a sum by $+$, and an assignment with a maximal level. Because the order may be partial, there may be several incomparable best assignments.

**Valued CSPs.** A *valuation structure* is $S = \langle E, \circledast, \succ \rangle$ where $E$ is a set totally ordered by $\succ$ with a least element $\bot$ and a greatest element $\top$, and $\circledast$ is commutative, associative and monotone ($a \succeq b \Rightarrow a \circledast c \succeq b \circledast c$), with unit $\bot$ and absorbing element $\top$. Here $\bot$ means "fully satisfied" and $\top$ means "forbidden". Each constraint $c$ has a valuation $\varphi(c) \in E$, and the valuation of a complete assignment $t$ is

$$\mathit{VP}(t) = \circledast_{c \text{ violated by } t} \ \varphi(c) .$$

The task is to find $t$ with minimal $\mathit{VP}(t)$. A later form, used in most work today, gives a valuation to each tuple, as SCSPs do.

**How they correspond.** A VCSP becomes an SCSP with $A = E$, $\times = \circledast$, $+ = $ the minimum with respect to $\succ$, $\mathbf{0} = \top$ and $\mathbf{1} = \bot$. The order is reversed, since in a VCSP smaller is better. Conversely, an SCSP whose order $\le_S$ is total gives a valuation structure with the reversed order and $\circledast = \times$. Bistarelli, Fargier, Montanari, Rossi, Schiex and Verfaillie (1999) showed that these maps preserve the optimal assignments, so totally ordered SCSPs and VCSPs have the same power. SCSPs with a partial order, such as the product of two semirings for two criteria, have no VCSP form.

**Common instances.**

| instance | SCSP $\langle A, +, \times, \mathbf{0}, \mathbf{1} \rangle$ | VCSP $\langle E, \circledast \rangle$ | best is |
|---|---|---|---|
| classical CSP | $\langle \{\mathrm{f}, \mathrm{t}\}, \vee, \wedge, \mathrm{f}, \mathrm{t} \rangle$ | $\langle \{\bot, \top\}, \max \rangle$ | any solution |
| fuzzy | $\langle [0,1], \max, \min, 0, 1 \rangle$ | $\langle [0,1], \max \rangle$ | the largest minimum preference |
| probabilistic | $\langle [0,1], \max, \cdot, 0, 1 \rangle$ | $\langle [0,1], 1 - (1-a)(1-b) \rangle$ | the most probable world |
| weighted | $\langle \mathbb{N} \cup \{\infty\}, \min, +, \infty, 0 \rangle$ | $\langle \mathbb{N} \cup \{\infty\}, + \rangle$ | the smallest total cost |
| [Max-CSP](/maximum-csp/) | weighted, each violation costs 1 | $\langle \mathbb{N}, + \rangle$, $\varphi(c) = 1$ | the fewest violations |

In the fuzzy row of the VCSP column, a preference $p$ becomes the valuation $1 - p$. In practice the weighted case uses costs in $\{0, \ldots, k\}$ with $k$ meaning "forbidden" and the bounded sum $a \oplus b = \min(k, a + b)$. This is the *weighted CSP* or *cost function network*, and with Boolean variables it is [weighted Max-SAT](/weighted-max-sat/).

**Idempotent or not.** When $\times$ is idempotent ($a \times a = a$), as $\min$ in the fuzzy case, ordinary local consistency extends directly: a constraint can be combined with its own projections without changing the problem. When it is not, as $+$ in the weighted case, counting a cost twice is wrong, and consistency must *move* costs between constraints instead of copying them (Schiex 2000, Cooper and Schiex 2004). This is soft arc consistency.

**Branch and bound with bounds.** The standard exact method for a totally ordered problem is [depth-first branch and bound](/depth-first-branch-and-bound/) over partial assignments. For the weighted case:

- *Upper bound* $\mathit{UB}$: the cost of the best complete assignment found so far, the [incumbent](/incumbent-solution/), or $k$ at the start.
- *Lower bound* by partial forward checking: for a partial assignment $t$ with unassigned variables $U$,
  $$\mathit{LB}(t) = \sum_{c \text{ fully assigned by } t} c(t) + \sum_{y \in U} \min_{b \in D(y)} \mathit{ic}(y, b) ,$$
  where $\mathit{ic}(y, b)$ is the total cost of the constraints between $y$ and assigned variables when $y = b$. Each term is at most the cost that any extension pays on disjoint sets of constraints, so $\mathit{LB}(t)$ is at most the cost of every extension.
- *Lower bound by soft arc consistency*: keep a zero-arity cost $c_\varnothing$. Node consistency moves $\min_b c_y(b)$ from each unary cost into $c_\varnothing$, and arc consistency moves $\min_{b} c_{xy}(a, b)$ from each binary cost into $c_x(a)$. Each move keeps the cost of every assignment the same, so $c_\varnothing$ is a lower bound. After the assignments of $t$ are applied, node consistency alone makes $c_\varnothing$ at least as large as the bound above, and arc consistency can only raise it (Larrosa and Schiex, 2004).
- *Pruning*: drop the node when $\mathit{LB}(t) \ge \mathit{UB}$, and remove a value $b$ of $y$ when $\mathit{LB}(t) + \mathit{ic}(y, b) - \min_{b'} \mathit{ic}(y, b') \ge \mathit{UB}$.

For the fuzzy case the same scheme works with $\max$ in place of $+$ in the bound: the cost of any extension is at least the largest cost already paid.

For an SCSP with a partial order, branch and bound must keep a set of incomparable best levels, and a node is pruned only when its bound is worse than or equal to one of them.

**How this page relates to Maximum CSP.** The [Maximum CSP](/maximum-csp/) page is about one optimization problem: hard constraints, each with a weight, and the goal of the fewest or lightest violations. Its algorithms and complexity results are for that case. This page is about the frameworks that contain it, where each tuple, not only each constraint, has a level, and the levels may be combined by $\min$, $\max$ or a product as well as by a sum.

## Examples

**One table, two semirings.** Take $x, y \in \{a, b\}$, a unary constraint on $x$ and a binary constraint on $(x, y)$. In the fuzzy reading the numbers are preferences, and in the weighted reading they are costs.

| $t = (x, y)$ | fuzzy $c_x$ | fuzzy $c_{xy}$ | fuzzy level $\min$ | weighted $c_x$ | weighted $c_{xy}$ | weighted cost $+$ |
|---|---|---|---|---|---|---|
| $(a, a)$ | 0.9 | 0.8 | 0.8 | 1 | 2 | 3 |
| $(a, b)$ | 0.9 | 0.2 | 0.2 | 1 | 0 | 1 |
| $(b, a)$ | 0.5 | 0.3 | 0.3 | 3 | 4 | 7 |
| $(b, b)$ | 0.5 | 1.0 | 0.5 | 3 | 0 | 3 |

The fuzzy optimum is $(a, a)$ with level $\max = 0.8$. The weighted optimum is $(a, b)$ with cost $\min = 1$. The choice of $\times$ and $+$ changes the answer.

**Soft arc consistency gives a bound at the root.** Take $x, y \in \{a, b\}$ and one weighted constraint $c_{xy}(a,a) = 1$, $c_{xy}(a,b) = 1$, $c_{xy}(b,a) = 2$, $c_{xy}(b,b) = 3$. With nothing assigned, the partial forward checking bound is 0. Arc consistency moves $\min_y c_{xy}(a, y) = 1$ to $c_x(a)$ and $\min_y c_{xy}(b, y) = 2$ to $c_x(b)$, which leaves $c_{xy} = (0, 0, 0, 1)$. Node consistency then moves $\min(1, 2) = 1$ from $c_x$ to $c_\varnothing$. The bound is now $c_\varnothing = 1$, which equals the optimum, at $(a, a)$ or $(a, b)$, and the cost of each of the four assignments is unchanged.

## Where it is used

- Scheduling and timetabling with preferences, such as the earth observation satellite scheduling benchmarks of Bensana, Lemaître and Verfaillie, and frequency assignment problems (CELAR).
- Probabilistic inference: finding the most probable explanation in a Bayesian network is a weighted CSP with costs $-\log p$, solved with the same branch and bound and [bucket elimination](/bucket-elimination/).
- Weighted CSP solvers such as toulbar2, and MaxSAT solvers for the Boolean case ([Max-SAT](/max-sat/), [partial Max-SAT](/partial-max-sat/)).
- Preference modelling in configuration, where a fuzzy or lexicographic semiring is more natural than costs.

## References

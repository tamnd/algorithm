---
tag: H27570
kind: technique
slug: orbital-branching
name: Orbital branching
aliases:
- symmetry breaking in branch-and-bound
- branching on orbits
area: optimization/integer-programming
level: research
summary: Branch on an orbit of symmetric binary variables, so that symmetric copies of a subproblem are not searched twice.
prereqs: [land-doig-algorithm, binary-integer-programming, graph-automorphism-group, automorphism-orbit]
see_also: [symmetry-breaking, graph-automorphism-group, automorphism-orbit, nauty, branching-rule, strong-branching, presolve, binary-integer-programming]
sources:
  - paper: doi:10.1007/s10107-009-0273-x
    title: James Ostrowski, Jeff Linderoth, Fabrizio Rossi and Stefano Smriglio, Orbital branching, Mathematical Programming 126(1), 2011
    locator: pp. 147 to 178 (the branching disjunction on an orbit, its validity, orbital fixing, and the computational comparison)
  - paper: "François Margot, Pruning by isomorphism in branch-and-cut, Mathematical Programming 94, 2002, 71 to 90"
    locator: isomorphism pruning, the earlier method that orbital branching is compared with
  - paper: "Robert G. Jeroslow, Trivial integer programs unsolvable by branch-and-bound, Mathematical Programming 6, 1974, 105 to 109"
    locator: the instance 2x_1 + ... + 2x_n = n with n odd and the exponential lower bound for variable branching
  - paper: "François Margot, Symmetry in integer linear programming, in 50 Years of Integer Programming 1958 to 2008, Springer, 2010"
    locator: survey of symmetry handling, including the formulation group, orbital fixing and orbital branching (pages unsure)
---

Orbital branching is a branching rule for binary programs with many symmetries. At a node of [branch and bound](/land-doig-algorithm/), it computes the group of permutations of the variables that map the node's problem to itself, picks an orbit of this group, and branches into "one chosen variable of the orbit is 1" and "all variables of the orbit are 0". The first child stands for all the children that variable branching would create on the other members of the orbit, because they are symmetric copies of it. Ostrowski, Linderoth, Rossi and Smriglio introduced the method at IPCO 2007, and the journal version appeared in 2011.

## In plain words

Many models contain parts that are interchangeable: identical machines, identical colors, identical bins. A solution can then be rewritten in many ways by swapping these parts, and plain branch and bound may search each rewritten copy again.

Orbital branching first finds which variables can be swapped with each other without changing the problem. Such a group of interchangeable variables is called an orbit. Instead of setting one variable to 1 or 0, it splits into "this one variable is 1" and "every variable of the group is 0". If some variable of the group is 1 in a good solution, a swapped copy of that solution has the chosen variable equal to 1, so the first part already holds an equally good solution. No second search of the copies is needed.

## When it applies

- A binary program $\max\{c^\top x : A x \le b,\ x \in \{0,1\}^n\}$ whose formulation has a large symmetry group. A permutation $\pi$ of the columns is a *symmetry of the formulation* if some permutation $\sigma$ of the rows gives $a_{\sigma(i) \pi(j)} = a_{ij}$, $b_{\sigma(i)} = b_i$ and $c_{\pi(j)} = c_j$ for all $i$ and $j$. Such a $\pi$ maps feasible points to feasible points of the same value.
- The group can be computed. In practice, the formulation is turned into a colored graph whose [automorphism group](/graph-automorphism-group/) is the symmetry group of the formulation, and a tool such as [nauty](/nauty/) or bliss computes generators and [orbits](/automorphism-orbit/).
- Typical sources of symmetry: identical machines in scheduling, the colors in [graph coloring](/graph-coloring/), the bins in bin packing, and the blocks in covering designs and codes.

## The template

At a node $N$ let $F_0$ and $F_1$ be the variables fixed to 0 and 1 by branching. The holes are GROUP (how the symmetry group of the node is computed) and CHOOSE-ORBIT.

```pseudo id=main
ORBITAL-BRANCH(N, x̄)
L1  G ← GROUP(N)                         ▷ e.g. the symmetries π of the formulation with π(F₀) = F₀ and π(F₁) = F₁
L2  O₁, ..., O_p ← the orbits of G on the free variables
L3  O ← CHOOSE-ORBIT(O₁, ..., O_p, x̄)    ▷ e.g. an orbit with a fractional x̄_j and the largest Σ x̄
L4  j ← any variable in O
L5  N¹ ← N with x_j = 1
L6  N⁰ ← N with x_i = 0 for all i ∈ O
L7  return N¹ and N⁰
```

**Why no optimum is lost.** Every $\pi$ in $G$ is a symmetry of the formulation that maps $F_0$ to $F_0$ and $F_1$ to $F_1$, so it maps the feasible points of $N$ to feasible points of $N$ with the same objective value. Let $x$ be a feasible point of $N$. If $x_i = 0$ for all $i \in O$, then $x$ is a point of $N^0$. Otherwise $x_i = 1$ for some $i \in O$. Since $O$ is an orbit, some $\pi \in G$ maps $i$ to $j$, and the point $y$ with $y_{\pi(k)} = x_k$ for all $k$ is feasible for $N$, has the same value, and has $y_j = x_i = 1$. So $y$ is a point of $N^1$. Hence the best value over $N^0$ and $N^1$ equals the best value over $N$, and the rule is correct inside any branch and bound. The children do not cover all points of $N$, only one representative of each class of symmetric points; this is how the rule saves work.

**Jeroslow's instance.** For odd $n$, consider the binary program with the single constraint
$$2x_1 + 2x_2 + \dots + 2x_n = n.$$
It has no solution, since the left side is even. A node that fixes $a$ variables to 1 and $z$ variables to 0 has a feasible LP relaxation exactly when $2a \le n$ and $2(n - z) \ge n$, that is, when $a \le \tfrac{n-1}{2}$ and $z \le \tfrac{n-1}{2}$. With no incumbent, every node with a feasible LP must be branched. So with variable branching, every node at depth at most $\tfrac{n-1}{2}$ has a feasible LP, and the tree contains the full binary tree of that depth, with at least $2^{(n+1)/2} - 1$ nodes. This is Jeroslow's lower bound.

With orbital branching, every permutation of the free variables is a symmetry of the node, so they form one orbit. The child $N^0$ fixes all free variables to 0 and is infeasible, and the child $N^1$ has one more variable fixed to 1. After $\tfrac{n+1}{2}$ steps the LP is infeasible. The tree has $n + 2$ nodes.

| $n$ | variable branching (exact count) | lower bound $2^{(n+1)/2} - 1$ | orbital branching |
|---|---|---|---|
| 5 | 39 | 7 | 7 |
| 7 | 139 | 15 | 9 |
| 11 | 1847 | 63 | 13 |

The exact counts for variable branching come from the rule above: a node is a leaf exactly when its LP is infeasible, so the counts do not depend on the order of the variables.

## Classic examples

- **Covering designs and codes.** Ostrowski and others tested orbital branching on highly symmetric instances such as covering design problems, Steiner triple covering problems and the construction of codes. They report that it was competitive with isomorphism pruning and much better than a commercial solver of that time on these symmetric instances. This is a measured result on their test set.
- **Isomorphism pruning.** Margot (2002) prunes a node of the tree if its set of variables fixed to 1 is not the lexicographically smallest in its orbit under the group. This keeps one representative of each class of symmetric nodes, at the cost of using a fixed order of the variables.
## Variations

- **Orbital fixing.** Variables in the same orbit as a variable fixed to 0 by branching can, under conditions given by Ostrowski and others and by Margot, also be fixed to 0. This removes symmetric copies without branching.
- **Choosing the orbit.** CHOOSE-ORBIT can prefer the orbit with the largest sum of LP values, the largest orbit, or the orbit of the variable that an ordinary branching rule such as [strong branching](/strong-branching/) would pick. Ostrowski and others compare several such rules in their computational study.
- **Group of the original formulation.** Computing the full group of each node is expensive. A cheaper choice for GROUP is the subgroup of the root group that fixes $F_0$ and $F_1$ setwise, which is what the template uses. It may be smaller than the full group of the node, but it is easy to maintain.
- **Symmetry-breaking constraints.** A different approach adds inequalities, such as lexicographic ordering constraints or orbitopes, that remove all but one member of each symmetry class from the feasible set. These interact badly with branching rules that ignore them; see [symmetry breaking](/symmetry-breaking/) for the same idea in constraint programming.
- **General integer variables.** For general integer variables, the analogous disjunction branches on the bound of one variable against the bounds of all variables in the orbit.

## Pitfalls

- **Symmetries of the formulation only.** The rule uses permutations that map the formulation to itself. Symmetries of the problem that the formulation hides, for example after a non-symmetric [presolve](/presolve/), are not found.
- **Unbalanced children.** The child $N^0$ fixes a whole orbit and is often pruned fast, while $N^1$ fixes one variable. If the orbits are small, the gain over variable branching is small.
- **Combination with other symmetry methods.** Using orbital branching together with symmetry-breaking inequalities or a different isomorphism pruning order can remove all optimal solutions, because each method keeps a different representative.
- **Group computation cost.** Computing orbits at every node takes time. Solvers compute the group once at the root and use subgroups at the nodes.
- **Not a partition.** The children do not cover all points of the node. Methods that need every solution, such as counting all optimal solutions, must not use this rule.

## Exercises

1. In Jeroslow's instance with $n = 5$, draw the orbital branching tree and check that it has 7 nodes.
2. Prove that the internal nodes of the variable branching tree for Jeroslow's instance are counted by $\sum_{a, z \le (n-1)/2} \binom{a + z}{a}$, and check the value 39 for $n = 5$.
3. For [graph coloring](/graph-coloring/) with $k$ interchangeable colors and variables $x_{vc}$, describe the orbits of the root group and the first orbital branching step.
4. Give a binary program with a symmetry of the problem that is not a symmetry of the formulation.
5. Suppose the group is computed before the constraints $x_1 \ge x_2 \ge \dots \ge x_n$ are added for one orbit. Show by an example that orbital branching with a chosen variable other than $x_1$ in line L4 can then cut off every optimal solution.

## References

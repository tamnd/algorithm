---
tag: G7Y062
kind: problem
slug: company-party-planning
name: Planning a company party (maximum weight independent set in a tree)
aliases:
- Planning a company party
area: graphs/tree-algorithms
level: core
summary: Choosing guests from a company hierarchy tree so that no employee attends with their direct supervisor and the total score is maximal.
prereqs: [rooted-tree, tree-dynamic-programming]
see_also: [maximum-independent-set-in-trees, independent-set-on-trees, left-child-right-sibling, independent-set, vertex-cover, rerooting-technique]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 14, Dynamic Programming, the end-of-chapter problem Planning a company party (Problem 15-6 in the third edition)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 10.2, Solving NP-Hard Problems on Trees (maximum-weight independent set on a tree)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 6, Section 6.7, Independent sets in trees
---

Planning a company party is a textbook dynamic programming problem from CLRS: a company has a hierarchy in the shape of a [rooted tree](/rooted-tree/), each employee has a conviviality rating, and the guest list must leave out every employee whose direct supervisor is invited, while the sum of the ratings is as large as possible. It is the [maximum-weight independent set problem on a tree](/maximum-independent-set-in-trees/), told as a story, and it is solved in $\Theta(n)$ time by keeping two values per employee: the best score of the employee's group with the employee invited, and with the employee not invited.

## In plain words

A company has a president at the top, and every other employee has exactly one direct boss. You plan a party. Each employee has a score that says how much fun they bring. Nobody enjoys a party with their direct boss, so you never invite an employee together with that employee's boss. You want the guest list with the highest total score.

Look at any boss and the whole group under that boss. Either the boss comes, and then none of the boss's direct reports can come, or the boss does not come, and then each direct report's group is free. So each employee needs only two numbers from each direct report: the best score of their group with them invited, and without them. Work from the bottom of the chart to the top.

## Definition

**Input.** A rooted tree $T$ on the employees $\{0, \ldots, n-1\}$, $n \ge 1$, with the president as the root $r$ and an edge from each employee $v \ne r$ to the direct supervisor $p(v)$. The tree is weighted on its vertices: employee $v$ has a conviviality rating $c(v)$, a real number. In CLRS the tree is stored in the [left-child, right-sibling](/left-child-right-sibling/) representation, where each node points to its first subordinate and to its next colleague with the same supervisor.

**Output.** A guest list $G \subseteq \{0, \ldots, n-1\}$ such that $v \in G$ implies $p(v) \notin G$ for each $v \ne r$, which maximizes $c(G) = \sum_{v \in G} c(v)$.

The condition says that $G$ is an [independent set](/independent-set/) of the tree, because the edges of the tree are exactly the pairs (employee, direct supervisor). The empty list is allowed, so the optimum is at least 0.

**The recurrence.** For an employee $v$ with direct reports $C(v)$, let $in(v)$ and $out(v)$ be the best scores within $v$'s group (the subtree of $v$) with $v$ invited and not invited. Then

$$in(v) = c(v) + \sum_{u \in C(v)} out(u), \qquad out(v) = \sum_{u \in C(v)} \max(in(u), out(u)),$$

and the answer is $\max(in(r), out(r))$. The proof and the algorithm are on the page [independent set on trees](/independent-set-on-trees/).

## Variants

- **The president must attend.** The answer is then $in(r)$, and the reconstruction starts with $r$ in the list. In the same way, any employee can be forced in or out by setting the case that is not allowed to $-\infty$.
- **Negative ratings.** Some employees spoil the party. The recurrence needs no change: such an employee is never worth inviting, since $in(v) \le out(v)$ whenever $c(v) \le 0$.
- **Left-child, right-sibling input.** With only the pointers $child(v)$ and $sibling(v)$, the children of $v$ are the list $child(v), sibling(child(v)), \ldots$, and the recurrence sums over that list. A walk with an explicit stack over these pointers visits each node once, so the time stays $\Theta(n)$.
- **Also no grand-boss.** If no employee may attend with any ancestor within distance 2, the state must remember more of the path above, and each vertex keeps three values instead of two.
- **Count the best lists.** Keep, with each of the two values, the number of lists that reach it; add the counts of the cases that tie.

## Examples

A company of 8 employees. The president 0 has two vice presidents, 1 and 2. Employees 3 and 4 report to 1, employees 5 and 6 report to 2, and employee 7 reports to 6. The ratings are $c = [1, 8, 4, 3, 3, 1, 6, 2]$.

| $v$ | direct reports | $in(v)$ | $out(v)$ |
|---|---|---|---|
| 7 | none | 2 | 0 |
| 6 | 7 | 6 | 2 |
| 5 | none | 1 | 0 |
| 4 | none | 3 | 0 |
| 3 | none | 3 | 0 |
| 2 | 5, 6 | $4 + 0 + 2 = 6$ | $1 + 6 = 7$ |
| 1 | 3, 4 | 8 | $3 + 3 = 6$ |
| 0 | 1, 2 | $1 + 6 + 7 = 14$ | $8 + 7 = 15$ |

The best party has score 15 and the guest list $\{1, 5, 6\}$: the president stays home, vice president 1 comes, vice president 2 does not, so 5 and 6 can come, and 7 cannot come because 6 does. If the president must attend, the answer is $in(0) = 14$, with the list $\{0, 3, 4, 5, 6\}$.

Three small shapes:

- **A company of one.** The list is $\{0\}$ if $c(0) > 0$, else empty.
- **A chain of command** $0 \to 1 \to \cdots \to n-1$, each the boss of the next. With equal positive ratings, the best list is every second employee, $\lceil n/2 \rceil$ guests.
- **A flat company**, the president and $n - 1$ direct reports. The answer is $\max(c(0), \sum_{v \ne 0} \max(c(v), 0))$.

## Known algorithms

- **[Independent set on trees](/independent-set-on-trees/).** The two-value dynamic program in one bottom-up pass and one top-down pass for the list. $\Theta(n)$ time and $\Theta(n)$ extra memory, with no recursion.
- **Recursive memoized form.** A post-order recursion over the left-child, right-sibling tree, as most solutions to the CLRS problem write it. Same $\Theta(n)$ time; on a deep hierarchy it needs a deep call stack.
- **Brute force.** Try all $2^n$ lists. Useful only to test the others on small companies.

## Bounds

$\Theta(n)$ time in the word RAM, with ratings of $O(1)$ words: the dynamic program gives $O(n)$, and each rating must be read, since a change of one rating can change the answer. The extra memory is $\Theta(n)$ for the two values per employee, or $O(h)$ beyond the values if only the score is needed and the tree is walked with a stack of height $h$.

## Reductions

- **To and from maximum-weight independent set in trees.** The two problems are the same: the hierarchy is a rooted tree, and any tree becomes a hierarchy by choosing a root. See [maximum independent set in trees](/maximum-independent-set-in-trees/).
- **Minimum-weight vertex cover.** The employees left out form a [vertex cover](/vertex-cover/) of the hierarchy of least total rating, so one problem solves the other.

## Applications

The story is a teaching device for [dynamic programming on trees](/tree-dynamic-programming/): it shows how a subproblem is "the best answer for a subtree, given the state of its root", and how the root's state is the only link between a subtree and the rest. The same pattern solves dominating sets, matchings and colorings on trees, and with the [rerooting technique](/rerooting-technique/) it gives, for every employee at once, the best party that this employee attends.

## References

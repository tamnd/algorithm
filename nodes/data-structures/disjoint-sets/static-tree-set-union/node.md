---
tag: 3Y45D0
kind: problem
slug: static-tree-set-union
name: Static tree set union
area: data-structures/disjoint-sets
level: research
summary: Special case of disjoint-set union where the union tree structure is known in advance.
prereqs: [dynamic-equivalence-problem, rooted-tree, disjoint-set-forest]
see_also: [gabow-tarjan-union-find, dynamic-equivalence-problem, union-find-lower-bound, tarjan-offline-lca, offline-minimum, offline-subarray-painting, arpa-offline-rmq, word-ram]
sources:
  - paper: doi:10.1016/0022-0000(85)90014-5
    title: "Harold N. Gabow and Robert E. Tarjan, A linear-time algorithm for a special case of disjoint set union, Journal of Computer and System Sciences 30(2) (1985), 209-221"
    locator: the definition of static tree set union, the linear-time algorithm, and the list of applications
  - paper: doi:10.1016/0022-0000(79)90042-4
    title: "Robert Endre Tarjan, A class of algorithms which require nonlinear time to maintain disjoint sets, Journal of Computer and System Sciences 18(2) (1979), 110-127"
    locator: the lower bound for separable pointer algorithms
  - paper: doi:10.1145/73007.73040
    title: "Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, Proceedings of the 21st Annual ACM Symposium on Theory of Computing (1989), 345-354"
    locator: the remark that the separable lower bound holds for the special case of Gabow and Tarjan
---

Static tree set union is the special case of the [dynamic equivalence problem](/dynamic-equivalence-problem/) in which the shape of all unions is known in advance. A rooted tree $T$ on the $n$ elements is given first. Every union joins the set of a node $v$ with the set of its parent in $T$, so each set is a connected part of $T$, and its name is its top node. The unions and finds still come online, in any order. Gabow and Tarjan (1985) solved this problem in $O(n + m)$ time for $m$ operations on a RAM with words of $\Theta(\log n)$ bits, while the general problem needs $\Theta(m\,\alpha(m, n))$. Many uses of union-find are of this kind: [Tarjan's offline LCA algorithm](/tarjan-offline-lca/), [offline minimum](/offline-minimum/), [painting subarrays](/offline-subarray-painting/) and [Arpa's trick](/arpa-offline-rmq/) all link along a tree that can be computed first.

## In plain words

Picture a family tree. At the start, every person is in a group of their own. A step of the first kind says: "this person joins the group of their parent". A step of the second kind asks: "who is the oldest person in my group?".

So a group is always a part of the tree that hangs from one person, its top. The answer to a question is that top. You can also see it like this: each joined person gets a mark, and the answer for a person is the first unmarked person on the way up to the root.

The family tree is known from the start. That small fact is enough to make each step take constant time on average, which is not possible for general merges.

## Definition

**Input.** A rooted tree $T$ on the nodes $\{1, \ldots, n\}$, given by its parent array, and then a sequence of $m$ operations, online:

- $\mathrm{link}(v)$, for a node $v$ that is not the root and has not been linked before: unite the set of $v$ with the set of $\mathrm{parent}_T(v)$;
- $\mathrm{find}(v)$: return the name of the set of $v$.

**State.** At the start each node is a set of its own. Each set is a subtree of $T$ in the sense of a connected set of nodes, and its *name* is its node closest to the root. Equivalently, call a node *marked* when it has been linked. Then

$$\mathrm{find}(v) = \text{the nearest ancestor } u \text{ of } v \text{ in } T, \text{ with } v \text{ itself included, that is not marked}.$$

The root is never marked, so the answer exists.

**Cost.** The total time of the $m$ operations and of reading $T$, in the worst case, as a function of $n$ and $m$.

## Variants

- **Interval union-find.** $T$ is the path $1 - 2 - \cdots - n$, with $n$ as the root. Then $\mathrm{link}(i)$ joins $i$ with $i + 1$, each set is an interval, and $\mathrm{find}(i)$ is the least unmarked position $\ge i$. This is the case of [offline minimum](/offline-minimum/) and of [painting subarrays](/offline-subarray-painting/).
- **Incremental tree set union.** The tree is not given at once but grows by new leaves, which can be added between the other operations. Gabow and Tarjan also treat this form in linear time; it is the form that some matching algorithms need.
- **Offline.** The whole sequence of operations is known. Then the problem is easier still, but the algorithm of Gabow and Tarjan does not need this.
- **General unions.** If a union may join any two sets, this is the [dynamic equivalence problem](/dynamic-equivalence-problem/), with its lower bound $\Omega(m\,\alpha(m, n))$.

## Examples

**A tree of 8 nodes.** Let the root be 0, with $\mathrm{parent}(1) = \mathrm{parent}(2) = 0$, $\mathrm{parent}(3) = \mathrm{parent}(4) = 1$, $\mathrm{parent}(5) = 2$ and $\mathrm{parent}(6) = \mathrm{parent}(7) = 5$.

| operation | marked nodes after it | answer |
|---|---|---|
| find(6) | none | 6 |
| link(6) | 6 | |
| find(6) | 6 | 5 |
| link(5) | 5, 6 | |
| find(7) | 5, 6 | 7 |
| find(6) | 5, 6 | 2 |
| link(3) | 3, 5, 6 | |
| link(1) | 1, 3, 5, 6 | |
| find(3) | 1, 3, 5, 6 | 0 |
| find(4) | 1, 3, 5, 6 | 4 |
| link(2) | 1, 2, 3, 5, 6 | |
| find(6) | 1, 2, 3, 5, 6 | 0 |

At the end the sets are $\{0, 1, 2, 3, 5, 6\}$, $\{4\}$ and $\{7\}$. Node 7 is still a set of its own although its parent is in the large set, because 7 was never linked.

**Tarjan's offline LCA.** The DFS of [Tarjan's offline LCA algorithm](/tarjan-offline-lca/) unites each child with its parent when it leaves the child. That is $\mathrm{link}(\text{child})$ in the tree itself, so the algorithm is an instance of this problem and runs in $O(n + q)$ time with the Gabow-Tarjan structure.

## Known algorithms

| method | time for $n$ nodes and $m$ operations | model |
|---|---|---|
| walk up the marked nodes, no shortcuts | $O(nm)$ | any |
| [disjoint-set forest](/disjoint-set-forest/) with union by rank and [path compression](/path-compression/), the top node stored at each root | $O(n + m\,\alpha(m, n))$ | pointer machine |
| parent pointers to the next node, with path compression alone | $O(n + m \log_{2 + m/n} n)$ | pointer machine |
| [Gabow-Tarjan](/gabow-tarjan-union-find/): microsets in words and a macro forest | $O(n + m)$ | RAM with words of $\Theta(\log n)$ bits |

The Gabow-Tarjan algorithm splits $T$ into small connected parts, the *microsets*, each of $O(\log n)$ nodes. Inside a microset, the marks and the shape are kept in a word, and a find becomes a table lookup or a few word operations. The links between microsets go into a general union-find structure on $O(n/\log n)$ nodes, whose cost $O(m\,\alpha)$ is then hidden by the smaller number of its operations. See the [algorithm page](/gabow-tarjan-union-find/).

## Bounds

- **Upper bound.** $O(n + m)$ on a RAM with words of $\Theta(\log n)$ bits (Gabow and Tarjan, 1985).
- **Lower bound.** $\Omega(n + m)$, to read the tree and the operations.
- **On the pointer machine.** Tarjan's lower bound of 1979 for separable pointer algorithms, $\Omega(m\,\alpha(m, n))$, holds even for this special case, as Fredman and Saks point out. So the linear bound needs the address arithmetic of a RAM, and it is a case where a RAM beats every separable pointer algorithm.
- **Compared with the general problem.** For general unions the [union-find lower bound](/union-find-lower-bound/) gives $\Omega(m\,\alpha(m, n))$ in the cell-probe model, so knowing the tree in advance is what makes the difference.

## Reductions

- **To general union-find.** Store at each root the top node of its set. Then $\mathrm{link}(v)$ is $\mathrm{union}(v, \mathrm{parent}(v))$ and $\mathrm{find}(v)$ reads the top node of the root of $v$.
- **From interval problems.** [Offline minimum](/offline-minimum/) and [painting subarrays](/offline-subarray-painting/) link each used position to the next one, so they are interval union-find, with $T$ a path.
- **From offline RMQ.** [Arpa's trick](/arpa-offline-rmq/) links each position to its next smaller element. That tree can be computed first with a stack, so the sweep is static tree set union.
- **From offline LCA.** [Tarjan's offline LCA algorithm](/tarjan-offline-lca/) links each child to its parent in the input tree.

## Applications

- [Lowest common ancestors](/lowest-common-ancestor/) offline, and through them [range minimum queries](/range-minimum-query/) offline, in linear time.
- Scheduling unit jobs with deadlines or release times, where each job takes the next free slot in one direction.
- Matching in general graphs, where the blossoms of Edmonds' algorithm are merged along a search tree that grows by leaves; this was one of the motivations of Gabow and Tarjan.
- Other algorithms on trees and graphs that merge along a depth-first search tree known in advance.

## References

---
tag: V4360G
kind: definition
slug: confluent-persistence
name: Confluent persistence
aliases:
- confluently persistent
area: data-structures/persistent-structures
level: advanced
summary: Full persistence where two versions can be combined into a new one, so versions form a DAG.
prereqs: [full-persistence]
see_also: [partial-persistence, version-tree, catenable-deque, purely-functional-data-structure, finger-tree, persistent-trie, dsst-persistence-theorem, structural-sharing]
sources:
  - paper: doi:10.1145/185675.185791
    title: James R. Driscoll, Daniel D. K. Sleator and Robert E. Tarjan, Fully persistent lists with catenation, Journal of the ACM 41(5), 1994
    locator: pages 943 to 959, the introduction (operations that combine two versions, and persistent catenable lists)
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: pages 86 to 124, the closing remarks (operations on more than one version are left open)
  - paper: doi:10.1016/s0196-6774(03)00044-0
    title: Amos Fiat and Haim Kaplan, Making data structures confluently persistent, Journal of Algorithms 48(1), 2003
    locator: pages 16 to 58 (a general transformation, the effective depth of a version, and a lower bound on space)
  - paper: doi:10.1137/1.9781611973099.50
    title: Sébastien Collette, John Iacono and Stefan Langerman, Confluent persistence revisited, Proceedings of the 23rd ACM-SIAM Symposium on Discrete Algorithms (SODA 2012)
    locator: pages 593 to 601 (a general transformation with polylogarithmic overhead for bounded in-degree)
  - paper: doi:10.1007/s00453-008-9274-z
    title: Erik D. Demaine, Stefan Langerman and Eric Price, Confluently persistent tries for efficient version control, Algorithmica 57(3), 2010
    locator: pages 462 to 483 (confluently persistent tries, with version control as the motivation)
---

Confluent persistence is the strongest of the usual degrees of [persistence](/persistent-data-structure/). As in [full persistence](/full-persistence/), every version can be queried and updated, and no update changes an existing version. In addition, an operation may take two or more versions as input and combine them into a new version, as the concatenation of two lists does. A version can then have two parents, so the versions form a directed acyclic graph instead of a [version tree](/version-tree/). Every [purely functional data structure](/purely-functional-data-structure/) with a binary operation, such as a [catenable deque](/catenable-deque/), is confluently persistent.

## Definition

Let a data structure have queries, unary updates, which take one version, and **meld** operations, which take two versions. Start from one or more initial versions. After $m$ operations the structure holds versions $D_0, D_1, \ldots, D_m$. A **confluently persistent** structure supports, for all $i$ and $j$ with $0 \le i, j \le m$:

- $\text{query}(i, q)$: answer the query $q$ with respect to $D_i$;
- $\text{update}(i, u)$: make $D_{m+1} = u(D_i)$;
- $\text{meld}(i, j, g)$: make $D_{m+1} = g(D_i, D_j)$.

No operation changes an existing version, and the case $i = j$ is allowed. The **version DAG** has a node for each version and an edge from $D_i$ to $D_k$ when $D_i$ is an input of the operation that made $D_k$. Edges go from older to newer versions, so the graph has no cycle. A version made by a meld has two incoming edges, one for each input, or a double edge when $i = j$.

The term was introduced by Driscoll, Sleator and Tarjan (1994) for lists with catenation, after the 1989 paper on persistence had left operations on several versions open. The two weaker notions are special cases: if no meld is used, the version DAG is a tree and the definition is that of full persistence; if, in addition, every update applies to the newest version, it is a path and the definition is that of [partial persistence](/partial-persistence/).

The new feature is that a version may contain parts of the same old version more than once. Fiat and Kaplan measure this by the number of paths from the initial versions to a version in the DAG. That number can grow exponentially in $m$, and so can the size of a version: catenating a list with itself $m$ times gives a list of length $2^m$ from $m$ operations. A representation must therefore share parts within one version, not only between versions, and the general methods of the [DSST theorem](/dsst-persistence-theorem/) for full persistence do not apply as they are.

## Examples and non-examples

- **Self-catenation.** Let $D_0 = \langle a \rangle$ and let $D_{k+1} = \text{cat}(D_k, D_k)$. Then $D_m$ has $2^m$ elements. A [rope](/rope/) or a list with sharing represents $D_m$ by $m + 1$ nodes, each with two pointers to the node before it. The version DAG has a double edge from each $D_k$ to $D_{k+1}$.
- **Persistent catenable lists and deques.** Driscoll, Sleator and Tarjan gave confluently persistent catenable lists with $O(\log \log k)$ time per catenation. Kaplan and Tarjan, and later Okasaki, gave purely functional [catenable deques](/catenable-deque/), with $O(1)$ worst-case and $O(1)$ amortized time per operation. A [finger tree](/finger-tree/) supports catenation in $O(\log \min(n_1, n_2))$ time.
- **Purely functional structures.** In a language without mutation, an operation on two values returns a new value that shares parts of both inputs and changes neither. So every functional structure with a binary operation, such as the union of two sets in a functional [binary search tree](/binary-search-tree/) or the merge of two functional heaps, is confluently persistent by construction.
- **Version control.** Each commit of a repository is a version of a file tree, and a merge commit has two parents. Demaine, Langerman and Price designed confluently persistent [tries](/persistent-trie/) with this use in mind.
- **Non-example: a version tree.** A text editor with branching undo, in which each edit applies to one old state, is fully persistent but not confluent. Its versions form a tree.
- **Non-example: an ephemeral meld.** The union of two disjoint sets in a [disjoint-set](/disjoint-set/) forest destroys both inputs. It combines two structures, but no input survives, so the structure is not persistent at all.

## Related definitions

- [Full persistence](/full-persistence/): updates of any version, with a version tree; the special case without melds.
- [Partial persistence](/partial-persistence/): updates of the newest version only.
- [Version tree](/version-tree/): the version graph of a fully persistent structure, which a meld turns into a DAG.
- [Purely functional data structure](/purely-functional-data-structure/): a structure without mutation, which gives confluent persistence at no extra cost to the interface.
- [Structural sharing](/structural-sharing/): the reuse of parts of old versions, which confluent persistence extends to parts of one version.
- [Catenable deque](/catenable-deque/) and [finger tree](/finger-tree/): the main confluently persistent sequences.
- General transformations: Fiat and Kaplan (2003) gave the first general method for pointer structures, with costs that depend on the number of paths in the version DAG, and a lower bound on space in terms of the same quantity; Collette, Iacono and Langerman (2012) gave a method with polylogarithmic overhead per operation for structures of bounded in-degree.

## References

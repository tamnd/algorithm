---
tag: Y3W16W
kind: algorithm
slug: chawathe-tree-diff
name: Chawathe change detection
aliases:
- change detection in hierarchically structured information
area: strings/text-processing-and-typesetting
level: advanced
summary: Turn a node matching of two ordered labeled trees into a least cost script of inserts, deletes, updates and subtree moves that keeps it, in O(n d) time for d misaligned nodes.
model: word-ram
complexity:
  vars: {n: the total number of nodes of the two trees, d: the number of misaligned nodes}
  time: {worst: O(n + n d)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [longest-common-subsequence, breadth-first-search, tree-traversal]
see_also: [tree-edit-distance, zhang-shasha-algorithm, myers-diff, semistructured-merge, heckel-diff, tichy-block-moves, tree-isomorphism, diff3]
sources:
  - paper: doi:10.1145/233269.233366
    title: Sudarshan S. Chawathe, Anand Rajaraman, Hector Garcia-Molina and Jennifer Widom, Change detection in hierarchically structured information, SIGMOD 1996, 493-504
    locator: the conference version of the report below; the section, figure and example numbers on this page are those of the report
  - url: http://ilpubs.stanford.edu:8090/115/1/1995-46.pdf
    title: Sudarshan S. Chawathe, Anand Rajaraman, Hector Garcia-Molina and Jennifer Widom, Change detection in hierarchically structured information, Stanford InfoLab report 1995-46, with appendices
    locator: Section 3.2, the edit operations, Example 3.1 and the cost model; Section 4, the running example of Figure 1, the align phase with the LCS and Figure 7, Algorithm EditScript in Figure 8, AlignChildren and FindPos in Figure 9, and the O(ND) bound; Section 5, Matching Criteria 1 to 3, Theorem 5.2, Algorithm Match in Figure 10, Example 5.1 and Algorithm FastMatch in Figure 11; Section 7, LaDiff; Section 8 and Table 1, the experiments and the post-processing; Appendix B, the running times of Match and FastMatch; Appendix C, Lemma C.1 and Theorem C.2
---

Chawathe change detection finds the changes between two versions of a tree, such as two versions of a structured document, as an *edit script*: a list of inserts and deletes of leaves, updates of values, and moves of whole subtrees. It works in two steps. First it matches the nodes of the old tree with the nodes of the new tree that stand for the same thing. Then Algorithm EditScript turns the matching into a script that keeps all the matched pairs and has the smallest cost among such scripts, in time $O(n d)$, where $n$ is the number of nodes and $d$ the number of misaligned nodes. Sudarshan Chawathe, Anand Rajaraman, Hector Garcia-Molina and Jennifer Widom described the method at Stanford in 1996, with Algorithm FastMatch for the matching of documents without keys, and built it into LaDiff, a tool that marks the changes between two LaTeX documents.

## In plain words

Think of a document as a tree: the document has sections, sections have paragraphs, and paragraphs have sentences. Between two versions, some sentences are new, some are gone, some have new words, and some paragraphs moved.

First decide which old parts are the same as which new parts. A sentence matches a sentence with almost the same words, and a paragraph matches a paragraph that keeps most of its sentences.

Then walk through the new tree from the top, one level at a time. For each new part, take its old partner, fix its words if they changed, and move it under the right parent if it is somewhere else. Put the children in the right order with as few moves as possible. Add the new parts that have no partner. At the end, remove the old parts that nobody matched.

## The problem

The input is two ordered trees $T_1$ (old) and $T_2$ (new), whose nodes have identifiers, labels and values, and a matching $M$: a set of pairs $(x, y)$ of a node of $T_1$ and a node of $T_2$ with the same label, each node in at most one pair. The four operations are INS$((w, l, v), y, k)$, which inserts a new leaf $w$ with label $l$ and value $v$ as the $k$-th child of $y$; DEL$(x)$, which deletes a leaf; UPD$(x, v)$, which sets the value of $x$; and MOV$(x, y, k)$, which makes $x$ the $k$-th child of $y$, with its subtree. Inserts, deletes and moves cost 1, and an update costs compare$(v, v')$, a number in $[0, 2]$. The output is a script of least cost that transforms $T_1$ into a tree that differs from $T_2$ only in identifiers, and whose final matching contains $M$. The paper calls this the minimum conforming edit script (MCES) problem.

## The algorithm

EditScript goes through $T_2$ in [breadth-first](/breadth-first-search/) order and changes $T_1$ as it writes each operation. When it reaches a node $x$, its parent is already in place in $T_1$, so it can put the partner of $x$ under the partner of $p(x)$. Each node of $T_2$ is marked "in order" once the position of its partner among its siblings is final.

```pseudo id=main
EDIT-SCRIPT(T1, T2, M)
L1  if the roots of T1 and T2 are not a pair of M then put new roots above T1 and T2 and add them to M as a pair
L2  for each node x of T2 in breadth-first order, with y = p(x):
L3      if x has no partner then INS((w, l(x), v(x)), partner(y), FIND-POS(x)) for a new w; add (w, x) to M; mark x in order
L4      else w ← partner(x)
L5          if v(w) ≠ v(x) then UPD(w, v(x))
L6          if x is not the root and (p(w), y) ∉ M then MOV(w, partner(y), FIND-POS(x)); mark x in order
L7      ALIGN-CHILDREN(partner(x), x)
L8  for each node w of T1 in post-order: if w has no partner then DEL(w)
L9  return the script and M

ALIGN-CHILDREN(w, x)
L10 mark all children of x out of order
L11 S1 ← the children of w whose partners are children of x; S2 ← the children of x whose partners are children of w
L12 S ← LCS(S1, S2), where a equals b if (a, b) ∈ M; mark the nodes of S2 in S in order
L13 for each a in S1 that is not in S, with partner b: MOV(a, w, FIND-POS(b)); mark b in order

FIND-POS(x)
L14 if no sibling of x to its left in T2 is marked in order then return 1
L15 u ← the partner of the rightmost such sibling; return 1 + the place of u among the children of p(u), without the partner of x
```

The [longest common subsequence](/longest-common-subsequence/) of line L12 keeps the most children in place, and only the others move. Lines L14 and L15 differ from Figure 9 of the paper in two details. The paper counts only the children that are marked in order, and it does not mark the nodes that lines L3 and L6 place. Both are needed: if $T_1$ is $r(d, a)$ with $d$ unmatched and $T_2$ is $r(a, b)$, counting only marked children puts the new $b$ at place 2, before $a$, and if $T_2$ is $r(a, b, c)$ with $b$ and $c$ new, an unmarked $b$ makes $c$ go directly after $a$.

**Finding the matching.** When the nodes have keys, the matching is simple. For documents without keys, the paper uses these rules. Two leaves may match if they have the same label and compare of their values is at most $f$, with $0 \le f \le 1$ (Criterion 1). Two internal nodes may match if they have the same label and more than a fraction $t$ of the leaves below the larger one are matched to leaves below the other, with $\frac12 \le t \le 1$ (Criterion 2). Algorithm FastMatch puts the nodes with each label in a chain from left to right. For each leaf label and then for each internal label, it computes an LCS of the two chains, with equal as the test, adds its pairs to the matching, and then pairs each node that is still unmatched with the first unmatched node of the other chain that passes the test. Algorithm Match does only this last step, for all nodes, from the bottom up.

## Example

This is the running example of the paper (Figure 1). The labels D, P and S stand for document, paragraph and sentence, the letters are the values of the sentences, and the numbers are the identifiers.

```
T1:  1 D                         T2:  11 D
       2 P:  5 a, 6 b, 7 c              12 P:  15 a, 16 c
       3 P:  8 d, 9 e                   13 P:  17 f
       4 P:  10 f                       14 P:  18 d, 19 e, 20 g
```

FastMatch first matches the sentences with equal values, $(5, 15)$, $(7, 16)$, $(8, 18)$, $(9, 19)$ and $(10, 17)$; sentence 6 has no partner. Then it matches the paragraphs: 2 has two of its three sentences matched into 12, 3 has two of the three sentences of 14, and 4 has the one sentence of 13, so with $t = 0.6$ it adds $(2, 12)$, $(3, 14)$ and $(4, 13)$. Last, it matches the documents, $(1, 11)$. Algorithm Match gives the same matching in Example 5.1 of the paper.

EditScript starts at the root 11. The roots are a pair, so line L1 does nothing. ALIGN-CHILDREN$(1, 11)$ compares $S_1 = 2, 3, 4$ with $S_2 = 12, 13, 14$, whose partners in $T_1$ are $2, 4, 3$. A longest common subsequence has length 2, so one paragraph must move. The code takes the subsequence $2, 4$ and writes MOV$(3, 1, 3)$; the paper takes $2, 3$ and writes MOV$(4, 1, 2)$, which costs the same. The children of 12, 13 and 14 are already aligned. Node 20 has no partner. Its marked left sibling is 19, whose partner 9 is the second child of 3, so line L3 writes INS$((21, S, g), 3, 3)$. The delete phase writes DEL$(6)$. The script has three operations, the least possible: sentence 6 must go, sentence $g$ must come, and the order of the paragraphs needs a move.

## Correctness

The proof file shows that EditScript is correct and minimal. When the loop reaches a node, its parent is processed, so the partner of the parent exists and no later operation changes its place. FIND-POS puts each node directly after the partner of its rightmost marked left sibling, so the marked partners stay in the order of $T_2$, and at the end all children of each node are marked. A node without a partner has no children with partners, so the post-order deletes it as a leaf. The resulting tree has the shape, the labels and the values of $T_2$.

For the cost, every script that pairs exactly the nodes of $M$ must delete each unmatched node of $T_1$, insert one for each unmatched node of $T_2$, update each pair with different values, and move each matched node whose parent is not the partner of its new parent. Among the children of a matched pair, the ones that never move keep their order, so they form a common subsequence, and at least the others must move. EditScript writes exactly these operations. With the definition of the paper, a script only needs to keep the pairs of $M$, and it may also update an unmatched leaf into an unmatched leaf of $T_2$, which can be cheaper than a delete and an insert. So minimality holds when the matching is maximal, which is what the matching criteria aim for.

## Complexity

EditScript visits each node a constant number of times, apart from ALIGN-CHILDREN and FIND-POS. The paper computes the LCS of line L12 with [Myers' algorithm](/myers-diff/), in time $O((|S_1| + |S_2|) d')$ for $d'$ misaligned children, and states a total of $O(n d)$, where $n$ is the number of nodes of both trees and $d$ the number of misaligned nodes: the least number of moves inside one parent over all minimum cost scripts. The code of this page uses the quadratic dynamic program for the LCS and scans the children at each call, so it takes $O(n^2)$ time and space in the worst case.

For the matching, let $c$ be the average cost of compare on two leaves. Algorithm Match takes time $O(n^2 c + m n)$ for $n$ leaves and $m$ internal nodes. For FastMatch, the paper bounds the time by $(n e + e^2) c + 2 l n e$, where $l$ is the number of internal labels and $e$ is the weighted edit distance: the cost of a shortest script in which inserts and deletes weigh 1, a move weighs the number of leaves of the moved subtree, and updates weigh 0. This bound assumes that leaf labels and internal labels are different, that all compares cost the same on average, and that a node with a given label has the average number of leaves. In the experiments on versions of three papers, FastMatch made about 20 times fewer comparisons than the bound, and $e$ was on average 3.4 times the number of operations.

## Properties

- **Conforming.** The final matching contains every pair of $M$; matched nodes are never deleted or inserted.
- **Minimum for the matching.** No script that pairs exactly the nodes of $M$ costs less. The quality of the result depends on the matching.
- **Moves of subtrees.** A moved node takes its subtree with it, so a moved paragraph costs one operation, not one per sentence.
- **Leaves only.** Inserts and deletes act on leaves. To delete an internal node, its children must first be moved away or deleted, which the post-order of line L8 does.
- **Order of the script.** An insert can come before a move into the new node, and the deletes come last, so the script can be applied in its order.
- **Unique matching.** With labels that form no cycles and Criteria 1 to 3, where Criterion 3 says that each leaf has at most one leaf on the other side with compare at most 1, there is a unique maximal matching (Theorem 5.2).

## Variants and improvements

- **Keys.** If the nodes have keys or object identifiers that stay the same between versions, the matching is given, and only EditScript is needed.
- **Post-processing of the matching.** When Criterion 3 fails, for example with many equal sentences, FastMatch can pair a leaf with the wrong copy. The paper corrects many such cases from the top down: a child of $x$ matched outside the partner of $x$ is matched again to a close child of the partner, if there is one.
- **Delta trees.** Section 6 of the paper writes the changes on the new tree, with marks for the inserted, deleted, updated and moved nodes, which is how LaDiff shows them.
- **General tree edit distance.** The [tree edit distance](/tree-edit-distance/) of the [Zhang and Shasha algorithm](/zhang-shasha-algorithm/) finds a least cost script without a given matching, but takes at least quadratic time and has no moves; its delete makes the children of the deleted node children of its parent.
- **Line diffs with moves.** On flat sequences, [Heckel's diff](/heckel-diff/) and [Tichy's block moves](/tichy-block-moves/) also report moved pieces.

## When to use it

Use it to find the changes between two versions of large hierarchical data, such as structured documents, XML or HTML pages, object databases or syntax trees, when moves of whole subtrees should count as one change. It is fastest when the versions are close. If the data has keys, the matching is free; if not, the criteria of FastMatch work when values seldom repeat. When the shortest script over all matchings is needed and the trees are small, use a general tree edit distance instead.

## Pitfalls

- **Unmatched roots.** If the roots are not a pair, add new roots above both trees, as line L1 does; the root of $T_1$ cannot be deleted while it has children.
- **FIND-POS as printed.** Counting only the children marked in order, or not marking the nodes placed by inserts and moves, puts new nodes at the wrong places; see the two cases under the algorithm.
- **The matching decides the result.** A bad matching gives a correct but long script. Two internal nodes with the same label are matched by their leaves, so a matching error at the leaves can carry up to the paragraphs and sections.
- **Repeated values.** Criterion 3 fails for documents with many equal or nearly equal sentences, and the matching may then not be optimal.
- **The LCS test.** The LCS of line L12 and of FastMatch can only test two items for equality. An LCS routine that sorts the items needs more than that; the paper notes that it could not use the LCS of the Unix diff for this reason.
- **Positions are 1-based.** MOV$(x, y, k)$ makes $x$ the $k$-th child after it is removed from its old place, which matters when $x$ moves inside its own parent.

## Implementations

## History

Chawathe, Rajaraman, Garcia-Molina and Widom worked at Stanford on change management for data warehouses, active databases and version management, where the old and new data often come as snapshots without keys. Earlier work on changes had dealt with flat files and relations, and the tree edit distance of Zhang and Shasha from 1989 was exact but at least quadratic. They set up the problem as a matching and a minimum conforming edit script, gave EditScript, Match and FastMatch, and built LaDiff, which marks the changes between two LaTeX documents with sentences, paragraphs, sections, lists and items. The work appeared at SIGMOD 1996, and as a Stanford report with the proofs and the analysis in appendices.

## References

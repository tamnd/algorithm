---
tag: KAQ8V7
kind: problem
slug: three-way-merge
name: Three-way merge
aliases:
- three-way file merge
area: strings/text-processing-and-typesetting
level: core
summary: Combine two edited versions of a file with their common ancestor, keeping the changes of both and reporting conflicts where they overlap.
prereqs: [shortest-edit-script, longest-common-subsequence]
see_also: [diff3, semistructured-merge, chawathe-tree-diff, operational-transformation, crdt, woot, patience-diff, histogram-diff]
sources:
  - paper: doi:10.1007/978-3-540-77050-3_40
    title: Sanjeev Khanna, Keshav Kunal and Benjamin C. Pierce, A formal investigation of Diff3, FSTTCS 2007, LNCS 4855, 485-496
    locator: the formal model of a merge with maximum matchings of the base against each version, the stable and unstable chunks and their four classes, the example of Fig. 1, and the properties that hold or fail (idempotence, stability, locality, and the safe configurations of Theorem 4.1.1)
  - paper: "Tom Mens, A state-of-the-art survey on software merging, IEEE Transactions on Software Engineering 28(5), 2002, 449-462"
    locator: two-way and three-way merging, textual, syntactic, semantic and structural merging, and state-based and operation-based merging
  - url: https://git-scm.com/docs/merge-strategies
    title: Git, merge strategies
    locator: the three-way merge of the recursive strategy, and the merged tree of the common ancestors that it uses as the base when there is more than one
  - paper: doi:10.1145/2025113.2025141
    title: Sven Apel, Jörg Liebig, Benjamin Brandl, Christian Lengauer and Christian Kästner, Semistructured merge, rethinking merge in revision control systems, ESEC/FSE 2011, 190-200
    locator: Section 2, unstructured and structured merge, and the conflicts of a line-based merge when two versions add members at the same place
---

A three-way merge takes a base version $O$ of a file and two versions $A$ and $B$ that were edited from it separately, and builds one version that has the changes of both. Where only one side changed a part of the file, that change is taken. Where both sides changed the same part in different ways, the merge reports a *conflict* and leaves the choice to a person. The base is what makes this possible: without it, a line that is in $A$ and not in $B$ could have been added in $A$ or deleted in $B$. Version control systems do a three-way merge each time they merge two branches, and the usual method is [diff3](/diff3/), built on two [shortest edit scripts](/shortest-edit-script/) against the base. Real-time collaborative editors solve a related problem with [operational transformation](/operational-transformation/) or a [CRDT](/crdt/) such as [WOOT](/woot/); these merge the edit operations as they happen, instead of three finished versions, and they never report a conflict.

## In plain words

Two people take a copy of the same file and change it, each in their own way. Now you want one file with both sets of changes.

Compare each changed copy with the original. A part that one person changed and the other did not is easy: take the change. A part that both changed in the same way is also easy. A part that both changed in different ways is a conflict, and the merge shows both versions so that a person can decide.

The original is needed. If you only had the two changed copies and a line was in one and not in the other, you could not tell whether one person added it or the other removed it.

## Definition

**Input.** Three sequences of lines: the base $O$, and two versions $A$ and $B$ derived from it.

**Alignment.** A merge starts from a matching of $O$ with $A$ and a matching of $O$ with $B$, each a set of pairs of equal lines that increase in both files, usually from a [longest common subsequence](/longest-common-subsequence/) of each pair of files. A line of $O$ that is matched in both is *stable*. Khanna, Kunal and Pierce cut the three files into *chunks*: a stable chunk is a run of lines that are matched in all three files at once, and an unstable chunk is the part between two stable chunks, given by its three pieces $(A_i, O_i, B_i)$, some of which may be empty.

**Merge rule.** For each unstable chunk:

- if $O_i = B_i$, only $A$ changed it, and the merge takes $A_i$;
- if $O_i = A_i$, only $B$ changed it, and the merge takes $B_i$;
- if $A_i = B_i \ne O_i$, both made the same change (a *false conflict*), and the merge takes it;
- otherwise all three differ, and the chunk is a *conflict*.

**Output.** The merged file: the stable chunks, the taken pieces, and for each conflict a marked region that shows $A_i$ and $B_i$, and often $O_i$. Some tools output, instead of one file, the three new versions $A'$, $O'$ and $B'$ that agree except at the conflicts.

**What a good merge means.** There is no single accepted correctness criterion. The rule above is fixed, but the result depends on the two matchings, which are not unique. Khanna, Kunal and Pierce state properties that one would like: running the merge again on its output should change nothing (idempotence), a small change of one input should cause only a small change of the output (stability), and changes in distant parts of the file should not interact (locality). They show that diff3 has none of them in general.

## Variants

- **Two-way merge.** Only $A$ and $B$, without the base. It cannot tell an add from a delete, so every difference is a conflict or a guess.
- **Line, word or character units.** The usual unit is the line. Smaller units give fewer false conflicts but more surprising results.
- **Structured merge.** Merge abstract syntax trees, not lines, so that changes that are independent in the program, such as two new methods at the same place, do not conflict; [semistructured merge](/semistructured-merge/) does this for declarations and keeps line merging for method bodies. A tree merge can use a tree diff with moves, such as [Chawathe's change detection](/chawathe-tree-diff/).
- **Several bases.** In a version history, two branches can have more than one nearest common ancestor. Git's recursive strategy first merges the common ancestors into one tree and uses that as the base.
- **Operation-based merge.** Record the edit operations, not only the states, and combine the two lists of operations. This is the setting of [operational transformation](/operational-transformation/) and of sequence [CRDTs](/crdt/), which choose an order for concurrent inserts and so never conflict.

## Examples

**A merge without conflicts.** Let $O = [a, b, c]$, $A = [a, x, b, c]$ and $B = [a, b, c, y]$. Each version adds one line at a different place. The stable lines are $a$, $b$ and $c$. The unstable chunks are (between $a$ and $b$) $A_i = [x]$ with $O_i$ and $B_i$ empty, and (after $c$) $B_i = [y]$ with $O_i$ and $A_i$ empty. Each chunk changed on one side only, so the merge is $[a, x, b, c, y]$.

**A conflict.** Let $O = [a, b, c]$, $A = [a, p, c]$ and $B = [a, q, c]$. Both versions changed $b$, in different ways, so the chunk $([p], [b], [q])$ is a conflict. A merge tool prints a region like this:

```
a
<<<<<<< A
p
||||||| O
b
=======
q
>>>>>>> B
c
```

**The example of Khanna, Kunal and Pierce.** Let $A = [1, 4, 5, 2, 3, 6]$, $O = [1, 2, 3, 4, 5, 6]$ and $B = [1, 2, 4, 5, 3, 6]$. With the matchings that GNU diff3 uses, $O$ and $A$ share 1, 2, 3, 6, and $O$ and $B$ share 1, 2, 4, 5, 6. The chunks are: stable 1; unstable $([4, 5], [\,], [\,])$, changed in $A$ only; stable 2; unstable $([3], [3, 4, 5], [4, 5, 3])$, a conflict; stable 6. The merge takes 4, 5 from $A$ and reports one conflict: in their notation the output is $A' = [1, 4, 5, 2, 3, 6]$, $O' = [1, 4, 5, 2, 3, 4, 5, 6]$ and $B' = [1, 4, 5, 2, 4, 5, 3, 6]$. With another longest matching of $O$ and $A$, for example 1, 4, 5, 6, the chunks and the conflict are different, which shows that the result depends on the matchings.

## Known algorithms

- **[diff3](/diff3/).** Compute the two matchings with a line diff, cut the files into stable and unstable chunks in one pass, and apply the merge rule. It is the merge of GNU diffutils and, in its essentials, of the merge commands of version control systems. Khanna, Kunal and Pierce give it as a precise algorithm and prove its properties.
- **Choice of the diff.** The two matchings can come from [Myers' algorithm](/myers-diff/), [patience diff](/patience-diff/) or [histogram diff](/histogram-diff/). The choice moves the chunk borders and so changes which conflicts appear.
- **[Semistructured merge](/semistructured-merge/).** Parse each version into a tree of declarations, merge the trees by name and kind, where the order of members does not matter, and run a line merge only inside the bodies.
- **Tree merges with a tree diff.** Compute edit scripts from the base tree to each version, for example with [Chawathe's change detection](/chawathe-tree-diff/), and combine the two scripts.
- **Operational transformation and CRDTs.** For edits that arrive one at a time, transform concurrent operations against each other ([operational transformation](/operational-transformation/)) or give each element an identity that fixes its place ([WOOT](/woot/) and other [CRDTs](/crdt/)).

## Bounds

- **Time.** A line merge costs two diffs plus a linear pass. With [Myers' algorithm](/myers-diff/) the diffs cost $O(n D)$ for files of $n$ lines in total and edit scripts of size $D$, and with the dynamic program for a longest common subsequence they cost $O(n^2)$. The chunk pass is $O(n)$.
- **The matchings.** The longest matchings are not unique, and the merge result depends on which ones are used, so a fast diff that gives a different longest matching can give a different merge.
- **Properties.** Khanna, Kunal and Pierce show that diff3 is not idempotent: a second run on the output of a first run can change the result. It is not stable, even for runs without conflicts: a small change of one input can change the output a lot. And it is not local in general. They also prove a positive result, their Theorem 4.1.1: for inputs that they call safe, which needs a line that occurs exactly once in each of the three files in a stable part, the merge gives the unique synchronization without conflicts.

## Reductions

- **To two diffs.** A three-way merge reduces to two [shortest edit script](/shortest-edit-script/) problems, $O$ against $A$ and $O$ against $B$, plus a linear pass over the two matchings.
- **From two-way merge.** A merge of $A$ and $B$ with an empty base has no stable line, so the whole file is one chunk, and it is a conflict unless $A = B$ or one side is empty. This is why a merge without a base cannot decide anything.
- **To tree merge.** A file is a tree of depth one, a root with its lines as children in order, so a merge of ordered trees includes the line merge as a special case.

## Applications

- **Version control.** Merging branches in Git, Mercurial, Subversion and their predecessors. Each merge of two branches is a three-way merge with a common ancestor as base.
- **File synchronizers.** Tools such as Unison keep replicas of a directory in step, and use a three-way merge when a file changed on both replicas since the last synchronization. Unison comes from Pierce's group.
- **Software merging research.** Mens surveys textual, syntactic, semantic and structural merging, and the state-based and operation-based approaches.
- **Patches.** Applying a patch made against an old version to a newer version is a merge with the old version as base.

## References

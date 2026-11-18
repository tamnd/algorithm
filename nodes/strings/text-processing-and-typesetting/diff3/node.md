---
tag: 8YT0S8
kind: algorithm
slug: diff3
name: diff3 algorithm
aliases:
- diff3 merge
area: strings/text-processing-and-typesetting
level: core
summary: Merge by diffing the ancestor with each version, splitting the files into stable and unstable chunks, and taking the side that changed in each chunk.
model: word-ram
complexity:
  vars: {n: the total number of lines of the three files}
  time: {worst: O(n^2)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [three-way-merge, shortest-edit-script, longest-common-subsequence]
see_also: [myers-diff, patience-diff, histogram-diff, heckel-diff, semistructured-merge, chawathe-tree-diff, operational-transformation]
sources:
  - paper: doi:10.1007/978-3-540-77050-3_40
    title: Sanjeev Khanna, Keshav Kunal and Benjamin C. Pierce, A formal investigation of Diff3, FSTTCS 2007, LNCS 4855, 485-496
    locator: Section 2, the stable and unstable chunks, their four classes and the output of a chunk; Figure 2, the algorithm of the parse, with Lemma 3.1; Figure 1, the example with the matchings of GNU diff3; Figures 3 and 4 and Theorem 4.1.1 on locality and idempotence; the history in Section 1
  - url: https://git-scm.com/docs/git-merge
    title: Git, git-merge, how conflicts are presented
    locator: the conflict markers of the default style, the diff3 style with the base after the ||||||| marker, and the zdiff3 style
  - url: https://git-scm.com/docs/git-merge-file
    title: Git, git-merge-file
    locator: the three-way merge of three files, the conflict markers, the labels of the -L option, the number of conflicts as exit value, and the note that it is a minimal clone of RCS merge
---

diff3 is the standard method for a [three-way merge](/three-way-merge/) of text files. It compares the common ancestor $O$ with each of the two versions $A$ and $B$, using a line diff such as [Myers' algorithm](/myers-diff/), and gets two matchings of equal lines. A line of $O$ that is matched in both versions is *stable*. One pass over the three files cuts them into stable chunks, where all three agree, and unstable chunks between them. In each unstable chunk the merge takes the side that changed, or the common change if both changed it in the same way, and it marks a conflict where the two sides changed it in different ways. It is the method of the GNU diff3 program, and version control systems such as CVS and Subversion use it to merge files. Khanna, Kunal and Pierce wrote it as a precise algorithm in 2007 and showed that it has fewer of the expected properties than its users believe.

## In plain words

Two people edit copies of the same file. To merge their work, compare the original with each copy, line by line.

Some lines are still in both copies, in their places. They are anchors. Between two anchors there is a gap, and in each gap you look at three small pieces: the original, the first copy and the second copy.

If the piece of one copy is the same as the original, only the other person changed this part, so you take their version. If both copies have the same new text, you take it. If all three pieces are different, both people changed the same part in different ways. That is a conflict, and the merge writes both versions, with the original, between marker lines, so that a person can choose.

## The problem

The input is a base $O$ and two versions $A$ and $B$, each a sequence of lines, and two matchings: $M_A$ pairs lines of $O$ with equal lines of $A$, and $M_B$ pairs lines of $O$ with equal lines of $B$, each strictly increasing in both files. Usually each matching is a longest common subsequence, from a [shortest edit script](/shortest-edit-script/). For a line $x$ of $O$ that has a partner in both, let $a(x)$ and $b(x)$ be its partners; the triple $(x, a(x), b(x))$ is then a stable point. The output is the merged file, with the stable lines, the changes of each side, and a marked region for each conflict.

## The algorithm

The indices $l_O$, $l_A$ and $l_B$ are the first lines of the three files that no chunk has taken yet.

```pseudo id=main
DIFF3(A, O, B, M_A, M_B)
L1  l_O ← 0; l_A ← 0; l_B ← 0; P ← an empty list of chunks
L2  loop: i ← 1; while (l_O + i - 1, l_A + i - 1, l_B + i - 1) is a stable point do i ← i + 1
L3      if i = 1 then x ← the least line x ≥ l_O of O with partners in both; if there is none, leave the loop
L4          append the unstable chunk (A[l_A .. a(x) - 1], O[l_O .. x - 1], B[l_B .. b(x) - 1]) to P; (l_O, l_A, l_B) ← (x, a(x), b(x))
L5      else append the stable chunk of the next i - 1 lines of each file to P; add i - 1 to l_O, l_A and l_B
L6  if some lines are left, append the rest of the three files to P as an unstable chunk
L7  for each chunk (A_i, O_i, B_i) of P: if it is stable, or O_i = B_i, or A_i = B_i, output A_i; else if O_i = A_i, output B_i; else output a conflict region
L8  return the output and the number of conflicts
```

Lines L1 to L6 are Figure 2 of Khanna, Kunal and Pierce, with indices from 0. Line L7 is the merge rule. Khanna, Kunal and Pierce name the classes of an unstable chunk: *changed in A* if $O_i = B_i \ne A_i$, *changed in B* if $O_i = A_i \ne B_i$, *falsely conflicting* if $A_i = B_i \ne O_i$, and *truly conflicting* if the three pieces are all different. A conflict region is written in the diff3 style of Git:

```
<<<<<<< A
the lines of A_i
||||||| O
the lines of O_i
=======
the lines of B_i
>>>>>>> B
```

The implementation takes both matchings from the shared helper, a [longest common subsequence](/longest-common-subsequence/) by dynamic programming, or from the caller. It also returns the three new versions $A'$, $O'$ and $B'$ of the paper, in which a chunk that changed on one side is copied to all three.

## Example

This is Figure 1 of Khanna, Kunal and Pierce. Let $A = [1, 4, 5, 2, 3, 6]$, $O = [1, 2, 3, 4, 5, 6]$ and $B = [1, 2, 4, 5, 3, 6]$. GNU diff3 matches the lines 1, 2, 3, 6 of $O$ with $A$, and the lines 1, 2, 4, 5, 6 of $O$ with $B$. The stable points are the lines 1, 2 and 6 of $O$.

| chunk | $A_i$ | $O_i$ | $B_i$ | class | merge |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | stable | 1 |
| 2 | 4, 5 | | | changed in A | 4, 5 |
| 3 | 2 | 2 | 2 | stable | 2 |
| 4 | 3 | 3, 4, 5 | 4, 5, 3 | truly conflicting | conflict region |
| 5 | 6 | 6 | 6 | stable | 6 |

So the merge is 1, 4, 5, 2, then a conflict that shows $[3]$, $[3, 4, 5]$ and $[4, 5, 3]$, then 6. In the form of the paper the output is $A' = [1, 4, 5, 2, 3, 6]$, $O' = [1, 4, 5, 2, 3, 4, 5, 6]$ and $B' = [1, 4, 5, 2, 4, 5, 3, 6]$.

The matching of $O$ with $A$ is not unique: 1, 4, 5, 6 is also a longest common subsequence, and the helper of this page picks it. Then the stable points are 1, 4, 5 and 6, and the merge has two conflicts, $([\,], [2, 3], [2])$ and $([2, 3], [\,], [3])$. The same three files give a different merge with a different diff.

## Correctness

The proof file shows that lines L1 to L6 return a *diff3 parse*, the definition of Khanna, Kunal and Pierce: the chunks cut the three files into consecutive pieces, every stable point lies in a stable chunk at the same place in its three pieces, and each stable chunk is as large as possible. The key fact is an invariant: every stable point that is not yet in a stable chunk lies after $l_O$, $l_A$ and $l_B$ in the three files, because the matchings increase. Line L3 takes the least such point, so no stable point falls inside an unstable chunk. Each round takes at least one line, so the loop ends. The proof then shows that the merge rule does what it should when only one side changed the file: if $A = O$, the merge is $B$, and if $B = O$, the merge is $A$, both without a conflict.

## Complexity

Let $n$ be the total number of lines of the three files, and count in the [word-RAM](/word-ram/) with lines compared in $O(1)$, for example by a hash of each line.

- **The chunk pass.** Each line of $O$ is tested at most twice in lines L2 and L3, and each line of each file is copied once, so lines L1 to L8 take $O(n)$ expected time with hash sets for the matchings.
- **The matchings.** Two line diffs dominate. With the dynamic program of the helper they cost $O(n^2)$ time and space. With [Myers' algorithm](/myers-diff/) they cost $O(n D)$ time, where $D$ is the size of the larger edit script, and $O(n)$ space in the linear space version.

## Properties

- **One side unchanged.** If $A = O$, the merge is $B$, and if $B = O$, it is $A$, for any maximum matchings. If $A = B$ and both use the same matching, the merge is $A$.
- **Depends on the matchings.** Two longest matchings can give different chunks and different conflicts, as in the example.
- **Not idempotent.** Figure 4 of Khanna, Kunal and Pierce: for $A = [1, 2, 4, 6, 8]$, $O = [1, 2, 3, 4, 5, 5, 5, 6, 7, 8]$ and $B = [1, 4, 5, 5, 5, 6, 2, 3, 4, 8]$, where each pair has one maximum matching, a run gives $A' = [1, 2, 4, 6, 8]$, $O' = [1, 2, 3, 4, 6, 7, 8]$ and $B' = [1, 4, 6, 2, 3, 4, 8]$, and a second run on these changes them again, to $[1, 4, 6, 2, 4, 6, 8]$, $[1, 4, 6, 2, 4, 6, 7, 8]$ and $[1, 4, 6, 2, 4, 8]$.
- **Not local.** Figure 3: let $O = (1, 2)^n\, 1, 2$, let $A$ add $1, 2$ at the start and $B$ replace the last $1, 2$ by $3$. The two edits are far apart for large $n$, yet with a maximum matching that shifts $A$ by one period the last chunk is a conflict, for every $n$.
- **Safe inputs.** Theorem 4.1.1: cut $O$ into a start, a middle and an end. If at most one side changes the start, at most one side changes the end, no side changes the middle, and the middle has a line that occurs exactly once in each of the three files, the merge is unique and has no conflict. A unique line such as a function header often plays this role in source code.
- **Not stable.** Khanna, Kunal and Pierce also show that similar inputs can give very different outputs, even without conflicts.

## Variants and improvements

- **Conflict styles.** The RCS merge style, the default of Git, shows only $A_i$ and $B_i$. The diff3 style adds $O_i$ after a `|||||||` marker. The zdiff3 style of Git also moves the equal lines at the start and end of a conflict out of the region.
- **The diff used.** The matchings can come from any line diff, such as [patience diff](/patience-diff/) or [histogram diff](/histogram-diff/), which match unique or rare lines first and so often give anchors that people expect.
- **Structure.** [Semistructured merge](/semistructured-merge/) parses the files into declarations and runs a diff3 merge only inside method bodies, and tree merges use a tree diff such as [Chawathe's change detection](/chawathe-tree-diff/).
- **Operations instead of states.** Editors for live collaboration merge each edit as it happens, with [operational transformation](/operational-transformation/) or a CRDT, and never show a conflict.

## When to use it

Use diff3 to merge two versions of a text file that have a known common ancestor, as version control systems do. It is simple, fast and easy to explain, and its conflict regions are what most programmers know. When the files have structure that a line merge does not respect, such as declarations whose order does not matter, use a structured or [semistructured merge](/semistructured-merge/). For edits that arrive one at a time from many users, use [operational transformation](/operational-transformation/).

## Pitfalls

- **Adjacent edits conflict.** If $A$ changes one line and $B$ changes the next line, no stable point lies between them, and the chunk is a conflict: $O = [a, b]$, $A = [x, b]$ and $B = [a, y]$ give one conflict. With one stable line between the edits there is no conflict.
- **False conflicts are taken without a note.** If both sides made the same change, the merge takes it once. This is right in most cases, but if both sides added the same line for different reasons, one copy is lost.
- **The matchings are part of the input.** A different diff, or another version of the same diff, can give different conflicts. Tests must fix the matchings or the diff.
- **A clean merge is not a correct program.** diff3 sees lines, not meaning. Two changes without a conflict can still break the program together, for example when one side renames a function and the other side adds a call to its old name.
- **Marker lines in the data.** A file that already has lines such as `=======` makes the conflict regions hard to read and to parse again.

## Implementations

## History

Khanna, Kunal and Pierce write that diff3 was developed by Randy Smith in 1988, as the GNU diff3 program, and that version control systems such as CVS and Subversion made it popular. The default conflict style of Git is the one of the merge program of RCS, and Git's merge-file command is a minimal clone of that program. In 2007 Khanna, Kunal and Pierce gave a formal account of diff3, with its chunk algorithm, the counterexamples to idempotence, stability and locality, and the condition on a unique line under which a merge is safe.

## References

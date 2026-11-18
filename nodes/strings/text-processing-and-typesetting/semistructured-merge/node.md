---
tag: 30FJFE
kind: algorithm
slug: semistructured-merge
name: Semistructured merge
aliases:
- structured merge
area: strings/text-processing-and-typesetting
level: research
summary: Merge program versions on their trees of declarations, matching elements by name so that reordered members do not conflict, with line merge inside bodies.
model: word-ram
complexity:
  vars: {n: the total number of nodes and body lines of the three versions}
  time: {worst: O(n^2)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: true, online: false}
prereqs: [three-way-merge, diff3, hash-table]
see_also: [chawathe-tree-diff, diff3, three-way-merge, operational-transformation, crdt, longest-common-subsequence]
sources:
  - paper: doi:10.1145/2025113.2025141
    title: Sven Apel, Jörg Liebig, Benjamin Brandl, Christian Lengauer and Christian Kästner, Semistructured merge, rethinking merge in revision control systems, ESEC/FSE 2011, 190-200
    locator: Section 2, the stack example with the methods top and size; Section 3, program structure trees, superimposition, the annotated grammar with FSTNonTerminal and FSTTerminal, line-based merge of terminals, deletions and conflict handlers; Section 4, the tool FSTMerge; Section 5, the study of 24 projects and 180 merge scenarios and the effect of renaming
  - paper: "Tom Mens, A state-of-the-art survey on software merging, IEEE Transactions on Software Engineering 28(5), 2002, 449-462"
    locator: textual, syntactic, semantic and structural merging, and the merge of trees and graphs
---

Semistructured merge is a [three-way merge](/three-way-merge/) for program files that uses part of the structure of the language. Each version is parsed into a tree of its declarations, such as classes, fields and methods. Declarations whose order does not matter, such as the methods of a Java class, are matched by kind and name, not by place, and merged again inside. Declarations whose text order matters, such as method bodies, are kept as plain text and merged line by line with [diff3](/diff3/). So two new methods that two developers add at the same place, which a line merge reports as a conflict, are both kept without one. Sven Apel, Jörg Liebig, Benjamin Brandl, Christian Lengauer and Christian Kästner described the method in 2011, built it into the tool FSTMerge, and found in 24 projects that it reduces the number of conflicts in most merges, but that renaming makes it worse.

## In plain words

Two people change the same class. One adds a method at the end, the other adds a different method at the end. A normal merge only sees lines, so it finds two new pieces of text at the same place, and it cannot know which one comes first. It gives up and reports a conflict.

But in many languages the order of the methods in a class does not matter. So read each version as a list of named parts, and match the parts by their names. A part that only one person added is simply kept. A part that both people have is merged again, and inside a method body, where the order of the lines matters, use the normal line merge.

Conflicts then only appear where both people changed the same method in different ways.

## The problem

The input is a base program $O$ and two revisions $A$ and $B$, each parsed into a *program structure tree*. A grammar of the language marks which constructs become *nonterminal* nodes, whose children may be in any order and have distinct keys (kind and name), and which become *terminal* nodes, whose content is kept as text. The output is a merged tree, printed back as a program, and a list of conflicts.

## The algorithm

The merge starts at the three roots and goes down the trees. For a node, $x$, $y$ and $z$ denote the children of $a$, $o$ and $b$ with a given key; any of them may be absent.

```pseudo id=main
MERGE(a, o, b)        ▷ a and b have the same key; o is their base, absent if both sides added the node
L1  if a is a terminal then return LINE-MERGE(a.body, o.body or nothing, b.body)
L2  K ← the keys of the children of a in their order, then the keys of the children of b that a does not have
L3  for each key k in K, with children x of a, y of o and z of b:
L4      if x and z are both present then append MERGE(x, y, z)
L5      else if y is absent then append the one of x and z that is present      ▷ added on one side
L6      else if the present one differs from y then append it and report a conflict      ▷ deleted on one side, changed on the other
        ▷ else the node was deleted on one side and not changed on the other: drop it
L7  return a with the appended children
```

LINE-MERGE is the merge rule of [diff3](/diff3/): match the base with each side by a [longest common subsequence](/longest-common-subsequence/), take the side that changed between two lines that all three keep, and mark a conflict where both changed in different ways. Lines L2 to L6 are *superimposition*, the composition of trees by name that the FeatureHouse tools of Apel and his colleagues use for software composition, plus the rules for deletions. Apel et al. handle deletions "following RCS's merge" and do not give the rules; lines L5 and L6 are the rules of this page. A grammar can also attach a *conflict handler* to a kind of terminal, which merges it in a special way: their example is the list of interfaces in an `implements` clause, which is merged as a set.

## Example

This is the stack example of Apel et al. The base class has the methods `push` and `pop`. Revision TOP adds a method `top`, and revision SIZE adds a method `size`, both after `pop`.

```
class Stack {
    void push(T item) { ... }
    T pop() { ... }
}
```

A line merge sees two blocks of new lines before the same closing brace. It cannot choose an order, so it reports one conflict:

```
<<<<<<< A
    T top() { ... }
||||||| O
=======
    int size() { ... }
>>>>>>> B
}
```

The semistructured merge parses the three versions into trees. Each root is a class node named Stack, with the method nodes as children. Line L2 lists the keys push, pop and top of revision TOP, then size from revision SIZE. The methods push and pop are in all three versions and unchanged, so line L4 merges them to themselves. The methods top and size have no base, and each is in one revision only, so line L5 keeps both. The result has push, pop, top and size, and no conflict.

Now let revision TOP rename `pop` to `remove`, and let revision SIZE add a line to the body of `pop`. The key of `remove` is new, so line L5 keeps it. The key of `pop` is in the base and in SIZE only, with a changed body, so line L6 keeps SIZE's `pop` and reports a conflict. The merge cannot see that the two are the same method.

## Correctness

The proof file shows three facts. If one revision equals the base, the merge returns the other revision, with no conflict, up to the order of the members. Members with different keys never conflict with each other, wherever the two sides put them, because line L4 matches children by key and not by place. And a merge without conflicts gives the same result when the two revisions are swapped, up to order. The line merge inside bodies has the same properties for lines, which the proof also shows, so the facts carry over to the whole tree by induction on its height.

## Complexity

Let $n$ be the total number of nodes and body lines of the three versions. With hash maps for the children, each nonterminal node takes expected time linear in its number of children, so the tree part of the merge is expected $O(n)$; Apel et al. note that the merge is done in linear time. The line merge of each terminal costs two longest matchings of its bodies, $O(|o| (|a| + |b|))$ with the dynamic program of this page, so the total is $O(n^2)$ in the worst case, with $O(n^2)$ space for the table. A diff such as [Myers' algorithm](/myers-diff/) makes the body merges faster when the changes are small. Parsing and printing the programs are linear for the usual grammars.

## Properties

- **No ordering conflicts.** Two revisions that add different members to the same node never conflict, wherever they place them.
- **One side unchanged.** If one revision equals the base, the merge is the other revision, up to order.
- **Conflicts follow the structure.** A conflict is always inside one method or about one declaration, never across the borders of classes or methods, which makes it easier to read.
- **Order of the result.** The members of a node come in the order of one revision, followed by the members that only the other revision added. Where the order matters, the grammar must make the construct a terminal, so that the line merge keeps its order.
- **Renaming hurts.** A renamed member is a deleted member plus a new one, so changes to it on the other side lead to a conflict, or to two copies.
- **Needs a parser.** Each version must parse. A revision with a syntax error cannot be merged this way.

## Variants and improvements

- **Granularity.** The grammar decides how deep the tree goes. Apel et al. stop at methods and fields, and keep statements as text; deeper trees give a merge of full syntax trees, which needs matching of ordered nodes, such as a tree diff like [Chawathe's change detection](/chawathe-tree-diff/).
- **Conflict handlers.** Special merges for some kinds of terminals, such as lists of interfaces or modifiers, remove more conflicts.
- **A mix with line merge.** Apel et al. found that a tool that merges each file both ways and keeps the result with fewer conflicts reduces the conflicts by 35% compared with a line merge alone, because it avoids the cases with renaming.
- **Tracking renames.** If the editor or the version control system records renames, renamed members can be matched to their old keys.
- **Operation-based merge.** Recording the edit operations, as in [operational transformation](/operational-transformation/) or a [CRDT](/crdt/), avoids the question of matching altogether.

## When to use it

Use it to merge source files in languages where many declarations can be in any order, such as Java, C# or Python classes, when branches often add members at the same places. It needs a grammar of the language with the right marks, and the versions must parse. Keep a line merge for files that do not parse and for other files, and prefer it when a revision renames many elements.

## Pitfalls

- **Keys must be unique.** Overloaded methods in Java have the same name, so the key of a method must include its parameter types, or two methods are merged as one.
- **Deleted versus changed.** If one side deletes a member and the other side changes it, there is no safe choice; the merge must report it, not drop the change silently.
- **Added on both sides.** Two revisions that add members with the same key and different bodies give a line merge with an empty base, which is one large conflict.
- **Order that matters.** Some members do depend on their order, such as field initializers that refer to each other. If the grammar marks them as unordered, the merge may move them and change the program.
- **Comments and layout.** A printer that writes the merged tree may lose comments or change the layout of code that neither side touched.

## Implementations

## History

Version control systems have merged files as lines since the early tools, and merges of full syntax trees were studied in research for a long time, as Mens surveys in 2002, but they need a full grammar and a merge for each language. Apel and his colleagues proposed the middle way in an earlier workshop paper, and described it in full at ESEC/FSE 2011. They built FSTMerge as an extension of FeatureHouse, their tool infrastructure for software composition, in which a generator makes almost all the code for a new language from an annotated grammar. In their study of 24 projects in Java, C# and Python, with 180 merge scenarios, semistructured merge reduced the number of conflicts in 60% of the scenarios, by 34 ± 21%. In 26% of the scenarios, it increased the number of conflicts, by 109 ± 170%, and they traced these cases to renaming.

## References

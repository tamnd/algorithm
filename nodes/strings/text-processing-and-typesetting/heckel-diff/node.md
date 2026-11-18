---
tag: T7BYC1
kind: algorithm
slug: heckel-diff
name: Heckel's diff algorithm
aliases:
- Heckel's algorithm
area: strings/text-processing-and-typesetting
level: core
summary: Link the lines that occur once in each file, then extend the links to equal neighbors. Expected linear time with hashing; it finds moved blocks, but the diff is not minimal.
model: word-ram
complexity:
  vars: {n: the total number of lines in both files, r: the number of linked line pairs}
  time: {expected: O(n + r log r)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: false, adaptive: false}
prereqs: [shortest-edit-script, hash-table]
see_also: [patience-diff, histogram-diff, myers-diff, longest-common-subsequence, longest-increasing-subsequence, tichy-block-moves, hunt-szymanski, block-edit-distance]
sources:
  - paper: doi:10.1145/359460.359467
    title: Paul Heckel, A technique for isolating differences between files, Communications of the ACM 21(4), 1978, 264-268
    locator: the six passes, the symbol table entries with the counters OC and NC and the old line number OLNO, the arrays OA and NA, and the begin and end lines of Fig. 1
  - paper: "J. W. Hunt and M. D. McIlroy, An algorithm for differential file comparison, Computing Science Technical Report 41, Bell Laboratories, 1976"
    locator: the diff program based on a longest common subsequence of lines, the method that Heckel compares with
  - paper: doi:10.1007/BF01840446
    title: Eugene W. Myers, An O(ND) difference algorithm and its variations, Algorithmica 1, 1986, 251-266
    locator: the shortest edit script, the minimum that Heckel's method does not always reach
  - url: https://github.com/onmyway133/DeepDiff
    title: DeepDiff, a Swift library for collection diffs
    locator: Sources/Shared/Algorithms/Heckel.swift
---

Heckel's diff algorithm compares two files line by line in six passes over the lines and a [hash table](/hash-table/) of line counts. A line that occurs exactly once in the old file and exactly once in the new file is taken as the same line in both, and each such pair is then extended to the equal lines just before and just after it. The method runs in expected linear time, and because the pairs may cross, it can report a block of lines that moved. It is a heuristic: unlike [Myers' algorithm](/myers-diff/), it does not always find a [shortest edit script](/shortest-edit-script/). Paul Heckel published it in 1978.

## In plain words

Compare two versions of a file. First count how often each line occurs in each version. A line that occurs once in the old version and once in the new version is almost surely the same line in both, so tie the two copies together.

A line next to a tied line often belongs with it, even when it is a common line such as a closing brace. So walk down the new file, and when the line after a tied line equals the line after its partner, tie those too. Then do the same walk upward.

The tied lines tell you what stayed. Lines that are not tied were removed or added. Tied lines whose order changed show a block that moved.

## The problem

The input is an old file $O = \langle O_1, \ldots, O_m \rangle$ and a new file $N = \langle N_1, \ldots, N_n \rangle$, as sequences of lines, where only an equality test and a hash of a line are available. The output is a set of *links*, pairs $(j, i)$ with $O_j = N_i$ where each line is in at most one pair, and from them an edit script of keeps, deletes and inserts that turns $O$ into $N$, plus the blocks of linked lines that moved. The page writes $n$ for the total number of lines of both files in the cost bounds. The goal is a readable diff in linear time, not a minimum one: [Myers' algorithm](/myers-diff/) and the [Hunt-Szymanski algorithm](/hunt-szymanski/) solve the minimum problem, the [shortest edit script](/shortest-edit-script/).

## The algorithm

Heckel keeps one symbol table entry per distinct line, with a count $OC$ of its copies in $O$, a count $NC$ of its copies in $N$, and $OLNO$, the number of an old line that holds it. The array $NA[0 \ldots n + 1]$ holds for each new line either its entry (the line is *free*) or the number of the old line it is linked to; $OA[0 \ldots m + 1]$ is the same for the old file. Index 0 and the last index are a begin line and an end line that Heckel adds to both files.

```pseudo id=main
HECKEL(O[1 .. m], N[1 .. n])
L1  T ← an empty hash table of entries (OC, NC, OLNO)
L2  for i ← 1 to n do e ← T[N[i]], made if missing; e.NC ← e.NC + 1; NA[i] ← e        ▷ pass 1
L3  for j ← 1 to m do e ← T[O[j]], made if missing; e.OC ← e.OC + 1; e.OLNO ← j; OA[j] ← e   ▷ pass 2
L4  NA[0] ← 0; OA[0] ← 0; NA[n + 1] ← m + 1; OA[m + 1] ← n + 1        ▷ link the begin and end lines
L5  for i ← 1 to n do                                                  ▷ pass 3: lines unique in both
        if NA[i] is an entry e with e.NC = 1 and e.OC = 1 then j ← e.OLNO; NA[i] ← j; OA[j] ← i
L6  for i ← 0 to n do                                                  ▷ pass 4: extend downward
        if NA[i] is a line j and NA[i + 1], OA[j + 1] are the same entry then NA[i + 1] ← j + 1; OA[j + 1] ← i + 1
L7  for i ← n + 1 downto 1 do                                          ▷ pass 5: extend upward
        if NA[i] is a line j and NA[i - 1], OA[j - 1] are the same entry then NA[i - 1] ← j - 1; OA[j - 1] ← i - 1
L8  L ← the pairs (NA[i], i) for 1 ≤ i ≤ n where NA[i] is a line      ▷ pass 6 starts here
L9  K ← a longest subset of L that increases in both coordinates
L10 return the script that keeps K, deletes and inserts the rest, and the pairs of L - K grouped into moved blocks
```

Lines L2 and L3 are Heckel's passes 1 and 2. Line L5 is pass 3: it links the lines that are unique in both files. Lines L6 and L7 are passes 4 and 5: a link from line $i$ to line $j$ pulls along the next pair $(i + 1, j + 1)$ if both are still free and equal, and the loop of line L6 runs upward in $i$, so a run of equal lines is linked in one sweep. The begin and end lines make the equal first and last lines of the two files act as if they were next to a link. Heckel's pass 6 prints the result from the arrays. Lines L8 to L10 are the version of pass 6 that this page uses to get an edit script: the links may cross, and a script can keep only pairs that do not cross, so line L9 keeps a [longest increasing subsequence](/longest-increasing-subsequence/) of them, by [patience sorting](/patience-sorting/). This choice of the kept pairs is a design choice of the page, not a step of the paper.

## Example

The old file has two functions, f and g, and the new file has the same functions in the other order.

| line | old $O$ | new $N$ |
| --- | --- | --- |
| 1 | int f() | int g() |
| 2 | { | { |
| 3 | return 1; | return 2; |
| 4 | } | } |
| 5 | int g() | int f() |
| 6 | { | { |
| 7 | return 2; | return 1; |
| 8 | } | } |

The table has six entries. The four lines int f(), return 1;, int g() and return 2; have $OC = NC = 1$. The lines { and } have $OC = NC = 2$.

| step | new links $(i, j)$, new line $i$ with old line $j$ |
| --- | --- |
| pass 3 (L5) | $(1, 5)$ int g(); $(3, 7)$ return 2;; $(5, 1)$ int f(); $(7, 3)$ return 1; |
| pass 4 (L6), $i = 1$ | $NA[2]$ and $OA[6]$ both hold the entry of {: link $(2, 6)$ |
| pass 4, $i = 3$ | $NA[4]$ and $OA[8]$ both hold }: link $(4, 8)$ |
| pass 4, $i = 5$ | link $(6, 2)$ |
| pass 4, $i = 7$ | link $(8, 4)$ |
| pass 5 (L7) | no free pairs are left |

All 8 lines are linked. In order of the new lines, the old line numbers are 5, 6, 7, 8, 1, 2, 3, 4. A longest increasing subsequence has length 4, and line L9 keeps the f block (1, 2, 3, 4). The result is a script that inserts the four lines of g at the top and deletes the four old lines of g at the bottom, and one moved block: old lines 5 to 8 went to new lines 1 to 4. The script has 8 operations, the minimum here, since a longest common subsequence has 4 lines. A tool that knows the moved block can print "lines 5 to 8 moved to the top" instead of a delete and an insert.

The standard example that the method is not minimal is $O = [u, a, a, a, v]$ and $N = [a, a, a, u, v]$. Pass 3 links $u$ and $v$. The lines next to them are linked already, or they are the begin line, so passes 4 and 5 link no $a$. The script keeps $u$ and $v$, inserts three $a$ lines and deletes three $a$ lines: 6 operations. The common subsequence $a, a, a, v$ gives 2 operations.

## Correctness

The proof file shows an invariant of the arrays: $NA[i] = j$ exactly when $OA[j] = i$, a linked pair has equal lines, and a free cell holds the entry of its own line. Passes 3 to 5 link only two free cells with the same entry, so the invariant holds after each step. From it follow three results. First, the links pair equal lines, each line is in at most one link, and every line that occurs exactly once in each file is linked to its copy. Second, the kept pairs of line L9 increase in both coordinates, so the script of line L10 is valid: applied to $O$, it gives $N$. Third, when neither file has a repeated line, all common lines are linked and line L9 keeps a longest common subsequence, so the script is a shortest edit script. With repeated lines the third result fails, as the second example shows.

## Complexity

Count in the [word-RAM](/word-ram/), with $n$ the total number of lines of both files and $r$ the number of links, $r \le n / 2$.

- **Time.** Lines L2 and L3 do one table lookup per line. With a hash table, a lookup costs $O(1)$ expected time plus the time to hash the line, which is linear in its length, so the passes over the text take expected time linear in the size of the input. Lines L4 to L8 do $O(1)$ work per line, without hashing, since they compare entries by identity. Line L9 does one binary search per link, $O(r \log r)$, and line L10 is one pass. In total, $O(n + r \log r)$ expected table operations and steps. Heckel's own pass 6, which prints the links without choosing an increasing subset, keeps the whole method $O(n)$ expected.
- **Worst case of the table.** The linear bound is an expected bound over the hash function. With a balanced search tree in place of the hash table, each lookup costs $O(\log n)$ comparisons, and the passes cost $O(n \log n)$ comparisons of lines.
- **Space.** The table has at most $n$ entries, and the arrays have $n + 4$ cells in total: $O(n)$.

## Properties

- **Not minimal.** The script can be much longer than a shortest one, as the second example shows. The method trusts unique lines and never searches.
- **Finds moves.** Links may cross, and the crossing links are blocks that moved. A diff based on a longest common subsequence cannot show a move; it shows a delete and an insert.
- **Linear and simple.** Six passes, no dynamic program and no recursion.
- **Greedy extension.** Passes 4 and 5 take the first equal neighbor that they meet, in a fixed order, and never undo a link.
- **Symmetric counts.** Only the counts $OC$ and $NC$ decide which lines are unique; the line contents are compared only through the table.

## Variants and improvements

- **Patience diff.** [Patience diff](/patience-diff/) also starts from the lines that are unique in both files, but it keeps only an increasing subset of them, by a longest increasing subsequence, and then recurses into the gaps, so lines between two anchors are matched again with new counts.
- **Histogram diff.** [Histogram diff](/histogram-diff/) uses lines with few copies when no unique line exists, and recurses as patience diff does.
- **Move detection by copies.** [Tichy's block move method](/tichy-block-moves/) builds the new file from copied blocks of the old file, so it can also express moves and repeated copies, with a different measure of cost.
- **List diffs in user interfaces.** Libraries that update a displayed list after a change in the data use Heckel's passes on item identifiers, because they need the moves, and the lists are often free of repeats. DeepDiff for Swift is one such library.

## When to use it

Use it when the diff must be fast and must show moved blocks, and when most lines are distinct, for example source files with many distinct statements, or lists of items with unique keys. Do not use it when a minimum diff is required, or when the files have long runs of repeated lines (blank lines, braces, table rows), since such lines can stay unlinked. For a minimum diff use [Myers' algorithm](/myers-diff/).

## Pitfalls

- **Begin and end lines.** Without the extra links of line L4, equal first lines and equal last lines that are not unique stay unlinked, because passes 4 and 5 need a linked neighbor to start from.
- **The order of pass 4 matters.** With $O = [\{, x, \}, \{, y, \}]$ and $N = [\{, y, \}, \{, x, \}]$, pass 4 links the first braces of both files from the begin line, and links each closing brace from the unique line before it. The second opening brace of each file is then left free, because its neighbors are already linked. The two blocks of three lines are not both found.
- **Crossing links are not a script.** An edit script can keep only pairs that increase in both files. Treating all links as kept lines gives an invalid script when a block moved. Choose an increasing subset, as line L9 does, and report the rest as moves.
- **Hash collisions.** If the table compares only hash values, two different lines with the same hash are taken as equal. Keep the full line in the entry and compare it.
- **The cost of hashing.** The linear time counts a line hash as one step. For very long lines, the time is linear in the total length of the text, not in the number of lines.

## Implementations

## History

Paul Heckel, then at Interactive Systems Consultants, published the method in Communications of the ACM in 1978. He presented it as a fast and simple alternative to the method of the Unix diff program of Hunt and McIlroy (1976), which computes a longest common subsequence of the lines. The same idea of unique lines as anchors came back in Bram Cohen's patience diff, and the passes are used today in list diff libraries.

## References

---
tag: 3MB06K
kind: algorithm
slug: patience-diff
name: Patience diff
aliases:
- patience diff algorithm
area: strings/text-processing-and-typesetting
level: core
summary: Match equal first and last lines, then the lines that occur once in both files by a longest increasing subsequence, and diff each gap between them again.
model: word-ram
complexity:
  vars: {n: the total number of lines in both files}
  time: {expected: O(n^2 log n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: true, online: false, adaptive: false}
prereqs: [longest-increasing-subsequence, patience-sorting, shortest-edit-script]
see_also: [heckel-diff, histogram-diff, myers-diff, longest-common-subsequence, hunt-szymanski, hash-table, diff3]
sources:
  - url: https://bramcohen.livejournal.com/73318.html
    title: Bram Cohen, Patience Diff Advantages, blog post, March 30, 2010
    locator: the four steps of the method (equal first lines, equal last lines, the longest common subsequence of the lines that occur once on both sides, and the same steps on each section between matched lines), and the example of a function inserted between two others
  - url: https://github.com/git/git/blob/master/xdiff/xpatience.c
    title: Git, the patience diff of the xdiff library (the option --patience)
    locator: the fallback to the classic diff in a range that has no line that is unique on both sides
  - paper: doi:10.1090/S0273-0979-99-00796-X
    title: David Aldous and Persi Diaconis, Longest increasing subsequences, from patience sorting to the Baik-Deift-Johansson theorem, Bulletin of the AMS 36(4), 1999, 413-432
    locator: patience sorting, and the number of piles as the length of a longest increasing subsequence
---

Patience diff compares two files line by line. It first matches the equal lines at the start and at the end. Then it takes only the lines that occur exactly once in each file, matches as many of them as it can in order, and diffs each gap between two matched lines in the same way. The matched unique lines are found as a [longest increasing subsequence](/longest-increasing-subsequence/), by [patience sorting](/patience-sorting/), which gives the method its name. Bram Cohen described it. The result is not always a [shortest edit script](/shortest-edit-script/), as from [Myers' algorithm](/myers-diff/), but it often reads better, because it does not align unrelated code on common lines such as braces and blank lines. [Heckel's algorithm](/heckel-diff/) also starts from unique lines, but it does not recurse, and it reports moves.

## In plain words

Two versions of a file usually start the same and end the same, so match those lines first.

In the middle part, look for lines that occur only once in each version. Such a line, for example the name of a function, is a safe anchor. The anchors may disagree on the order, so keep the largest set of them that is in the same order in both versions.

Between two anchors there is a smaller middle part. Do the same steps there. A line can be rare in a small part even if it is common in the whole file. When a part has no anchor at all, either stop or use an ordinary diff for that part.

## The problem

The input is an old file $A$ and a new file $B$, as sequences of lines with an equality test and a hash of a line. The output is a matching, a set of pairs $(i, j)$ with $A[i] = B[j]$ that increase in both files, and the edit script that keeps the matched lines, deletes the other old lines and inserts the other new lines. The goal is a diff that a person can read, in which the kept lines are the lines that really stayed. The length of the matching is not the goal: a longest one is a [longest common subsequence](/longest-common-subsequence/), and it can keep a closing brace of one function and give it to another.

## The algorithm

The pseudocode uses half-open ranges: MATCH works on the old lines $A[alo \ldots ahi - 1]$ and the new lines $B[blo \ldots bhi - 1]$. The fallback is a choice. Without it, a range with no anchor stays unmatched, as in Cohen's steps; with it, the range is matched by an ordinary diff, as Git does. The implementation of this page uses the dynamic program for a longest common subsequence as the fallback.

```pseudo id=main
PATIENCE(A, B)
L1  M ← an empty list; MATCH(1, |A| + 1, 1, |B| + 1)
    MATCH(alo, ahi, blo, bhi)
L2      while alo < ahi, blo < bhi and A[alo] = B[blo] do append (alo, blo) to M; alo ← alo + 1; blo ← blo + 1   ▷ step 1
L3      T ← empty; while alo < ahi, blo < bhi and A[ahi - 1] = B[bhi - 1] do ahi ← ahi - 1; bhi ← bhi - 1; put (ahi, bhi) at the front of T   ▷ step 2
L4      S ← a longest subsequence, increasing in j, of the pairs (i, j) in order of i whose line occurs once in A[alo .. ahi - 1] and once in B[blo .. bhi - 1]   ▷ step 3
L5      if S is empty then append the matching of FALLBACK(alo, ahi, blo, bhi) to M, which may be no pairs
L6      else for each (i, j) in S in order do MATCH(alo, i, blo, j); append (i, j) to M; alo ← i + 1; blo ← j + 1
            MATCH(alo, ahi, blo, bhi)   ▷ step 4: the gap after the last anchor
L7      append T to M
L8  return the script that keeps the pairs of M
```

Line L4 counts the lines of each side of the range in a [hash table](/hash-table/) and keeps the lines with count 1 on both sides. Sorted by their old line number, these pairs form a sequence of new line numbers, and a longest increasing subsequence of it is the largest set of anchors that do not cross. Patience sorting finds it with one binary search per pair. Line L6 then calls MATCH on each gap: the gap before the first anchor, the gaps between two anchors and, after the loop, the gap after the last anchor. In a gap, line L4 counts again, so a line that occurs twice in the files but once in the gap becomes an anchor there.

## Example

A function is inserted between two others.

| line | old $A$ | new $B$ |
| --- | --- | --- |
| 1 | void func1() { | void func1() { |
| 2 | x += 1 | x += 1 |
| 3 | } | } |
| 4 | (blank) | (blank) |
| 5 | void func2() { | void functhreehalves() { |
| 6 | x += 2 | x += 1.5 |
| 7 | } | } |
| 8 | | (blank) |
| 9 | | void func2() { |
| 10 | | x += 2 |
| 11 | | } |

Line L2 matches the first four lines. Line L3 matches the last three lines: } with }, x += 2 with x += 2, and void func2() { with void func2() {. The remaining range is empty in $A$ and holds new lines 5 to 8 in $B$, so line L4 finds no pair, and the four lines are inserted. The diff shows the new function as one block:

```
 void func1() {
     x += 1
 }

+void functhreehalves() {
+    x += 1.5
+}
+
 void func2() {
     x += 2
 }
```

A longest common subsequence has 7 lines, and the matching above is one. Another one, just as long, matches the old } and blank line of func1 with new lines 7 and 8, the ones of the new function. Its diff inserts the lines "}", blank, "void functhreehalves() {" and "x += 1.5" after "x += 1", so the new function looks split across the old one. Cohen's post shows that a standard diff can print this second form. A method that only makes the script short has no reason to prefer the first form.

The second example shows the counts in a gap. Take $A = [a, b, U, b, a]$ and $B = [b, a, U, a, b]$. The first lines differ and the last lines differ. In the whole files only $U$ occurs once on each side, so it is the only anchor, and line L6 calls MATCH on the two gaps. In the gap before $U$, both $a$ and $b$ now occur once on each side. Their pairs are $(1, 2)$ and $(2, 1)$, which cross, so line L4 keeps one, the pair $(2, 1)$ that patience sorting returns. The gap after $U$ gives $(5, 4)$ in the same way. The matching has 3 pairs.

## Correctness

The proof file shows two results. First, each call of MATCH appends only pairs of equal lines inside its range, in increasing order, and each recursive call is on a smaller range; so the method stops, $M$ is a matching, and the script turns $A$ into $B$. Second, when no line occurs twice in $A$ and no line occurs twice in $B$, the result is a longest common subsequence: matching equal first lines and equal last lines never loses length, every common line in the inner range is unique on both sides, line L4 takes a longest increasing set of them, and no gap can hold another common pair, since it would make that set longer. With repeated lines the result can be shorter than the optimum, and the script longer than a shortest one.

## Complexity

Count in the [word-RAM](/word-ram/), with $n$ the total number of lines of both files, and a hash table with $O(1)$ expected time per operation.

- **One call.** A range with $s$ lines in total costs $O(s)$ expected time to count, and $O(s \log s)$ to sort the unique pairs and to find the longest increasing subsequence.
- **No repeated lines.** The top call costs $O(n \log n)$. The gap calls find no pairs and do not recurse, and the gaps are disjoint, so the total is $O(n \log n)$ expected.
- **Worst case.** Every call with anchors appends at least one anchor, and a line is an anchor at most once, so there are at most about $2n$ calls, each on at most $n$ lines: $O(n^2 \log n)$ expected. The fallback adds its own cost; the dynamic program of this page costs the product of the sizes of the two sides of each range where it runs, at most $O(n^2)$ in total, since those ranges are disjoint.
- **Files that are almost equal.** Lines L2 and L3 match the common start and end in linear time, so a small change in a large file costs little beyond one pass.
- **Space.** The table, the piles and $M$ need $O(n)$, and the recursion is at most $O(n)$ deep.

## Properties

- **Not minimal.** The matching can be shorter than a longest common subsequence when lines repeat, so the script can have more operations than a shortest one.
- **Anchors on rare lines.** Matches come from lines that are unique in their range, which in source code are often declarations and statements with names, not braces or blank lines.
- **No moves.** The output is an ordinary edit script. Anchors that cross are dropped, not reported as moves.
- **Local counts.** Counting again in each gap finds anchors that are not unique in the whole files.

## Variants and improvements

- **The fallback.** Without a fallback, ranges with no unique line stay as one delete and insert block. Git runs its ordinary Myers diff in such ranges.
- **Histogram diff.** [Histogram diff](/histogram-diff/) extends the idea to lines with few copies, and uses a line with the lowest count in the range as the anchor, so it still works when no line is unique.
- **Heckel's passes.** [Heckel's algorithm](/heckel-diff/) also starts from the unique lines, extends them to equal neighbors, keeps crossing links as moves, and does not recurse.
- **Merges.** A three-way merge such as [diff3](/diff3/) needs two diffs against a base. With a diff that keeps the structure of the code, the conflicts it reports fall at more natural places.

## When to use it

Use it for diffs that people read, especially of source code, where a minimum diff can align braces and blank lines of unrelated functions. Git gives it as the option --patience. Do not use it when the shortest script is required, for example to compute an edit distance; use [Myers' algorithm](/myers-diff/) or the [Hunt-Szymanski algorithm](/hunt-szymanski/) for that.

## Pitfalls

- **No unique lines.** Files made mostly of repeated lines, such as tables of equal rows, have few anchors. Without a fallback, large ranges stay unmatched.
- **Counts per range.** The counts of line L4 must be taken in the current range, not in the whole files, or the recursion finds no new anchors.
- **Crossing anchors.** Keeping all unique pairs gives an invalid script when a block moved. Only an increasing subset can be kept.
- **Steps 1 and 2 matter.** Equal first and last lines that are not unique, such as a closing brace at the end of the file, are matched only by lines L2 and L3. A version without these steps leaves them to the fallback.
- **Recursion depth.** The depth can grow with the number of lines. An implementation in a language with a small call stack should use an explicit stack.

## Implementations

## History

Bram Cohen designed patience diff and described its steps in a blog post in 2010, "Patience Diff Advantages", with the example of a function inserted between two others. The name comes from patience sorting, the card game method that gives a longest increasing subsequence and that Aldous and Diaconis survey. Git provides the method as a diff option and falls back to its ordinary diff in ranges without unique lines. Histogram diff, written for JGit, extends it.

## References

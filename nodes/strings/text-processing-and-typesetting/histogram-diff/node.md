---
tag: BNZ7EN
kind: algorithm
slug: histogram-diff
name: Histogram diff
aliases:
- histogram diff algorithm
area: strings/text-processing-and-typesetting
level: advanced
summary: Count the old lines of a range, keep the run of equal lines whose rarest line has the lowest count, and diff the parts before and after it again. From JGit; also in Git.
model: word-ram
complexity:
  vars: {n: the total number of lines in both files, c: the bound on the count of a line that may start a run (64 in JGit)}
  time: {expected: O(c n^3)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: true, online: false, adaptive: true}
prereqs: [patience-diff, shortest-edit-script, hash-table]
see_also: [heckel-diff, myers-diff, longest-common-subsequence, longest-common-substring, hunt-szymanski, diff3, three-way-merge]
sources:
  - url: https://github.com/eclipse-jgit/jgit/blob/master/org.eclipse.jgit/src/org/eclipse/jgit/diff/HistogramDiff.java
    title: JGit, HistogramDiff.java (Copyright 2010, Google Inc. and others)
    locator: the class comment, which calls the method an extended form of Bram Cohen's patience diff, the default maxChainLength of 64, the fallback algorithm (MyersDiff by default), and diffReplace, which recurses before and after the common region
  - url: https://github.com/eclipse-jgit/jgit/blob/master/org.eclipse.jgit/src/org/eclipse/jgit/diff/HistogramDiffIndex.java
    title: JGit, HistogramDiffIndex.java
    locator: scanA, which counts the lines of the old region, and tryLongestCommonSequence, which grows each match, takes the least count over the region, and keeps a region that is longer or has a lower count
  - url: https://github.com/git/git/commit/8c912eea94a2138e8bc608f7c390eb0b313effb0
    title: Tay Ray Chuan, teach --histogram to diff, Git commit 8c912ee, 2011
    locator: the port of JGit's HistogramDiff to the xdiff library of Git
  - paper: doi:10.1007/s10664-019-09772-z
    title: Yusuf Sulistyo Nugroho, Hideaki Hata and Kenichi Matsumoto, How different are different diff algorithms in Git? Use --histogram for code changes, Empirical Software Engineering 25(1), 2020, 790-823
    locator: the comparison of the Myers and Histogram options of Git on 14 Java projects, and the manual study that favors Histogram for code changes
  - url: https://bramcohen.livejournal.com/73318.html
    title: Bram Cohen, Patience Diff Advantages, blog post, 2010
    locator: patience diff, the method that histogram diff extends
---

Histogram diff compares two files line by line. In a range of the files it counts how often each old line occurs, finds runs of equal lines in both files, and keeps the run whose rarest line has the lowest count, then the longest such run. It then diffs the parts before and after that run in the same way. It extends [patience diff](/patience-diff/): patience diff can anchor only on a line that occurs once on both sides, while histogram diff can also anchor on a line with two or three copies. The method comes from JGit, the Java version of Git, and Git has it as the option --histogram. Like patience diff it does not always give a [shortest edit script](/shortest-edit-script/), as [Myers' algorithm](/myers-diff/) does, and like [Heckel's algorithm](/heckel-diff/) it trusts rare lines more than common ones.

## In plain words

Lines that are rare are good anchors. A function name usually occurs once. A closing brace occurs many times and says little about where you are.

So, for the part of the files that you work on, count how often each line occurs in the old version. Then go through the new version. For each line that also occurs in the old version, line up the copies and stretch the match up and down as long as the lines stay equal. Give the stretch the count of its rarest line.

Keep the stretch with the lowest count, and among those the longest one. Then do the same in the part above it and the part below it. If a part has common lines but all of them are very frequent, use an ordinary diff for that part.

## The problem

The input is an old file $A$ and a new file $B$, as sequences of lines with an equality test and a hash of a line. The output is a matching, a set of pairs $(i, j)$ with $A[i] = B[j]$ that increase in both files, and the edit script that keeps the matched lines. As for patience diff, the goal is a diff that a person can read, and the length of the matching is not the goal: a [longest common subsequence](/longest-common-subsequence/) can tie unrelated parts of the files together through braces and blank lines.

## The algorithm

The pseudocode uses half-open ranges $A[alo \ldots ahi - 1]$ and $B[blo \ldots bhi - 1]$. A *run* is a block $A[as \ldots ae - 1] = B[bs \ldots be - 1]$ of equal lines. For a line $x$, $\mathrm{cnt}(x)$ is the number of its copies in the old side of the range, and the count of a run is the least $\mathrm{cnt}$ of its lines. The bound $c$ is the parameter that JGit calls maxChainLength, 64 by default.

```pseudo id=main
HISTOGRAM(A, B)
L1  match the equal first lines and the equal last lines of A and B
L2  MATCH on the range between them
    MATCH(alo, ahi, blo, bhi)
L3      if one side is empty then return; R ← REGION(alo, ahi, blo, bhi)
L12     if R = none then append the matching of FALLBACK(alo, ahi, blo, bhi), and return
L13     if R is empty then return   ▷ no common line: the range is one replace
L14     MATCH on the part before R; append the pairs of R; MATCH on the part after R
L15 return the script that keeps the matched pairs
    REGION(alo, ahi, blo, bhi)
L4      count cnt(x) for each line x of A[alo .. ahi - 1], and list its copies in order
L5      best ← the empty run; cnt ← c + 1; common ← false
L6      for j ← blo while j < bhi, moving to next afterwards:
L7          next ← j + 1; if B[j] occurs in the old side then common ← true
            if B[j] occurs in the old side and cnt(B[j]) ≤ cnt then for each copy A[i] = B[j], skipping copies up to the end of the last run tried:
L8              grow the run (i, i + 1, j, j + 1) backward and forward while the lines stay equal and inside the range; rc ← its count
L9              next ← max(next, be)
L10             if the run is longer than best or rc < cnt then best ← the run; cnt ← rc
L11     if common and cnt > c then return none else return best
```

Line L1 runs once, for the whole files. JGit trims the common start and end before it starts, and the recursion does not trim again. Line L4 is the histogram that gives the method its name. Line L7 skips lines that are more frequent than the best run found so far, so as the scan goes on, only rarer lines are tried. Line L9 moves the scan of $B$ past the run just grown, so the lines inside a run are not tried again as starting points. Line L10 replaces the best run when the new run is longer or its rarest line is rarer; since only lines with $\mathrm{cnt} \le$ cnt are tried, cnt never grows. Line L11 returns none, the signal for the fallback, when there are common lines but every one of them occurs more than $c$ times in the old side. JGit uses [Myers' algorithm](/myers-diff/) as the fallback; the implementation of this page uses the dynamic program for a longest common subsequence.

## Example

Take the old file $A = [\}, \}, x, \}, \}, y]$ and the new file $B = [y, \}, \}, x, w]$, numbered from 1.

| step | what happens |
| --- | --- |
| L1 | $A_1 = \}$ and $B_1 = y$ differ, and $A_6 = y$ and $B_5 = w$ differ, so nothing is trimmed |
| L4 | $\mathrm{cnt}(\}) = 4$, $\mathrm{cnt}(x) = 1$, $\mathrm{cnt}(y) = 1$ |
| $j = 1$, $B_1 = y$ | $y$ is $A_6$. The run cannot grow: $B_1$ is the first line and $A_6$ the last. Run $A_6 = B_1$, count 1. It is the best run, and cnt $= 1$ |
| $j = 2, 3$, a brace | $\mathrm{cnt}(\}) = 4 > 1$, so the braces are not tried |
| $j = 4$, $B_4 = x$ | $x$ is $A_3$. The run grows backward over two braces: $A_1 A_2 A_3 = B_2 B_3 B_4$, with count $\min(4, 4, 1) = 1$. It is longer, so it becomes the best run |
| $j = 5$, $B_5 = w$ | $w$ is not in $A$ |

The part before the run is $A$ empty and $B_1 = y$, and the part after it is $A_4 A_5 A_6$ and $B_5 = w$, which have no common line. So the result keeps the three lines $\}, \}, x$, inserts $y$ at the top, and replaces $\}, \}, y$ with $w$: 5 operations, which is the minimum here. The braces had the highest count but were matched anyway, because they belong to the run of $x$.

The method is not always minimal. For $A = [u, a, a, a, v]$ and $B = [a, a, a, u, v]$, line L1 matches $v$. The scan first grows the run $a, a, a$ with count 3, then the run $u$ with count 1, which wins because it is rarer. The parts beside $u$ are empty on one side, so the script has 6 operations, while $a, a, a, v$ gives 2. And it can lose even when every line is unique, where patience diff is exact: for $A = [1, 2, 3, 4, 5, 6, 7]$ and $B = [6, 7, 1, 3, 5]$, every run has count 1, so the longest run $6, 7$ wins, and the result has 2 pairs instead of the 3 of $1, 3, 5$.

## Correctness

The proof file shows that each quadruple that REGION stores is a run inside the range, that REGION returns the empty run exactly when the two sides have no common line, and that it returns none exactly when the sides have common lines and each of them occurs more than $c$ times in the old side. The last part uses that cnt never grows: a run is tried only from a line with $\mathrm{cnt} \le$ cnt, and its count is at most that. From these facts, by induction on the size of the range, each call of MATCH appends a matching of its range in increasing order, the recursion stops because the parts beside a run are smaller, and the script turns $A$ into $B$. The examples above show that the matching is not always a longest one.

## Complexity

Count in the [word-RAM](/word-ram/), with $n$ the total number of lines of both files, $c$ the bound on counts, and a hash table with $O(1)$ expected time per operation.

- **One range.** Line L4 costs $O(s)$ expected for a range of $s$ lines. Each position of $B$ that line L6 visits tries at most $c + 1$ copies, and each try grows a run in at most $O(s)$ steps, so one call of REGION costs $O(c s^2)$ in the worst case.
- **The recursion.** Each call removes at least one matched pair, ranges at the same depth are disjoint, and the depth is at most $n$, which gives the bound $O(c n^3)$ expected. This bound is loose: line L9 skips the lines of each run that it grows, and in real files the runs are short and the counts small. The JGit source states that the method typically runs faster than its Myers diff.
- **Common start and end.** Line L1 is linear, so a small change in a large file is cheap.
- **The fallback.** The fallback runs on disjoint ranges; with the dynamic program of this page it costs $O(n^2)$ in total, and with Myers' method it costs $O(n D)$ for $D$ the size of the edit script in those ranges.
- **Space.** The histogram, the lists of copies and the matching need $O(n)$, and the recursion is at most $O(n)$ deep.

## Properties

- **Not minimal.** The examples above give scripts longer than a shortest one, also for files whose lines are all unique.
- **Rare lines first.** The anchor of a range is a run whose rarest line has the lowest count, so names and statements win over braces and blank lines.
- **Counts on one side.** Only the old side is counted. A line that occurs once in $A$ and many times in $B$ still has count 1.
- **Like patience diff on unique lines.** When a range has a line that occurs once in it, the best run has count 1, as in patience diff. The two methods then still differ in which unique lines they keep: patience diff keeps a longest increasing set of them, histogram diff keeps one run and recurses.
- **Adaptive.** Equal start and end lines are matched in one pass, and a range with no common line is one replace, without further work.

## Variants and improvements

- **The bound $c$.** A larger $c$ lets more frequent lines start runs, and sends fewer ranges to the fallback, at a higher cost per range. JGit also stops with the fallback when a bucket of its hash table gets longer than $c$, so that a bad hash does not make the scan slow.
- **The fallback.** JGit lets the caller set the fallback algorithm; without one, a range that needs it is reported as one replace.
- **Patience diff.** [Patience diff](/patience-diff/) keeps all the unique lines that do not cross, by a longest increasing subsequence, instead of one run.
- **Heckel's passes.** [Heckel's algorithm](/heckel-diff/) grows matches of unique lines to their neighbors in the same way as line L8, but does not recurse and reports crossing matches as moves.

## When to use it

Use it for diffs of source code that people read and that tools use to find the lines a commit changed. In Git it is the option --histogram, or the setting diff.algorithm = histogram. Nugroho, Hata and Matsumoto compared it with the default Myers diff of Git on 14 Java projects: the two options gave different numbers of changed lines in 1.7 to 8.2 percent of the commits, and in a manual study the histogram diffs described the code changes better more often, so they recommend it for code. Do not use it when a shortest script is needed, for example to compute an edit distance.

## Pitfalls

- **Counting both sides.** The counts are of the old side of the current range only, and they must be counted again in each range of the recursion.
- **The order of the scan.** The result depends on the order of the scan of $B$ and on the rule of line L10: a run replaces the best one only if it is strictly longer or strictly rarer, so among equal runs the first one found wins.
- **Frequent lines.** A file made of lines that all occur more than $c$ times goes entirely to the fallback, and the method is then as slow as the fallback.
- **Trimming in the recursion.** JGit trims the common start and end only once, at the start. A version that trims again in each range is a different method, and its results can differ from those of JGit.
- **Recursion depth.** The depth can grow with the number of lines; an implementation in a language with a small call stack should use an explicit stack.

## Implementations

## History

Histogram diff was written for JGit, and its source file carries the copyright line of Google Inc. and others from 2010. Its class comment calls it an extended form of Bram Cohen's patience diff. Tay Ray Chuan ported it to the xdiff library of Git in 2011, and it appeared in Git 1.7.7 as the option --histogram. In 2020, Nugroho, Hata and Matsumoto measured how the choice of diff algorithm in Git changes the results of studies of code history, and recommended the histogram option for code changes.

## References

---
title: Heckel's links pair equal lines, and the script built from them turns the old file into the new file
proves: [correctness]
status: full
---

We use the pseudocode of the page. The old file is $O[1 \ldots m]$ and the new file is $N[1 \ldots n]$. Line L4 adds the begin line at index 0 and the end line at index $m + 1$ of $O$ and $n + 1$ of $N$. We say that $NA[i]$ is *linked* when it holds a line number, and *free* when it holds a symbol table entry. The same words apply to $OA[j]$.

**Invariant (I).** After line L4 and after each later step of lines L5 to L7, for all $0 \le i \le n + 1$ and $0 \le j \le m + 1$:

1. $NA[i] = j$ if and only if $OA[j] = i$;
2. if $NA[i] = j$ with $1 \le i \le n$, then $1 \le j \le m$ and $N[i] = O[j]$;
3. a free $NA[i]$ holds the entry of the text $N[i]$, and a free $OA[j]$ holds the entry of the text $O[j]$.

*Proof.* After lines L2 and L3, every $NA[i]$ and $OA[j]$ with $1 \le i \le n$, $1 \le j \le m$ is free and holds the entry of its own text, because the table has one entry for each distinct text. Line L4 links the begin lines to each other and the end lines to each other, so part 1 holds. Parts 2 and 3 hold, since no real line is linked.

Line L5 links $NA[i]$ to $OA[j]$ only when $NA[i]$ is free with an entry $e$ such that $e.NC = e.OC = 1$, and $j = e.OLNO$. Since $e.OC = 1$, line L3 met the text of $e$ at exactly one old line, and $e.OLNO$ is that line, so $O[j] = N[i]$. Since $e.NC = 1$, no other new line holds $e$, so no other step of line L5 writes $OA[j]$. Lines L2 to L4 link no real line, so $OA[j]$ was free before this step. So the step links two free cells with the same text, and keeps (I).

Line L6 links $NA[i + 1]$ to $OA[j + 1]$ only when $NA[i] = j$ and both $NA[i + 1]$ and $OA[j + 1]$ are free and hold the same entry. By part 3, $N[i + 1] = O[j + 1]$. A free cell is never one of the begin or end lines, so $1 \le i + 1 \le n$ and $1 \le j + 1 \le m$. Both cells were free, so no other link uses them, and part 1 still holds. Line L7 is the same with $i - 1$ and $j - 1$. $\square$

**Theorem 1 (the links).** The list $L$ of line L8 is a set of pairs $(j, i)$ with $O[j] = N[i]$, such that each old line and each new line occurs in at most one pair. Each line whose text occurs exactly once in $O$ and exactly once in $N$ is in a pair, with its copy in the other file.

*Proof.* The first sentence is (I), parts 1 and 2. For the second, let the text $t$ occur once in each file, at $O[j]$ and $N[i]$. Its entry has $OC = NC = 1$ and $OLNO = j$. Before line L5 reaches $i$, $NA[i]$ is still free: lines L2 to L4 link no real line, and an earlier step of line L5 links only cells that hold another entry. So line L5 links $i$ and $j$, and later steps never unlink a cell. $\square$

**Theorem 2 (the script).** The pairs $K$ of line L9 are increasing in both coordinates, and the script of line L10 turns $O$ into $N$.

*Proof.* The pairs of $L$ come in increasing order of the new line $i$, and their old lines $j$ are distinct by Theorem 1. Line L9 takes a longest strictly increasing subsequence of the old lines, so the chosen pairs increase in both coordinates. Each chosen pair has equal lines by Theorem 1. So $K$ is a common subsequence of $O$ and $N$, given by its positions. The helper matching_to_script keeps exactly the pairs of $K$, deletes every other old line and inserts every other new line, in order. Applying the result to $O$ gives the kept lines of $K$ with the new lines between them in their order, which is $N$. $\square$

**Theorem 3 (files without repeated lines).** If no text occurs twice in $O$ and no text occurs twice in $N$, the script of line L10 is a [shortest edit script](/shortest-edit-script/).

*Proof.* Each common text occurs once in each file, so Theorem 1 links all common lines in line L5. No other pair of equal lines exists, so $L$ is the set of all pairs of equal lines. A common subsequence of $O$ and $N$ uses only pairs of equal lines, increasing in both coordinates, so it is an increasing subsequence of $L$. Line L9 takes a longest one, so $|K|$ is the length of a [longest common subsequence](/longest-common-subsequence/), and the script has the least number of operations, $m + n - 2|K|$. $\square$

**The script is not minimal in general.** Take $O = [u, a, a, a, v]$ and $N = [a, a, a, u, v]$. Line L5 links $u$ and $v$. Line L6 at $i = 0$ compares $NA[1]$, the entry of $a$, with $OA[1]$, which is linked to $u$, so it does nothing; at $i = 4$ and $i = 5$ the next new cell is linked. Line L7 at $i = 4$ compares $NA[3]$, the entry of $a$, with $OA[0]$, the begin line, which is linked. So no $a$ is linked, $K = \{(1, 4), (5, 5)\}$, and the script has $10 - 4 = 6$ operations. The common subsequence $a, a, a, v$ gives a script of 2 operations.

**Termination and cost.** Each of the lines L2, L3, L5, L6 and L7 is one loop over at most $n + 2$ or $m + 2$ cells, with a constant number of table operations and cell reads per step. Line L9 runs a patience-pile longest increasing subsequence on $r = |L|$ pairs, with one binary search per pair. Line L10 is one pass over both files.

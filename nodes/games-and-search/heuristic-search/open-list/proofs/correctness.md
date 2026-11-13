---
title: The open list returns the live entry of least f, ties toward larger g, and uses linear space
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The heap $H$ holds entries $(f, -g, t, n)$, compared as tuples, and the table $\mathit{best}$ maps a state $n$ to the triple $(g, f, t)$ of its live entry. The stamps $t$ come from a counter, so no two entries have the same stamp. An entry $(f, -g, t, n)$ of $H$ is *live* if $\mathit{best}[n] = (g, f, t)$, and *stale* otherwise. The abstract content of OPEN is the set of pairs $n \mapsto (g, f)$ in $\mathit{best}$, and the order on it is by $f$, then by larger $g$, then by smaller stamp, which is the order of the tuples $(f, -g, t)$.

The data structure is correct when PUSH, REMOVE and CONTAINS change and read this content as their names say, and POP-MIN removes and returns the least element of the content, or reports that it is empty.

**Invariant.** Between operations:

- **(H)** $H$ is a binary min-heap of tuples.
- **(L)** For each $n$ in $\mathit{best}$, $H$ holds the live entry of $n$.
- **(S)** $|H| \le 2\,|\mathit{best}| + s$, where $s$ is the slack constant.

At the start both are empty, so the invariant holds.

**Lemma 1 (PUSH).** PUSH keeps the invariant. If $n$ is in OPEN with $g' \le g$, it changes nothing. Otherwise the content afterwards maps $n$ to $(g, f)$, and the other states keep their pairs.

*Proof.* Line L1 returns in the first case. Otherwise line L2 gives $n$ a new stamp $t$ and line L3 adds $(f, -g, t, n)$ to $H$, which keeps (H). The new entry is the live entry of $n$, so (L) holds for $n$. The old entry of $n$, if there was one, has another stamp and is now stale. Entries of other states do not change. Lines L12 and L13, if they run, replace $H$ by a heap of exactly the live entries, which keeps (H) and (L) and gives $|H| = |\mathit{best}|$. If they do not run, $|H| \le 2|\mathit{best}| + s$ by the test of line L12. So (S) holds. $\square$

**Lemma 2 (REMOVE and CONTAINS).** REMOVE deletes $n$ from the content and keeps the invariant. CONTAINS reports whether $n$ is in the content.

*Proof.* Line L11 deletes $n$ from $\mathit{best}$, so its entry in $H$ becomes stale. (H) and (L) hold for the other states, and lines L12 and L13 restore (S) as in Lemma 1. Line L10 reads $\mathit{best}$, which is the content. $\square$

**Lemma 3 (POP-MIN).** If the content is not empty, POP-MIN removes and returns its least element $(n, g, f)$ in the order of $(f, -g, t)$, and keeps the invariant. If it is empty, POP-MIN returns *empty* and leaves $H$ empty.

*Proof.* Each pass of the loop of lines L5 to L8 removes the least entry of $H$, which keeps (H). A stale entry is not in the content, so removing it changes nothing. Let $e^\ast$ be the live entry of least tuple, which exists by (L) when the content is not empty. Every entry removed before $e^\ast$ is smaller than $e^\ast$, so it is stale, since $e^\ast$ is the least live one. So the first live entry that line L7 sees is $e^\ast$, and line L8 deletes its state from $\mathit{best}$ and returns it. (L) still holds for the other states. Lines L12 and L13 restore (S) as before.

If the content is empty, all entries are stale, the loop removes all of them, and line L9 returns *empty*. The loop runs at most $|H|$ times, so the operation stops. $\square$

**Theorem 4 (cost).** Let $k$ be the number of states in OPEN. Each operation takes $O(\log(k + s) + 1)$ amortized time, and the space is $O(k + s)$ entries at all times.

*Proof.* The space bound is (S), and by (S) each heap operation costs $O(\log |H|) = O(\log(k + s))$, where we take $k$ as the largest size of OPEN during the run. We use a charging argument. An entry becomes stale at most once, in PUSH (the old entry of $n$) or in REMOVE. After that it leaves $H$ exactly once, either at line L6 as a skipped entry or at line L13 when the heap is rebuilt without it. At the moment it becomes stale we charge it $O(\log(k + s))$ for its later removal at line L6 and $O(1)$ for its share of a later rebuild.

A rebuild runs only when $|H| > 2|\mathit{best}| + s$, that is when the stale entries number more than $|\mathit{best}| + s$, so more than half of $H$ is stale. The heapify of line L13 takes $O(|H|)$ time, which is at most a constant times the number of stale entries that it drops, and each of them paid $O(1)$ for this. The skipped entries of POP-MIN paid for themselves. What remains for each operation is a constant number of heap operations and table operations, $O(\log(k + s))$, plus the charge it puts on at most one new stale entry, also $O(\log(k + s))$. CONTAINS does no heap operation and costs $O(1)$. $\blacksquare$

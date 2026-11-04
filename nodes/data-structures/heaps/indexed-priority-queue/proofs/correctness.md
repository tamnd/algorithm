---
title: The indexed priority queue keeps its heap and its position map
proves: [correctness, termination]
status: full
---

Write $p(j) = \lfloor (j - 1)/2 \rfloor$ and $K(j) = \mathit{key}[\mathit{pq}[j]]$ for a position $0 \le j < n$. Let $S$ be the set of items in the queue.

**Invariants.** Between operations:

> **(H)** $K(p(j)) \le K(j)$ for each $1 \le j < n$;
>
> **(P)** $\mathit{pq}[0 \ldots n - 1]$ lists the items of $S$, each once; $\mathit{qp}[\mathit{pq}[j]] = j$ for each $0 \le j < n$; and $\mathit{qp}[i] = -1$ for each $i \notin S$.

Both hold for the empty queue, where $n = 0$ and $\mathit{qp}$ is all $-1$.

**Lemma 1 (EXCH).** If $\mathit{qp}[\mathit{pq}[j]] = j$ for each $j < n$ before EXCH$(a, b)$ with $a, b < n$, then the same holds after it, and the set of items in $\mathit{pq}[0 \ldots n - 1]$ is unchanged.

*Proof.* Line L13 swaps two cells of $\mathit{pq}$, so the set is the same. The positions $j \notin \{a, b\}$ keep their item, and that item's entry in $\mathit{qp}$ is unchanged, because the two entries written belong to the items now at $a$ and $b$, which are distinct from the item at $j$. Those two entries are set to $a$ and $b$. $\square$

So (P) is kept by any sequence of EXCH calls. SWIM and SINK change $\mathit{pq}$ only through EXCH, and they change no key.

**Lemma 2 (SWIM).** Suppose (P) holds, and (H) holds for each $j \ne t$, and if $t \ge 1$ then $K(p(t)) \le K(c)$ for each child $c$ of $t$. Then SWIM$(t)$ stops after at most $\lfloor \lg(t + 1) \rfloor$ iterations, and after it (H) and (P) hold.

**Lemma 3 (SINK).** Suppose (P) holds, and (H) holds for each $j$ that is not a child of $t$, and if $t \ge 1$ then $K(p(t)) \le K(c)$ for each child $c$ of $t$. Then SINK$(t)$ stops after at most $\lfloor \lg n \rfloor$ iterations, and after it (H) and (P) hold.

*Proofs.* These are the sift-up and sift-down lemmas of a binary heap applied to the array $K(0 \ldots n - 1)$: by Lemma 1, EXCH$(a, b)$ swaps $K(a)$ and $K(b)$ and keeps (P). The invariant of SWIM is that each edge $(p(j), j)$ with $j \ne t$ holds and that $K(p(t))$, if it exists, is at most each child key of $t$; a swap at a failing edge moves the possible failure from $t$ to $p(t)$. The invariant of SINK is that each edge except those from $t$ to its children holds, and that $K(p(t))$, if it exists, is at most each child key of $t$; a swap with the smaller child $c$ moves the possible failure to the edges out of $c$. Each iteration moves $t$ one level, so the bounds on the iterations follow. The details are those of the proofs on the pages [heap increase-key](/heap-increase-key/) and [heap extract-max](/heap-extract-max/), with the order reversed. $\square$

**INSERT$(i, k)$** with $i \notin S$. Line L2 appends $i$ at position $n$ and sets $\mathit{qp}[i] = n$, so (P) holds for $S \cup \{i\}$. The new cell is a leaf, so (H) holds except at the edge into it, and the new cell has no children; Lemma 2 applies.

**DECREASE-KEY$(i, k)$** with $k \le \mathit{key}[i]$ and $t = \mathit{qp}[i]$. Lowering $K(t)$ keeps the edges from $t$ to its children. The edge into $t$ may fail, and $K(p(t))$ is at most the old $K(t)$ and so at most each child key. Lemma 2 applies. CHANGE-KEY with a larger key is the mirror case: the edge into $t$ still holds, and only the edges out of $t$ can fail. The precondition of Lemma 3 asks that $K(p(t))$ is at most each child key of $t$, which holds since $K(p(t))$ is at most the old $K(t)$, which was at most each child key. Lemma 3 applies.

**DELETE$(i)$** with $j = \mathit{qp}[i]$. Line L10 swaps the cells $j$ and $n - 1$ by EXCH and drops the last cell, which now holds $i$; line L12 sets $\mathit{qp}[i] = -1$. So (P) holds for $S \setminus \{i\}$. If $j = n - 1$, the dropped cell was a leaf, and (H) holds. Else the cell $j$ holds the old last item $y$, and only the edges at $j$ can fail. If $K(j) < K(p(j))$, the children of $j$ were at least the old key at $j$, which was at least $K(p(j)) > K(j)$, so the edges out of $j$ hold, and Lemma 2 applies to SWIM$(j)$; the item then moves up, and the later SINK finds a cell whose children are not smaller, by (H), and stops at once. Else the edge into $j$ holds, and $K(p(j))$ is at most the old key at $j$, which was at most each child key, so SWIM$(j)$ does nothing and Lemma 3 applies to SINK$(j)$.

**EXTRACT-MIN.** If $n \ge 1$, (H) and transitivity along the path to the root give $K(0) \le K(j)$ for each $j$, so $i = \mathit{pq}[0]$ has the smallest key. Lines L5 and L6 are DELETE$(i)$ with $j = 0$, where the root has no parent, so only SINK is needed, by the same case analysis. Line L7 returns $i$ and its key.

**Theorem.** Each operation stops in $O(\log n)$ time, keeps (H) and (P), and does what its name says on the set $S$ and the keys; EXTRACT-MIN returns an item of smallest key, and CONTAINS$(i)$, which tests $\mathit{qp}[i] \ne -1$, is correct by (P).

*Proof.* This collects the cases above, with Lemmas 2 and 3 for the time. $\blacksquare$

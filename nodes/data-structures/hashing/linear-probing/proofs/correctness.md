---
title: Linear probing with backward-shift deletion is a correct dictionary
proves: [correctness, termination]
status: full
---

All indices are taken modulo $m$. For slots $a$ and $b$, the cyclic path $[a, b]$ is the list $a, a+1, \ldots, b$, and $(a, b]$ is the same list without $a$. A slot $s$ is in $(a, b]$ exactly when $0 < (s - a) \bmod m \le (b - a) \bmod m$. A table is *valid* when:

> **(V1)** the stored keys are distinct;
> **(V2)** at least one slot is EMPTY;
> **(P)** for each key $x$ at slot $p$, every slot of the path $[h(x), p]$ other than $p$ is full.

The empty table is valid. We show that each operation, run on a valid table, ends, gives the right result, and leaves a valid table that stores the right set.

**Lemma 1 (SEARCH).** On a valid table, SEARCH$(T, k)$ ends after at most $m$ probes. It returns the slot of $k$ if $k$ is stored, and NIL otherwise.

*Proof.* The loop of line L8 visits $h(k), h(k)+1, \ldots$ and stops at the first EMPTY slot or at $k$. By (V2) an EMPTY slot exists, so the loop ends within $m$ probes. It returns $j$ only when $T[j] = k$ (line L9), and by (V1) that slot is the only one that holds $k$. If $k$ is stored at $p$, then by (P) the slots of $[h(k), p]$ before $p$ are full and do not hold $k$, so the loop reaches $p$ and returns it. If $k$ is not stored, line L9 never succeeds, and the loop ends at an EMPTY slot with NIL. $\square$

**Lemma 2 (INSERT).** On a valid table with $n + 1 < m$ when $k$ is new, INSERT$(T, k)$ ends. If $k$ is stored, it changes nothing in the key layout and returns the slot of $k$. Otherwise it stores $k$, and the table stays valid.

*Proof.* Lines L1 to L4 are the loop of SEARCH, so by Lemma 1 they end, and they return at line L3 exactly when $k$ is stored. Otherwise the loop stops at the first EMPTY slot $e$ of the path from $h(k)$, and every slot of $[h(k), e]$ before $e$ is full. Line L5 puts $k$ at $e$. Then (V1) holds because $k$ was absent. (V2) holds because the table now has $n + 1 < m$ keys. (P) holds for $k$ by the choice of $e$. For another key $x$ at $p$, the slots of $[h(x), p]$ before $p$ were full and are still full, because line L5 only fills a slot. $\square$

**Lemma 3 (DELETE).** On a valid table, DELETE$(T, k)$ ends. If $k$ is not stored, nothing changes. Otherwise the result is a valid table that stores the old keys without $k$.

*Proof.* By Lemma 1, line L12 finds $k$ at slot $i_0$, or returns NIL and line L13 ends the call. Assume $k$ is at $i_0$. Before line L14 the table had at least one EMPTY slot by (V2), and $i_0$ was full, so the first EMPTY slot $e$ after $i_0$ exists, with $e \ne i_0$. Call the slots of $(i_0, e)$, which are all full at the start, the *run*. We write $T_0$ for the table before line L14.

*Keys outside the run are not affected.* Let $x$ be a key of $T_0$ at a slot $p$ that is neither $i_0$ nor in the run. The path $[h(x), p]$ of $x$ has only full slots of $T_0$ before $p$, so it does not contain $e$. A cyclic path that does not contain $e$ and ends at $p$, which is outside $[i_0, e]$, cannot contain a slot of $[i_0, e)$: to leave this range going forward it must pass $e$. So the path of $x$ avoids $i_0$ and the run. The loop below changes only slots of $\{i_0\} \cup$ run, and $p$ is not among them, so $x$ keeps (P).

*The loop invariant.* At each test of line L18, with the current values of $i$ and $j$:

> **(D1)** $j$ is in $[i_0, e]$, and $i$ is in $[i_0, j)$, so $i$ comes before $j$ on the path from $i_0$.
> **(D2)** Of the slots of $[i_0, e)$, exactly $i$ is EMPTY; the others are full.
> **(D3)** Each slot of $(j, e)$ holds the same key as in $T_0$.
> **(D4)** Each key at a slot of $[i_0, j)$ satisfies (P) in the current table.
> **(D5)** The keys of the current table are the keys of $T_0$ without $k$.

The first time, line L17 has set $j = i_0 + 1$ and $i = i_0$. Then (D1) holds, (D2) holds because line L14 emptied $i_0$ and the run is full, (D3) holds because only $i_0$ changed, (D4) holds because the only slot of $[i_0, i_0 + 1)$ is the EMPTY slot $i_0$, and (D5) holds by line L14.

*Step.* Assume (D1) to (D5) at the test. If $T[j] = $ EMPTY, line L18 returns; we treat this case at the end. Otherwise $j$ is in the run by (D2) and (D1), so by (D3) it holds a key $x$ of $T_0$, with home $r = h(x)$ (line L19). In $T_0$ the path $[r, j]$ had only full slots before $j$, so it does not contain $e$.

- *Case 1: $r$ is in $(i, j]$.* Then the path $[r, j]$ lies in $(i, j]$, so it avoids the hole $i$. Its slots other than $j$ lie in $[i_0, e)$ (the path avoids $e$ and ends at $j \in [i_0, e)$), so by (D2) they are full now. Hence $x$ satisfies (P), and line L20 leaves it. Now (D4) holds for $[i_0, j]$. After line L17 increases $j$ by one, (D1) to (D5) hold at the next test.
- *Case 2: $r$ is not in $(i, j]$.* The path $[r, j]$ contains $i$: it ends at $j$, it does not start in $(i, j]$, and $i$ is the slot just before $(i, j]$. Line L21 moves $x$ to $i$. The path $[r, i]$ is the part of $[r, j]$ up to $i$, so its slots before $i$ were full in $T_0$ and differ from $i$. They are full now: those in $[i_0, e)$ by (D2), and the others because the loop changes no slot outside $[i_0, e)$. So $x$ satisfies (P) at $i$. Slot $j$ becomes the only EMPTY slot of $[i_0, e)$, so (D2) holds with $i \leftarrow j$. The other keys at slots of $[i_0, j)$ keep (P): the path of such a key at $q$ ends at $q$, which comes before $j$ on the path from $i_0$, and its start is not in $(q, e)$, else the path would pass $e$, which is impossible as above. So the path does not contain $j$, and emptying $j$ does not break it. Thus (D4) holds for $[i_0, j]$ with the new hole at $j$. (D3) and (D5) hold, since only $x$ moved. After line L17, all five facts hold at the next test.

*Termination.* Each pass of the loop increases $j$ by exactly one along the path from $i_0$, and by (D1) $j$ never passes $e$. Slot $e$ is EMPTY when it is reached, because by (D3) and the definition of $e$ the loop changes no slot outside $[i_0, e)$. So the loop ends after at most $(e - i_0) \bmod m \le m - 1$ passes.

*End.* When line L18 returns, $j = e$. By (D4) every key in $[i_0, e)$ satisfies (P), and by the first part every key outside $[i_0, e]$ does too. Slot $e$ is EMPTY. So (P) holds for the whole table. (V1) holds by (D5), and (V2) holds because the hole $i$ is EMPTY. By (D5) the table stores the old keys without $k$. $\square$

**Theorem.** Starting from the empty table, every sequence of INSERT (each new key with $n + 1 < m$), SEARCH and DELETE operations ends, each SEARCH returns the slot of its key exactly when the key is in the current set, and the table stays valid.

*Proof.* By induction on the number of operations. The empty table is valid and stores the empty set. If the table is valid and stores the current set before an operation, Lemmas 1, 2 and 3 show that the operation ends, gives the right answer, and leaves a valid table that stores the new set. $\blacksquare$

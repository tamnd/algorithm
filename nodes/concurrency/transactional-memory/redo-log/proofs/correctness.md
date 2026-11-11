---
title: The redo log returns the last write and writes back the right state
proves: [correctness]
status: full
---

We prove that the redo log of the page (lines L1 to L6) implements its abstract type: a lookup returns the last value that the transaction wrote to the word, or MISS if it wrote none, and write-back leaves memory as if each write of the transaction had been applied to it in order. We also prove that the filter has no false negatives.

**Setting.** The log is private to one transaction, so its operations run one at a time. Let $W = (a_1, v_1), \dots, (a_t, v_t)$ be the writes of the transaction so far, in order. Let $A$ be the set of words in $W$, and for $a \in A$ let last$(a)$ be the value of the last write to $a$ in $W$. The state of the log is the list of entries $E$, the map index, and the filter bits $F$.

**Invariant.** After the writes $W$:

1. $E$ has exactly one entry for each $a \in A$ and no other entries, in the order of the first write to each word;
2. index$[a] = i$ if and only if $E[i]$ is the entry of $a$, for each $a \in A$, and index has no other keys;
3. the entry of $a$ holds last$(a)$;
4. for each $a \in A$, all the filter bits of $a$ are set in $F$.

*Proof by induction on $t$.* For $t = 0$, after a discard (L6) or at the start, $E$, index and $F$ are empty, and $A$ is empty. Suppose the invariant holds after $t$ writes and the next write is $(a, v)$. If $a \in A$, then by (2) the probe at L1 finds the entry of $a$ and sets its value to $v$; now last$(a) = v$, and nothing else changes, so (1) to (4) still hold. If $a \notin A$, the probe finds nothing, and L2 appends $(a, v)$ at position $|E|$, sets index$[a] = |E|$ and sets the filter bits of $a$. Now $a$ is in $A$ with last$(a) = v$, its first write is the latest one, so the order in (1) holds, and (2), (3), (4) hold for $a$ and still hold for the other words. The same argument holds for the scan variant, where the probe compares $a$ with each entry in turn, because by (1) at most one entry matches. $\square$

**Lookup.** If $a \in A$, all its filter bits are set by (4), so L3 does not return MISS; the probe at L4 finds the entry of $a$ by (2) and returns last$(a)$ by (3). If $a \notin A$, either some filter bit of $a$ is clear and L3 returns MISS, or the probe at L4 finds no entry by (2) and L4 returns MISS. So the filter can only make a lookup faster: it never hides a word that was written (no false negatives), and a false positive costs one extra probe and nothing else.

**Write-back.** Let $M$ be the memory before L5 and $M'$ after it. L5 writes each entry once. By (1) the entries are for distinct words, so the order of the writes does not matter, and $M'(a) = $ last$(a)$ for $a \in A$ and $M'(a) = M(a)$ for $a \notin A$. Applying the writes $W$ to $M$ one by one gives the same memory: the last write to each word decides its value, and words that are not written keep theirs. Write-back writes exactly $|A|$ words, however many times each word was written.

**Discard.** L6 empties the log without a memory step, so an aborted transaction leaves memory unchanged. $\blacksquare$

The proof is about the private log only. That the write-back is atomic with respect to other transactions is the job of the STM: [TL2](/tl2/) holds the write locks of all words in $A$ during L5, and [NOrec](/norec/) holds its global sequence lock.

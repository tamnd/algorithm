---
title: Jones-Kelly checking catches every out-of-bounds access to a live referent object
proves: [correctness, invariant]
status: full
---

**Setting.** The program runs a finite sequence of ALLOC, ADD, LOAD, STORE and FREE from the main block. Every pointer it uses is the result of ALLOC or of ADD on a pointer it holds. For a pointer $p$ that ALLOC returned for allocation $j$, or that ADD derived from such a pointer, we say that $p$ is derived from $j$, and we write $\mathit{off}(p) = p - b_j$ for its intended offset when $p \ne$ ILLEGAL, where $(b_j, n_j)$ is the object of $j$. The allocator returns blocks of $n_j + 1$ bytes that do not overlap any block in use. ILLEGAL is never in a range $[b, b + n]$ of an object.

**Lemma 1 (the table).** After each operation the objects in $T$ are exactly the live allocations, and their closed ranges $[b, b + n]$ are pairwise disjoint. So LOOKUP$(p)$ returns the unique live object whose closed range holds $p$, or none.

*Proof.* Line L2 inserts each allocation when it starts and line L15 deletes it when it is freed, so $T$ holds the live allocations. The range $[b, b + n]$ is the block of $n + 1$ bytes that line L1 took, and the allocator gives disjoint blocks. Line L4 searches for that range. $\square$

**Lemma 2 (derived pointers).** Let $p$ be derived from allocation $j$, and assume that $j$ was live during every ADD in the derivation of $p$. Then $p = $ ILLEGAL or $b_j \le p \le b_j + n_j$. If moreover every intermediate pointer of the derivation had intended offset in $[0, n_j]$, then $p \ne$ ILLEGAL.

*Proof.* By induction on the number of ADD steps. ALLOC returns $b_j$ in line L3. Now let $q = $ ADD$(p, k)$ with $p$ derived from $j$, and $j$ live. If $p = $ ILLEGAL, line L5 reports an error and $q$ does not exist. Otherwise $b_j \le p \le b_j + n_j$ by the hypothesis, so by Lemma 1, line L6 returns $o = (b_j, n_j)$, and line L7 does not apply. Line L8 returns $p + k$ if it lies in $[b_j, b_j + n_j]$, and line L9 returns ILLEGAL otherwise. Either way the claim holds for $q$. For the second part, if $\mathit{off}(p + k) \in [0, n_j]$ then $p + k \in [b_j, b_j + n_j]$, so line L8 returns $p + k$ and not ILLEGAL. $\square$

**Theorem.** Let $p$ be derived from allocation $j$, let $j$ be live at an access of $w \ge 1$ bytes through $p$ (it is then live during the whole derivation, since a freed allocation is never live again).

1. If the access is out of bounds, that is, $p = $ ILLEGAL or $\mathit{off}(p) < 0$ or $\mathit{off}(p) + w > n_j$, then CHECK reports an error.
2. If the access is in bounds and the derivation of $p$ never left $[0, n_j]$, then CHECK passes.

*Proof.* (1) If $p = $ ILLEGAL, line L10 reports an error. Otherwise, by Lemma 2, $b_j \le p \le b_j + n_j$, so $\mathit{off}(p) \ge 0$ and the access is out of bounds only if $p + w > b_j + n_j$. By Lemma 1, line L11 returns $(b_j, n_j)$, and line L13 reports the error.

(2) By Lemma 2, $p \ne$ ILLEGAL and $b_j \le p \le b_j + n_j$, so line L10 passes and line L11 returns $(b_j, n_j)$, which is not none, so line L12 passes. The access is in bounds, so $p + w \le b_j + n_j$, and line L13 passes. $\blacksquare$

**What is not claimed.** If the derivation left $[0, n_j]$ and came back, line L9 made the pointer ILLEGAL and the access is refused although it is in bounds. If $j$ was freed and its block was given to a new allocation, LOOKUP finds the new object and the access can pass. Both cases appear in the example on the page.

**Termination.** Every operation runs a bounded number of lines, each LOOKUP searches a finite table, and the allocator scans a finite list of holes.

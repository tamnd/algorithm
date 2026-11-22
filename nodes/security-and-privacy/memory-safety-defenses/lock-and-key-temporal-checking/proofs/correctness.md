---
title: The lock and key check passes exactly when the allocation is live
proves: [correctness, invariant]
status: full
---

**Setting.** The program runs a finite sequence of the operations of the main block. Every pointer it uses comes from ALLOC, ADD or LOADPTR of a location whose metadata entry was written by STOREPTR, and the program cannot write the key or the lock of a pointer. Allocation $j$ gets the key $k_j$ in line L2 and the lock location $\ell_j$ in line L3. A pointer *belongs to* $j$ if ALLOC returned it for $j$, or ADD derived it from a pointer that belongs to $j$, or LOADPTR loaded it from a location where STOREPTR last stored a pointer that belongs to $j$. A pointer with the null lock and key 0 belongs to no allocation; the null lock holds a value that is not a key.

**Lemma 1 (invariant K).** After each operation:

(a) every pointer that belongs to $j$ has key $k_j$ and lock $\ell_j$, and every entry $\mathit{META}[a]$ written for such a pointer is $(k_j, \ell_j)$;

(b) the keys $k_j$ are distinct and none equals INVALID;

(c) if $j$ is live, $\mathit{LOCKS}[\ell_j] = k_j$, and no other live allocation has lock $\ell_j$;

(d) if $j$ is freed, $\mathit{LOCKS}[\ell_j]$ is INVALID or the key of an allocation made after $j$ was freed.

*Proof.* By induction on the number of operations. At the start there are no allocations. Assume (a) to (d) before an operation.

- ALLOC, allocation $j$. Line L2 takes the counter, which is larger than every earlier key and is not INVALID, so (b) holds. Line L3 takes a lock location that no live allocation holds, and line L4 writes $k_j$ to it, so (c) holds for $j$ and is unchanged for other live allocations. If $\ell_j$ was the lock of a freed allocation $i$, its new value $k_j$ is the key of an allocation made after $i$ was freed, so (d) holds for $i$. Line L5 returns a pointer with $(k_j, \ell_j)$, which gives (a).
- ADD copies the key and the lock in line L6, so (a) holds for the result.
- STOREPTR and LOADPTR copy the key and the lock to and from $\mathit{META}$ in lines L14 and L15, so (a) holds. They write no lock.
- LOAD and STORE write no lock and no key.
- FREE$(p)$ with $p$ belonging to $j$. If line L11 reports an error, nothing changes. Otherwise $\mathit{LOCKS}[\ell_j] = k_j$, and by (b) and (d) a freed $j$ could not pass, so $j$ is live. Line L12 writes INVALID to $\ell_j$, which gives (d) for $j$, and line L13 makes $\ell_j$ free. No other live allocation had lock $\ell_j$ by (c), so (c) still holds for them. $\square$

**Theorem.** For a pointer $p$ that belongs to allocation $j$, CHECK$(p)$ passes exactly when $j$ is live. For a pointer that belongs to no allocation, CHECK fails.

*Proof.* By Lemma 1(a), $p.\mathit{key} = k_j$ and $p.\mathit{lock} = \ell_j$, so line L7 compares $\mathit{LOCKS}[\ell_j]$ with $k_j$. If $j$ is live, they are equal by (c), and the check passes. If $j$ was freed, $\mathit{LOCKS}[\ell_j]$ is INVALID, which is not $k_j$ by (b), or the key $k_i$ of an allocation $i$ made after $j$ was freed, so $i \ne j$ and $k_i \ne k_j$ by (b). Either way line L8 reports a temporal error. A pointer that belongs to no allocation has the null lock, which holds a value that is not a key, while the pointer's key is 0, so line L7 fails. $\blacksquare$

**Corollary.** Every LOAD, STORE, STOREPTR and LOADPTR through a pointer of a freed allocation reports a temporal error, and so does every FREE of such a pointer, which includes every double free. This holds for all copies, in registers and in memory, without any search, and also after the block and the lock location are reused.

**Termination.** Every operation runs a bounded number of lines, apart from the search of the allocator, which scans a finite list of holes.

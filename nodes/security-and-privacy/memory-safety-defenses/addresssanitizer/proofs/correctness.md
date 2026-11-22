---
title: The shadow check reports an aligned access exactly when it touches a byte outside every live object
proves: [correctness, invariant]
status: full
---

**Setting.** Memory is split into granules of 8 bytes. A chunk consists of a redzone of RZ bytes, the object of $n \ge 1$ bytes padded to $\lceil n/8 \rceil \cdot 8$ bytes, and another redzone of RZ bytes, where RZ is a positive multiple of 8. Chunks start on granule boundaries, so every object starts on one. Chunks are live, in the quarantine, or part of the free memory, and the allocator only hands out free memory. At the start the whole shadow holds the redzone value, which is negative. A byte is *live* if it lies in a live object. An access of $w \in \{1, 2, 4, 8\}$ bytes at $a$ has $a \bmod w = 0$, so all its bytes lie in the granule $\lfloor a/8 \rfloor$, at positions $a \mathbin{\&} 7$ to $(a \mathbin{\&} 7) + w - 1$.

**Lemma 1.** In every granule, the live bytes form a prefix: positions $0$ to $j - 1$ for some $j$ in 0 to 8.

*Proof.* Objects do not overlap, each starts on a granule boundary and is followed by a redzone of at least one granule. So a granule meets at most one object, and that object starts at or before the granule's start. Its bytes in the granule are positions $0$ to $j - 1$. $\square$

**Lemma 2 (invariant S).** After each operation, the shadow byte of every granule $g$ is 0 if $j(g) = 8$, is $j(g)$ if $1 \le j(g) \le 7$, and is negative if $j(g) = 0$.

*Proof.* By induction on the number of operations. At the start no byte is live, and every shadow byte is negative. Loads and stores change no shadow byte and no live byte.

- MALLOC$(n)$. The chunk $[c, c + \ell)$ comes from free memory, so before the call it held no live byte, and after the call its only live bytes are $[b, b + n)$. Line L5 makes the granules of both redzones negative; they hold no live byte. Line L6 sets the $\lfloor n/8 \rfloor$ granules that $[b, b + n)$ fills to 0, and if $n \bmod 8 \ne 0$, sets the next granule, which holds the first $n \bmod 8$ bytes of the object and then padding, to $n \bmod 8$. These are all the granules of the chunk. Granules outside it do not change, and neither do their live bytes.
- FREE$(p)$. If line L8 reports an error, nothing changes. Otherwise the object $[p, p + n)$ stops being live, and line L9 makes its $\lceil n/8 \rceil$ granules negative. The redzones stay negative. Lines L10 to L12 move chunks between the quarantine and free memory, which changes no shadow byte and no live byte. $\square$

**Theorem.** CHECK$(a, w)$ reports an error if and only if some byte of $[a, a + w)$ is not live.

*Proof.* Let $g$ be the granule of $a$, $k$ its shadow byte, $j = j(g)$, and $e = (a \mathbin{\&} 7) + w - 1$, the position of the last byte of the access; $0 \le e \le 7$. By Lemma 1 the access touches a byte that is not live exactly when $e \ge j$. By Lemma 2 there are three cases. If $j = 8$, then $k = 0$, line L3 does not report, and $e \le 7 < j$. If $1 \le j \le 7$, then $k = j \ne 0$, and line L3 reports exactly when $e \ge j$. If $j = 0$, then $k < 0 \le e$, so line L3 reports, and the access touches only bytes that are not live. $\blacksquare$

**Corollary.** An access through a pointer derived from an object $o$ is reported if it leaves $o$ and touches a byte that is in a redzone, in free memory or in the quarantine. An access after FREE$(o)$ is reported while the chunk of $o$ is in the quarantine, because none of its bytes is then live. The access is not reported if all its bytes lie in another live object, for example after an overflow longer than the redzone, or after the chunk of $o$ left the quarantine and was reused.

**Termination.** CHECK runs two lines. MALLOC and FREE write a finite number of shadow bytes, and the loop of lines L11 and L12 removes one chunk from the finite quarantine in each round.

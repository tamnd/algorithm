---
title: A cuckoo filter has no false negatives
proves: [correctness, invariant, termination]
status: full
---

Let $\tau(j, \phi) = (\phi, \{j, \mathrm{alt}(j, \phi)\})$ be the token of a fingerprint $\phi$ stored in bucket $j$ or in the victim slot with bucket $j$, and $\tau(x) = (\phi(x), \{i_1(x), i_2(x)\})$ the token of a key $x$. Let $\mathcal{T}$ be the multiset of tokens of the stored entries and $\mathcal{K}$ the multiset of tokens of the copies of keys in $S$. Assume that each DELETE$(x)$ is applied only when $x$ has a copy in $S$.

**Lemma 1 (alt is an involution).** For each $i$ and $\phi$, $\mathrm{alt}(\mathrm{alt}(i, \phi), \phi) = i$, and so $\tau(\mathrm{alt}(j, \phi), \phi) = \tau(j, \phi)$. Also $\tau(i_1(x), \phi(x)) = \tau(i_2(x), \phi(x)) = \tau(x)$.

*Proof.* With $d = g(\phi) \bmod m$, $(i \oplus d) \oplus d = i$. Since $m$ is a power of two and $i, d < m$, the value $i \oplus d$ is also below $m$. The token of $(\mathrm{alt}(j, \phi), \phi)$ has the set $\{\mathrm{alt}(j, \phi), j\}$, the same as for $(j, \phi)$. For a key, $i_2(x) = \mathrm{alt}(i_1(x), \phi(x))$ by definition. $\square$

**Lemma 2 (invariant (T)).** After each operation, $\mathcal{T} = \mathcal{K}$.

*Proof.* By induction. Line L1 makes both empty. A QUERY changes nothing.

*INSERT$(x)$ that returns false at line L2* changes nothing.

*INSERT$(x)$ otherwise.* $\mathcal{K}$ gains $\tau(x)$. Call the fingerprint in hand, with the bucket $i$ that it is meant for, the *carried entry*. At line L3 the carried entry is $(i_1(x), \phi(x))$, whose token is $\tau(x)$ by Lemma 1. We claim that, during the insert, the stored entries together with the carried entry have token multiset $\mathcal{T}_{\text{old}} + \{\tau(x)\}$. Line L4 or L9 stores the carried entry at $i$ or $\mathrm{alt}(i, \phi)$, which keeps its token by Lemma 1. Line L5 changes $i$ to $i$ or $\mathrm{alt}(i, \phi)$, which keeps the token. Line L7 swaps the carried entry with a stored entry $(i, \psi)$ of $T[i]$: the stored part now has $(i, \phi)$ and the carried entry is $(i, \psi)$. The carried entry before the swap had token $\tau(i, \phi)$, which is now stored, and the stored entry $\tau(i, \psi)$ is now carried, so the multiset is unchanged. Line L8 changes $i$ to $\mathrm{alt}(i, \psi)$, which keeps the token. Line L10 stores the carried entry in the victim slot with its bucket. So at the end $\mathcal{T} = \mathcal{T}_{\text{old}} + \{\tau(x)\} = \mathcal{K}$. Line L10 is reached only when the victim slot is empty, because line L2 returned otherwise, so no victim is overwritten.

*DELETE$(x)$.* $\mathcal{K}$ loses one copy of $\tau(x)$. If line L14 removes $\phi(x)$ from $T[i_1(x)]$ or $T[i_2(x)]$, the removed token is $\tau(x)$ by Lemma 1. Line L15 then empties the victim slot and runs lines L4 to L10 on its entry, which keeps the token multiset by the argument for INSERT; the victim slot is empty when line L10 can run, so it is not overwritten. If line L16 clears a victim $(j, \phi(x))$ with $j \in \{i_1(x), i_2(x)\}$, its token is $\tau(x)$ by Lemma 1. In each case $\mathcal{T}$ loses one copy of $\tau(x)$. Line L17 is not reached: $\tau(x) \in \mathcal{K} = \mathcal{T}$, so some entry has token $\tau(x)$. Its fingerprint is $\phi(x)$ and its bucket $j$ satisfies $\{j, \mathrm{alt}(j, \phi(x))\} = \{i_1(x), i_2(x)\}$, so $j \in \{i_1(x), i_2(x)\}$, and line L14 or L16 finds it. $\square$

**Theorem.** After any sequence of operations that respects the precondition of DELETE, QUERY$(x)$ returns true for each $x$ with a copy in $S$, and each operation ends.

*Proof.* If $x$ has a copy in $S$, then $\tau(x) \in \mathcal{K} = \mathcal{T}$ by Lemma 2. As at the end of the proof of Lemma 2, the entry with this token has fingerprint $\phi(x)$ and bucket $i_1(x)$ or $i_2(x)$, in the table or in the victim slot. Line L12 checks exactly these places, so it returns true. Each loop of INSERT runs at most MaxKicks rounds, and DELETE runs at most one such insert, so each operation ends. $\blacksquare$

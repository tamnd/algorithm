---
title: A collision of BLAKE2 gives a collision of its compression function, and the final flag stops length extension
proves: [correctness]
status: full
---

We use the notation of the page. Fix the instance (BLAKE2b or BLAKE2s), the digest length $nn$ and the key length $kk$. For an input $x$ (the data, after the key block if $kk > 0$), let $d_0, \ldots, d_{D-1}$ be its padded blocks, $t_i$ the counter given to the call $i$, and $f_i$ its flag. Write $F(h, d, t, f)$ for the compression function and $h_0$ for the state after line L1.

**Lemma 1 (the call sequence is injective).** If $x \ne x'$ have the same $kk$, then the sequences $(d_i, t_i, f_i)$ and $(d'_i, t'_i, f'_i)$ differ.

*Proof.* The counter of the last call is $t_{D-1} = ll + bb \cdot [kk > 0]$, so it fixes the input length $ll$. If $ll \ne ll'$, the last counters differ. If $ll = ll'$, then $D = D'$ and every $t_i = t'_i$, and the padding of both inputs is the same zero bytes in the same places, so $x \ne x'$ means some block $d_i \ne d'_i$. $\square$

**Theorem 1 (collisions).** If $x \ne x'$ and $\mathrm{BLAKE2}(x) = \mathrm{BLAKE2}(x')$ with the full output of $w$ bytes (64 for BLAKE2b, 32 for BLAKE2s), then one can find, from the two computations, two different tuples $(h, d, t, f) \ne (h', d', t', f')$ with $F(h, d, t, f) = F(h', d', t', f')$.

*Proof.* Let $h_{i+1} = F(h_i, d_i, t_i, f_i)$ and the same for $x'$. The full output is $h_D = h'_{D'}$. Walk back from the last calls. If $(h_{D-1}, d_{D-1}, t_{D-1}, f_{D-1}) \ne (h'_{D'-1}, d'_{D'-1}, t'_{D'-1}, f'_{D'-1})$, this pair is a collision of $F$. If they are equal, then $h_{D-1} = h'_{D'-1}$ and we repeat with the earlier calls. If the last calls do not collide, their counters are equal, so $ll = ll'$ and $D = D'$, because $D$ depends only on $ll$ and $kk$. So the two chains have the same length, and the walk compares calls with the same index. Suppose no step gives a collision. Then all $D$ tuples are equal pairwise, which Lemma 1 rules out. $\square$

With a shorter output, the same argument applies to a collision of the truncated output of the last $F$; this is why the claimed collision level is $2^{4 nn}$ and not more.

**Theorem 2 (no length extension).** Knowing $\mathrm{BLAKE2}_K(m)$ does not let one compute $\mathrm{BLAKE2}_K(m \| s)$ for some $s \ne \varepsilon$ with one call to $F$ from the known digest.

*Proof.* The digest is $F(h, d, t, \text{true})$. Every computation of a longer input passes through a state $F(h, d, t, \text{false})$ at the place where the shorter computation ended. Getting that state from the digest would need the output of $F$ on a different flag, which is a fresh input to $F$. In the ideal model of Luykx, Mennink and Neves this output is independent of the digest. $\square$

**Remarks.** Theorems 1 and 2 are exact reductions: they lose nothing. They say nothing about how hard it is to find a collision of $F$. That is the cryptanalytic conjecture discussed on the page. The tests check that the code computes the function of RFC 7693 on the published traces and the Appendix E self-test.

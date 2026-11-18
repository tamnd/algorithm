---
title: The toroidal clip stack equals a fresh fill after every move, the windows nest for clip sizes of at least four, and a lookup equals a full mipmap sample at the level it uses
proves: [correctness]
status: full
---

We use the notation of the page and the code. Level $l$ has the side $N / 2^l$, and the levels $0, \ldots, k - 1$ with $N / 2^l > C$ form the clip stack; $C$ is even. For a clip center $c$ (integer level 0 texels), $c_l = \lfloor c / 2^l \rfloor$ per coordinate, and the window $W_l(c)$ is the set of texels $t$ with $c_l - C/2 \le t < c_l + C/2$ in each coordinate. The slot of the texel $t$ of a stack level is $\sigma(t) = (t_x \bmod C, t_y \bmod C)$. The texel values of the full mipmap are $m_l(t)$.

## The slots

**Lemma 1.** For each $l$ and $c$, $\sigma$ is one to one on $W_l(c)$.

*Proof.* In each coordinate the texels of the window take $C$ consecutive integer values, and $C$ consecutive integers have $C$ distinct residues mod $C$. So two texels of the window with the same slot have the same $x$ and the same $y$. $\square$

## The update

**Proposition 2.** After RECENTER$(c)$ (lines L1 to L5), for each stack level $l$ the window is $W_l(c)$ and the slot $\sigma(t)$ holds $m_l(t)$ for every texel $t$ of $W_l(c)$ inside the texture. The call writes exactly the texels of $W_l(c)$ that are not in the old window. So the stack equals the stack of a fresh build at $c$.

*Proof.* By induction on the calls. For the first call (from the constructor) there is no old window, so lines L3 and L4 write every texel of $W_l(c)$, each to its own slot by Lemma 1. For a later call, let $W'$ be the old window, with $\sigma(t)$ holding $m_l(t)$ for $t \in W'$ by induction. A texel $t \in W_l(c) \cap W'$ is skipped, and its slot still holds $m_l(t)$: a write in this call goes to the slot of a texel $t' \in W_l(c) \setminus W'$, and $\sigma(t') \ne \sigma(t)$ by Lemma 1 on $W_l(c)$. Each texel of $W_l(c) \setminus W'$ is written by line L4 with its value. Line L5 sets the window. The writes are exactly the texels of $W_l(c) \setminus W'$, and the contents of the slots depend only on $W_l(c)$, as for a fresh build. $\square$

If the center moves by $d \ge 0$ level 0 texels along one axis, $c_l$ moves by at most $\lceil d / 2^l \rceil \le d / 2^l + 1$, and the new texels form a strip of at most that many columns of $C$ texels. So a move writes at most $C (d / 2^l + 1)$ texels at level $l$, and $O(C (d + k))$ over the stack. When $d$ is a multiple of $2^{k-1}$, the rounding does not change the shifts, and the count is exactly $C \sum_{l < k} d / 2^l$; the test checks $C (8 + 4 + 2)$ for $d = 8$ and $k = 3$.

## The windows nest

**Lemma 3.** If $C \ge 4$, then for every $l \ge 0$ and $c$, the window of level $l$ lies inside the window of level $l + 1$ when both are written in level 0 units.

*Proof.* Let $X_l = 2^l c_l$, so that $c - 2^l < X_l \le c$ in each coordinate. In level 0 units the window of level $l$ is the interval $[X_l - 2^{l-1} C, X_l + 2^{l-1} C)$ in each coordinate. On the low side,

$$X_{l+1} - 2^l C \le c - 2^l C \le c - 2^l - 2^{l-1} C < X_l - 2^{l-1} C,$$

where the middle step is $2^{l-1} C \ge 2^l$, that is $C \ge 2$. On the high side,

$$X_l + 2^{l-1} C \le c + 2^{l-1} C \le c - 2^{l+1} + 2^l C < X_{l+1} + 2^l C,$$

where the middle step is $2^{l-1} C \ge 2^{l+1}$, that is $C \ge 4$. $\square$

The pyramid levels $l \ge k$ hold the whole texture. So by Lemma 3 the set of levels whose window holds a given texel position is all levels from some level on. The bilinear taps of a coarser level reach a little farther from the point than those of a finer level, so line L6 defines $l_{\min}$ as the smallest $l$ such that every level from $l$ on holds the taps; it exists because the coarsest level is in the pyramid or, if $N \le C$, there is no stack.

## The lookup

**Proposition 4.** For every point $(u, v)$ in the texture and every $\lambda \ge 0$, LOOKUP$(u, v, \lambda)$ reads only texels of the windows, and it returns the trilinear sample of the full mipmap at the level of detail $\max(\lambda, l_{\min})$.

*Proof.* Line L7 sets $l = \max(\lambda, l_{\min})$. The trilinear sample of line L8 reads the bilinear taps of the levels $\lfloor l \rfloor$ and, if the fraction is not zero, $\lfloor l \rfloor + 1$. Both are at least $l_{\min}$, so by the definition of line L6 their taps are in the windows. The taps are clamped to the texture, so they are texels inside it. By Proposition 2 each slot that is read holds $m_l(t)$, and the pyramid levels are the mipmap levels. So each read value equals the value that the full mipmap gives, and the weights depend only on $(u, v)$ and $l$. $\square$

So when $l_{\min} \le \lambda$, the lookup equals the sample of the full mipmap at $\lambda$. When $l_{\min} > \lambda$, it equals the sample at the coarser level $l_{\min}$, a blurred value of the same image. The tests check Proposition 2 after 60 random moves, Lemma 3 for $C \in \{4, 8, 16, 32\}$ and random centers, and Proposition 4 on 800 random lookups.

---
title: The piece table operations keep the invariant and implement the list operations
proves: [correctness]
status: full
---

We use the invariant (P1) to (P3) of the page. Write $L_k = \ell(p_0) + \cdots + \ell(p_{k-1})$ for the prefix sums of the piece lengths, so $L_0 = 0$ and $L_P = n$ by (P2). By (P2), position $j$ of the text, for $L_k \le j < L_{k+1}$, is character $j - L_k$ of $str(p_k)$.

**Lemma 1 (FIND).** For $0 \le i < n$, FIND returns the unique $(k, off)$ with $L_k \le i < L_{k+1}$ and $off = i - L_k$. For $i = n$ it returns $(P, 0)$.

*Proof.* Before the round for $k$, $off = i - L_k$: this holds for $k = 0$, and line L4 subtracts $\ell(p_k)$, which makes it $i - L_{k+1}$. The round returns at the first $k$ with $i - L_k < \ell(p_k)$, that is $i < L_{k+1}$, and $i \ge L_k$ holds since the earlier rounds did not return. By (P1) the $L_k$ are strictly increasing, so this $k$ is unique. If no round returns, then $i \ge L_P = n$, so $i = n$. $\square$

**CHAR-AT.** By Lemma 1 and the remark above, line L22 returns position $i$ of the text, and $s + off$ is in range by (P1).

**INSERT.** Let $x \ne \varepsilon$ and $a = \lvert T.add \rvert$ before line L7. After line L7, $T.add[a .. a + \lvert x \rvert - 1] = x$, and by (P3) the strings of the old pieces do not change. Let $t$ be the text before the call. We show that the new piece list spells $t[0 .. i-1] \cdot x \cdot t[i ..]$.

- *Line L9.* Here $off = 0$, so $i = L_k$: position $i$ is the boundary after $p_{k-1}$. The piece $p_{k-1} = (add, s, \ell)$ with $s + \ell = a$ names $T.add[s .. a-1]$, and the new piece $(add, s, \ell + \lvert x \rvert)$ names $T.add[s .. a-1] \cdot x$. So the text becomes $str(p_0) \cdots str(p_{k-1}) \cdot x \cdot str(p_k) \cdots$, as required. The new piece is in range since $s + \ell + \lvert x \rvert = \lvert T.add \rvert$.
- *Line L10.* Again $i = L_k$ (including $k = P$, $i = n$), and the new piece $(add, a, \lvert x \rvert)$ names $x$, put between $p_{k-1}$ and $p_k$.
- *Line L11.* Here $0 < off < \ell(p_k)$, and $str(p_k) = buf_b[s .. s + off - 1] \cdot buf_b[s + off .. s + \ell - 1]$. The three new pieces spell $str(p_k)[0 .. off-1] \cdot x \cdot str(p_k)[off ..]$, and position $i$ is offset $off$ in $p_k$ by Lemma 1. All three have positive length because $0 < off < \ell$, and they are in range.

In each case the new pieces have length at least 1 and lie in their buffers, so (P1) holds; the text is as required and $T.n$ grows by $\lvert x \rvert$, so (P2) holds; only appends were made to $T.add$, so (P3) holds.

**DELETE.** Let $0 \le i \le i + d \le n$ and let $t$ be the text before the call. Call the characters at positions $i$ to $i + d - 1$ the *doomed* characters. We prove that the loop keeps this claim: the current piece list spells $t$ with the doomed characters that were already removed taken out; the pieces before index $k$ hold no doomed character; the $d$ doomed characters that remain are the first $d$ characters starting at offset $off$ of $p_k$ and the pieces after it; and (P1) holds.

At the start, the claim holds by Lemma 1, with nothing removed yet. In a round, $t' = \min(d, \ell - off)$ is the number of remaining doomed characters inside $p_k$, at offsets $off$ to $off + t' - 1$.

- Line L16 ($off = 0$, $t' = \ell$): the whole piece is doomed and is removed; the next piece is now at index $k$, and its offset 0 is the next doomed character.
- Line L17 ($off = 0$, $t' < \ell$): the head of length $t'$ is removed and the rest is kept; then $d - t' = 0$, so the loop ends after this round.
- Line L18 ($off > 0$, $off + t' = \ell$): the tail is removed; the next doomed character, if any, is at offset 0 of $p_{k+1}$, which becomes the current piece.
- Line L19 ($off > 0$, $off + t' < \ell$): the middle is removed, and the head and the tail are kept as two pieces of positive length; again $d - t' = 0$.

In each case the pieces made have positive length and lie in their buffers, so (P1) holds, and line L20 updates $d$ and sets $off = 0$ in agreement with the claim. Each round removes $t' \ge 1$ characters, because $off < \ell$ (by Lemma 1 for the first round, and $off = 0 < \ell$ later), so the loop ends, and at the end all $d$ doomed characters are removed. The buffers are untouched, so (P3) holds, and line L12 sets $T.n$ to the new length, so (P2) holds. $\blacksquare$

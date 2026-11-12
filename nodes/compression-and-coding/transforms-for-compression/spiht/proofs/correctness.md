---
title: The SPIHT decoder follows the encoder bit for bit, every prefix of the stream decodes with a bounded error, and the full stream is lossless
proves: [correctness]
status: full
---

**Setup.** The input is an $R \times C$ array of integer wavelet coefficients $c(i, j)$ in the Mallat layout with $L \ge 1$ levels, where $R$ and $C$ are multiples of $2^{L+1}$. Let $R_0 = R / 2^L$ and $C_0 = C / 2^L$ be the sides of the LL band; both are even. Write $S_n(T) = 1$ if $\max_{(i,j) \in T} |c(i,j)| \ge 2^n$ and $0$ otherwise, and $n_{\max} = \lfloor \lg \max |c| \rfloor$. The sets are: $H$, the LL band; $O(i, j)$, the offspring; $D(i, j)$, all descendants; $L(i, j) = D(i, j) \setminus O(i, j)$. The offspring rule is: for $(i, j)$ in the LL band with $(i \bmod 2, j \bmod 2) = (d_i, d_j)$, no offspring if $d_i = d_j = 0$, and otherwise the $2 \times 2$ block with top-left corner $(i - d_i + d_i R_0, \; j - d_j + d_j C_0)$; for $(i, j)$ outside the LL band, the $2 \times 2$ block at $(2i, 2j)$ if $2i < R$ and $2j < C$, and none otherwise. Lines L1 to L11 are those of the pseudocode on the page.

**Lemma 1 (the trees partition the coefficients).** Every coefficient outside $H$ is in $O(i, j)$ for exactly one $(i, j)$, no coefficient of $H$ is in any $O(i, j)$, and the parent relation has no cycles. So the sets $D(h)$ for the roots $h \in H$ with offspring are disjoint, and together with $H$ they cover all $R C$ coefficients.

*Proof.* Let $(r, c) \notin H$. Case 1: $r < 2R_0$ and $c < 2C_0$, a band of the coarsest level. Write $r = d_r R_0 + r'$ and $c = d_c C_0 + c'$ with $0 \le r' < R_0$, $0 \le c' < C_0$ and $(d_r, d_c) \in \{0, 1\}^2 \setminus \{(0, 0)\}$. Since $R_0$ and $C_0$ are even, the LL coefficient $(2\lfloor r'/2 \rfloor + d_r, \; 2\lfloor c'/2 \rfloor + d_c)$ has the block with corner $(2 \lfloor r'/2 \rfloor + d_r R_0, \; 2 \lfloor c'/2 \rfloor + d_c C_0)$, which contains $(r, c)$. The block determines $(d_r, d_c)$ and the two floors, so this parent is the only one in $H$. A parent outside $H$ has $i \ge R_0$ or $j \ge C_0$, so its block has $2i \ge 2R_0$ or $2j \ge 2C_0$ and does not contain $(r, c)$. Case 2: $r \ge 2R_0$ or $c \ge 2C_0$. No LL block reaches it, and the only block at $(2i, 2j)$ that contains it is the one of $(\lfloor r/2 \rfloor, \lfloor c/2 \rfloor)$, which lies outside $H$. Every block lies outside $H$, because each block starts in a row $\ge R_0$ or a column $\ge C_0$. Finally, each child has a larger $i + j$ than its parent: in the LL rule the row or the column grows by $R_0 - 1 \ge 1$ or $C_0 - 1 \ge 1$ and neither shrinks, and outside the LL band $2i + 2j > i + j$ because $(i, j) \ne (0, 0)$. So there are no cycles, every chain of parents ends in $H$, and the sets $D(h)$ are the disjoint trees of the roots. $\square$

**Lemma 2 (synchronization).** Run the decoder on the full stream. Before each bit is read, its lists LIP, LIS and LSP, its plane $n$ and its position in the loops are equal to those of the encoder before it writes that bit.

*Proof.* By induction on the number of bits. Both start with the same state at line L1: the lists depend only on $R$, $C$ and $L$, and $n_{\max}$ is in the header. Each step of the encoder writes a bit and then moves to a state that depends only on its current state and that bit: a significance bit chooses between moving an entry to the LSP (followed by a sign bit) and keeping it in a list (lines L3, L6); a set bit chooses between splitting the set and moving on (lines L5, L8); the test $L(i, j) \ne \emptyset$ of line L7 depends only on the geometry; the refinement pass (line L10) visits the LSP entries that existed before the pass, a number the decoder also knows. The decoder takes the same branch because it reads the same bit. $\square$

**Lemma 3 (the invariant of the sorting pass).** After the sorting pass of plane $n$ (lines L3 to L9):

1. every coefficient is in exactly one of: the LSP, the LIP, a set $D(i, j)$ of a type A entry of the LIS, or a set $L(i, j)$ of a type B entry;
2. every coefficient in the LIP and in the set of every LIS entry has $|c| < 2^n$;
3. a coefficient enters the LSP in the pass of plane $m$ only if $2^m \le |c| < 2^{m+1}$.

*Proof.* Part 1 holds after line L1 by Lemma 1, since $H$ is the LIP and the trees of the roots with offspring are the type A entries. Each operation keeps it. A coefficient leaves the LIP only for the LSP. A type A entry $(i, j)$ whose test gives 1 is replaced by its offspring, which go to the LIP or the LSP, and by $L(i, j)$ as a type B entry, or by nothing if $L(i, j)$ is empty; $D = O \cup L$ is a disjoint union. A type B entry whose test gives 1 is replaced by the type A entries of its offspring, and $L(i, j)$ is the disjoint union of their sets $D(k, l)$.

For part 2, the pass tests every LIP entry at the start (line L3), and every entry that enters the LIP later in the pass is tested before it enters (line L6). The LIS loop of line L4 runs to the end of the list, including the entries appended during the pass, so every entry still in the LIS at the end has been tested at threshold $2^n$ and gave 0. An entry that gave 1 was removed or replaced.

For part 3, a coefficient enters the LSP only after its own test gave 1, so $|c| \ge 2^m$. At the plane $m + 1$ it was not in the LSP, so by part 2 of the invariant for plane $m + 1$ it had $|c| < 2^{m+1}$; for $m = n_{\max}$ this holds by the definition of $n_{\max}$. $\square$

So after the sorting pass of plane $n$ the LSP holds exactly the coefficients with $|c| \ge 2^n$, since by parts 1 and 2 the others are all below $2^n$, and by part 3 those in the LSP are at least $2^n$.

**Lemma 4 (what the decoder knows).** After the refinement pass of plane $n$ (line L10), for each coefficient in the LSP the decoder knows its sign and the value $K = \lfloor |c| / 2^n \rfloor 2^n$.

*Proof.* Let the coefficient enter the LSP at plane $m \ge n$. By Lemma 3, bit $m$ of $|c|$ is 1 and the higher bits are 0. The refinement passes of the planes $m - 1, \ldots, n$ each send one more bit, because line L10 visits the entries that were in the LSP before the pass, which includes this one for every plane below $m$. So the decoder knows bits $m$ down to $n$, which give $K$. The sign was sent right after the significance bit. $\square$

**Theorem (error after each pass).** After the refinement pass of plane $n$, the decoder that outputs $\pm(K + 2^{n-1})$ for each LSP coefficient ($\pm K$ when $n = 0$) and 0 for the others has $|c - \hat c| \le 2^n - 1$ for every coefficient when $n \ge 1$, and $\hat c = c$ when $n = 0$.

*Proof.* For a coefficient outside the LSP, $|c| < 2^n$ by Lemma 3, so $|c - 0| \le 2^n - 1$. For one in the LSP, Lemma 4 gives $K \le |c| < K + 2^n$, an interval of $2^n$ integers whose midpoint $K + 2^{n-1}$ is within $2^{n-1} \le 2^n - 1$ of every point. For $n = 0$ the coefficients outside the LSP have $|c| < 1$, so $c = 0$, and those inside have $K = |c|$. $\blacksquare$

**Theorem (every prefix decodes).** Cut the stream after any number of bits, during the pass of plane $n$. The decoder of the implementation stops at the first missing bit and keeps a coefficient insignificant if its sign bit is missing. Then $|c - \hat c| \le 2^{n+1} - 1$ for every coefficient.

*Proof.* Up to the cut the decoder is in the encoder's state by Lemma 2. A coefficient that is not significant for the decoder was not in the LSP after plane $n + 1$ (or $n = n_{\max}$), so $|c| < 2^{n+1}$ by Lemma 3 and the error of the estimate 0 is at most $2^{n+1} - 1$. A significant coefficient has its bits known down to plane $k = n + 1$ (it was in the LSP after plane $n + 1$ and its refinement bit for plane $n$ was not read yet) or $k = n$, so as in Lemma 4 the decoder knows $|c|$ to within an interval of $2^k$ integers and its midpoint is within $2^{k-1}$; for $k = n + 1$ that is $2^n \le 2^{n+1} - 1$, and for $k = n$ it is smaller. A cut at the very end of the pass of plane $n$ makes the decoder stop at the first read of plane $n - 1$, and the bound $2^n - 1$ is that of the previous theorem. $\blacksquare$

**Corollary (lossless).** The full stream gives $\hat c = c$ by the case $n = 0$. The integer S-transform of the implementation is a bijection on integers: with $d = a - b$ and $s = b + \lfloor d/2 \rfloor$ the inverse is $b = s - \lfloor d/2 \rfloor$, $a = d + b$, a lifting step in each direction. So the inverse transform of the decoded coefficients is the original image. $\blacksquare$

The bounds hold for the coefficients. The S-transform is not orthonormal, so they do not give the same bound for the pixels, and the mean squared error of the image after each pass falls in the tests on the page but is not proved to fall.

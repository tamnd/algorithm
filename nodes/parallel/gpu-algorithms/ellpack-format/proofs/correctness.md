---
title: ELLPACK stores each nonzero exactly once, its SpMV computes Ax, and its warp loads are contiguous
proves: [correctness]
status: full
---

**Setting.** $A$ is an $M \times N$ matrix with $r_i$ nonzeros in row $i$ and $\mathit{nnz} = \sum_i r_i$ nonzeros in all. BUILD (lines L1 to L5) sets $K = \max_i r_i$, fills $M K$ slots with the value 0 and the column PAD, and then writes the $s$-th nonzero $(c, v)$ of row $i$, in increasing column order, at position $sM + i$ of the arrays $\mathit{data}$ and $\mathit{indices}$. SPMV (lines L6 to L11) computes $y_i = \sum_{s < K,\ \mathit{indices}[sM+i] \ne \text{PAD}} \mathit{data}[sM+i] \cdot x[\mathit{indices}[sM+i]]$.

**Lemma 1 (layout).** The map $(s, i) \mapsto sM + i$ is a bijection from $\{0, \ldots, K-1\} \times \{0, \ldots, M-1\}$ onto $\{0, \ldots, MK - 1\}$. After BUILD, for each row $i$, the slots $s < r_i$ hold the nonzeros of row $i$, each exactly once, and the slots $r_i \le s < K$ hold $(0, \text{PAD})$.

*Proof.* Division with remainder writes each $q \in \{0, \ldots, MK-1\}$ uniquely as $q = sM + i$ with $0 \le i < M$ and $0 \le s < K$, so the map is a bijection. Row $i$ has $r_i \le K$ nonzeros, so line L5 writes them to the slots $s = 0, \ldots, r_i - 1$ of row $i$, each to a different slot, and by the bijection no two rows share a slot. The other slots keep the padding from line L2. $\square$

**Theorem 1 (SpMV).** SPMV returns $y = Ax$.

*Proof.* By Lemma 1, the slots of row $i$ with an index other than PAD are exactly the nonzeros $(c, v)$ of row $i$, each once. So $y_i = \sum_{c : A_{ic} \ne 0} A_{ic} x_c = \sum_{c=0}^{N-1} A_{ic} x_c$, because the zero entries add nothing. $\square$

If the code does not test for PAD and uses a valid column such as 0 as the padding index, each padding slot adds $0 \cdot x_0 = 0$, and the result is the same in exact arithmetic. In IEEE floating point it is the same unless $x_0$ is infinite or NaN, since $0 \cdot \infty$ is NaN.

**Lemma 2 (counts).** The format has $MK - \mathit{nnz}$ padding slots, and stores $2MK$ words for $\mathit{data}$ and $\mathit{indices}$. ELLPACK-R stores $M$ more words for the row lengths.

*Proof.* There are $MK$ slots, and by Lemma 1 exactly $\mathit{nnz}$ of them hold nonzeros. Each slot has one word in each of the two arrays. $\square$

**Lemma 3 (contiguous warp loads).** Give row $i$ to thread $i$, and let a warp hold the threads $w, w+1, \ldots, w+31$. At slot $s$ the warp loads the words $sM + w, \ldots, sM + w + 31$ of each array, which are 32 consecutive words. With 4-byte words and 32-byte sectors these touch 4 sectors if $sM + w$ is a multiple of 8, and at most 5 sectors in all cases.

*Proof.* The addresses are $sM + w + \ell$ for the lanes $\ell = 0, \ldots, 31$, so they are consecutive. 32 words of 4 bytes are 128 bytes. A range of 128 consecutive bytes that starts at a multiple of 32 covers exactly 4 sectors of 32 bytes, and any range of 128 consecutive bytes meets at most 5 such sectors. If $M$ is a multiple of 8 (or the arrays are padded to a leading dimension that is) and $w$ is a multiple of 32, then $sM + w$ is a multiple of 8 for every $s$. $\square$

In the CSR format with one thread per row, lane $\ell$ at step $s$ loads word $\mathit{rowptr}[w + \ell] + s$. These addresses are $r_{w+\ell}$ apart, so when the rows have 8 or more entries every lane touches its own sector, up to 32 sectors per load. This is why the column-major layout of ELL matters on a GPU. $\blacksquare$

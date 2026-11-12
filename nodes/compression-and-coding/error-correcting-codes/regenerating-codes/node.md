---
tag: SKYSW3
kind: definition
slug: regenerating-codes
name: Regenerating codes
area: compression-and-coding/error-correcting-codes
level: research
summary: "Erasure codes for distributed storage that rebuild a lost node with less network traffic than a Reed-Solomon code, by trading storage per node against repair bandwidth."
history:
  year: 2010
  people: [Alexandros G. Dimakis, P. Brighten Godfrey, Yunnan Wu, Martin J. Wainwright, Kannan Ramchandran]
  note: Dimakis et al. found the storage and repair bandwidth tradeoff with network coding (conference version 2007, journal 2010). Rashmi, Shah and Kumar gave the product-matrix codes with exact repair in 2011.
prereqs: [erasure-codes, network-coding]
see_also: [reed-solomon-code, max-flow-min-cut-theorem, cut, vandermonde-matrix, singleton-bound, erasure-decoding, locally-decodable-codes, lagrange-interpolation]
sources:
  - paper: doi:10.1109/TIT.2010.2054295
    title: Alexandros G. Dimakis, P. Brighten Godfrey, Yunnan Wu, Martin J. Wainwright and Kannan Ramchandran, Network coding for distributed storage systems, IEEE Transactions on Information Theory 56(9), 2010, pages 4539 to 4551
    locator: The information flow graph, the cut-set bound B ≤ Σ min(α, (d - i)β) over i < k, the tradeoff curve, and the formulas for the minimum storage (MSR) and minimum bandwidth (MBR) points
  - paper: doi:10.1109/TIT.2011.2159049
    title: K. V. Rashmi, Nihar B. Shah and P. Vijay Kumar, Optimal exact-regenerating codes for distributed storage at the MSR and MBR points via a product-matrix construction, IEEE Transactions on Information Theory 57(8), 2011, pages 5227 to 5239
    locator: The product-matrix MBR code (symmetric message matrix [[S, T], [T^T, 0]]) for all d, and the product-matrix MSR code for d ≥ 2k - 2
  - paper: doi:10.1109/TIT.2012.2208937
    title: Parikshit Gopalan, Cheng Huang, Huseyin Simitci and Sergey Yekhanin, On the locality of codeword symbols, IEEE Transactions on Information Theory 58(11), 2012, pages 6925 to 6934
    locator: The definition of locality r and the bound d ≤ n - k - ceil(k/r) + 2
  - paper: "Cheng Huang, Huseyin Simitci, Yikang Xu, Aaron Ogus, Brad Calder, Parikshit Gopalan, Jin Li and Sergey Yekhanin, Erasure coding in Windows Azure Storage, USENIX Annual Technical Conference (ATC), 2012"
    title: Erasure coding in Windows Azure Storage
    locator: The (12, 2, 2) local reconstruction code used in production
---

A regenerating code is an erasure code for data spread over many storage nodes, designed so that a failed node can be rebuilt cheaply over the network. With a Reed-Solomon code, rebuilding one node means downloading as much data as the whole file, even though the node held only a small part of it. Dimakis, Godfrey, Wu, Wainwright and Ramchandran showed in 2010, with network coding, that a node can be rebuilt with much less traffic if each helper sends a small function of what it stores. They found the exact tradeoff between the amount each node stores and the amount a repair downloads.

## Definition

**Parameters.** A file of $B$ symbols over a finite field is stored on $n$ nodes, $\alpha$ symbols per node.

- *Reconstruction:* the data at any $k$ nodes determines the file.
- *Repair:* when a node fails, a new node contacts any $d$ of the $n - 1$ survivors ($k \le d \le n - 1$), the *helpers*. Each helper sends $\beta \le \alpha$ symbols, computed from its own data. The *repair bandwidth* is $\gamma = d\beta$.
- *Exact repair* rebuilds the lost content exactly. *Functional repair* builds new content that keeps the reconstruction property, but may differ from the lost one.

A code with these properties is an $(n, k, d, \alpha, \beta, B)$ regenerating code.

**The cut-set bound (Dimakis et al. 2010).** Model the life of the system as an *information flow graph*: a source, a node for each storage node at each time, edges of capacity $\alpha$ for what a node stores and $\beta$ for each repair download, and a data collector that connects to $k$ nodes. Every data collector must receive the whole file, so every source to collector [cut](/cut/) has capacity at least $B$. Take a collector that connects to $k$ nodes, each repaired in turn with the earlier ones among its helpers. The $i$-th of them ($i = 0, \ldots, k-1$) brings either its storage $\alpha$ or its $d - i$ downloads from outside, so

$$B \le \sum_{i=0}^{k-1} \min\bigl(\alpha, (d - i)\beta\bigr).$$

With functional repair, random linear network coding over a large field reaches every $(\alpha, \beta)$ that satisfies this bound, by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) for multicast. The bound gives a tradeoff curve: the least $\alpha$ for each $\beta$.

**The two end points.** For fixed $(n, k, d, B)$:

- *Minimum storage regenerating (MSR) point:* the least storage, $\alpha = B/k$, as in an MDS code. Then
$$\alpha_{\text{MSR}} = \frac{B}{k}, \qquad \beta_{\text{MSR}} = \frac{B}{k(d - k + 1)}, \qquad \gamma_{\text{MSR}} = \frac{B d}{k(d - k + 1)}.$$
- *Minimum bandwidth regenerating (MBR) point:* the least repair bandwidth, at which a node downloads exactly what it stores. Then
$$\beta_{\text{MBR}} = \frac{2B}{k(2d - k + 1)}, \qquad \alpha_{\text{MBR}} = \gamma_{\text{MBR}} = d\beta_{\text{MBR}} = \frac{2Bd}{k(2d - k + 1)}.$$

At MSR, the bound holds with $\alpha \le (d - k + 1)\beta$, so every term is $\alpha$ and $k\alpha = B$. At MBR, $\alpha = d\beta$, every term is $(d - i)\beta$, and the sum is $\beta\, k(2d - k + 1)/2 = B$. A Reed-Solomon code has $\alpha = B/k$ and repairs by downloading $\alpha$ from each of $k$ nodes, $\gamma = B$. With $d = n - 1$ the MSR point repairs with $\gamma = B(n - 1)/(k(n - k))$, which is much less than $B$ when $n - k$ is not tiny.

**Exact repair with product-matrix codes (Rashmi, Shah and Kumar 2011).** These codes have $\beta = 1$. Node $i$ has a fixed *encoding vector* $\psi_i$ of length $d$, and the file is placed in a *message matrix* $M$. Node $i$ stores $\psi_i^{T} M$.

- *MBR, for all $d$.* $\alpha = d$, $B = k(2d - k + 1)/2$, and
$$M = \begin{pmatrix} S & T \\ T^{T} & 0 \end{pmatrix},$$
with $S$ a symmetric $k \times k$ matrix ($k(k+1)/2$ symbols) and $T$ a $k \times (d-k)$ matrix. The vectors $\psi_i$ are rows of an $n \times d$ [Vandermonde matrix](/vandermonde-matrix/), so any $d$ of them are independent, and any $k$ of their first $k$ entries too. To repair node $f$, helper $j$ sends the one symbol $\psi_j^{T} M \psi_f$. The new node solves a $d \times d$ system for $M\psi_f$, and since $M$ is symmetric, $(M\psi_f)^{T} = \psi_f^{T} M$ is the lost content. To reconstruct, write $\psi_i = (\varphi_i, \delta_i)$; then $k$ nodes give $\Phi S + \Delta T^{T}$ and $\Phi T$, with $\Phi$ invertible, which yield $T$ and then $S$.
- *MSR, for $d \ge 2k - 2$.* For $d = 2k - 2$: $\alpha = k - 1$, $B = k(k-1)$, $M$ stacks two symmetric $(k-1) \times (k-1)$ matrices $S_1, S_2$, and $\psi_i = (\varphi_i, \lambda_i \varphi_i)$ with distinct $\lambda_i$. Helper $j$ sends $\psi_j^{T} M \varphi_f$; the new node gets $S_1 \varphi_f$ and $S_2 \varphi_f$ and forms $\varphi_f^{T} S_1 + \lambda_f \varphi_f^{T} S_2$. Larger $d$ follows by shortening a code with more nodes.

Exact repair cannot reach most points strictly between MSR and MBR, unlike functional repair. Later work built exact MSR codes for all parameters, with very large $\alpha$.

**Locally recoverable codes are a different idea.** A code has *locality* $r$ if each symbol is a function of some $r$ other symbols (Gopalan, Huang, Simitci and Yekhanin 2012). Such a code lowers the number of nodes read in a repair, not the bytes per node: a helper sends whole symbols, not functions of them. The price is distance: $d \le n - k - \lceil k/r \rceil + 2$, where $d$ here is the minimum distance. Windows Azure Storage uses a (12, 2, 2) local reconstruction code: 12 data fragments in two groups of 6, one local parity per group and 2 global parities. A lost data fragment is rebuilt from the 6 other fragments of its group, not from 12. Regenerating codes keep the MDS property at MSR and save bandwidth inside each helper's message; LRCs give up distance to read fewer nodes.

## Examples and non-examples

**The tradeoff for $n = 10$, $k = 5$, $d = 9$, $B = 1$.**

| scheme | storage $\alpha$ | repair download $\gamma$ |
|---|---|---|
| Reed-Solomon $[10, 5]$ | 0.2 | 1 |
| MSR point | 0.2 | $9/25 = 0.36$ |
| MBR point | $9/35 \approx 0.257$ | $9/35 \approx 0.257$ |

MSR keeps the storage of Reed-Solomon and cuts repair traffic by almost two thirds. MBR stores 29 percent more and repairs with the least traffic possible. The tests compute the least $\alpha$ for 41 values of $\beta$ between the two points and check that the curve falls from $\alpha_{\text{MBR}}$ to $\alpha_{\text{MSR}}$.

**A product-matrix MBR code.** Take $n = 6$, $k = 3$, $d = 4$ over $\mathrm{GF}(13)$, with $\psi_i = (1, x, x^2, x^3)$ for $x = i = 1, \ldots, 6$. Then $B = 3 \cdot 6/2 = 9$, $\alpha = 4$ and $\beta = 1$, exactly the MBR point, since $\min(4, 4) + \min(4, 3) + \min(4, 2) = 9$. The tests rebuild every node from every set of 4 helpers, exactly, and rebuild the file from all 20 sets of 3 nodes. For the same file a Reed-Solomon $[6, 3]$ code stores 3 symbols per node and repairs by downloading 9; the MSR point would store 3 and download 6. The MBR code stores 4 and downloads 4.

**Non-example: replication.** Three full copies of the file repair a node by copying $B$ from one survivor. Repair is simple, but the storage is $3B$, far above the tradeoff curve for any useful $k$. Regenerating codes are about coded storage.

**Non-example: a Reed-Solomon code with naive repair.** It is an $(n, k, d = k)$ code at the MSR storage, but its repair downloads $\gamma = B$, well above $\gamma_{\text{MSR}}$ when $d > k$. With $d = k$ the MSR formula gives $\gamma = B$, so naive repair is optimal only when the new node contacts exactly $k$ helpers. Reed-Solomon codes can repair with less bandwidth when helpers send traces of their symbols, but that is a different repair scheme, not the naive one.

**Non-example: an LRC.** The Azure code above reads 6 fragments in place of 12 to repair a data fragment, but each helper sends its whole fragment. It does not reach the MSR or MBR point; it optimizes a different cost.

## Related definitions

- [Erasure codes](/erasure-codes/): the basic setting; MSR codes are MDS codes with a repair property.
- [Network coding](/network-coding/) and the [max-flow min-cut theorem](/max-flow-min-cut-theorem/): the source of the cut-set bound and of functional repair.
- [Reed-Solomon codes](/reed-solomon-code/): the baseline that regenerating codes improve on.
- [Locally decodable codes](/locally-decodable-codes/): local recovery of message symbols under adversarial errors, a third meaning of "local".
- [Singleton bound](/singleton-bound/): MSR codes meet it; LRCs pay the extra term $\lceil k/r \rceil - 1$.

## References

- Alexandros G. Dimakis, P. Brighten Godfrey, Yunnan Wu, Martin J. Wainwright and Kannan Ramchandran, "Network coding for distributed storage systems", IEEE Transactions on Information Theory 56(9), 2010, pages 4539 to 4551.
- K. V. Rashmi, Nihar B. Shah and P. Vijay Kumar, "Optimal exact-regenerating codes for distributed storage at the MSR and MBR points via a product-matrix construction", IEEE Transactions on Information Theory 57(8), 2011, pages 5227 to 5239.
- Parikshit Gopalan, Cheng Huang, Huseyin Simitci and Sergey Yekhanin, "On the locality of codeword symbols", IEEE Transactions on Information Theory 58(11), 2012, pages 6925 to 6934.
- Cheng Huang et al., "Erasure coding in Windows Azure Storage", USENIX ATC 2012.

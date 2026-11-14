---
title: PPSFP reports the same faults as serial simulation
proves: [correctness]
status: full
---

Let $C$ be a combinational circuit with lines $0, \ldots, L - 1$ in topological order, so every input of a line has a smaller index. Let $\Phi$ be the list of single stuck-at faults and $t_1, \ldots, t_T$ the two-valued vectors. For a vector $t$, write $g_t(k)$ for the value of line $k$ in the good circuit and $f_t(k)$ for its value in the circuit with fault $f$. A fault $f$ is detected by $t$ when $f_t(o) \ne g_t(o)$ for some primary output $o$.

Fix a block $B = (b_0, \ldots, b_{m-1})$ of $m \le w$ vectors and let $M = 2^m - 1$. For a word $u$, write $u_i$ for its bit $i$. The words are below $2^m$, and as on the parallel fault simulation page, a gate evaluated on words with the mask $M$ gives in each bit $i < m$ the gate applied to the bits $i$ of its inputs. This is Lemma 1 of that proof, and it holds because AND, OR, XOR and the complement by $M$ combine equal bit positions only.

**Lemma 1 (good words).** After line L2, $\mathrm{good}[k]_i = g_{b_i}(k)$ for every line $k$ and every $i < m$.

*Proof.* By induction over $k$. A primary input gets bit $i$ from vector $b_i$. A gate line is evaluated on the words of its inputs, which are final and correct by induction, and the gate acts bit by bit. $\square$

Now fix a fault $f = (\ell, v)$ and consider the call of line L4. Define the correct faulty word $F[k]$ by $F[k]_i = f_{b_i}(k)$ for $i < m$. The walk keeps a map bad from lines to words. Write $\mathrm{cur}[k]$ for $\mathrm{bad}[k]$ if $k$ is in the map, and $\mathrm{good}[k]$ otherwise.

**Lemma 2 (lines before the site).** $F[k] = \mathrm{good}[k]$ for every line $k$ that is not reachable from $\ell$, and in particular for every $k < \ell$.

*Proof.* The value of such a line does not depend on the value of $\ell$, since no path leads from $\ell$ to it, and the fault changes only $\ell$. $\square$

**Lemma 3 (the walk).** When the walk ends, $\mathrm{cur}[k] = F[k]$ for every line $k$.

*Proof.* If the stuck word $vM$ (all bits $v$) equals $\mathrm{good}[\ell]$, then $g_{b_i}(\ell) = v$ for every $i$, so the faulty circuit computes the same value as the good one on every line under every vector of the block. Then $F = \mathrm{good}$ everywhere, and the walk returns with an empty map. Otherwise $\mathrm{bad}[\ell] = vM = F[\ell]$.

The walk takes scheduled lines in increasing index, and it schedules only fanouts of a taken line, which have larger indices. So each line is taken at most once, and when line $k$ is taken, no line with an index below $k$ is taken later. We show by induction over $k > \ell$, in increasing order, that after all lines up to $k$ are settled, $\mathrm{cur}[k] = F[k]$.

If $k$ is taken, all its inputs $j$ have $j < k$ and are settled, so $\mathrm{cur}[j] = F[j]$ by induction (or by Lemma 2, or by the case of $\ell$). The walk evaluates the gate of $k$ on these words, which gives $F[k]$ bit by bit, since $f$ does not sit on $k$. It stores the word in bad if it differs from $\mathrm{good}[k]$. If it equals $\mathrm{good}[k]$, then $\mathrm{cur}[k] = \mathrm{good}[k] = F[k]$ too.

If $k$ is not taken, no input of $k$ was stored in bad, since a stored line schedules all its fanouts, and $\ell$ is stored. So every input $j$ of $k$ has $\mathrm{cur}[j] = \mathrm{good}[j]$, and by induction $F[j] = \mathrm{good}[j]$. The gate of $k$ on the good words gives $\mathrm{good}[k]$, so $F[k] = \mathrm{good}[k] = \mathrm{cur}[k]$. $\square$

**Lemma 4 (seen).** The word seen of line L4 has bit $i$ equal to 1 exactly when $b_i$ detects $f$.

*Proof.* By Lemma 3, $\mathrm{cur}[o] \oplus \mathrm{good}[o]$ has bit $i$ equal to $f_{b_i}(o) \oplus g_{b_i}(o)$, and outputs that are not in bad contribute 0, which is right since then $\mathrm{cur}[o] = \mathrm{good}[o]$. The OR over the outputs is 1 in bit $i$ exactly when some output differs under $b_i$. $\square$

**Theorem.** PPSFP reports, for each vector $t_j$, exactly the faults that serial fault simulation reports: without dropping, all faults of $\Phi$ that $t_j$ detects; with dropping, the faults whose first detecting vector is $t_j$.

*Proof.* Without dropping, every fault stays alive, and by Lemma 4 each block reports $f$ at exactly the vectors of the block that detect it. With dropping, we show that a fault is alive at the start of a block exactly when no earlier vector detects it. This holds for the first block. Line L5 keeps $f$ when seen is 0, that is when no vector of the block detects it, and line L6 removes it otherwise. So the claim carries over to the next block. In a block where $f$ is alive and seen is not 0, the lowest set bit of seen is the first vector of the block that detects $f$, by Lemma 4, and no earlier block detects it. So line L6 reports $f$ at its first detecting vector, and at no other vector. $\square$

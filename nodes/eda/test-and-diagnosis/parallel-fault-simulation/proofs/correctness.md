---
title: Parallel fault simulation reports the same faults as serial simulation
proves: [correctness]
status: full
---

Let $C$ be a combinational circuit with lines $0, \ldots, L - 1$ in topological order, so every input of a line has a smaller index. Let $\Phi$ be the list of single stuck-at faults and $t_1, t_2, \ldots$ the two-valued vectors. For a vector $t$, write $g_t(k)$ for the value of line $k$ in the good circuit and $f_t(k)$ for its value in the circuit with fault $f$. A fault $f$ is detected by $t$ when $f_t(o) \ne g_t(o)$ for some primary output $o$. Let $\mathrm{alive}_i$ be the set of faults alive while vector $t_i$ is simulated: $\Phi$ for $i = 1$, and with dropping, $\Phi$ minus the faults reported for $t_1, \ldots, t_{i-1}$.

Fix a vector $t$ and a group $G = (f_1, \ldots, f_m)$ with $m \le w - 1$, and let $M = 2^{m+1} - 1$ be the word of $m + 1$ ones. For a word $u$, write $u_i$ for its bit $i$. Define the reference value of bit $i$ of line $k$ as
$$r_i(k) = g_t(k) \text{ if } i = 0, \qquad r_i(k) = (f_i)_t(k) \text{ if } 1 \le i \le m.$$

**Lemma 1 (bitwise gates).** Let $\mathrm{op}$ be a gate type and $u^1, \ldots, u^d$ words below $2^{m+1}$. The word $W$ that line L6 computes satisfies $W < 2^{m+1}$ and $W_i = \mathrm{op}(u^1_i, \ldots, u^d_i)$ for $0 \le i \le m$.

*Proof.* AND starts from $M$ and takes the AND of the inputs, OR and XOR start from 0, and BUF copies its input. In each case bit $i$ of the result is the AND, OR, XOR or copy of the bits $i$ of the inputs, since these operations combine equal bit positions only, and no bit above $m$ is set. The inverting types then XOR with $M$, which complements bits $0$ to $m$ and leaves the higher bits 0. $\square$

**Lemma 2 (insertion).** For $0 \le i \le m$, bit $i$ of $\mathrm{clear}[k]$ is 1 exactly when $i \ge 1$ and $f_i = (k, 0)$, and bit $i$ of $\mathrm{set}[k]$ is 1 exactly when $i \ge 1$ and $f_i = (k, 1)$. So bit $i$ of $(W \mathbin{\&} \lnot \mathrm{clear}[k]) \mid \mathrm{set}[k]$ is the stuck value $v$ if $f_i = (k, v)$, and $W_i$ otherwise.

*Proof.* Line L3 sets bit $i$ of $\mathrm{clear}[k]$ for $f_i = (k, 0)$ and of $\mathrm{set}[k]$ for $f_i = (k, 1)$, and nothing else. A fault has one line and one value, so at most one of the two masks has bit $i$ set. If $\mathrm{clear}[k]$ has it, the AND makes the bit 0 and the OR leaves it. If $\mathrm{set}[k]$ has it, the OR makes it 1. If neither has it, both operations leave $W_i$. $\square$

**Invariant.** After line L7 has processed line $k$ in the pass for $t$ and $G$, bit $i$ of $\mathrm{word}[k]$ is $r_i(k)$ for every $0 \le i \le m$, and $\mathrm{word}[k] < 2^{m+1}$.

*Proof.* By induction over $k$ in topological order. If $k$ is a primary input, line L5 gives the word $M$ or 0, so every bit is $t(k) = g_t(k)$. If $k$ is not a primary input, every input $j$ of $k$ has $j < k$ and is already processed, so by induction and Lemma 1, $W_i$ is the gate of $k$ applied to the values $r_i(j)$ of its inputs. In the circuit of bit $i$, that is the value of $k$ before any fault on $k$ acts. Lemma 2 then replaces bit $i$ by the stuck value exactly when $f_i$ sits on $k$. The value of $k$ in the good circuit is the gate on the good inputs, and in the circuit with fault $f_i$ it is the stuck value if $f_i$ sits on $k$ and the gate on the faulty inputs otherwise. These are exactly the cases above, so bit $i$ of $\mathrm{word}[k]$ is $r_i(k)$. Neither mask has a bit above $m$, so the word stays below $2^{m+1}$. $\square$

**Lemma 3 (comparison).** For $1 \le i \le m$, bit $i$ of the word diff of line L8 is 1 exactly when $t$ detects $f_i$.

*Proof.* For an output $o$, the word "bit 0 of $\mathrm{word}[o]$ copied into every bit" has every bit equal to $g_t(o)$, by the invariant. So bit $i$ of $\mathrm{word}[o]$ XOR this word is $(f_i)_t(o) \oplus g_t(o)$, which is 1 exactly when $o$ differs under $f_i$. The OR over the outputs is 1 exactly when some output differs. $\square$

**Theorem.** For each vector $t_i$, the algorithm reports exactly the faults of $\mathrm{alive}_i$ that $t_i$ detects. So its output is the same as that of serial fault simulation, with or without dropping.

*Proof.* Line L2 cuts $\mathrm{alive}_i$ into groups, and each alive fault is in exactly one of them. By Lemma 3, line L9 reports a fault of a group exactly when $t_i$ detects it. So the union over the groups is the set of faults of $\mathrm{alive}_i$ that $t_i$ detects. With dropping, line L10 removes exactly these faults, so the alive set of the next vector is $\mathrm{alive}_{i+1}$. Without dropping, the alive set stays $\Phi$, and $\mathrm{alive}_{i+1} = \Phi$ too. By induction over $i$, every vector is simulated against the right alive set. $\square$

The count of passes is $\lceil |\mathrm{alive}_i| / (w - 1) \rceil$ for vector $t_i$, and each pass processes each line once, which gives the bound of the complexity section.

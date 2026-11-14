---
title: The operation count of a march test, no false alarms, and the faults of one cell that the 10N march test detects
proves: [correctness]
status: full
---

The memory has $N$ one-bit cells with addresses $0, \ldots, N - 1$. A march test is a list of elements $M_0, \ldots, M_{e-1}$. Element $M_k$ has an address order and a list of $m_k$ operations. Lines L1 to L7 of the page apply each element to every address in its order and all its operations to one address before the next. The page writes March C− as
$$\Updownarrow(w0);\ \Uparrow(r0, w1);\ \Uparrow(r1, w0);\ \Downarrow(r0, w1);\ \Downarrow(r1, w0);\ \Updownarrow(r0)$$
and MATS+ as $\Updownarrow(w0);\ \Uparrow(r0, w1);\ \Downarrow(r1, w0)$. A fault counts as detected when the test fails from every initial content of the memory, since the content at power-up is not known.

**Theorem 1 (operation count).** A test that does not fail performs exactly $N \sum_k m_k$ operations. March C− performs $10N$ operations and MATS+ performs $5N$.

*Proof.* Line L2 visits each of the $N$ addresses once per element, whatever the order, and line L3 runs the $m_k$ operations of $M_k$ at each address. Only line L6 leaves early, and only on a failure. So element $M_k$ contributes $N m_k$ operations. For March C−, $(m_0, \ldots, m_5) = (1, 2, 2, 2, 2, 1)$ and the sum is 10. For MATS+, $(1, 2, 2)$ sums to 5. $\square$

Call a test **consistent** when, reading its operations in order and ignoring addresses, every read $rv$ has a write before it and the last write before it is $wv$.

**Theorem 2 (no false alarm).** A test passes on a fault-free memory from every initial content if and only if it is consistent.

*Proof.* In a fault-free memory, a read returns the value of the last write to the same cell, or the initial value if there was none. Fix a cell $a$. The operations on $a$ are those of $M_0$, then those of $M_1$, and so on, in the order of the list, because each element touches $a$ once and runs all its operations there. So the operations that reach $a$ are exactly the operation list of the test, in order. If the test is consistent, the last write before each read $rv$ on $a$ is $wv$, and the read returns $v$. If a read $rv$ has a last write $w\lnot v$ before it, it fails from every initial content. If a read $rv$ has no write before it, it reads the initial value of the cell, and it fails when the memory starts with $\lnot v$ in that cell. $\square$

March C− and MATS+ are consistent: in March C− the reads expect 0, 1, 0, 1 and 0, and each follows a write of that value in the element before.

A cell **stuck at** $v$ always holds $v$. A cell with a **transition fault** $\uparrow$ cannot go from 0 to 1, and with $\downarrow$ it cannot go from 1 to 0. In both cases the other cells and the address decoder work.

**Theorem 3.** March C− detects every stuck-at cell and every transition fault, from every initial content.

*Proof.* Let $i$ be the faulty cell. The other cells behave as in a fault-free memory, and reads of address $i$ return the content of cell $i$.

- Stuck at 1: $M_1$ reads $i$ expecting 0 and gets 1.
- Stuck at 0: $M_1$ writes 1 to $i$, and the first operation of $M_2$ at $i$ reads it expecting 1 and gets 0.
- Transition fault $\uparrow$: after $M_0$ the cell holds 0, from either initial value, since the write of 0 needs no rising transition. The write of 1 in $M_1$ fails, and the read of $M_2$ gets 0.
- Transition fault $\downarrow$: if the cell starts at 1, the write of $M_0$ fails and the read of $M_1$ gets 1. If it starts at 0, $M_1$ writes 1, $M_2$ reads 1 and then writes 0, which fails, and the read of $M_3$ gets 1. $\square$

**Theorem 4.** MATS+ misses every transition fault $\downarrow$.

*Proof.* Start from all 0. Then $M_0$ writes 0 with no transition, $M_1$ reads 0 and writes 1, and $M_2$ reads 1 and writes 0. The last write fails on the faulty cell, but no read follows it, so every read returns the expected value. $\square$

**What is cited and what is checked.** That March C− detects every unlinked inversion, idempotent and state coupling is proved on the [memory coupling fault](/memory-coupling-fault/) page, and this page does not repeat it. That it detects the address decoder faults of van de Goor's model is shown in his book (1991) and is not proved here. The tests of this page check both claims by injecting every fault of each class, from every initial content, into memories of 2 to 5 cells. That is an exhaustive check for those sizes, not a proof for every $N$.

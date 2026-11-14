---
title: Cycle-based simulation computes the Mealy machine of the design, and agrees with unit-delay timing when the period exceeds the depth
proves: [correctness]
status: full
---

Let the design have primary inputs, registers $r$ with outputs $q_r$, data inputs $d_r$ and initial values, and gates. After the cut of line L1, the logic $L$ has inputs $x$ (the primary inputs) and $q$ (the register outputs), and every loop of gates of the design passes through a register, so $L$ has no loop. For values $s$ of the registers and $x$ of the inputs, every net $n$ of $L$ has a unique value $L_n(s, x)$, defined by induction on the level. Put $\delta(s, x) = (L_{d_r}(s, x))_r$ and $\lambda(s, x) = (L_o(s, x))_o$ for the primary outputs $o$. Lines L1 to L8 refer to the pseudocode of the page.

**Theorem 1 (the Mealy machine).** For inputs $x_1, \ldots, x_T$, let $s_k = \delta(s_{k-1}, x_k)$. In cycle $k$, line L6 records $\lambda(s_{k-1}, x_k)$, and after line L7 of cycle $k$, $s = s_k$.

*Proof.* Line L2 succeeds, since $L$ has no loop (Kahn's algorithm levelizes every loop-free netlist; see the proof of compiled-code simulation). By induction on $k$: before cycle $k$, $s = s_{k-1}$ (true for $k = 1$ by L3). Line L5 evaluates the gates in an order where every gate follows the drivers of its inputs, so by induction along the order, every net $n$ gets the value $L_n(s_{k-1}, x_k)$. Line L6 records $\lambda(s_{k-1}, x_k)$. Line L7 reads all values $L_{d_r}(s_{k-1}, x_k)$ before it writes any register, so $s = \delta(s_{k-1}, x_k) = s_k$. $\square$

**Timed model.** Give every gate delay 1, and let the clock have period $p$. In cycle $k$ the primary inputs hold $x_k$ and the registers hold $s'_{k-1}$ during the time steps $(k-1)p, \ldots, kp - 1$. A gate output at step $t$ is the gate function of the values at step $t - 1$; before the first step the gate outputs have arbitrary values. At the end of cycle $k$ the registers take $s'_k$, the values of the $d_r$ at step $kp - 1$, and the outputs are sampled at the same step. Let $D$ be the depth of $L$, the largest level of a net.

**Theorem 2 (agreement with timing).** If $p \ge D + 1$, then $s'_k = s_k$ for every $k$, and the outputs sampled at step $kp - 1$ are $\lambda(s_{k-1}, x_k)$.

*Proof.* Induction on $k$, with $s'_0 = s_0$. In cycle $k$, the inputs and registers are $x_k$ and $s'_{k-1} = s_{k-1}$ at all steps of the cycle. Claim: a net of level $\ell$ has the value $L_n(s_{k-1}, x_k)$ at every step $t$ with $(k-1)p + \ell \le t \le kp - 1$. For $\ell = 0$ the net is an input or a register output, constant over the cycle. For a gate output of level $\ell \ge 1$ and a step $t \ge (k-1)p + \ell$, its value is the gate function of the values at step $t - 1 \ge (k-1)p + \ell - 1$, where every input of the gate, of level at most $\ell - 1$, already has its final value by induction. So the gate output has the value $L_n(s_{k-1}, x_k)$. Since $\ell \le D \le p - 1$, step $kp - 1$ lies in the range for every net, so the sampled outputs are $\lambda(s_{k-1}, x_k)$ and $s'_k = \delta(s_{k-1}, x_k) = s_k$. $\square$

The bound is tight for some designs. If $p \le D$, a net of level $D$ whose value changes in a cycle can be sampled before it settles; the tests show a design with $D = 3$ where $p = 2$ gives a different run. Real delays are not unit, and the condition $p \ge D + 1$ becomes the setup constraint of static timing analysis, with the delay of each path in place of its length.

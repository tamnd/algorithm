---
title: The looping algorithm sets a Benes network to realize any permutation, with N log2 N - N/2 switches
proves: [correctness]
status: full
---

We use the pseudocode of the page and the recursive network: for $N = 2^n \ge 4$, input switch $k$ takes lines $2k$ and $2k+1$ and sends its top output to line $k$ of the upper subnetwork $U$ and its bottom output to line $k$ of the lower subnetwork $L$; output switch $k$ takes line $k$ of $U$ on top and line $k$ of $L$ at the bottom and drives output lines $2k$ and $2k+1$. Lines and switches are numbered from 0, and $x \oplus 1$ is the other line of the same switch.

**The constraint graph.** For a permutation $\pi$ of the $N$ inputs, define two maps on inputs: $a(x) = x \oplus 1$ (the other input of the same input switch) and $b(x) = \pi^{-1}(\pi(x) \oplus 1)$ (the input whose output is on the same output switch as the output of $x$). Both are involutions without fixed points, so each splits the inputs into pairs. Let $H$ be the multigraph on the inputs with an $a$-edge $\{x, a(x)\}$ and a $b$-edge $\{x, b(x)\}$ for each $x$. Each input has one $a$-edge and one $b$-edge, so every connected component of $H$ is a cycle whose edges alternate between $a$-edges and $b$-edges. It has even length (a pair joined by both an $a$-edge and a $b$-edge is a cycle of length 2). A valid coloring is one in which the two ends of every edge get different colors: each input switch then sends one input up and one down, and each output switch gets one cell from each subnetwork.

**Lemma 1 (one loop colors one cycle).** Assume that, when line L4 starts with an uncolored input $x$, every cycle of $H$ is either fully colored or fully uncolored. Then the loop of lines L5 to L7 colors exactly the cycle of $x$, with a valid coloring, and stops with $y = x$.

*Proof.* Write the cycle of $x$ as $v_0 = x$, $v_1 = a(v_0)$, $v_2 = b(v_1)$, $v_3 = a(v_2)$, and so on, with $v_{2m} = v_0$ for the first such index $2m$, where $2m$ is the length of the cycle. Line L7 sets $y \leftarrow b(a(y))$, so the values of $y$ in the loop are $v_0, v_2, v_4, \ldots$ Pass $t$ colors $v_{2t}$ up and $v_{2t+1}$ down (line L6). The vertices $v_0, \ldots, v_{2m-1}$ are distinct and lie in a cycle that was fully uncolored, so the loop test of line L5 passes for $t = 0, \ldots, m-1$ and fails at $y = v_{2m} = x$. Every $a$-edge of the cycle is $\{v_{2t}, v_{2t+1}\}$, colored up and down. Every $b$-edge is $\{v_{2t+1}, v_{2t+2}\}$, colored down and up, including the last one, $\{v_{2m-1}, v_0\}$. $\square$

By induction over the passes of line L3, the assumption of Lemma 1 holds at each start, so after the loop of line L3 every input has a color and the coloring is valid.

**Lemma 2 (the subnetwork permutations).** The maps $\pi_U$ and $\pi_L$ of line L10 are permutations of $\{0, \ldots, N/2 - 1\}$.

*Proof.* Each input switch $k$ has exactly one up input $x$, because $\{2k, 2k+1\}$ is an $a$-edge, so $\pi_U(k)$ is set exactly once. Each output switch $k'$ receives the outputs $2k'$ and $2k'+1$, whose inputs $\pi^{-1}(2k')$ and $\pi^{-1}(2k'+1)$ form a $b$-edge, so exactly one of them is up, and $k'$ is the value $\pi_U(k)$ for exactly one $k$. So $\pi_U$ is a bijection. The same argument with down inputs gives $\pi_L$. $\square$

**Theorem (correctness).** For every permutation $\pi$ of $N = 2^n$ inputs, the settings returned by the algorithm send the value at input $x$ to output $\pi(x)$, for every $x$.

*Proof.* Induction on $n$. For $N = 2$ the single switch is crossed exactly when $\pi(0) = 1$, which is line L1.

Let $N \ge 4$ and take an up input $x$ on input switch $k = \lfloor x/2 \rfloor$. If $x = 2k$, the switch is straight (line L8) and $x$ leaves on top. If $x = 2k + 1$, then $2k$ is down, the switch is crossed, and $x$ again leaves on top. So $x$ enters $U$ at line $k$. By Lemma 2 and the induction hypothesis, $U$ is set to realize $\pi_U$, so $x$ leaves $U$ at line $k' = \pi_U(k) = \lfloor \pi(x)/2 \rfloor$ and enters output switch $k'$ on top. If $\pi(x) = 2k'$, the input routed to output $2k'$ is $x$, which is up, so the switch is straight (line L9) and $x$ leaves at $2k' = \pi(x)$. If $\pi(x) = 2k'+1$, the input routed to $2k'$ is the other input on the same $b$-edge, which is down, so the switch is crossed and $x$ leaves at $2k'+1 = \pi(x)$. A down input goes through $L$ in the same way, with top and bottom exchanged. $\blacksquare$

**Counts.** Let $S(N)$ be the number of switches and $D(N)$ the number of columns. Then $S(2) = 1$, $S(N) = N + 2S(N/2)$, $D(2) = 1$ and $D(N) = D(N/2) + 2$. By induction, $S(N) = N \log_2 N - N/2$: for $N = 2$ this is $2 - 1 = 1$, and $N + 2\left(\frac N2 (\log_2 N - 1) - \frac N4\right) = N \log_2 N - N/2$. Also $D(N) = 2 \log_2 N - 1$.

**Running time.** Each input is colored once in the loops of lines L3 to L7, and lines L8 to L10 take $O(N)$ time, so the work outside the recursive calls is $O(N)$, and $T(N) = 2T(N/2) + O(N) = O(N \log N)$. This is $O(1)$ per switch.

**Waksman's saving.** The first loop starts at $x = 0$ and colors it up, so input switch 0 is straight in every subnetwork with $N \ge 4$. Replacing it by two wires saves $N/2 - 1$ switches over the whole network (one for each of the $1 + 2 + \cdots + N/4 = N/2 - 1$ subnetworks of size at least 4), which leaves $N \log_2 N - N + 1$ switches. The algorithm still realizes every permutation, because it never crosses those switches.

**Lower bound.** A network of $s$ two-state switches has at most $2^s$ settings, and a rearrangeable network on $N$ lines must realize all $N!$ permutations, so $s \ge \log_2 N! = N \log_2 N - N \log_2 e + O(\log N)$. The Benes network is within $O(N)$ switches of this bound.

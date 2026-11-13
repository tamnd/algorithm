---
title: Hysteresis thresholding marks exactly the candidates connected to a strong pixel
proves: [correctness]
status: full
---

Let $C = \{p : s(p) \ge t_\ell\}$ be the candidates and $T = \{p : s(p) \ge t_h\}$ the strong pixels. Since $t_\ell \le t_h$, $T \subseteq C$. Let $R$ be the set of pixels $q$ for which there is a path $p_0, p_1, \ldots, p_k = q$ with $p_0 \in T$, every $p_i \in C$, and $p_{i+1}$ an 8-neighbor of $p_i$. We prove that HYSTERESIS returns the mask of $R$.

**Lemma 1 (each pixel is pushed at most once).** A pixel is pushed only at line L2 or line L7, and both lines set $E$ to true at the same time. Line L2 visits each pixel once, before any push at line L7, and line L7 pushes $q$ only when $E(q)$ is false. $E$ never becomes false again. So each pixel is pushed at most once. $\square$

So the loop of lines L3 to L7 runs at most $W H$ times, and the algorithm stops.

**Lemma 2 (every marked pixel is in $R$).** *Invariant:* every pixel with $E(p)$ true is in $R$.

*Proof.* At the start $E$ is all false. Line L2 marks a pixel of $T$, which is in $R$ by the path of length 0. Line L7 marks a pixel $q$ with $s(q) \ge t_\ell$, so $q \in C$, and $q$ is a neighbor of the popped pixel $p$, which is marked and so in $R$ by the invariant. A path to $p$ in $R$ followed by the step to $q$ is a path to $q$, so $q \in R$. $\square$

**Lemma 3 (every pixel of $R$ is marked).** At line L8, every pixel of $R$ has $E$ true.

*Proof.* By Lemma 1, every pushed pixel is popped before the loop ends, because the loop runs until the stack is empty. Every marked pixel was pushed, so every marked pixel is popped once, and at that pop line L5 examines all its neighbors $q$ inside the image. If such a $q$ is a candidate, then after line L6 it is marked: either it was marked already, or line L7 marks it.

Take $q \in R$ with a path $p_0, \ldots, p_k = q$ as in the definition. We show by induction on $i$ that $p_i$ is marked. Pixel $p_0 \in T$ is marked at line L2. If $p_i$ is marked, it is popped at some time, and $p_{i+1}$ is a candidate neighbor of $p_i$, so it is marked after that pop. So $p_k = q$ is marked. $\square$

**Theorem.** HYSTERESIS returns $E$ with $E(p)$ true exactly for $p \in R$, after at most $W H$ pushes and $8 W H$ neighbor tests.

*Proof.* Lemmas 2 and 3 give the two inclusions, and Lemma 1 gives the count, with 8 neighbor tests per pop. $\blacksquare$

**Corollary (components).** $R$ is the union of the connected components of the graph on $C$, with the 8-neighbor edges, that contain a pixel of $T$. A pixel $q$ is in $R$ exactly when its component meets $T$, because the paths in the definition of $R$ are exactly the paths in that graph. This is the form that the second reference implementation checks, by labeling the components with repeated propagation of the minimum label until no label changes. The first reference implementation runs a separate breadth-first search from each strong pixel.

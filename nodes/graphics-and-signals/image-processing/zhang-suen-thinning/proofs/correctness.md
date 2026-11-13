---
title: Zhang-Suen thinning stops, returns a subset that is a fixed point, and deletes only pixels that are simple one at a time
proves: [termination, subset, fixed-point, local-simplicity, parallel-counterexample]
status: full
---

**Notation.** The image is a finite set $X$ of foreground pixels in $D = \{0, \dots, W-1\} \times \{0, \dots, H-1\}$, with $y$ growing downward; every pixel outside $X$, inside or outside $D$, is background. For a pixel $P_1$ the neighbors $P_2, \dots, P_9$ are, in this order, the pixels at the offsets $(0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1)$, clockwise from the north; we also write $P_i$ for the value 0 or 1 at that pixel. $B = P_2 + \dots + P_9$, and $A$ is the number of indices $i$ in the circular sequence $P_2, \dots, P_9, P_2$ with a 0 followed by a 1. The foreground is taken with 8-adjacency and the background with 4-adjacency.

**Theorem 1 (termination, subset and fixed point).** ZHANG-SUEN stops after at most $|X| + 1$ iterations. Its output $Y$ satisfies $Y \subseteq X$, and neither subiteration deletes any pixel of $Y$.

*Proof.* Lines L5 to L7 only mark foreground pixels, and line L8 only sets pixels to 0, so the foreground never grows and $Y \subseteq X$. An iteration that does not stop at line L9 has set `changed` at line L8, so it has deleted at least one pixel. The foreground has $|X|$ pixels at the start, so at most $|X|$ iterations delete something, and the next one stops. In the last iteration the first subiteration marks nothing, so the image is the same when the second subiteration starts, and it marks nothing either. So $Y$ is a fixed point of both subiterations, and running the algorithm on $Y$ stops after one iteration with $Y$ unchanged. $\square$

**Lemma 2 (the ring).** The 8 neighbors in the order $P_2, \dots, P_9, P_2$ form a cycle in which consecutive pixels are 4-adjacent. The cycle alternates between the edge neighbors $P_2, P_4, P_6, P_8$ and the corner neighbors $P_3, P_5, P_7, P_9$.

*Proof.* Consecutive offsets in the list differ by 1 in exactly one coordinate: $(0,-1) \to (1,-1) \to (1,0) \to (1,1) \to (0,1) \to (-1,1) \to (-1,0) \to (-1,-1) \to (0,-1)$. The even positions have one zero coordinate and the odd positions have none. $\square$

**Lemma 3 (one run).** If $2 \le B \le 6$ and $A = 1$, the foreground neighbors form one run $R_1$ of consecutive pixels of the ring, and the background neighbors form one run $R_0$ of length $8 - B \ge 2$.

*Proof.* Since $1 \le B \le 7$, the circular sequence has both values. Then the number of maximal runs of 1 equals the number of 0 to 1 steps, which is $A = 1$, and the number of runs of 0 equals the number of runs of 1. $\square$

**Theorem 4 (a deleted pixel is simple when it is deleted alone).** Let $p \in X$ satisfy $2 \le B \le 6$ and $A = 1$. Then $X \setminus \{p\}$ has the same number of 8-connected components as $X$, and the background of $X \setminus \{p\}$ has the same number of 4-connected components as the background of $X$.

*Proof.* *Foreground.* Let $X' = X \setminus \{p\}$. Two pixels connected by an 8-path in $X'$ are connected in $X$. Conversely, take an 8-path in $X$ between two pixels of $X'$, and look at a visit of the path to $p$. The pixels just before and just after it are foreground neighbors of $p$, so they lie in $R_1$. By Lemmas 2 and 3, $R_1$ is a 4-connected, hence 8-connected, chain of pixels of $X'$, so the visit to $p$ can be replaced by a walk along $R_1$. So the components of $X'$ are the components of $X$ with $p$ removed. No component vanishes, because the component of $p$ also holds the $B \ge 2$ pixels of $R_1$.

*Background.* Let $Z$ be the background of $X$ and $Z' = Z \cup \{p\}$. A run of at least 2 consecutive ring pixels holds an edge neighbor by Lemma 2, so $R_0$ holds a pixel $q$ that is 4-adjacent to $p$. Then $p$ joins the 4-component of $q$ and creates no new component. It does not join two different components either: every 4-neighbor of $p$ in $Z$ is an edge pixel of $R_0$, and $R_0$ is a 4-connected chain in $Z$ by Lemma 2, so all of them are in one 4-component of $Z$ already. $\square$

The bound $B \le 6$ matters for the background part: with $B = 7$ the only background neighbor can be a corner neighbor, so $p$ has no background 4-neighbor, and deleting $p$ would make $p$ a new background component, a one pixel hole. The bound $B \ge 2$ keeps the end pixels of a line, which have $B = 1$.

**Proposition 5 (parallel deletion is not safe).** Theorem 4 does not extend to the parallel deletion of all marked pixels: for the $2 \times 2$ square every pixel is marked in the first subiteration, and the whole component is deleted.

*Proof.* Take $X = \{(0,0), (1,0), (0,1), (1,1)\}$. For the pixel $(0,0)$ the ring $P_2, \dots, P_9$ is $0, 0, 1, 1, 1, 0, 0, 0$: $B = 3$, one 0 to 1 step so $A = 1$, and $P_2 = P_8 = 0$, so $P_2 P_4 P_6 = 0$ and $P_4 P_6 P_8 = 0$. For $(1,0)$ the ring is $0, 0, 0, 0, 1, 1, 1, 0$, for $(0,1)$ it is $1, 1, 1, 0, 0, 0, 0, 0$, and for $(1,1)$ it is $1, 0, 0, 0, 0, 0, 1, 1$. Each has $B = 3$ and $A = 1$. In each, $P_4 = 0$ or $P_6 = 0$, so both products of the first subiteration are 0. All four pixels are marked on the same image and deleted at line L8, and the foreground becomes empty. Each deletion alone keeps the topology by Theorem 4; together they remove a component. $\blacksquare$

---
title: Why the sample lifetimes decay exponentially, why the update is conservative, and why a ghost on a flat background only shrinks
proves: [correctness]
status: full
---

Notation as on the page. Pixel $x$ holds $N$ samples $M(x)$, a value $v$ is background when at least $\#_{\min}$ samples $s$ have $|v - s| < R$, and each random choice of lines L5 and L6 is independent of all others. The claims are about the random update. They say nothing about whether the mask matches the true moving objects.

## Claim 1: memoryless survival

Fix a sample $s$ in $M(x)$. Each time line L5 or line L6 writes into $M(x)$, the sample $s$ survives with probability $(N - 1)/N$, whatever happened before. After $k$ writes it survives with probability $((N - 1)/N)^k = e^{-k \ln(N/(N-1))}$.

*Proof.* A write into $M(x)$ picks the index to replace uniformly from $\{1, \ldots, N\}$, independently of the past. The sample $s$ is lost only if its index is picked, which has probability $1/N$. The writes use independent random numbers, so the survival probabilities multiply. $\square$

The age of $s$ does not enter: an old sample and a new one have the same chance to survive the next write. This is why ViBe needs no time stamps.

## Claim 2: the expected lifetime

(a) If $x$ is background in every frame and no neighbor writes into $M(x)$, the number of frames that $s$ survives is geometric with parameter $1/(\varphi N)$, and its mean is $\varphi N$.

(b) If $x$ and its 8 neighbors are background in every frame and every neighbor has 8 neighbors, then $s$ survives one frame with probability
$$q = \Big(1 - \frac{1}{\varphi N}\Big)\Big(1 - \frac{1}{8 \varphi N}\Big)^8,$$
and the mean lifetime is $1/(1 - q)$.

*Proof.* (a) In one frame, line L5 writes into $M(x)$ with probability $1/\varphi$, and that write removes $s$ with probability $1/N$ by Claim 1. So $s$ is lost in a given frame with probability $p = 1/(\varphi N)$, independently over frames. The first loss is geometric, with mean $1/p = \varphi N$.

(b) In one frame, the own write removes $s$ with probability $1/(\varphi N)$, as in (a). A neighbor $y$ removes $s$ if it makes a neighbor write (probability $1/\varphi$), chooses $x$ among its 8 neighbors (probability $1/8$), and picks the index of $s$ (probability $1/N$), so with probability $1/(8 \varphi N)$. The 9 events use independent random numbers, so $s$ survives the frame with probability $q$, and the lifetime is geometric with mean $1/(1 - q)$. $\square$

With $N = 20$ and $\varphi = 16$, (a) gives a mean of 320 frames and (b) gives $q \approx 0.993764$ and a mean of about 160.36 frames. Since $1 - q \approx 2/(\varphi N)$ to first order, the mean in (b) is about $\varphi N / 2$. The tests check (a) by sampling and the numbers of (b) exactly.

## Claim 3: the update is conservative

Line L5 never writes into the set of a foreground pixel, and only background values are written by lines L5 and L6. In a frame where every pixel is foreground, no set changes.

*Proof.* Line L4 skips foreground pixels, so lines L5 and L6 run only for a background pixel $x$, and they write the value $v(x)$. Line L5 writes into $M(x)$ only, and $x$ is background. If every pixel is foreground, lines L5 and L6 never run. $\square$

A foreground pixel can still receive a value through line L6 of a background neighbor. That is the spatial spread, and it is the reason a ghost, or a stopped object, is eaten from its border.

## Claim 4: on a flat background a ghost only shrinks

Suppose that from some frame on, every frame is the same flat image with value $b$ at every pixel. Then a pixel that is background in one of these frames is background in every later one. So the number of foreground pixels never grows.

*Proof.* Let $c(x)$ be the number of samples $s \in M(x)$ with $|b - s| < R$. Every write of lines L5 and L6 in these frames writes the value $b$ of some background pixel, because the image is flat. A write replaces one sample of some $M(x)$ by $b$, and $|b - b| = 0 < R$. If the replaced sample was close to $b$, then $c(x)$ stays the same; otherwise it grows by 1. So $c(x)$ never decreases. A pixel is background exactly when $c(x) \ge \#_{\min}$, which then stays true. The classification of line L2 uses the sets as they are at the start of the frame, before the updates, so the argument holds frame by frame. $\square$

The claim needs the flat image. If two neighbors show values farther apart than $R$, a write from one into the other can remove a close sample and turn a background pixel to foreground. The tests check the claim on a $6 \times 6$ ghost: the counts per frame never grow, and with $\varphi = 1$ they reach 0.

## Claim 5: the early stop gives the same answer

The loop of line L2 that stops when the count reaches $\#_{\min}$ returns background exactly when the full count of close samples is at least $\#_{\min}$.

*Proof.* The count only grows during the loop. If the loop stops early, the count of the samples read so far is $\#_{\min}$, and the full count is at least that. If it does not stop, it has read every sample, so its count is the full count, and that count is below $\#_{\min}$. $\square$

## Claim 6: cost of one frame

For $P$ pixels, line L2 reads at most $N$ samples per pixel, line L5 makes one random draw and at most one write per pixel, and line L6 makes at most two random draws, a list of at most 8 neighbors and one write. So a frame costs $O(P N)$ operations, with a random integer at unit cost, and the model takes $O(P N)$ space. Line L1 makes $N$ random draws per pixel once, so it costs $O(P N)$. $\square$

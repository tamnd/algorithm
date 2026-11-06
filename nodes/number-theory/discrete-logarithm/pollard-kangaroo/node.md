---
tag: VXD7T2
kind: algorithm
slug: pollard-kangaroo
name: Pollard's kangaroo algorithm
aliases:
- Pollard's lambda method
- wild and tame kangaroos
- kangaroo method
area: number-theory/discrete-logarithm
level: advanced
summary: Solves g^x = h for x in an interval of width w. A tame kangaroo from the middle and a wild one from h make small known jumps until they meet, in about 2 w^(1/2) steps and O(1) memory, heuristically.
solves: [interval-discrete-logarithm-problem]
model: generic-group-model
complexity:
  vars:
    w: the width b - a of the interval
    k: the number of binary digits of the modulus p, when the group is a subgroup of (Z/pZ)^*
  time:
    heuristic: O(w^(1/2))
    worst: O(w^(1/2))
  space:
    heuristic: O(1)
    extra: O(w^(1/2))
  bit_operations:
    worst: O(w^(1/2) k^2)
properties:
  deterministic: false
  recursive: false
prereqs: [interval-discrete-logarithm-problem, pollard-rho-discrete-logarithm, distinguished-points]
see_also: [baby-step-giant-step, parallel-collision-search, pohlig-hellman, short-discrete-logarithm, generic-group-model, shoup-generic-lower-bound]
sources:
  - paper: doi:10.1090/S0025-5718-1978-0491431-9
    title: John M. Pollard, Monte Carlo methods for index computation (mod p), Mathematics of Computation 32(143), 1978
    locator: pages 918 to 924 (the lambda method, with a tame kangaroo that sets a trap)
  - paper: doi:10.1007/s001450010010
    title: John M. Pollard, Kangaroos, Monopoly and discrete logarithms, Journal of Cryptology 13(4), 2000
    locator: pages 437 to 447 (analysis of the serial and parallel methods, and jumps that are powers of two)
  - paper: doi:10.1007/PL00003816
    title: Paul C. van Oorschot and Michael J. Wiener, Parallel collision search with cryptanalytic applications, Journal of Cryptology 12(1), 1999
    locator: pages 1 to 28 (kangaroos with distinguished points, and the cost of about 3.28 w^(1/2) for repeating Pollard's original method)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 14, Section 14.5 (the walk in 14.5.1, the algorithm and Example 14.5.2, Heuristic 14.5.4 and Theorem 14.5.5 giving (2 + o(1)) w^(1/2), Exercise 14.5.6, inversion in 14.5.5, and Section 14.5.6 on the analysis of Montenegro and Tetali) and Section 14.6 (distributed kangaroos)
---

Pollard's kangaroo algorithm, also called the lambda method, solves the [interval discrete logarithm problem](/interval-discrete-logarithm-problem/): find $x \in [a, b]$ with $g^x = h$. A tame kangaroo starts at a known power of $g$ in the middle of the interval and a wild kangaroo starts at $h$; both make small jumps by powers of $g$ chosen from the current position, so each knows how far it has travelled. Once the two land on a common point they follow the same path, and a [distinguished point](/distinguished-points/) on that path reveals $x$ as the difference of their distances. With a mean jump of about $\sqrt w / 2$ for width $w = b - a$, the method takes about $2\sqrt w$ group operations and constant memory, under a random walk heuristic, which makes it the method of choice for a short exponent in a large group.

## In plain words

Two kangaroos hop along the same road. Where each one lands decides the length of its next hop, by a fixed rule. The tame kangaroo starts from a spot whose position we know; the wild one starts from the spot we want to locate. Both keep count of how far they have hopped.

Hops are short, so if the kangaroo behind ever lands exactly where the one in front has been, the two follow the same footprints from then on. Here and there along the road are flagged spots, and each kangaroo reports a flag when it reaches one. When both report the same flag, the difference between their distances tells us where the wild kangaroo started. Only the flags need to be remembered.

## The problem

**Input.** A modulus $p \ge 2$, an element $g$ of $(\mathbb{Z}/p\mathbb{Z})^*$, a target $h$, and integers $0 \le a \le b$. The method needs no knowledge of the order of $g$ and works in any group with a unique representation of elements.

**Output.** Some $x \in [a, b]$ with $g^x = h$, or NONE if there is none.

**Cost model.** The group is the cyclic subgroup $\langle g \rangle$ of $(\mathbb{Z}/p\mathbb{Z})^*$. One group operation is a multiplication modulo $p$, $O(k^2)$ bit operations for a $k$-bit $p$; the jumps $g^{2^j}$ are precomputed with $O(\log w)$ squarings. Costs are in group operations as a function of the width $w$, not of the group order. The bound of about $2\sqrt w$ operations is heuristic, under the assumption that the walk behaves like a random walk with independent footprints (Galbraith, Heuristic 14.5.4); Montenegro and Tetali proved $(2 + o(1))\sqrt w$ for jumps that are powers of $2$ when the partition is a random function. The version below also has a proved worst case of $O(\sqrt w)$ operations, because it ends with a [baby-step giant-step](/baby-step-giant-step/) certificate; that last step needs $O(\sqrt w)$ memory. The lower bound $\Omega(\sqrt w)$ holds in the [generic group model](/generic-group-model/).

## The algorithm

The jumps are $g^{s_j}$ with $s_j = 2^j$ for $0 \le j < k$, and $S$ maps an element to a jump index in $\{0, \dots, k - 1\}$ by a function of its representation. A point is distinguished if another function of its representation is $0$, with probability $\theta$ about $8 / \sqrt w$.

```pseudo id=main
POLLARD-KANGAROO(g, h, a, b)             ▷ returns x in [a, b] with g^x = h, or NONE
L1  w ← b − a ; h' ← h · g^(−a)           ▷ now look for z in [0, w] with g^z = h'
L2  k ← least k with (2^k − 1)/k ≥ √w / 2 ▷ jumps 2^0, ..., 2^(k−1), mean about √w / 2
L3  repeat R times
L4      (T, t) ← (g^⌊w/2⌋, ⌊w/2⌋) ; (W, u) ← (h', 0)   ▷ tame in the middle, wild at the target
L5      D ← empty table                  ▷ distinguished point ↦ (kind, distance)
L6      repeat N_max times
L7          for each kangaroo (Y, d) of kind κ in (tame, wild) do   ▷ alternate jumps
L8              if Y is distinguished then
L9                  if D[Y] holds the other kind then
L10                     z ← (tame distance) − (wild distance)
L11                     if 0 ≤ z ≤ w and g^z = h' then return a + z
L12                 D[Y] ← (κ, d)
L13             j ← S(Y) ; Y ← Y · g^(2^j) ; d ← d + 2^j
L14     choose a fresh function S
L15 z ← BABY-STEP-GIANT-STEP(g, h', w + 1) ; return a + z if z ≤ w, else NONE
```

Line L1 shifts the interval to $[0, w]$. Line L2 picks the jump set, so that the mean jump $m = (2^k - 1)/k$ is about $\sqrt w / 2$, the value that minimizes the expected cost. Line L4 starts the tame kangaroo at $g^{\lfloor w/2 \rfloor}$ and the wild one at $h'$; the invariants are $T = g^t$ and $W = h' g^u$. Lines L7 to L13 move the two kangaroos in turn. When a kangaroo stands on a distinguished point, line L9 looks it up; if the other kangaroo has been there, then $g^t = h' g^u$, so $h' = g^{t - u}$ and line L11 returns the answer after a check. Otherwise line L12 records the point. If the walk fails within $N_{\max}$ rounds, which happens with small probability for a solvable instance and always for an unsolvable one, line L14 changes the walk and the search starts again. After $R$ failures, line L15 decides the instance with baby-step giant-step: a kangaroo search that fails proves nothing, so this step is what makes NONE reliable.

## Example

This is Galbraith's Example 14.5.2. Let $p = 263$ and $g = 3$, of prime order $131$, with $h = 181$ and $x \in [0, 52]$, so $w = 52$. Since $\sqrt{52}/2 \approx 3.6$, take $k = 4$, jumps $\{1, 2, 4, 8\}$ with mean $3.75$, $S(y) = y \bmod 4$, and let a point be distinguished when its residue is divisible by $3$. The tame kangaroo starts at $3^{26} \equiv 26$ and the wild one at $181$.

| $i$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| tame point | 26 | 2 | **162** | 235 | **129** |
| tame distance $t$ | 26 | 30 | 34 | 38 | 46 |
| wild point | 181 | **51** | **75** | 2 | **162** |
| wild distance $u$ | 0 | 2 | 10 | 18 | 22 |

Distinguished points are in bold. The tame kangaroo records $162$ with $t = 34$, and the wild one reaches $162$ with $u = 22$. So $x = 34 - 22 = 12$, and indeed $3^{12} \equiv 181 \pmod{263}$. The paths had met already at $2$, but that point is not distinguished, so the collision is seen only at the next distinguished point.

For no solution, take $p = 23$, $g = 5$, $h = 14$ and $[a, b] = [0, 10]$: the only logarithm of $14$ modulo $22$ is $21$, the kangaroo search finds no collision that passes line L11, and line L15 returns NONE.

## Correctness

The invariants $T = g^t$ and $W = h' g^u$ hold at line L4 and are kept by line L13, since multiplying by $g^{2^j}$ adds $2^j$ to the exponent. When line L9 finds that the tame and the wild kangaroo have stood on the same point $Y$, $g^{t} = Y = h' g^{u}$ for the recorded distances, so $h' = g^{t - u}$. Line L11 returns $a + z$ only when $0 \le z \le w$ and $g^z = h'$, which means $g^{a + z} = h$ with $a + z \in [a, b]$; so every value returned by the kangaroo phase is correct. If the kangaroo phase fails, line L15 runs baby-step giant-step with $m = \lceil \sqrt{w + 1} \rceil$, which finds the least $z \ge 0$ with $g^z = h'$ if it is below $m^2 \ge w + 1$, so it returns a value in $[a, b]$ exactly when one exists. Hence the output is correct in all cases, and the algorithm always stops. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Heuristic average case.** The rear kangaroo first has to pass the start of the front one, on average $w / (4m)$ jumps, and then each of its jumps lands on a footprint of the front one with probability about $1/m$, so about $m$ more jumps are needed. With alternate jumps, the total is about $2(w / (4m) + m)$, minimized at $m = \sqrt w / 2$, giving $2\sqrt w$, plus about $2/\theta$ to reach the next distinguished point: $(2 + o(1))\sqrt w$ group operations (Galbraith, Theorem 14.5.5). The worst case over instances is $(3 + o(1))\sqrt w$ with the same $m$ (Galbraith, Exercise 14.5.6).
- **Proved bounds.** Montenegro and Tetali proved the $(2 + o(1))\sqrt w$ bound when $S$ is a random function and distinguished points are well distributed, and Pollard proved it with $o(1)$ replaced by an $\varepsilon < 0.06$ (Galbraith, Section 14.5.3). For the version above, $R$ attempts of $N_{\max} = O(\sqrt w)$ rounds and the final baby-step giant-step give $O(\sqrt w)$ group operations in the worst case, unconditionally.
- **Space.** The kangaroo phase stores about $2\theta\sqrt w$ distinguished points, a constant for $\theta \approx c / \sqrt w$. The certificate of line L15 needs $O(\sqrt w)$ stored elements, and is reached only when the kangaroos fail or there is no solution.
- **Bit operations.** $O(\sqrt w \, k^2)$ for a subgroup of $(\mathbb{Z}/p\mathbb{Z})^*$ with $k$-bit $p$ and schoolbook multiplication.

## Properties

- **Needs only the width.** The cost depends on $w$, not on the group order, which may even be unknown.
- **Las Vegas.** The kangaroo phase never returns a wrong answer, because line L11 checks it; only its running time and success are random.
- **Constant memory.** Except for the certificate, the method stores a few distinguished points, unlike baby-step giant-step on the same interval.
- **Parallel.** With many tame and wild kangaroos reporting distinguished points to a server, the speedup is linear in the number of processors (van Oorschot and Wiener; Pollard 2000; Galbraith, Section 14.6).
- **Generic.** Only the group law, equality and functions of a unique representation are used.

## Variants and improvements

- **Pollard's original trap.** The tame kangaroo jumps a fixed number of times and stops at a trap; the wild kangaroo jumps until it lands in the trap or passes it. Each run succeeds with a fixed probability, and repeating it until success costs about $3.28\sqrt w$ operations (van Oorschot and Wiener, as cited by Galbraith).
- **Parallel kangaroos.** Herds of $N/2$ tame and $N/2$ wild kangaroos with jumps of mean about $N\sqrt w / 4$, so that kangaroos of the same herd rarely collide, give about $2\sqrt w / N$ operations per processor (Galbraith, Section 14.6).
- **Three and four kangaroos.** For $g$ of odd order, after centring the interval, wild kangaroos from both $h$ and $h^{-1}$ give about $1.818\sqrt w$ with three kangaroos and about $1.714\sqrt w$ with four (Galbraith, Pollard and Ruprai; Galbraith, Section 14.5.5).
- **Gaudry-Schost.** A birthday based method on overlapping tame and wild sets, which handles multidimensional problems and, combined with the four kangaroo idea, reaches about $1.660\sqrt w$ (Galbraith, Section 14.7).
- **Full group.** With $w$ equal to the group order the kangaroo method costs about $2\sqrt r$ against about $1.25\sqrt r$ for rho with distinguished points, so rho is better unless $w$ is much smaller than $r$ (Galbraith, Section 14.5.4).

## When to use it

Use the kangaroo method when the exponent is known to lie in a short interval of a large group: short Diffie-Hellman exponents, partially leaked keys, small messages encoded as $g^m$, or the last step of a point count in the Hasse interval. It is also the natural finish after [Pohlig-Hellman](/pohlig-hellman/) has found $x$ modulo a smooth part of the order, leaving an unknown in an interval. If memory for $\sqrt w$ elements is available and a deterministic answer is wanted, [baby-step giant-step](/baby-step-giant-step/) on the interval is simpler. If $w$ is close to the group order, use [Pollard's rho](/pollard-rho-discrete-logarithm/).

## Pitfalls

- **Treating failure as NONE.** A kangaroo run that ends without a collision does not show that there is no solution. Returning NONE after line L14 is wrong; the right line is L15, which certifies the answer.
- **Jumps that are too large or too small.** A mean jump far from $\sqrt w / 2$ in line L2 increases the cost: with large jumps the kangaroos skip over each other's footprints, and with small jumps the rear kangaroo takes too long to catch up.
- **No bound on the walk.** Without $N_{\max}$ in line L6, an unsolvable instance or an unlucky walk runs forever, because the kangaroos never meet.
- **Wrong sign of the difference.** The answer is the tame distance minus the wild distance, as in line L10, whichever kangaroo reached the point first. Subtracting the earlier visitor's distance from the later one's gives the negative of the answer whenever the wild kangaroo arrived first.
- **Accepting any collision.** If $g$ has small order, a collision gives some $z$ with $g^z = h'$ that may lie outside $[0, w]$. Line L11 must check the range, not only the equation.
- **Forgetting the shift.** If line L1 omits $h \cdot g^{-a}$ and the tame kangaroo starts at $g^{\lfloor w/2 \rfloor}$, the kangaroos search $[0, w]$ instead of $[a, b]$.

## Implementations

## History

John Pollard proposed the kangaroo, or lambda, method in his 1978 paper on Monte Carlo methods for index computation, alongside the rho method; a tame kangaroo set a trap for a wild one. Van Oorschot and Wiener showed in 1999 how distinguished points make the method parallel with linear speedup and estimated the cost of repeating the original method. Pollard's 2000 paper "Kangaroos, Monopoly and discrete logarithms" analysed the serial and parallel versions, and Montenegro and Tetali later proved the $(2 + o(1))\sqrt w$ bound under idealized assumptions. Galbraith, Pollard and Ruprai found the three and four kangaroo variants while Galbraith was writing the chapter on these methods.

## References

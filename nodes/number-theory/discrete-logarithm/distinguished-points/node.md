---
tag: JF4YEQ
kind: technique
slug: distinguished-points
name: Distinguished points
aliases:
- distinguished point method
- distinguished point collision detection
area: number-theory/discrete-logarithm
level: advanced
summary: Walks of a pseudorandom map stop at points with an easily checked rare property, and only those endpoints are stored. Merging walks end at the same point, so collisions are found with little memory.
prereqs: [pollard-rho-discrete-logarithm, birthday-paradox, hash-table]
see_also: [parallel-collision-search, pollard-kangaroo, pollard-rho-collision-search, floyd-cycle-detection, brent-cycle-detection, hellman-time-memory-tradeoff, rainbow-table, meet-in-the-middle-attack]
sources:
  - paper: doi:10.1007/PL00003816
    title: Paul C. van Oorschot and Michael J. Wiener, Parallel collision search with cryptanalytic applications, Journal of Cryptology 12(1), 1999
    locator: pages 1 to 28 (the method, its analysis and its use for discrete logarithms, hash collisions and meet in the middle attacks)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 14, Section 14.2.4 (Definition 14.2.11, Example 14.2.12, Lemma 14.2.14, Heuristic 14.2.15, Theorem 14.2.16 and Exercises 14.2.17 to 14.2.22), Section 14.3 (distributed rho) and Section 14.6 (distributed kangaroos)
  - paper: doi:10.1007/s001450010010
    title: John M. Pollard, Kangaroos, Monopoly and discrete logarithms, Journal of Cryptology 13(4), 2000
    locator: pages 437 to 447 (distinguished points for parallel kangaroos)
---

The distinguished point method finds a collision of a pseudorandom map $f$ on a large set with little memory and in a form that runs in parallel. A point is distinguished if it has an easily checked rare property, such as a hash value ending in $k$ zero bits. Each walk $x, f(x), f(f(x)), \dots$ is followed until it reaches a distinguished point, and only that endpoint, with what is needed to rebuild the walk, is stored. Two walks that ever meet follow the same path afterwards and so end at the same distinguished point, which a [hash table](/hash-table/) lookup reveals. It turns [Pollard's rho](/pollard-rho-discrete-logarithm/) and [kangaroo](/pollard-kangaroo/) methods into the [parallel collision search](/parallel-collision-search/) of van Oorschot and Wiener.

## In plain words

Many hikers start at random places on a huge map and follow fixed rules for each step, so two hikers who ever stand on the same spot walk together from then on. Nobody writes down every spot. Instead, a few spots are marked with a flag, and a hiker who reaches a flag reports it to the base camp and goes home.

If two hikers ever crossed paths, they reach the same flag, and the base camp sees the same flag reported twice. Then it knows a crossing happened somewhere behind that flag, and can find it. Flags are rare enough that the camp keeps a short list, and common enough that the extra walking after a crossing is small.

## When it applies

- There is a deterministic map $f : S \to S$ on a finite set that behaves like a random map, and a collision $f(x) = f(y)$ with $x \ne y$, or two walks through a common point, solves the problem. In discrete logarithms, $S = \langle g \rangle$ and each point carries a label $(a, b)$ with $x = g^a h^b$.
- Membership in the distinguished set $D$ is cheap to test from a unique representation of the point, and $D$ is spread evenly over $S$, for example $D = \{x : H(x) \equiv 0 \pmod{2^k}\}$ for a hash $H$, with density $\theta \approx 2^{-k}$.
- A walk's start can be recorded, so that its path can be rebuilt, or the labels carry all the information needed, so that it never has to be.
- The cost of $f$ dominates, and storing about $\theta$ times the number of steps is affordable.

## The template

Let $\theta = |D| / |S|$. Start points come from a random source, and a walk longer than $L_{\max}$ (about $20/\theta$) is abandoned because it has probably entered a cycle without a distinguished point.

```pseudo id=main
DP-COLLISION-SEARCH(f, D, RANDOM-START, L_max)
L1  T ← empty hash table                 ▷ distinguished point ↦ (start, length)
L2  loop
L3      x₀ ← RANDOM-START() ; x ← x₀ ; ℓ ← 0
L4      while x ∉ D and ℓ < L_max do     ▷ follow the walk to a distinguished point
L5          x ← f(x) ; ℓ ← ℓ + 1
L6      if x ∉ D then continue           ▷ probably a cycle: discard the walk
L7      if x ∈ T and T[x].start ≠ x₀ then
L8          return LOCATE(T[x], (x₀, ℓ))   ▷ two walks ended at the same point
L9      T[x] ← (x₀, ℓ)
LOCATE((y₀, ℓ₁), (z₀, ℓ₂))               ▷ assume ℓ₁ ≥ ℓ₂, else swap
L10 advance y₀ by ℓ₁ − ℓ₂ steps of f
L11 while f(y₀) ≠ f(z₀) do
L12     y₀ ← f(y₀) ; z₀ ← f(z₀)
L13 if y₀ = z₀ then return FAILURE       ▷ one walk started on the other: a "Robin Hood"
L14 return (y₀, z₀)                      ▷ a collision f(y₀) = f(z₀) with y₀ ≠ z₀
```

**Why it works.** Since $f$ is deterministic, two walks that contain a common point agree from then on, so if either reaches a distinguished point, both reach the same one; line L7 detects it. Line L10 puts both walks at the same distance from the common endpoint, and lines L11 and L12 step them together until the next step would merge them, so the returned pair is a collision unless the two walks were the same walk from the start, which line L13 reports.

**Discrete logarithms.** For rho, each point carries labels $(a, b)$ with $x = g^a h^b$, and the table stores the labels of the endpoint instead of the start. Two walks ending at the same point $g^a h^b = g^A h^B$ give $(b - B) x \equiv A - a \pmod r$ directly, so LOCATE is not needed. If $b \equiv B$, the collision is useless, and the search goes on.

**Cost.** Under the random map heuristic, about $\sqrt{\pi |S| / 2}$ points are visited before the first collision, and detecting it costs about $2/\theta$ more steps on average, since each of the two walks needs an expected $1/\theta$ steps to reach $D$ (Galbraith, Lemma 14.2.14). For a group of prime order $r$, rho with distinguished points takes $(\sqrt{\pi/2} + o(1))\sqrt r \approx 1.253 \sqrt r$ group operations when $\theta \gg 1/\sqrt r$, heuristically (Galbraith, Theorem 14.2.16). The table holds about $\theta \sqrt{\pi |S| / 2}$ entries; with $\theta = \log r / \sqrt r$ that is $O(\log r)$ entries (Galbraith, Exercise 14.2.17). Abandoned walks waste a fraction of about $e^{-\theta L_{\max}}$ of the steps.

**Example.** Take HAC's subgroup of order $r = 191$ generated by $g = 2$ in $(\mathbb{Z}/383\mathbb{Z})^*$, $h = 228$, the three-set walk of Pollard (multiply by $h$, square, or multiply by $g$ according to $x \bmod 3$), and let $D$ be the residues divisible by $8$. Walks start at $g^{a_0} h^{b_0}$:

| start $(a_0, b_0)$ | walk | length | endpoint and labels |
|---|---|---|---|
| $(1, 0)$ | $2, 4, 146, 292, 317, 251, 119, 238, 261, 330, 128$ | 10 | $128$, $(24, 12)$ |
| $(5, 1)$ | $19, 119, 238, 261, 330, 128$ | 5 | $128$, $(24, 12)$ |
| $(10, 3)$ | $346, 373, 18, 324, 34, 92, 184$ | 6 | $184$, $(41, 21)$ |
| $(17, 2)$ | $248$ | 0 | $248$, $(17, 2)$ |
| $(30, 5)$ | $128$ | 0 | $128$, $(30, 5)$ |

The second walk merges with the first at $119$ and also reaches $128$, but with the same labels, so $b - B = 0$ and the collision is useless. The fifth start is itself $128$, with labels $(30, 5)$. Now $2^{24} \cdot 228^{12} = 2^{30} \cdot 228^{5}$ gives $(12 - 5) x \equiv 30 - 24 \pmod{191}$, so $x \equiv 6 \cdot 7^{-1} \equiv 110$, the answer of HAC's Example 3.61, after $21$ steps and with a table of three points.

## Classic examples

- **Rho with distinguished points.** The standard serial form of [Pollard's rho](/pollard-rho-discrete-logarithm/): many short walks from random starts $g^{a_0} h^{b_0}$, about $1.253 \sqrt r$ operations instead of about $3.09 \sqrt r$ with Floyd's method (Galbraith, Sections 14.2.2 and 14.2.4).
- **Parallel collision search.** $N$ processors run walks independently and send distinguished points to one server, which gives a linear speedup, $\sqrt{\pi r / 2} / N + 2/\theta$ steps per processor ([parallel collision search](/parallel-collision-search/)). All elliptic curve discrete logarithm records used it.
- **Parallel kangaroos.** Herds of tame and wild [kangaroos](/pollard-kangaroo/) report distinguished points, and a tame and a wild kangaroo at the same point solve the interval problem (van Oorschot and Wiener; Pollard 2000).
- **Hash collisions and meet in the middle.** Van Oorschot and Wiener applied the method to find collisions of hash functions and to run meet in the middle attacks, such as on double DES, with little memory per processor.
- **Time-memory tradeoffs.** In [Hellman's tradeoff](/hellman-time-memory-tradeoff/), chains end at distinguished points, which reduces table lookups during the online phase; Galbraith attributes this use of the idea to Rivest.

## Variations

- **Labels or restarts.** Store the labels of the endpoint (discrete logarithms, where the collision is solved from them) or the start and length (generic collisions, where LOCATE rebuilds the paths).
- **Choosing $\theta$.** Larger $\theta$ means more storage and less overhead after the collision; smaller $\theta$ the opposite. Van Oorschot and Wiener choose $\theta$ so that the table fits in memory and $1/\theta$ is small next to the work per processor.
- **Many targets.** Distinguished points from earlier logarithms to the same base can be kept and rewritten as pure powers of $g$ once their discrete logarithm is known, so that $L$ logarithms cost about $\sqrt{2 r L}$ in total (Kuhn and Struik, Galbraith Exercise 14.2.22); the walk must not depend on the targets.
- **Negation and Frobenius classes.** On elliptic curves, the walk runs on classes $\{\pm P\}$, which saves a factor $\sqrt 2$ but creates short fruitless cycles; walks that exceed $L_{\max}$ or revisit a point must escape them.
- **Several herds.** For kangaroos and the Gaudry-Schost method, each stored point carries the herd it came from, and only collisions between different herds count.

## Pitfalls

- **Walks trapped in cycles.** A walk that enters a cycle with no distinguished point never ends. The bound $L_{\max}$ of line L4 is required, and line L6 must discard the walk; omitting it hangs a processor forever.
- **A bad distinguishing property.** If $D$ is defined by a few bits of the raw representation, and the walk correlates with those bits, walks may avoid $D$ or crowd into part of it. Use a hash of a unique representation, as in Galbraith's Example 14.2.12.
- **Useless collisions.** In the discrete logarithm form, two walks from related starts can reach the same point with the same labels, as in the example above. The test $b \ne B$ must precede the division, and the search must continue when it fails.
- **Same walk counted twice.** If a start is reused, or if line L7 does not check that the two walks are different, the method reports a "collision" of a walk with itself. LOCATE's line L13 catches the case where one start lies on the other walk.
- **Non-unique representations.** Projective coordinates or unreduced residues make equal points look different, so merged walks are not detected. Normalize every point before the test of line L4.

## Exercises

1. Show that the expected number of steps for a walk to reach $D$ is $1/\theta$ when the points are independent and uniform, and that this stays $1/\theta$ after any number of non-distinguished steps (Galbraith, Lemma 14.2.14).
2. With $\theta = \log r / \sqrt r$, show that the expected table size is $O(\log r)$ points for a rho search of $O(\sqrt r)$ steps.
3. Explain why taking $D = S$, so that every point is distinguished, gives an algorithm much slower than [baby-step giant-step](/baby-step-giant-step/) (Galbraith, Exercise 14.2.21).
4. Prove that LOCATE returns a true collision $f(y_0) = f(z_0)$ with $y_0 \ne z_0$ whenever neither start lies on the other walk.
5. For $N$ processors and a server, compute the expected number of steps per processor and the number of messages sent to the server, as functions of $r$, $N$ and $\theta$.

## References

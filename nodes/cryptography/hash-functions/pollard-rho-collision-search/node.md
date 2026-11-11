---
tag: YJ25N1
kind: algorithm
slug: pollard-rho-collision-search
name: Pollard rho collision search
aliases:
- Floyd cycle collision search
area: cryptography/hash-functions
level: advanced
summary: Find a hash collision with almost no memory by walking x, H(x), H(H(x)), and so on until the walk cycles. It costs about 2^(n/2) steps; distinguished points make it run on many machines.
solves: [collision-finding]
model: query-model
complexity:
  vars: {n: the digest length in bits, N: the number of values 2^n, m: the number of parallel machines, θ: the fraction of distinguished points}
  time: {worst: O(2^n), average: Θ(2^(n/2))}
  space: {extra: O(1)}
properties: {deterministic: true}
history:
  year: 1975
  people: [John M. Pollard, Robert W. Floyd, Paul C. van Oorschot, Michael J. Wiener]
  note: Pollard used cycle finding on a random-looking map to factor integers in 1975. Van Oorschot and Wiener made the method parallel with distinguished points in 1994, and published the full analysis in 1999.
prereqs: [birthday-attack, floyd-cycle-detection]
see_also: [birthday-attack, collision-finding, brent-cycle-detection, cycle-detection, distinguished-points, pollard-rho, pollard-rho-discrete-logarithm, meet-in-the-middle-attack]
sources:
  - paper: doi:10.1007/PL00003816
    title: Paul C. van Oorschot and Michael J. Wiener, Parallel collision search with cryptanalytic applications, Journal of Cryptology 12(1), 1999, pages 1 to 28
    locator: Section 4 (parallel collision search with distinguished points and its expected run time) and Section 5 (applications to hash functions)
  - paper: "John M. Pollard, A Monte Carlo method for factorization, BIT Numerical Mathematics 15(3), 1975, pages 331 to 334"
    locator: the walk x, f(x), f(f(x)) and the use of Floyd's cycle test
  - paper: "Richard P. Brent, An improved Monte Carlo factorization algorithm, BIT Numerical Mathematics 20(2), 1980, pages 176 to 184"
    locator: the cycle finding method with power-of-two checkpoints
  - paper: "Jean-Jacques Quisquater and Jean-Paul Delescaille, How easy is collision search? Application to DES, EUROCRYPT 1989, LNCS 434, pages 429 to 434"
    locator: distinguished points used to find collisions of DES as a function of the key
  - paper: "Philippe Flajolet and Andrew M. Odlyzko, Random mapping statistics, EUROCRYPT 1989, LNCS 434, pages 329 to 354"
    locator: the expected tail, cycle and rho lengths of a random mapping
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 2.1.6 (random mappings, with the expected tail length and cycle length sqrt(πn/8)) and Section 9.7.1 (memoryless collision search)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition, Addison-Wesley, 1997
    locator: Section 3.1, exercises 6 and 7 (Floyd's cycle finding method and Brent's variant)
---

Pollard rho collision search finds a collision of a hash function $H$ with $n$-bit output while it stores only a few values. It walks the sequence $x_0, H(x_0), H(H(x_0)), \ldots$. Since there are only $2^n$ values, the walk repeats, and it then runs in a cycle. The point where the tail of the walk joins the cycle has two different predecessors, one on the tail and one on the cycle, and these two inputs collide. The method costs about $2^{n/2}$ steps, like the [birthday attack](/birthday-attack/), but uses $O(1)$ memory in place of $2^{n/2}$. With [distinguished points](/distinguished-points/), van Oorschot and Wiener run it on $m$ machines with a speedup of $m$.

## In plain words

Pick a starting value and hash it. Hash the result, then hash that result, and go on. You are hopping around a finite set, so sooner or later you land on a value you have visited before. From then on you go round the same loop for ever. Drawn on paper, the path looks like the Greek letter rho: a tail that leads into a circle.

Where the tail meets the circle, two different values hash to the same next value: the last value of the tail and the last value of the circle. That is the collision.

You do not need to remember the path. Send two walkers, one twice as fast as the other. The fast one catches up with the slow one inside the loop. Then a second pass finds the meeting point.

## The problem

The input is a function $f : S \to S$ on a finite set $S$ of size $N$, and a start $x_0 \in S$. For a hash with $n$-bit output, take $S = \{0,1\}^n$ and $f(x) = H(g(x))$, where $g$ maps an $n$-bit string to a message, for example its encoding as bytes. A collision of $f$ with $g$ injective is a collision of $H$. The output is a pair $a \ne b$ with $f(a) = f(b)$. The cost is the number of calls of $f$ in the [query model](/query-model/).

Write $x_i = f^i(x_0)$. Let $\mu \ge 0$ be the *tail length*, the least index whose value comes again, and $\lambda \ge 1$ the *cycle length*, the least period: $x_{\mu + \lambda} = x_\mu$. The *rho length* is $\rho = \mu + \lambda$, the number of distinct values on the walk. If $\mu \ge 1$, then $x_{\mu-1} \ne x_{\mu+\lambda-1}$ and $f$ maps both to $x_\mu$. If $\mu = 0$, the start is on the cycle and the walk gives no collision.

## The algorithm

RHO-COLLISION uses [Floyd's cycle detection](/floyd-cycle-detection/) to get a point on the cycle, then walks from the start and from that point in step to the join.

```pseudo id=main
RHO-COLLISION(f, x0)
L1  t ← f(x0); h ← f(f(x0))
L2  while t ≠ h do                      ▷ phase 1: h moves twice as fast as t
L3      t ← f(t); h ← f(f(h))
L4  t ← x0                              ▷ now h = x_i with λ | i and i ≥ μ
L5  if t = h then return FAIL           ▷ μ = 0: x0 is on the cycle
L6  while f(t) ≠ f(h) do                ▷ phase 2: t = x_j, h = x_(i+j)
L7      t ← f(t); h ← f(h)
L8  return (t, h)                       ▷ t = x_(μ−1) on the tail, h on the cycle
```

On FAIL, restart from another random $x_0$. This happens with probability about $\sqrt{\pi/2N}$, the expected fraction of points that lie on a cycle of a random map. Over 20000 random maps on $2^{10}$ points with the seed 8, the rate was 0.0385, against 0.0392 from the formula.

**Parallel form with distinguished points.** Call a point *distinguished* if, for example, its low $d$ bits are zero, a fraction $\theta = 2^{-d}$ of all points. Each machine starts a walk at a random point and steps until it reaches a distinguished point. It sends the triple (start, distinguished point, length) to a central table and starts a new walk. When two walks from different starts end at the same distinguished point, they have merged. Replay both from their starts, with the longer one first moved ahead by the difference in length, and step them together until their next values are equal. The two current points are a collision. A walk that runs much longer than $1/\theta$ steps is probably in a cycle with no distinguished point, and is dropped.

The Python code for this page runs Floyd's method and Brent's method on SHA-256 truncated to 24, 28 and 32 bits, and the distinguished point form at 28 bits. It is for study only and it is not constant time. Do not use it against real systems. For real hashing use hashlib, a FIPS 140 validated module, or libsodium.

## Example

Let $f(x)$ be the first 24 bits of SHA-256 of $x$ written in 4 bytes, so $N = 2^{24}$, and start at $x_0 = 0$.

- Brent's method gives the tail length $\mu = 2188$ and the cycle length $\lambda = 312$, so $\rho = 2500$. The mean of $\rho$ over random maps is $\sqrt{\pi N/2} \approx 5134$.
- RHO-COLLISION returns $a$ = 0x26d7b6 and $b$ = 0xda48a8. Both map to 0x51a803. So SHA-256 of the 4-byte strings 00 26 d7 b6 and 00 da 48 a8 agrees on its first 3 bytes.
- The run made 11864 calls of $f$ and stored two values. The birthday attack on the same function stores about 5000 digests.

At 32 bits, from $x_0 = 0$, the walk has $\mu = 80895$ and $\lambda = 13887$. RHO-COLLISION returns the pair 0xe638f884 and 0x402ac96a, both mapped to 0x5d10bb55, after 411756 calls.

With distinguished points at 28 bits, $d = 6$ and the seed 5, the search finds the pair 0x58fb857 and 0x9b94638 after 45804 calls. It stores 729 distinguished points, against about $1.25 \cdot 2^{14} \approx 20500$ entries for the table of the birthday attack.

**Simulation.** Over 2000 random maps on $N = 2^{16}$ values with the seed 7, the mean tail length is $0.611\sqrt N$, the mean cycle length $0.644\sqrt N$ and the mean rho length $1.255\sqrt N$. Theory gives $(\rho - 1)/2$, $(\rho + 1)/2$ and $\sqrt{\pi/2} \approx 1.2533$ in units of $\sqrt N$. Floyd's method made $4.31\sqrt N$ calls on average.

## Correctness

After phase 1, $t = x_i$ and $h = x_{2i}$, where $i$ is the least $i \ge 1$ with $x_i = x_{2i}$. Two points of the walk with indices $a < b$ are equal exactly when $a \ge \mu$ and $\lambda \mid b - a$. So $i$ is the least multiple of $\lambda$ with $i \ge \max(\mu, 1)$. In phase 2, after $j$ steps, $t = x_j$ and $h = x_{i+j}$. These are equal exactly when $j \ge \mu$. So the first $j$ with $f(t) = f(h)$ is $j = \mu - 1$, and then $t = x_{\mu - 1}$ is a tail point, $h = x_{i + \mu - 1}$ is on the cycle, and they differ. The full proof is below.

## Complexity

For a random map $f$ on $N$ points and a random start, the rho length has $\Pr[\rho > k] = \prod_{i=1}^{k-1}(1 - i/N)$, exactly as the first repeat of the [birthday attack](/birthday-attack/). Given $\rho$, the cycle length $\lambda$ is uniform on $1, \ldots, \rho$. So

$$\mathbb{E}[\rho] = Q(N) = \sum_{k=1}^{N} \frac{N!}{(N-k)!\,N^k} \sim \sqrt{\pi N/2}, \qquad \mathbb{E}[\lambda] = \frac{Q(N) + 1}{2}, \qquad \mathbb{E}[\mu] = \frac{Q(N) - 1}{2}.$$

Both $\mathbb{E}[\mu]$ and $\mathbb{E}[\lambda]$ are about $\sqrt{\pi N/8} \approx 0.627\sqrt N$ (HAC Section 2.1.6, Flajolet and Odlyzko).

- **Floyd calls.** Phase 1 runs $i \le \rho$ rounds of 3 calls. Phase 2 runs $\mu$ rounds of 2 calls, plus 2 calls for the first test. So at most $3\rho + 2\mu + 2$ calls, about $4.3\sqrt N$ on average in the simulation above.
- **Brent calls.** Brent's method finds $\lambda$ with one call per step and power-of-two checkpoints, in $O(\rho)$ calls. A second pass of about $\lambda + 2\mu$ calls finds the join. It uses fewer calls than Floyd, with the same order.
- **Space.** $O(1)$: two or three points.
- **Parallel form.** With $m$ machines and a fraction $\theta$ of distinguished points, van Oorschot and Wiener give an expected time of about $\left(\sqrt{\pi N/2}/m + 2.5/\theta\right)$ steps per machine. The table holds about $\theta \sqrt{\pi N/2}$ points. The first term is the birthday cost shared over the machines. The second is the walk to the next distinguished point after the collision, plus the replay.

## Properties

- **Memoryless.** The memory does not grow with $N$. This is the main gain over the [birthday attack](/birthday-attack/), whose $2^{n/2}$ table is the real limit for $n \ge 80$.
- **Deterministic walk.** Given $f$ and $x_0$, the output is fixed. To get another collision, change $x_0$ or change $g$.
- **Only one kind of collision.** The walk finds the collision at the join of its own tail. It cannot target a collision between two fixed sets of messages unless $g$ mixes them; see below.
- **Needs $f : S \to S$.** The output of $H$ must be fed back as an input. The map $g$ from digests to messages does this.
- **Linear speedup.** The parallel form gains a factor $m$ with $m$ machines and needs no communication beyond the distinguished points.

## Variants and improvements

- **[Brent's cycle detection](/brent-cycle-detection/).** One walker, and a saved point that moves to the walker at each power of two. It needs fewer calls of $f$ than Floyd. See [cycle detection](/cycle-detection/) for the general problem and other methods, such as Nivasch's stack method.
- **Meaningful collisions.** Let one bit of $x$ choose between a fair and a fraudulent family of messages, and the other bits choose the variant. Each collision found is between the two families with probability about 1/2. Repeat with a new $g$ until it is. This is the memoryless form of Yuval's attack.
- **[Meet in the middle](/meet-in-the-middle-attack/) with no memory.** A collision between $f_1$ and $f_2$ is found by walking $f(x) = f_1(x)$ or $f_2(x)$, chosen by one bit of $x$. Van Oorschot and Wiener apply this to double encryption.
- **Many collisions.** With distinguished points the table keeps its walks, so the search can go on and find many collisions from one table. Van Oorschot and Wiener use this for meet in the middle attacks, where only one special collision among many is useful.
- **Discrete logarithms and factoring.** The same walk solves other problems: [Pollard rho for factoring](/pollard-rho/) and [for discrete logarithms](/pollard-rho-discrete-logarithm/).

## When to use it

Use it in place of the birthday attack when $2^{n/2}$ digests do not fit in memory. A single machine with Floyd or Brent suits $n$ up to about 64. For larger targets use the parallel form, which also gives a whole family of collisions from one run. In a security estimate, count the generic collision cost of an $n$-bit hash as $2^{n/2}$ calls with negligible memory. The memory of the birthday table is not a defense.

## Pitfalls

- **Start on the cycle.** If $\mu = 0$, the walk has no tail and phase 2 gives no collision. Line L5 tests for this. Without the test, the code returns the pair $(x_0, x_0)$.
- **The map must be fixed.** The walk relies on $f$ being a function. A random choice inside $f$, or state that changes between calls, breaks the cycle argument.
- **Long cycles with no distinguished point.** In the parallel form a walk can enter a cycle with no distinguished point. Bound the walk length, about $20/\theta$, and restart it.
- **Robin Hood merges.** A walk that starts on another walk's path ends at the same distinguished point but gives no collision. The replay detects this when the two aligned walks are already equal, and the search must go on.
- **Collisions of $g$.** If $g$ is not injective, a collision of $f$ may be a collision of $g$ only. Use an injective encoding.

## Implementations

## History

Pollard introduced the walk on a random-looking map for factoring in 1975, and for discrete logarithms in 1978. He used Floyd's cycle finding idea, which Knuth credits to Floyd. Brent gave a faster cycle finder in 1980. Quisquater and Delescaille used distinguished points in 1989 to find collisions of DES as a function of its key. Van Oorschot and Wiener gave the general parallel collision search with distinguished points at ACM CCS 1994, with its expected run time, and the journal version in 1999. They estimated that a machine of about 10 million US dollars could find an MD5 collision by this generic method in about 24 days. Wang and her coauthors found MD5 collisions by differential methods in 2004, far faster.

## References

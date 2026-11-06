---
tag: M0GDZC
kind: algorithm
slug: parallel-collision-search
name: Parallel collision search
aliases:
- van Oorschot-Wiener parallel collision search
- parallel rho
- distributed Pollard rho
area: number-theory/discrete-logarithm
level: advanced
summary: Parallelizes Pollard's rho across many processors with linear speedup and low communication. Clients walk until a distinguished point and report it; a repeated report solves the discrete logarithm.
solves: [discrete-logarithm-problem]
model: generic-group-model
complexity:
  vars:
    n: the order of g, usually a prime r after Pohlig-Hellman
    N: the number of client processors; time and bit operations are per client, and space is the server table
    d: the mean distance between distinguished points, 1 over their density theta
    k: the number of binary digits of the modulus p, when the group is a subgroup of (Z/pZ)^*
  time:
    heuristic: O(n^(1/2)/N + d)
  space:
    heuristic: O(n^(1/2)/d + N)
  bit_operations:
    heuristic: O((n^(1/2)/N + d) k^2)
properties:
  deterministic: false
  recursive: false
prereqs: [distinguished-points, pollard-rho-discrete-logarithm]
see_also: [pollard-kangaroo, pollard-rho-collision-search, elliptic-curve-discrete-logarithm-problem, birthday-paradox, hash-table, meet-in-the-middle-attack, pohlig-hellman, baby-step-giant-step]
sources:
  - paper: doi:10.1007/PL00003816
    title: Paul C. van Oorschot and Michael J. Wiener, Parallel collision search with cryptanalytic applications, Journal of Cryptology 12(1), 1999
    locator: pages 1 to 28 (the parallel collision search method, its run time analysis, and its use for discrete logarithms and hash collisions)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 14, Section 14.3 (Algorithms 17 and 18 for server and clients, Heuristic 14.3.1, Theorem 14.3.2 and Exercise 14.3.3) and Section 14.2.4 (distinguished points)
  - paper: doi:10.1007/bfb0054891
    title: Edlyn Teske, Speeding up Pollard's rho method for computing discrete logarithms, ANTS-III, Lecture Notes in Computer Science 1423, 1998
    locator: pages 541 to 554 (r-adding walks, used here as the client walk)
  - paper: doi:10.1504/ijact.2012.045590
    title: Joppe W. Bos, Marcelo E. Kaihara, Thorsten Kleinjung, Arjen K. Lenstra and Peter L. Montgomery, Solving a 112-bit prime elliptic curve discrete logarithm problem on game consoles using sliding FFT, International Journal of Applied Cryptography 2(3), 2012
    locator: the main result (a parallel rho computation with distinguished points on the curve secp112r1)
---

Parallel collision search, due to van Oorschot and Wiener, runs [Pollard's rho method](/pollard-rho-discrete-logarithm/) on many processors at once with a linear speedup. Each client walks the same pseudorandom map from its own random start $g^a h^b$ until it reaches a [distinguished point](/distinguished-points/), sends that point and its exponents to a server, and starts again. Two walks that ever meet end at the same distinguished point, so the server sees that point twice and solves a linear congruence for $\log_g h$. With $N$ clients, each does about $\sqrt{\pi n / 2} / N$ group operations, heuristically, and the server stores only a small fraction of all points visited.

## In plain words

Many searchers each follow a trail of fixed rules from a random starting spot, writing down how they got there. Some spots carry a flag. A searcher who reaches a flag phones the base with the flag's name and the notes, then starts again somewhere new.

Two searchers who step on the same spot follow the same trail from then on, so they reach the same flag. When the base hears about one flag twice, the two sets of notes describe the same spot in two ways, and comparing them reveals the secret. The searchers never talk to each other, and the base only keeps the short list of flags it has heard about.

## The problem

**Input.** A prime $p$, an element $g$ of $(\mathbb{Z}/p\mathbb{Z})^*$ of known order $n$, an element $h$, and a number $N \ge 1$ of clients. The method works the same way in any cyclic group with a unique representation of elements, and its main use is on elliptic curves.

**Output.** The $x \in \{0, \dots, n - 1\}$ with $g^x = h$, or NONE if $h \notin \langle g \rangle$.

**Cost model.** The group is the cyclic subgroup $\langle g \rangle$ of order $n$, usually a prime $r$ after [Pohlig-Hellman](/pohlig-hellman/). One walk step is one group operation, a multiplication modulo $p$ costing $O(k^2)$ bit operations for a $k$-bit $p$; a restart costs $O(\log n)$ group operations. The measure is the number of group operations per client, with all clients equally fast and communication free and reliable. The server's work is one [hash table](/hash-table/) lookup per report. The bound $\sqrt{\pi n / 2} / N + 1/\theta$ per client is heuristic, under the assumption that the walk behaves like a random map and that walks rarely cycle before a distinguished point (Galbraith, Heuristic 14.3.1 and Theorem 14.3.2); no rigorous analysis is known. The lower bound $\Omega(\sqrt r)$ on the total work is proved in the [generic group model](/generic-group-model/).

## The algorithm

The walk is Teske's $r$-adding walk: pick exponent pairs $(u_j, v_j)$ for $0 \le j < r$, put $M_j = g^{u_j} h^{v_j}$, and step from $x$ to $x M_j$ with $j = S(x)$ chosen by a hash of $x$. Every point carries a label $(a, b)$ with $x = g^a h^b$. The distinguished set $D$ is defined by the same hash, for example $D = \{x : H(x) \equiv 0 \pmod{1/\theta}\}$. A client whose walk reaches length $L_{\max}$ without a distinguished point is probably in a cycle and starts again. An epoch with a fixed walk lasts at most $B$ rounds, after which a new walk is drawn.

```pseudo id=main
PARALLEL-COLLISION-SEARCH(g, h, n, N)  ▷ ⟨g⟩ cyclic of order n, N clients; returns x with g^x = h, or NONE
L1  if h^n ≠ 1 then return NONE
L2  if h = 1 then return 0
L3  loop                                ▷ one epoch per random walk
L4      choose random (u_j, v_j), M_j ← g^u_j · h^v_j for 0 ≤ j < r, and a random distinguished set D of density θ
L5      T ← empty table on the server
L6      for i ← 1 to N do start client i at x_i = g^a_i · h^b_i with random a_i, b_i, and ℓ_i ← 0
L7      repeat B times
L8          for i ← 1 to N do            ▷ simultaneous on real machines
L9              if x_i ∈ D then           ▷ client i sends (x_i, a_i, b_i) to the server
L10                 if T holds (x_i, a', b') then
L11                     ▷ g^a_i h^b_i = g^a' h^b', so (b_i − b') x ≡ a' − a_i (mod n)
L12                     s ← (b_i − b') mod n ; d ← gcd(s, n) ; if s = 0 or d > ⌊√n⌋ + 1 then skip to L17
L13                     y ← ((a' − a_i)/d) · (s/d)^(−1) mod (n/d)
L14                     for t ← 0 to d − 1 do
L15                         if g^(y + t n/d) = h then return y + t n/d   ▷ and stop all clients
L16                 else T[x_i] ← (a_i, b_i)
L17             if x_i ∈ D or ℓ_i ≥ L_max then restart client i at a random g^a_i · h^b_i with ℓ_i ← 0
L18             else j ← S(x_i) ; (x_i, a_i, b_i) ← (x_i · M_j, a_i + u_j, b_i + v_j) ; ℓ_i ← ℓ_i + 1
```

Lines L1 and L2 handle membership and the trivial target as in [rho](/pollard-rho-discrete-logarithm/): $\langle g \rangle$ is the unique subgroup of order $n$ of the cyclic group $(\mathbb{Z}/p\mathbb{Z})^*$. Line L4 draws a walk and line L6 starts the clients at independent uniform labels. In each round, line L9 tests the current point of each client. A distinguished point is looked up at line L10; if the server already holds it, lines L12 to L15 solve the congruence exactly as in the serial method, testing the $d = \gcd(s, n)$ candidates, and if not, line L16 stores it. After a report, or when a walk is too long, line L17 restarts the client from a fresh random point, and otherwise line L18 makes one step, keeping $x_i = g^{a_i} h^{b_i}$. A collision that gives no answer leaves the table as it was and the search goes on; line L3 draws a new walk if $B$ rounds pass without an answer. The implementation simulates the $N$ clients in round robin, with $r = 16$, $1/\theta = \max(1, \lfloor \sqrt n \rfloor / (8N))$, $L_{\max} = 20/\theta$ and $B = 8(\lfloor \sqrt n \rfloor / N + 1/\theta) + 16$, and decides $x \in D$ and $S(x)$ from $x \cdot \kappa \bmod p$ for a random key $\kappa$.

## Example

Take $p = 383$, $g = 2$ of prime order $n = 191$ and $h = 228$, the group of HAC's Example 3.61, with $N = 2$ clients. Use $r = 4$ multipliers chosen by $S(x) = x \bmod 4$:

| $j$ | $(u_j, v_j)$ | $M_j = g^{u_j} h^{v_j}$ |
|---|---|---|
| 0 | $(1, 0)$ | 2 |
| 1 | $(1, 4)$ | 184 |
| 2 | $(4, 1)$ | 201 |
| 3 | $(2, 3)$ | 136 |

Let $D$ be the residues divisible by $8$, so $\theta \approx 1/8$, and let the starting labels be drawn in the order $(1, 0)$, $(0, 1)$, $(2, 3)$, $(5, 2)$. Client 1 starts at $g = 2$ and client 2 at $h = 228$. The table shows each client's point and label at the start of each round, and what the server does in that round.

| round | client 1 | client 2 | server |
|---|---|---|---|
| 1 | 2, (1, 0) | 228, (0, 1) | |
| 2 | 19, (5, 1) | 73, (1, 1) | |
| 3 | 286, (7, 4) | 27, (2, 5) | |
| 4 | 36, (11, 5) | 225, (4, 8) | |
| 5 | 72, (12, 5), reported | 36, (5, 12) | stores 72 with (12, 5) |
| 6 | 136, (2, 3), reported | 72, (6, 12), reported | stores 136; finds 72 again |

The walks meet at $36$: client 1 is there in round 4 and client 2 arrives one round later, with a different label. Both then step by $M_0$ to $72$, which is distinguished. Client 1 reports it in round 5 and restarts at $g^2 h^3 = 136$, which is itself distinguished and is reported in round 6. In the same round client 2 reports $72$ with $(6, 12)$, and the server has $g^{12} h^5 = g^6 h^{12}$. Line L12 gives $s = 12 - 5 = 7$ and $d = 1$, and line L13 gives $y = (12 - 6) \cdot 7^{-1} \equiv 6 \cdot 82 \equiv 110 \pmod{191}$. Indeed $2^{110} \equiv 228 \pmod{383}$. The search used $9$ walk steps and stored two points.

## Correctness

Every client keeps $x_i = g^{a_i} h^{b_i}$: line L6 and line L17 set $x_i$ from its label, and line L18 multiplies by $M_j = g^{u_j} h^{v_j}$ while adding $(u_j, v_j)$. So every table entry and every report satisfies the same relation, and a match at line L10 gives $g^{a_i - a'} = h^{b' - b_i}$. If $h = g^{x^*}$, then $s x^* \equiv a' - a_i \pmod n$, and when $s \ne 0$ the solutions are the $d$ values $y + t n/d$ of lines L13 and L14, one of which is $x^*$. Line L15 checks each value before returning, so any answer is correct, and since $n$ is the order of $g$ it is the unique solution in $[0, n)$. If $h \notin \langle g \rangle$, line L1 returns NONE. For termination, each epoch has a positive probability of success that does not depend on earlier epochs, for example when client 1's first start is distinguished and its second start is the same point with $b$ larger by one; so the algorithm stops with probability $1$, although the number of epochs is not bounded in the worst case. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Group operations per client, heuristic.** Under Heuristic 14.3.1 the clients together sample about $\sqrt{\pi n / 2}$ points before some point is visited twice, so each does about $\sqrt{\pi n / 2} / N$ steps. The collision is noticed only when the second walk reaches the next distinguished point, about $1/\theta$ further steps. Galbraith's Theorem 14.3.2 gives $(1 + 2 \theta \log n)\sqrt{\pi n / 2} / N + 1/\theta$ group operations per client, counting the restarts, which is $(\sqrt{\pi / 2} / N + o(1))\sqrt n$ when $\theta < 1/\log^2 n$.
- **Useless collisions.** Because each start has uniform random labels, the label $b$ at a collision is uniform among the $n$ labels of that point, and the probability that $s = 0$ is $1/n$. For prime $n$ the expected number of collisions needed is $1 + o(1)$.
- **Speedup.** The total work is about $\sqrt{\pi n / 2} + N/\theta$, against about $3.09\sqrt n$ for serial rho with Floyd's method, so the speedup is linear in $N$ while $N/\theta$ stays small. Running $N$ independent copies of serial rho would give only a $\sqrt N$ speedup.
- **Space.** Each client stores one point and its label. The server stores about $\theta\sqrt{\pi n / 2} + N$ triples (Theorem 14.3.2). In practice the storage is fixed first and $\theta$ chosen to fit it.
- **Communication.** About $\theta$ messages per client step, each of $O(\log p)$ size.
- **Bit operations.** $O((\sqrt n / N + 1/\theta) k^2)$ per client in a subgroup of $(\mathbb{Z}/p\mathbb{Z})^*$ with $k$-bit $p$, heuristic.

## Properties

- **Randomized, Las Vegas.** Every answer is checked at line L15, so it is always right; only the running time is random.
- **Generic.** The clients use only the group law, equality and a hash of a unique representation, so the method runs on elliptic curves, Jacobians and class groups.
- **Embarrassingly parallel.** Clients share nothing but the walk and send rare short messages; clients may join, leave or crash without harm to correctness, and a lost report only delays the answer.
- **Linear speedup.** Unlike independent serial runs, the walks of all clients feed one birthday collision.
- **Incremental.** Work is never wasted within an epoch: a distinguished point stored early can match a report much later.

## Variants and improvements

- **Kangaroos in parallel.** For an exponent in an interval of width $w$, van Oorschot and Wiener run herds of tame and wild [kangaroos](/pollard-kangaroo/) with distinguished points, about $2\sqrt w / N$ operations per client, heuristic; Pollard's 2000 paper gives a variant without useless collisions between kangaroos of the same kind.
- **Equivalence classes.** On elliptic curves the walk is defined on classes $\{P, -P\}$, which saves a factor $\sqrt 2$, and Frobenius classes on Koblitz curves save more; fruitless cycles must be detected, which distinguished points with $L_{\max}$ help with (Galbraith, Section 14.4).
- **General collisions.** The same method finds collisions of any function, such as a hash function, and runs [meet in the middle attacks](/meet-in-the-middle-attack/) with little memory. There the labels do not solve the problem, and the colliding walks are retraced from their recorded starts, which costs a few more multiples of $1/\theta$ (van Oorschot and Wiener). This is [Pollard rho collision search](/pollard-rho-collision-search/) in parallel.
- **Many logarithms.** Kuhn and Struik keep the server's table across several targets, with a walk whose multipliers are powers of $g$ alone so that old distinguished points stay valid; solving $L$ logarithms then costs about $\sqrt{2 L n}$ group operations in total instead of $L\sqrt n$, heuristic.

## When to use it

Use it for any large generic discrete logarithm, which in practice means elliptic curves with a large prime order subgroup, once [Pohlig-Hellman](/pohlig-hellman/) has reduced to prime order. It is the method behind the public elliptic curve records, and behind every serious estimate of the cost of breaking a curve with many machines. For one machine, the distinguished point version is still the fastest rho, with $N = 1$. For small orders, [baby-step giant-step](/baby-step-giant-step/) is simpler, and for subgroups of $(\mathbb{Z}/p\mathbb{Z})^*$ with large $p$ the [index calculus](/index-calculus/) family is faster.

## Pitfalls

- **No restart after a report.** If a client continues its walk after a report instead of restarting at line L17, two walks that merged with a useless collision, $s = 0$, stay merged, give the same useless collision at every later distinguished point, and one client is wasted for the rest of the epoch. The right line is L17: restart after every report, from a fresh random label.
- **The same randomness on every client.** If all clients seed their generators alike, they start at the same points and walk the same trails, and $N$ clients do the work of one. Line L6 and line L17 must give each client independent uniform $a_i$ and $b_i$.
- **No cycle bound.** A walk that enters a cycle without a distinguished point never reports, and without the test $\ell_i \ge L_{\max}$ of line L17 its client is lost. Bound the walk length by a multiple of $1/\theta$, here $20/\theta$.
- **Density too small.** If $1/\theta$ is close to $\sqrt{\pi n / 2} / N$, clients may not reach even one distinguished point before the answer is due, and the $1/\theta$ term dominates. Galbraith's Exercise 14.3.3 asks for $1/\theta \le \sqrt{\pi n / 2} / (N \log n)$; pick $\theta$ from the storage available, not too small.
- **Dividing by a zero coefficient.** As in serial rho, line L12 must test $s \ne 0$ and handle $d = \gcd(s, n) > 1$ with lines L13 to L15; inverting $s$ modulo $n$ directly fails or returns a wrong value.
- **Storing before looking up.** If a report is written into $T$ before the lookup of line L10, or overwrites the triple already there, the earlier report is lost and the collision is missed. Line L10 must look up first, and line L16 stores only points that are new.
- **Different walks on different clients.** All clients must use the same $M_j$, the same $S$ and the same $D$ in an epoch; otherwise walks that meet do not merge. A new walk at line L4 must also clear the table at line L5, since old entries come from another walk.

## Implementations

## History

Pollard's rho method of 1978 is serial: Floyd's cycle finding follows a single walk. Distinguished points were proposed for time-memory tradeoffs, an idea van Oorschot and Wiener credit to Rivest, and Quisquater and Delescaille used them to find collisions of DES. Van Oorschot and Wiener's paper, presented in 1994 and published in the Journal of Cryptology in 1999, made the method general: they showed how distinguished points give rho and kangaroo a linear speedup, analysed the run time, and estimated the cost of special purpose machines for elliptic curve logarithms and for attacks on double DES. Teske's $r$-adding walks of 1998 became the standard walk. The method solved the Certicom challenges ECCp-109 in 2002 and ECC2-109 in 2004 with thousands of volunteers' computers, and Bos and coauthors used it on a cluster of PlayStation 3 consoles for the $112$-bit curve secp112r1.

## References

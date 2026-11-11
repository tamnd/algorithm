---
tag: 7QZBWQ
kind: technique
slug: time-memory-tradeoff
name: Time-memory tradeoff
aliases:
- TMTO
area: cryptography/hash-functions
level: advanced
summary: Spend about N work once to build compact tables, then invert a fixed function on N points with time T and memory M such that T M^2 = N^2, far below N for both.
prereqs: [preimage-finding, exhaustive-key-search]
see_also: [hellman-time-memory-tradeoff, rainbow-table, distinguished-points, exhaustive-key-search, preimage-finding, password-hashing, meet-in-the-middle-attack, pollard-rho-collision-search]
sources:
  - paper: doi:10.1109/TIT.1980.1056220
    title: Martin E. Hellman, A cryptanalytic time-memory trade-off, IEEE Transactions on Information Theory 26(4), 1980, pages 401 to 406
    locator: the chain tables, the matrix stopping rule mt^2 = N, and the tradeoff curve T M^2 = N^2 with precomputation N
  - paper: "Alex Biryukov and Adi Shamir, Cryptanalytic time/memory/data tradeoffs for stream ciphers, ASIACRYPT 2000, LNCS 1976, pages 1 to 13"
    locator: the tradeoff T M^2 D^2 = N^2 for 1 at most D^2 at most T, with precomputation N/D
  - paper: "Philippe Oechslin, Making a faster cryptanalytic time-memory trade-off, CRYPTO 2003, LNCS 2729, pages 617 to 630"
    locator: rainbow tables and the factor 2 gain in online work
  - paper: "Amos Fiat and Moni Naor, Rigorous time/space tradeoffs for inverting functions, STOC 1991, pages 534 to 541"
    locator: the tradeoff for every function, T M^3 = N^3 up to small factors, with no assumption of randomness
  - paper: "Andrew Chi-Chih Yao, Coherent functions and program checkers, STOC 1990, pages 84 to 94"
    locator: the lower bound T M at least about N for inverting a random permutation with advice
  - paper: "Elad Barkan, Eli Biham and Adi Shamir, Rigorous bounds on cryptanalytic time/memory tradeoffs, CRYPTO 2006, LNCS 4117, pages 1 to 21"
    locator: the lower bound for chain-based tradeoffs, and fuzzy rainbow tables
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 7.2 (exhaustive key search and the time-memory tradeoff)
---

A time-memory tradeoff is a way to invert a fixed function $f$ on $N$ points with less time than [exhaustive search](/exhaustive-key-search/) and less memory than a full table. The cost is a precomputation of about $N$ calls of $f$, done once before any target is known. The precomputation walks long chains of the form $x \to R(f(x)) \to \cdots$ and stores only the two ends of each chain. The online phase recomputes the missing parts. Hellman's scheme reaches any point on the curve $T M^2 = N^2$ with $1 \le T \le N$, for example $T = M = N^{2/3}$. When the attacker has $D$ targets and one success is enough, Biryukov and Shamir improve this to $T M^2 D^2 = N^2$. The technique attacks keys under a fixed chosen plaintext, unsalted password hashes and stream cipher states. A random salt or IV per target defeats it.

## In plain words

To undo a scrambling function, you can try every input each time, which is slow, or keep a list of every input with its output, which is huge. A tradeoff keeps a small summary instead, and does some of the work again when it is needed.

The summary is made of long chains of scrambled values. You keep only the first and the last value of each chain. Later, to undo a given output, you walk forward until you reach one of the last values, then go back to the matching first value and walk to the answer.

Longer chains mean less memory but more walking. Shorter chains mean the reverse. You choose where to stand between the two.

## When it applies

The technique needs four things.

- **A fixed function.** The same $f$ must be inverted for every target. This holds for a cipher key under a fixed chosen plaintext, $f(K) = E_K(P_0)$, for an unsalted password hash, and for the map from the internal state of a stream cipher to its first output bits.
- **A reduction.** A cheap function $R$ from outputs back to inputs, so that chains can be built. For keys, drop or fold some bits. For passwords, map a hash to a string over the target alphabet.
- **Many targets or a hard deadline.** The precomputation costs about $N$, so the tradeoff pays off only when the tables are used many times, or when each answer is needed fast.
- **A space that fits the precomputation.** $N$ up to about $2^{64}$ in practice.

It does not apply when each target uses a new function: a salted hash, a key derivation with a random nonce, or a cipher with a random IV. Then each target needs its own precomputation, which costs as much as exhaustive search.

## The template

```pseudo id=main
TMTO-PRECOMPUTE(f, N, m, t, ℓ)
L1  for i ← 1 to ℓ do                                   ▷ hole: how many tables
L2      for j ← 1 to m do
L3          SP ← a random start; EP ← walk t steps of R_(i,·) ∘ f from SP   ▷ hole: the reductions
L4          store (EP, SP) in table i, keyed by EP      ▷ hole: what to do on a repeated EP

TMTO-ONLINE(y)
L5  for i ← 1 to ℓ and each position s of y in a chain do   ▷ hole: the order of guesses
L6      z ← walk from R(y) to the end of the chain, assuming position s
L7      if z is a stored EP of table i then
L8          x ← walk from the matching SP to position s
L9          if f(x) = y then return x                   ▷ else a false alarm
L10 return FAIL
```

The holes are filled differently by each scheme.

- **[Hellman tables](/hellman-time-memory-tradeoff/).** One reduction $R_i$ for all columns of table $i$. About $\ell = t$ tables, each with $m$ chains and $m t^2 = N$. The online phase walks once per table and looks up the end table at each step.
- **[Rainbow tables](/rainbow-table/).** A single table, with a different reduction $R_j$ for each column $j$. The guesses go from the last column to the first.
- **Distinguished points.** Each chain ends at the first point with a fixed pattern, so lines L6 and L7 look up the table only once per chain.

**The tradeoff curve for Hellman.** With $\ell = t$ tables of $m$ chains and $m t^2 = N$:

- memory $M = m t$ pairs;
- online time $T = t^2$ calls of $f$, plus false alarms;
- precomputation $P = m t^2 = N$;
- success about $1 - e^{-0.8} \approx 0.55$, since each table covers about $0.8\,mt$ points.

So $T M^2 = t^2 \cdot m^2 t^2 = N^2$. Any $T$ between 1 and $N$ is possible by the choice of $t$.

## Classic examples

- **DES under a chosen plaintext.** $N = 2^{56}$. Hellman's choice $T = M = N^{2/3}$ gives about $2^{37.3}$ for both, after $2^{56}$ precomputation. This was Hellman's original target in 1980.
- **Unsalted password hashes.** Rainbow tables cracked the LAN Manager hashes of Windows, which have no salt and split a password into two 7-character halves. Oechslin (2003) showed the attack running in seconds on a PC.
- **Stream ciphers with data.** For a cipher with an internal state of $N$ values, each window of output bits is a target, and inverting any one gives the state. With $D$ targets, Biryukov and Shamir use $\ell = t/D$ tables, so that $M = mt/D$, $T = t^2/D$ and $P = N/D$, and get $T M^2 D^2 = N^2$ for $D^2 \le T$. For $N = 2^{64}$ and $D = 2^{16}$ this gives $T = M = 2^{32}$ with $P = 2^{48}$. Biryukov, Shamir and Wagner applied such tradeoffs to the GSM cipher A5/1 in 2000.
- **The Babbage and Golic tradeoff.** With $D$ targets, store $M$ random states with their outputs, sorted by output. A target is found when $M D \ge N$. This gives $T M = N$ with $T = D$ and $P = M$. It is the case $t = 1$ of the general scheme.
- **Lookup tables for tiny spaces.** With $N$ below about $2^{40}$, a full table of all $N$ outputs is often simplest. This is the end $T = 1$, $M = N$ of the curve.

## Variations

- **Rigorous versions.** Hellman's analysis treats $f$ and $R$ as random functions. Fiat and Naor (1991) give a scheme that works for every $f$, with $T M^3 = N^3$ up to small factors.
- **Lower bounds.** For inverting a random permutation with $M$ words of advice and $T$ queries, Yao (1990) shows $T M \ge \Omega(N)$, and Hellman's method with cycles reaches it. For random functions, Barkan, Biham and Shamir (2006) show that chain-based schemes cannot beat $T M^2 \approx N^2$ by more than small factors.
- **Checkpoints and perfect tables.** Extra bits per chain detect false alarms early. Dropping merged chains gives tables with distinct end points.
- **Memory-efficient collision search.** A related idea, walks with [distinguished points](/distinguished-points/), turns the memory of a birthday or meet in the middle attack into time. See [Pollard rho collision search](/pollard-rho-collision-search/) and [meet in the middle](/meet-in-the-middle-attack/).
- **Quantum tradeoffs.** With quantum queries, inverting $f$ costs about $N^{1/2}$ by Grover search with no precomputation. Tradeoffs with quantum advice are an active research area.

## Pitfalls

- **Precomputation counts.** An attack with $T = M = N^{2/3}$ still needs about $N$ work once. For one target it is slower than exhaustive search.
- **Salts and IVs defeat it.** A unique random salt of at least 64 bits per password, or a fresh IV per message, makes a precomputed table useless. This is the main lesson for designers. See [password hashing](/password-hashing/).
- **Success is not 100%.** One configuration reaches about 55% to 90% depending on the number of tables. Plan for misses, or add tables.
- **False alarms cost time.** Each match of an end point must be checked by rebuilding the chain. Ignoring them gives wrong answers, and underestimating them gives wrong costs.
- **Merges limit coverage.** Beyond the matrix stopping rule $m t^2 = N$, more chains add little coverage. Use more tables, with different reductions, instead.
- **Disk access dominates.** For large tables on disk, each lookup is slow. Distinguished points and rainbow tables reduce the number of lookups.

## Exercises

1. For $N = 2^{40}$, choose $m$, $t$ and $\ell$ for Hellman tables with $T = M$. How many pairs are stored, and how many calls of $f$ does a target cost?
2. Show that $\ell$ Hellman tables with $\ell = t$ and a rainbow table of $m t$ chains of length $t$ use the same memory and precomputation. Count the online calls of $f$ for each.
3. A system hashes passwords with a 12-bit salt. How much more precomputation and memory does a rainbow table attack need? Is the salt enough?

## References

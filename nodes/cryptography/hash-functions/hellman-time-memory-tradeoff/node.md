---
tag: EQFZ4J
kind: algorithm
slug: hellman-time-memory-tradeoff
name: Hellman time-memory tradeoff
aliases:
- Hellman tables
area: cryptography/hash-functions
level: advanced
summary: Invert a fixed one-way function on N points by precomputing chains and storing only their two ends. With mt^2 = N and t tables, it uses N^(2/3) memory and N^(2/3) time per target.
solves: [preimage-finding]
model: query-model
complexity:
  vars: {N: the number of points 2^n, m: the chains per table, t: the chain length, ℓ: the number of tables}
  time: {worst: O(t^2 ℓ), average: O(t ℓ)}
  space: {extra: Θ(m ℓ)}
properties: {deterministic: false}
history:
  year: 1980
  people: [Martin E. Hellman]
  note: Hellman proposed the chain tables to recover DES keys from a fixed chosen plaintext, with precomputation N and then T = M = N^(2/3) per key.
prereqs: [time-memory-tradeoff]
see_also: [time-memory-tradeoff, rainbow-table, exhaustive-key-search, preimage-finding, distinguished-points, data-encryption-standard, one-way-function, password-hashing]
sources:
  - paper: doi:10.1109/TIT.1980.1056220
    title: Martin E. Hellman, A cryptanalytic time-memory trade-off, IEEE Transactions on Information Theory 26(4), 1980, pages 401 to 406
    locator: Section II (the chains and tables), Section III (the coverage bound and the matrix stopping rule mt^2 = N), and the choice T = M = N^(2/3)
  - book: isbn:9780201101508
    title: Dorothy E. Denning, Cryptography and Data Security, Addison-Wesley, 1982
    locator: the discussion of Hellman's tradeoff in Chapter 2, with Rivest's idea of distinguished points to reduce memory accesses
  - paper: "Philippe Oechslin, Making a faster cryptanalytic time-memory trade-off, CRYPTO 2003, LNCS 2729, pages 617 to 630"
    locator: Section 2 (Hellman tables, false alarms and merges) and Section 4 (the comparison with rainbow tables)
  - paper: "Amos Fiat and Moni Naor, Rigorous time/space tradeoffs for inverting functions, STOC 1991, pages 534 to 541"
    locator: a version of the tradeoff that works for every function, with T M^3 = N^3 up to small factors
  - paper: "Elad Barkan, Eli Biham and Adi Shamir, Rigorous bounds on cryptanalytic time/memory tradeoffs, CRYPTO 2006, LNCS 4117, pages 1 to 21"
    locator: a lower bound on the time of a broad class of chain-based tradeoffs
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 7.2 (exhaustive key search and the time-memory tradeoff for DES)
---

Hellman's time-memory tradeoff inverts a fixed function $f$ on $N$ points much faster than [exhaustive search](/exhaustive-key-search/), after a one-time precomputation of about $N$ calls. It builds chains $x, R(f(x)), R(f(R(f(x)))), \ldots$ of length $t$ and stores only the start and end of each. Given $y = f(x)$, it walks forward from $R(y)$ until it meets a stored end, then rebuilds that chain from its start to find the preimage. With $\ell$ tables of $m$ chains, chosen so that $m t^2 = N$ and $\ell = t$, the memory is $M = mt$ and the time per target is $T = t^2$. So $T M^2 = N^2$, for example $T = M = N^{2/3}$, with success about 55%. It solves [preimage finding](/preimage-finding/) for a fixed function, such as a cipher with a fixed chosen plaintext or an unsalted password hash. The [time-memory tradeoff](/time-memory-tradeoff/) page covers the general idea, and [rainbow tables](/rainbow-table/) are its faster successor.

## In plain words

Suppose you must often undo a scrambling function, and you can prepare once in advance. You could store every input next to its output, but that needs too much memory. You could try every input each time, but that needs too much time.

Hellman's idea sits in between. Start from a random point, scramble it, turn the result back into a valid input, and repeat many times. This gives a long chain. Write down only the first and the last point of each chain. Later, when you get an output to undo, keep scrambling it until you reach one of the stored last points. Then go back to the matching first point, and walk the chain again until you reach the input just before your output.

## The problem

The input is a function $f : X \to Y$ with $|X| = N$, given as a black box, and later a target $y = f(x)$ for a random $x$. The output is any $x'$ with $f(x') = y$. The precomputation may call $f$ before the target is known and store $M$ words. The online phase gets $y$ and may call $f$ $T$ times. A *reduction function* $R : Y \to X$ maps outputs back to inputs. Hellman's choice for DES was to drop 8 bits of the 64-bit ciphertext to get a 56-bit key. Table $i$ uses its own reduction $R_i$, and walks the map $g_i = R_i \circ f$.

## The algorithm

```pseudo id=main
HELLMAN-PRECOMPUTE(f, m, t, ℓ)
L1  for i ← 1 to ℓ do
L2      T_i ← empty dictionary                         ▷ end point → start point
L3      for j ← 1 to m do pick a random start point SP
L4          EP ← g_i^t(SP)                             ▷ g_i = R_i ∘ f, applied t times
L5          if EP is not a key of T_i then T_i[EP] ← SP

HELLMAN-INVERT(y)
L6  for i ← 1 to ℓ do
L7      z ← R_i(y)                                     ▷ the point after x in the chain of x
L8      for s ← 0 to t − 1 do                          ▷ z = g_i^s(R_i(y))
L9          if z ∈ T_i then x ← g_i^(t−1−s)(T_i[z]); if f(x) = y then return x
L10         z ← g_i(z)
L11 return FAIL
```

At line L9, the chain from $T_i[z]$ reaches $z$ after $t$ steps. If $x$ lies on it, $x$ is the point $t - 1 - s$ steps after the start. The test $f(x) = y$ is needed: when it fails, the walk from $R_i(y)$ merged into a stored chain without $x$ on it. This is a *false alarm*. The search then goes on.

The Python code for this page runs the tables on a toy one-way function on 20 bits, a 64-bit mixer with its top bits kept. Each $R_i$ XORs a constant that depends on $i$. The code is for study only and it is not constant time. Do not use the toy function. Store passwords with a salted memory-hard function such as Argon2 or scrypt, from libsodium or hashlib, so that no table can be precomputed.

## Example

Take $n = 20$, so $N = 2^{20}$, and $m = 64$, $t = 128$, $\ell = 128$, which satisfies $m t^2 = N$. The seed is 1980.

- **Precomputation.** $m t \ell = 2^{20}$ calls of $f$. Of the 8192 chains, 35 ended at an end point already in their table and were dropped. The tables store 8157 pairs, which is 0.8% of $N$.
- **Coverage bound.** Hellman's bound below gives at least 0.00619 per table, against the ideal $mt/N = 0.0078$. Over 128 tables this gives $1 - (1 - 0.00619)^{128} \approx 0.548$.
- **Online.** For 100 random targets $y = f(x)$, the code found a preimage for 71. On average it made 10739 calls of $f$, 9181 lookups and 36 false alarms per target. The worst case is $t \ell = 16384$ lookups.
- **A traced target.** For $x$ = 0xa5cd6 and $y$ = 0xe3bd5, the code returned 0x35c7c after 6539 calls and 17 false alarms. This is not $x$, but $f$(0x35c7c) = $y$: any preimage counts.

The success of 0.71 is above the bound of 0.548 for two reasons. The bound counts only the chance that $x$ itself is covered, and a stored chain may hold another preimage of $y$. Also, the bound is a lower bound.

## Correctness

The method never returns a wrong answer, because line L9 returns $x$ only after it checks $f(x) = y$. It succeeds on $y$ whenever some table $i$ has a stored chain that contains a preimage $x'$ of $y$ at a position $j \le t - 1$ from its start: then $g_i^{t-1-j}(R_i(y)) = g_i^{t-j}(x')$ is the end point, the walk at line L8 meets it at $s = t - 1 - j$, unless it meets an earlier false alarm first, and the walk from the start gives $x'$. False alarms only cost time, since the search goes on after them. The full proof is below.

## Complexity

Let $N$ be the number of points.

- **Precomputation.** $P = m t \ell$ calls of $f$.
- **Memory.** $M = m \ell$ start and end pairs.
- **Online time.** At most $t$ steps of line L10 and $t$ lookups per table, so $t \ell$ calls of $f$, plus up to $t$ calls for each false alarm. Hellman estimates the expected number of false alarms per table to be a small constant when $m t^2 \approx N$, so $T = O(t \ell)$ calls.
- **Coverage.** For one table, Hellman shows

$$\Pr[\text{success}] \;\ge\; \frac{1}{N} \sum_{i=1}^{m} \sum_{j=0}^{t-1} \left(1 - \frac{i t}{N}\right)^{j+1}.$$

The term for $(i, j)$ bounds the chance that point $j$ of chain $i$ is new, given that the first $i - 1$ chains cover at most $(i-1)t$ points. The sum is close to $mt/N$ while $m t^2 \ll N$, and stops growing once $m t^2 \gg N$: then new chains mostly repeat covered points. This is the *matrix stopping rule*: choose $m t^2 = N$. A table then covers about $0.8 \, mt$ points.

- **Many tables.** One table covers only a fraction $1/t$ of the space. So use $\ell \approx t$ tables, each with its own reduction, so that chains in different tables do not merge. With $\ell = t$ and $m t^2 = N$, success is about $1 - e^{-0.8} \approx 0.55$, and $M = mt$, $T = t^2$, $P = N$. Hence

$$T M^2 = t^2 \cdot m^2 t^2 = (m t^2)^2 = N^2.$$

The usual point is $T = M = N^{2/3}$ and $t = m = N^{1/3}$. For DES with $N = 2^{56}$, this is about $2^{37}$ words and $2^{37}$ cipher calls per key, after $2^{56}$ precomputation.

## Properties

- **Fixed function only.** The tables invert one $f$. A salt, an IV or a new plaintext changes $f$ and makes the tables useless.
- **Probabilistic.** It fails for points not covered by the tables. More tables raise the success rate at a cost in memory and time.
- **Precomputation is about $N$.** It pays off only when many targets will be inverted with the same tables, or when the online phase must be fast.
- **Merges waste work.** Two chains of one table that meet at the same column end at the same point and one is dropped. Chains that meet at different columns are both kept, and share their remaining points. This is the main loss of coverage.
- **Lookups dominate.** Each online step looks up an end point in a table. For tables on disk, Rivest's distinguished points reduce the number of lookups.

## Variants and improvements

- **[Distinguished points](/distinguished-points/).** Rivest suggested ending each chain at the first point with a fixed pattern, such as $d$ leading zero bits (Denning 1982). Then the online phase needs a table lookup only at distinguished points, about once per chain length, not at every step. Merges of chains are also detected at once, since merged chains end at the same point.
- **[Rainbow tables](/rainbow-table/).** Oechslin (2003) uses a different reduction at each column of one large table. Two chains merge only if they meet in the same column. One table replaces $t$ Hellman tables, and the online phase needs about half the calls of $f$ and far fewer lookups.
- **Data tradeoff.** With $D$ targets, of which one inversion suffices, as in stream ciphers, Biryukov and Shamir give $T M^2 D^2 = N^2$ with $D \le T$. See [time-memory tradeoff](/time-memory-tradeoff/).
- **Fiat and Naor.** Hellman's analysis assumes $f$ behaves like a random function. Fiat and Naor (1991) give a variant that works for every function, at a cost of $T M^3 = N^3$ up to small factors.
- **Lower bounds.** Barkan, Biham and Shamir (2006) show that, for a wide class of chain-based schemes, Hellman's tradeoff cannot be improved by more than small factors.

## When to use it

Use it to invert a fixed function many times, when exhaustive search per target is too slow and a full table is too large: the key of a cipher under a fixed chosen plaintext, a hash of a password with no salt, or the state of a stream cipher from a known output. In practice, rainbow tables have replaced Hellman tables for most of these uses. Use the analysis to choose parameters: $m t^2 \approx N$ and $\ell \approx t$.

On the defense side, a random salt of at least 64 bits per password, or a fresh IV per message, makes every precomputation useless. See [password hashing](/password-hashing/).

## Pitfalls

- **Do not exceed the matrix stopping rule.** With $m t^2 \gg N$, extra chains only add merges and false alarms.
- **Each table needs its own reduction.** If two tables use the same $R$, their chains merge and the second table adds almost nothing.
- **Check every candidate.** A match of an end point is not a solution. Skipping the check at line L9 returns wrong answers.
- **Count the precomputation.** An attack with $T = M = N^{2/3}$ still costs $N$ calls once. It is not cheaper than exhaustive search for one target.
- **The reduction must cover the inputs.** If $R$ hits only part of $X$, for example only printable passwords of one length, the tables only cover that part.

## Implementations

## History

Hellman published the tradeoff in 1980, with DES as the target: a fixed chosen plaintext, a 56-bit key, and $N^{2/3} \approx 2^{37}$ for both memory and time. Rivest suggested distinguished points, which Denning described in 1982. Fiat and Naor gave a rigorous version for every function in 1991. Biryukov and Shamir added the data parameter in 2000 and, with Wagner, applied tradeoffs to the GSM cipher A5/1. Oechslin introduced rainbow tables in 2003, and tools such as Ophcrack used them to break Windows LAN Manager hashes, which have no salt. Barkan, Biham and Shamir proved lower bounds for chain-based tradeoffs in 2006.

## References

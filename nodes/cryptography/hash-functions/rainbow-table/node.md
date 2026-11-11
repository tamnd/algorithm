---
tag: W2QHWJ
kind: data-structure
slug: rainbow-table
name: Rainbow table
aliases:
- rainbow chains
area: cryptography/hash-functions
level: advanced
summary: A table of chain start and end points for inverting a fixed hash, with a different reduction in each column. It replaces t Hellman tables, with fewer merges and about half the online work.
model: query-model
complexity:
  vars: {N: the number of points 2^n, m: the number of chains, t: the chain length}
  time: {worst: O(t^2)}
  space: {extra: Θ(m)}
prereqs: [hellman-time-memory-tradeoff]
see_also: [hellman-time-memory-tradeoff, time-memory-tradeoff, password-hashing, distinguished-points, preimage-finding, exhaustive-key-search, hash-table, bcrypt]
sources:
  - paper: "Philippe Oechslin, Making a faster cryptanalytic time-memory trade-off, CRYPTO 2003, LNCS 2729, pages 617 to 630"
    locator: Section 3 (rainbow chains, one reduction function per column), Section 4 (the success probability 1 minus the product of (1 - m_i/N), and the factor 2 in work), and Section 5 (the Windows LAN Manager experiment)
  - paper: doi:10.1109/TIT.1980.1056220
    title: Martin E. Hellman, A cryptanalytic time-memory trade-off, IEEE Transactions on Information Theory 26(4), 1980, pages 401 to 406
    locator: the classic tables that rainbow tables replace
  - book: isbn:9780201101508
    title: Dorothy E. Denning, Cryptography and Data Security, Addison-Wesley, 1982
    locator: the discussion of Hellman's tradeoff in Chapter 2, with Rivest's suggestion of distinguished points
  - paper: "Gildas Avoine, Pascal Junod and Philippe Oechslin, Characterization and improvement of time-memory trade-off based on perfect tables, ACM Transactions on Information and System Security 11(4), 2008"
    locator: perfect rainbow tables, checkpoints against false alarms, and the optimal parameters
  - paper: "Elad Barkan, Eli Biham and Adi Shamir, Rigorous bounds on cryptanalytic time/memory tradeoffs, CRYPTO 2006, LNCS 4117, pages 1 to 21"
    locator: fuzzy rainbow tables, which add distinguished points to rainbow chains
  - url: "https://www.rfc-editor.org/rfc/rfc9106"
    title: Alex Biryukov, Daniel Dinu, Dmitry Khovratovich and Simon Josefsson, RFC 9106, Argon2 Memory-Hard Function for Password Hashing and Proof-of-Work Applications, 2021
    locator: Section 3.1 (the salt input) and Section 4 (parameter choice), the defense against precomputed tables
---

A rainbow table is a precomputed structure for inverting one fixed function $f$, such as an unsalted password hash. It stores $m$ chains of length $t$, and keeps only the start and the end of each chain. The chains alternate $f$ with *reduction functions* that map outputs back to inputs, and column $j$ of every chain uses its own reduction $R_j$. Oechslin introduced this in 2003 as an improvement of [Hellman's tables](/hellman-time-memory-tradeoff/). Two chains merge only if they collide in the same column, so one table of $mt$ chains does the work of $t$ Hellman tables, the online phase needs about half as many calls of $f$, and a lookup in the table is needed only $t$ times per target instead of $t^2$. A random salt per password makes all such tables useless, which is why modern [password hashing](/password-hashing/) always salts.

## In plain words

You want to find which password gave a stored hash. You cannot store every password with its hash: there are too many. So build chains in advance: take a password, hash it, turn the hash into a new password by a fixed rule, hash that, and go on. Keep only the first and last password of each chain.

The trick of a rainbow table is to change the rule at each step of the chain, like the colors of a rainbow. Then two chains can only run together if they hit the same password at the same step.

To crack a hash, guess that it sits at the last step, then at the step before, and so on. For each guess, finish the chain to its end and look for that end in the table. When you find it, rebuild the chain from its start to reach the password.

## The abstract type

A rainbow table supports two operations for a fixed $f : X \to Y$ with $|X| = N$ and fixed parameters $t$ and $R_0, \ldots, R_{t-1}$:

- **ADD-CHAIN($x_0$).** Add the chain that starts at $x_0$.
- **LOOKUP($y$).** Return some $x$ with $f(x) = y$, or FAIL.

A lookup is *sound*: it never returns a wrong $x$. It is complete for the targets $y$ that are *covered*: those with $y = f(x_j)$ for some point $x_j$ in a column $j \le t - 1$ of a stored chain. The table makes no promise for other targets.

## Representation

A chain from the start $x_0$ is

$$x_0 \xrightarrow{f} y_0 \xrightarrow{R_0} x_1 \xrightarrow{f} y_1 \xrightarrow{R_1} x_2 \;\cdots\; x_{t-1} \xrightarrow{f} y_{t-1} \xrightarrow{R_{t-1}} x_t,$$

so $x_{j+1} = R_j(f(x_j))$. The table is a [hash table](/hash-table/) or a sorted file that maps each end point $x_t$ to its start point $x_0$. Only these $2m$ values are stored. Each $R_j$ maps $Y$ onto $X$. For passwords, $R_j$ turns a hash into a candidate password over the target alphabet, and it mixes in the column number $j$.

In a *perfect* table, chains with an end point that is already present are dropped, so all end points are distinct. The invariant of the structure is: for each stored pair, the chain from the start reaches the end after $t$ steps.

## Operations

```pseudo id=main
ADD-CHAIN(x0)
L1  x ← x0
L2  for j ← 0 to t − 1 do x ← R_j(f(x))
L3  if x is a key of E then return false               ▷ a merge: drop the chain
L4  E[x] ← x0; return true

LOOKUP(y)
L5  for j ← t − 1 down to 0 do                         ▷ guess: y = f(x_j)
L6      z ← R_j(y)                                     ▷ then z = x_(j+1)
L7      for c ← j + 1 to t − 1 do z ← R_c(f(z))        ▷ finish the chain: z = x_t
L8      if z is a key of E then
L9          x ← E[z]; for c ← 0 to j − 1 do x ← R_c(f(x))    ▷ rebuild: x = x_j
L10         if f(x) = y then return x                  ▷ else a false alarm
L11 return FAIL
```

The guesses run from the last column to the first, because a guess at column $j$ costs $t - 1 - j$ calls of $f$ at line L7. The cheap guesses come first, and the total for all guesses is $t(t-1)/2$.

The Python code for this page builds rainbow tables and Hellman tables for a toy one-way function on 18 bits, a 64-bit mixer with its top bits kept, with $R_j(y) = y \oplus c_j$ for a constant $c_j$ per column. It is for study only and it is not constant time. Do not use the toy function or these tables against real systems. To store passwords, use a salted memory-hard function such as Argon2 or scrypt, from libsodium or hashlib.

## Example

Take $n = 18$, so $N = 2^{18} = 262144$, and $t = 64$. The rainbow table gets $m = 4096$ chains. The Hellman side gets 64 tables of 64 chains, each of length 64. So both spend $mt = 2^{18}$ calls of $f$ on precomputation.

| | rainbow | Hellman |
|---|---|---|
| chains built | 4096 | 4096 |
| pairs stored | 2699 | 4066 |
| success over 400 targets | 0.70 | 0.75 |
| predicted success | 0.559 | at least 0.548 |
| calls of $f$ per target | 1166 | 2485 |
| table lookups per target | 36.1 | 2133 |
| false alarms per target | 8.5 | 16.2 |

The rainbow table needs 47% of the calls of $f$ and 1.7% of the lookups. It stores fewer pairs: 1397 chains had an end point that was already present and were dropped, because with $mt = N$ the table is past full. Both success rates are above the prediction because the toy $f$ is not injective. A lookup succeeds when it finds any preimage of $y$, while the formulas count only the chance that the chosen $x$ itself is covered.

Before the drop, the 4096 chains covered a fraction of the points within 0.01 of Oechslin's formula. The test checks this, and also checks the invariant of each stored pair.

## Correctness

**Invariant.** ADD-CHAIN stores $E[x_t] = x_0$ only after computing $x_t$ from $x_0$ by the $t$ steps of line L2, and never overwrites a key. So each stored start reaches its end.

**Lookup.** A result is returned only after the test $f(x) = y$ at line L10, so it is always right. Suppose $y = f(x_j)$ for column $j$ of a stored chain. When the loop reaches that $j$, line L6 gives $z = R_j(y) = x_{j+1}$, line L7 gives $z = x_t$, which is a key, and line L9 rebuilds $x = x_j$. Then line L10 returns $x_j$, unless an earlier guess has already returned a correct answer. A false alarm, where the end point matches but $f(x) \ne y$, only costs time. The full proof is below.

## Complexity

- **Build.** $mt$ calls of $f$ for $m$ chains.
- **Space.** At most $m$ pairs of points, about $2m \log_2 N$ bits. Real tools compress the end points further.
- **Lookup.** $\sum_{j} (t - 1 - j) = t(t-1)/2$ calls of $f$ at line L7, at most $t$ table lookups, and up to $t$ calls per false alarm. A Hellman setup of $t$ tables of $m/t$ chains, with the same memory, needs $t^2$ calls and $t^2$ lookups. So the rainbow table halves the work of $f$ in the worst case, and cuts the lookups by a factor of $t$.
- **Coverage.** Oechslin's estimate of success for a table that keeps all $m$ chains, with $m_1 = m$ and $m_{i+1} = N(1 - e^{-m_i/N})$ the expected number of distinct points in column $i + 1$, is

$$P = 1 - \prod_{i=1}^{t} \left(1 - \frac{m_i}{N}\right).$$

For the example, $P \approx 0.559$.

- **Tradeoff.** With $mt^2 \approx N$ as for Hellman, the same relation $T M^2 \approx N^2$ holds up to a constant factor of about 2 in favor of rainbow tables.

## Variants

- **Perfect tables.** Drop chains with repeated end points, and build more chains to fill the table. All end points are distinct, so each lookup finds at most one chain per column. Avoine, Junod and Oechslin analyse their best parameters.
- **[Distinguished points](/distinguished-points/).** Rivest's idea, as reported by Denning, ends each chain at the first point with a fixed pattern. Used with Hellman tables, it reduces the lookups. Barkan, Biham and Shamir combine both ideas in *fuzzy rainbow tables*.
- **Checkpoints.** Store a few bits of an inner point of each chain, so that most false alarms are detected without rebuilding the chain.
- **Several tables.** Real tools use a few rainbow tables with different reductions, each near full, to reach a success rate of 99% or more.
- **Alphabet-aware reductions.** For passwords, $R_j$ maps a hash to a string over a chosen character set and length, so the table covers exactly the passwords of that form.

## When to use it

Rainbow tables are the standard precomputed attack on fast unsalted hashes: LAN Manager and NT hashes of Windows, an unsalted MD5 or SHA-1 of a password, or a cipher key from a fixed known plaintext. They pay off when the same function will be inverted for many targets, and when the target space is small, such as passwords of up to 8 characters.

On the defense side:

- Add a unique random salt of at least 16 bytes to each password before hashing. The attacker would need one table per salt value, which is no better than [exhaustive search](/exhaustive-key-search/).
- Use a slow, memory-hard function such as Argon2, scrypt or [bcrypt](/bcrypt/), so that each guess is costly.
- A secret key in the hash, a pepper or an HMAC, also stops precomputation.

## Pitfalls

- **Unsalted hashes.** A hash of a password with no salt can be looked up in a public table. A salt shared by all users only forces one new table.
- **Coverage is not 100%.** One table covers part of the space. Plan several tables, and expect some targets to fail.
- **Do not skip the check.** A matching end point does not prove a hit. Line L10 must compute $f(x)$ and compare.
- **Reduction must depend on the column.** A rainbow table with the same reduction in each column is a single Hellman table, with all its merges.
- **The alphabet of the reduction.** A table built for lowercase letters never finds a password with a digit. Choose the reduction to match the target space.

## Implementations

## History

Hellman described chain tables in 1980, and Rivest suggested distinguished points to cut the number of table accesses. Oechslin introduced rainbow chains at CRYPTO 2003. He showed that LAN Manager password hashes of Windows, which have no salt, could be cracked in seconds, with a success rate near 99.9%, using tables of about 1.4 GB. Tools such as Ophcrack and RainbowCrack then made precomputed tables widely available. The attacks pushed operating systems and web applications to salted, slow password hashes. Later work by Avoine, Junod and Oechslin, and by Barkan, Biham and Shamir, refined the analysis and the false alarm handling.

## References

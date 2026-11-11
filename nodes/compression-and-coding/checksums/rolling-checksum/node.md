---
tag: 6HMBPD
kind: algorithm
slug: rolling-checksum
name: Rolling checksum
aliases:
- rsync rolling checksum
area: compression-and-coding/checksums
level: core
summary: A checksum of a fixed-size window that moves one byte in O(1) time. rsync uses it to find old blocks at any offset of a new file, and Rabin fingerprints use it to cut content-defined chunks.
model: word-ram
complexity:
  vars: {n: the length of the new file, m: the length of the old file, S: the block size}
  time: {worst: Θ(n S), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(m / S + S)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1996
  people: [Andrew Tridgell, Paul Mackerras]
  note: Tridgell and Mackerras described the rsync algorithm and its rolling checksum in the ANU technical report TR-CS-96-05 in June 1996. Mackerras suggested the form of the checksum, based on Adler-32.
prereqs: [adler-32]
see_also: [polynomial-rolling-hash, rabin-fingerprint, rabin-karp, dedup, delta-encoding, md4, md5, sliding-window]
sources:
  - paper: "Andrew Tridgell and Paul Mackerras, The rsync algorithm, Technical Report TR-CS-96-05, Department of Computer Science, Australian National University, June 1996"
    title: Andrew Tridgell and Paul Mackerras, The rsync algorithm, TR-CS-96-05, 1996
    locator: Section 3 (Rolling checksum, the sums a and b modulo 2^16 and their recurrence) and Section 4 (Checksum searching, the 16-bit hash, the weak and strong checks)
  - paper: "Andrew Tridgell, Efficient Algorithms for Sorting and Synchronization, PhD thesis, Australian National University, February 1999"
    title: Andrew Tridgell, Efficient Algorithms for Sorting and Synchronization, PhD thesis, 1999
    locator: Chapter 3, Section 3.2.5 (Selecting the fast signature, with footnote 9 on Mackerras and Adler), Section 3.2.6 (The signature search algorithm) and Section 3.3 (Choosing the block size)
  - paper: "Michael O. Rabin, Fingerprinting by Random Polynomials, Technical Report TR-15-81, Center for Research in Computing Technology, Harvard University, 1981"
    title: Michael O. Rabin, Fingerprinting by Random Polynomials, TR-15-81, 1981
    locator: The fingerprint of a bit string as its residue modulo a random irreducible polynomial over GF(2), and the bound on the probability of a collision
  - paper: doi:10.1145/502034.502052
    title: Athicha Muthitacharoen, Benjie Chen and David Mazieres, A Low-bandwidth Network File System, SOSP 2001
    locator: Section 3.1 (chunk boundaries where the low 13 bits of the Rabin fingerprint of a 48-byte window equal a fixed value, with a 2 KB minimum and a 64 KB maximum chunk size)
---

A rolling checksum is a checksum of a window of $S$ bytes that can move one byte to the right in $O(1)$ time: drop the byte that leaves, add the byte that enters, and do not look at the rest of the window. This page covers the checksum of rsync, from Andrew Tridgell and Paul Mackerras (1996), which is the [Adler-32](/adler-32/) pair of sums modulo $2^{16}$ over a fixed window. rsync uses it to find, at every byte offset of a new file, the blocks that the receiver already has in its old file, and it confirms each hit with a strong hash. A last section covers the other common rolling checksum, a Rabin fingerprint, used to cut a file into content-defined chunks. The [polynomial rolling hash](/polynomial-rolling-hash/) of string matching is a third kind, with a different goal and analysis; this page links to it but does not cover it.

## In plain words

You have an old copy of a file, and someone else has a new copy that differs by a few edits. To send only the changes, you cut your old file into blocks of, say, 700 bytes and send a short checksum of each block. The other side now has to find those blocks in the new file, but an insertion can shift them to any position, not only to multiples of 700.

So the other side slides a 700-byte window one byte at a time and needs the checksum of each window. From scratch that costs 700 steps per position. A rolling checksum costs a few: subtract the byte that left, add the byte that came in, fix the weights. When the checksum matches one of your blocks, a slower strong hash confirms the match, and the other side sends "copy your block 12" in place of 700 bytes.

## The problem

**The rolling checksum.** For a window $X_k, \ldots, X_l$ of $L = l - k + 1$ bytes and $M = 2^{16}$, rsync defines

$$a(k, l) = \sum_{i=k}^{l} X_i \bmod M, \qquad b(k, l) = \sum_{i=k}^{l} (l - i + 1)\, X_i \bmod M, \qquad s = a + 2^{16} b.$$

This is Adler-32 without its start value and with modulus $2^{16}$. The task is to compute $s$ for every window position $k = 0, 1, \ldots, n - S$ of a file of $n$ bytes in $O(1)$ time per step.

**The delta.** The receiver has an old file of $m$ bytes and sends, for each full block $j$ of $S$ bytes, the pair (weak checksum, strong hash). The sender has the new file. It must output a list of instructions, "copy block $j$" or "these literal bytes", from which the receiver rebuilds the new file exactly. We want few literal bytes when the files are close. The delta of files is a different thing from the [delta encoding](/delta-encoding/) of a sequence of numbers.

## The algorithm

Moving the window from $[k, l]$ to $[k + 1, l + 1]$ changes the sums by

$$a(k+1, l+1) = a(k, l) - X_k + X_{l+1}, \qquad b(k+1, l+1) = b(k, l) - L\, X_k + a(k+1, l+1),$$

both modulo $M$. The byte $X_k$ leaves, and it had weight $L$ in $b$. Every other byte gains weight 1, which adds the new $a$. The sender uses this inside the search loop, given here with the roll written out in lines L9 and L10.

```pseudo id=main
DELTA(new[0 .. n−1], sig, S)                 ▷ sig[j] = (weak, strong) of old block j
L1  H ← a hash table from each weak value to the blocks j that have it
L2  k ← 0; (a, b) ← WEAK(new[0 .. S−1])
L3  while k + S ≤ n do
L4      if a + 2^16·b is in H and STRONG(new[k .. k+S−1]) equals the strong hash of some j in it then
L5          emit the pending literal bytes, then COPY j; k ← k + S
L6          (a, b) ← WEAK(new[k .. k+S−1])            ▷ if a full window is left
L7      else
L8          append new[k] to the pending literal bytes
L9          a ← (a − new[k] + new[k+S]) mod 2^16     ▷ roll, if new[k+S] exists
L10         b ← (b − S·new[k] + a) mod 2^16
L11         k ← k + 1
L12 append new[k .. n−1] to the literal bytes and emit them
```

The receiver applies the instructions to its old file: COPY $j$ copies bytes $jS$ to $jS + S - 1$, and a literal is copied as it is. The strong hash in the 1996 paper is [MD4](/md4/). The implementation uses [MD5](/md5/) from Python's `hashlib`, as modern rsync does; the algorithm does not depend on the choice. It also differs from rsync in two small ways, which do not change the output: it looks up the full 32-bit weak value in a Python dictionary, where rsync uses a 16-bit hash of it and a sorted table (Section 4 of the report), and it indexes only full blocks of the old file, so a short last block is never matched.

## Example

The window "abcd" (bytes 97, 98, 99, 100) with $L = 4$ has $a = 394$ and $b = 4 \cdot 97 + 3 \cdot 98 + 2 \cdot 99 + 100 = 980$. Rolling to "bcde" drops 97 and adds 101:

$$a' = 394 - 97 + 101 = 398, \qquad b' = 980 - 4 \cdot 97 + 398 = 990,$$

and indeed $4 \cdot 98 + 3 \cdot 99 + 2 \cdot 100 + 101 = 990$. Weak collisions are easy to find: the blocks 01 03 00 and 02 01 01 both have $a = 4$ and $b = 9$. The tests check that the delta then sends the bytes, because the strong hashes differ.

For the delta, take an old file of 8,000 random bytes, insert 13 bytes after byte 100, and use $S = 64$. Block 0 of the old file still sits at offset 0, so the delta starts with COPY 0. Old block 1 (bytes 64 to 127) holds the insertion point, so it no longer occurs in the new file. The window fails at offsets 64 to 140, and at offset 141 it finds old block 2, 13 bytes after its old place. From there every old block is found. So the delta is COPY 0, then $77 = S + 13$ literal bytes, then COPY 2 to COPY 124. The tests check that at most $S + 13$ bytes are literal and that at least 123 blocks are copied, and they rebuild 500 random edited files from their deltas, for block sizes 1, 4, 16 and 32.

## Correctness

The roll is exact: it gives the same $(a, b)$ as recomputing the sums over the new window, so the weak values that the sender compares are the true weak checksums of its windows. A COPY is emitted only when the strong hashes are equal, and the instructions cover the new file from left to right without gaps, so the receiver rebuilds the new file exactly, as long as the strong hash has no collision between the two blocks. The proof is in the correctness file below.

## Complexity

The roll takes $O(1)$ time. The loop of lines L3 to L11 advances $k$ by 1 or by $S$. A step without a weak hit costs $O(1)$ time. A weak hit costs $O(S)$ for the strong hash, and a match costs another $O(S)$ for the fresh weak sum of line L6. Matches cover disjoint parts of the file, so they cost $O(n)$ in total. False weak hits are the only other cost: in the worst case every offset has one, and the time is $\Theta(nS)$. For data that is not built against it, a false hit at an offset has a probability of about $(m/S)/2^{32}$, so the expected time is $\Theta(n)$. The table holds one entry per old block, $\Theta(m/S)$ space, plus the window. Tridgell's thesis (Section 3.3) shows that the block size that minimizes the bytes sent for $Q$ small differences is about $\sqrt{24 n / Q}$.

## Properties

- **Exact roll.** The roll gives the same values as a recompute at every offset, for any byte values. The tests check this at every offset of random data for window lengths 1, 2, 7, 64 and 700.
- **Order sensitivity.** The sum $b$ weighs each byte by its position, so moving a byte inside the window changes $b$. A plain sum, which Tridgell tried first, cannot see this (thesis, Section 3.2.5).
- **A filter, not a proof.** The weak checksum has only 32 bits and many easy collisions, so a match must be confirmed. With a 128-bit strong hash, rsync fails only if the strong hash collides; rsync also checks a hash of the whole file after the rebuild (thesis, Section 3.4.2).
- **Online.** The sender reads the new file once from left to right and emits instructions as it goes.

## Variants and improvements

- **Rabin fingerprints and content-defined chunking.** A [Rabin fingerprint](/rabin-fingerprint/) (Rabin 1981) reads a window of $w$ bytes as a polynomial $W(x)$ over GF(2) and keeps $W(x) \bmod P(x)$ for a fixed [irreducible polynomial](/irreducible-polynomial/) $P$ of degree $d$. It also rolls in $O(1)$: multiply by $x^8$, add the new byte, and subtract the old byte times $x^{8w} \bmod P$, with two tables of 256 entries. LBFS (2001) uses it to cut files where the content says so: a chunk ends after a window whose fingerprint has a fixed value in its low 13 bits, with a minimum of 2 KB and a maximum of 64 KB per chunk. Since the cut points depend only on the 48 bytes before them, an insertion moves only the cut points near it, and the chunks after it are the same as before. Each chunk is then named by a strong hash, which makes [deduplication](/dedup/) across files and versions possible. The implementation uses a degree 63 polynomial, which the tests prove irreducible with Rabin's test, a 48-byte window, 8 low bits, and a minimum of 64 and a maximum of 2048 bytes, smaller than in LBFS so that the tests run fast. On 20,000 random bytes, an insertion of 15 bytes near the start changes at most 3 chunks, while the same insertion changes more than 70 fixed blocks of 256 bytes.
- **rsync versus CDC.** rsync needs a round trip: the receiver sends block checksums, and the sender searches at every offset. CDC needs no search, because both sides cut at the same places on their own, but its chunks vary in size.
- **Polynomial rolling hash.** The [polynomial rolling hash](/polynomial-rolling-hash/) of [Rabin-Karp](/rabin-karp/) keeps $\sum X_i r^{L-i} \bmod p$ for a random base $r$ and a prime $p$, and so it has a provable collision bound for any fixed pair of strings. The rsync checksum is the case $r = 1$ for $a$ and a weighted sum for $b$, with no randomness; it is cheaper but has no such bound. Tridgell's thesis notes the similarity (footnote 9 of Section 3.2.5).
- **Other rolling functions.** Chunking tools also use other rolling functions, such as Gear or Buzhash, which are cheaper than a Rabin fingerprint. They trade speed against the spread of the values.

## When to use it

Use the rsync rolling checksum to send a new version of a file to a receiver that has an old version, when the edits are few and can shift data. Use content-defined chunking with a Rabin fingerprint (or a faster rolling hash) when you want to store or send many versions and files and find the common chunks without comparing pairs of files. Use the [polynomial rolling hash](/polynomial-rolling-hash/) for string matching, where you need a collision bound. None of these is a guard against an attacker who chooses the data: the weak checksums are easy to collide, and only the strong hash protects the result.

## Pitfalls

- **Off-by-one in the roll.** The weight of the leaving byte in $b$ is the window length $L$, not $L - 1$. The roll must update $a$ first and then use the new $a$ in $b$.
- **Negative values.** In languages where $x \bmod M$ can be negative, reduce after the subtractions, or keep the sums in unsigned 16-bit types.
- **Trusting the weak checksum.** Two different blocks often share the weak value. A COPY without a strong check corrupts the result.
- **The last block.** The old file usually ends with a short block. Either index it with its own length or, as here, do not index it; then it is always sent as literal bytes.
- **The block size.** A block size close to the size of the checksums gains nothing, and a large block size sends many literal bytes for each small edit.

## Implementations

## History

Andrew Tridgell and Paul Mackerras published the rsync algorithm in the technical report TR-CS-96-05 of the Australian National University in June 1996. Tridgell's 1999 PhD thesis gives the full account. He first tried the first and last 4 bytes of each block as the fast signature, which failed on structured data such as tar files, and then a plain sum, which ignores the order of the bytes. The final form was suggested by Mackerras and is based on the Adler checksum of zlib (thesis, Section 3.2.5). Michael O. Rabin had defined fingerprints by random irreducible polynomials in 1981. Muthitacharoen, Chen and Mazieres used them in LBFS in 2001 to cut files into content-defined chunks, a method that many deduplicating storage and backup systems use in some form.

## References

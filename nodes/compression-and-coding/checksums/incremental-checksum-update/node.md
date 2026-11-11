---
tag: RGZ1Q3
kind: algorithm
slug: incremental-checksum-update
name: Incremental checksum update
aliases:
- RFC 1624 checksum update
area: compression-and-coding/checksums
level: advanced
summary: Patch the Internet checksum in O(1) when one 16-bit field changes, by HC' = ~(~HC + ~m + m') (RFC 1624). The older RFC 1141 rule can give -0 where a recompute gives +0.
model: word-ram
complexity:
  vars: {n: the number of header bytes}
  time: {worst: Θ(1), average: Θ(1), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1994
  people: [Anil Rijsinghani]
  note: RFC 1071 (1988) gave the update C' = C + (-m) + m' for the sum. RFC 1141 (1990) gave a form for the stored checksum, and RFC 1624 (1994) corrected its -0 result.
prereqs: [internet-checksum]
see_also: [ones-complement-arithmetic, additive-checksum, fletcher-checksum, adler-32, rolling-checksum, checksum]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc1624
    title: A. Rijsinghani, editor, RFC 1624, Computation of the Internet Checksum via Incremental Update, May 1994
    locator: Section 2 (Eqn. 1 and Eqn. 2), Section 3 (Eqn. 3 and Eqn. 4, the two zeros), Section 4 (the example with m = 0x5555, m' = 0x3285), Section 5 (checksum verification by end systems) and Section 6 (historical note)
  - url: https://www.rfc-editor.org/rfc/rfc1141
    title: T. Mallory and A. Kullberg, RFC 1141, Incremental Updating of the Internet Checksum, January 1990
    locator: The update formula ~C' = ~C + m + ~m' and the example of a TTL decrement
  - url: https://www.rfc-editor.org/rfc/rfc1071
    title: R. Braden, D. Borman and C. Partridge, RFC 1071, Computing the Internet Checksum, September 1988
    locator: Section 2 (4), Incremental Update, C' = C + (-m) + m'
  - url: https://www.rfc-editor.org/rfc/rfc791
    title: J. Postel, RFC 791, Internet Protocol, September 1981
    locator: Section 3.1, the Time to Live and Header Checksum fields (a router changes the TTL and must recompute the header checksum)
---

An incremental checksum update recomputes the [Internet checksum](/internet-checksum/) of a header after one 16-bit word changes from $m$ to $m'$, in $O(1)$ time, without a pass over the header. A router does this for every IPv4 packet it forwards, because it decrements the TTL. Network address translation does it when it rewrites an address or a port. The correct rule is Eqn. 3 of RFC 1624, $HC' = \lnot(\lnot HC + \lnot m + m')$ in [ones' complement arithmetic](/ones-complement-arithmetic/). The older rule of RFC 1141 is correct modulo $2^{16} - 1$ but gives 0xFFFF ($-0$) in the cases where a full recompute gives 0x0000 ($+0$). This page is about the patch of a sum after a change at a known place. A [rolling checksum](/rolling-checksum/) is a different update: it moves a window along the data.

## In plain words

A checksum is a total of all the words of a header, flipped bit for bit. If you change one word, you do not need to add up the whole header again. Take the old total, remove the old word and add the new one. In ones' complement arithmetic, removing a word means adding its flipped form.

There is a catch. This arithmetic has two zeros, all zeros and all ones. A full recompute can give all zeros as the checksum, but it never gives all ones. One old shortcut sometimes gives all ones where the recompute gives all zeros. Both mean zero to the arithmetic, but they are different bit patterns, and a router that tests the header in a strict way may see an error. The rule of RFC 1624 never makes this mistake.

## The problem

The input is a header whose checksum field holds $HC = \lnot S$, where $S$ is the ones' complement sum of the other words. One word changes from $m$ to $m'$. The output is $HC'$, the value that a full recompute of the new header gives: $HC' = \lnot S'$, where $S'$ is the ones' complement sum of the other words of the new header. All values are 16-bit words. We write $\oplus$ for ones' complement addition, $\lnot$ for the bitwise complement, and $+0 = 0x0000$, $-0 = 0xFFFF$.

The RFCs give four equations.

| name | formula | result |
|---|---|---|
| RFC 1071 Section 2 (4), RFC 1624 Eqn. 1 | $C' = C + (-m) + m'$ | for the sum $C$, not for the stored $HC$ |
| RFC 1141, RFC 1624 Eqn. 2 | $HC' = HC + m + \lnot m'$ | gives $-0$ where the true value is $+0$ |
| RFC 1624 Eqn. 3 | $HC' = \lnot(\lnot HC + \lnot m + m')$ | correct |
| RFC 1624 Eqn. 4 | $HC' = HC - \lnot m - m'$ | correct, with ones' complement subtraction |

## The algorithm

```pseudo id=main
UPDATE(HC, m, m′)                           ▷ 16-bit words, ones' complement arithmetic
L1  c ← not HC                              ▷ the sum S of the other words
L2  c ← c ⊕ (not m)                         ▷ take out the old word: add its negative
L3  c ← c ⊕ m′                              ▷ put in the new word
L4  return not c                            ▷ HC′
```

Here $a \oplus b$ is the 16-bit add with the end-around carry: $s \leftarrow a + b$, then $s \leftarrow (s \text{ and } 0xFFFF) + (s \gg 16)$. A router that decrements the TTL changes the word at bytes 8 and 9 of the IPv4 header: the TTL is its high byte, so $m' = m - 0x100$. A NAT box that rewrites a 32-bit address calls UPDATE twice, once for each half. TCP and UDP checksums cover the addresses through the pseudo header, so they need the same patch.

## Example

**RFC 1624 Section 4.** The sum of the other header words is $C = 0xCD7A$, the word $m = 0x5555$ changes to $m' = 0x3285$, and the old checksum is $HC = \lnot(0xCD7A \oplus 0x5555) = \lnot 0x22D0 = 0xDD2F$.

| step | operation | value |
|---|---|---|
| L1 | $\lnot 0xDD2F$ | 0x22D0 |
| L2 | $0x22D0 \oplus \lnot 0x5555 = 0x22D0 \oplus 0xAAAA$ | 0xCD7A |
| L3 | $0xCD7A \oplus 0x3285$ | 0xFFFF |
| L4 | $\lnot 0xFFFF$ | 0x0000 |

A full recompute gives the same: $0xCD7A + 0x3285 = 0xFFFF$, so $HC' = 0x0000$. RFC 1141 instead computes $0xDD2F \oplus 0x5555 = 0x3285$, then $0x3285 \oplus \lnot 0x3285 = 0xFFFF$. It stores 0xFFFF, a value that a full recompute never gives for a header with a nonzero word. Both values pass a receiver that sums the whole header, because $0xCD7A \oplus 0x3285 \oplus 0xFFFF$ and $0xCD7A \oplus 0x3285 \oplus 0x0000$ are both 0xFFFF (RFC 1624 Section 5). A router that compares the stored field with a fresh recompute does see a difference.

**A TTL decrement.** The header 4500 0073 0000 4000 4011 b861 c0a8 0001 c0a8 00c7 has TTL 0x40. The word 0x4011 becomes 0x3F11. UPDATE computes $\lnot 0xB861 = 0x479E$, then $0x479E \oplus \lnot 0x4011 = 0x479E \oplus 0xBFEE = 0x078D$, then $0x078D \oplus 0x3F11 = 0x469E$, and returns $\lnot 0x469E = 0xB961$. That is the old checksum plus 0x0100, as RFC 1141 notes for a TTL decrement, and it matches a full recompute.

## Correctness

Let $T$ be the plain integer sum of the other header words, so $S = \mathrm{oc}(T)$, where $\mathrm{oc}(T)$ is 0 for $T = 0$ and otherwise the value in $[1, 65535]$ congruent to $T$ modulo 65535. Line L1 recovers $S$. Lines L2 and L3 give a value congruent to $T - m + m'$, which is the new sum modulo 65535. The value is never $+0$, because the operands of line L3 cannot all be zero. So line L4 returns $\lnot S'$ exactly when the new sum $S'$ is not $+0$, that is, whenever the new header has a nonzero word. In IPv4 the version field is 4, so this always holds. The full proof, and the exact cases where RFC 1141 and Eqn. 4 differ from a recompute, are in the correctness file below.

## Complexity

UPDATE does three ones' complement additions and two complements, so it takes $\Theta(1)$ time and $\Theta(1)$ space, independent of the header length $n$. A full recompute takes $\Theta(n)$ time. For an IPv4 header, $n$ is at most 60 bytes, so the gain is a constant factor, but it is a large one for a router that forwards millions of packets per second. The gain is larger for TCP and UDP, where the checksum covers the whole payload: a NAT box that rewrites an address must not read the payload.

## Properties

- **Exact.** Eqn. 3 and Eqn. 4 give the same value as a full recompute for every header that has a nonzero word other than the checksum.
- **RFC 1141.** Eqn. 2 is congruent to the right value modulo 65535. It differs from a recompute exactly when the recompute gives 0x0000, and then it gives 0xFFFF, with one exception: for $HC = 0x0000$, $m = 0x0000$ and $m' = 0xFFFF$ it gives 0x0000, which is right. The tests find more than 1000 random edits where the true checksum is 0x0000 and check this.
- **Composable.** Several changes can be applied one after the other, or summed first: take out all the old words and put in all the new ones, in any order.
- **Byte order independent.** As for the full sum, a little-endian machine can work on swapped words and swap the result.
- **Does not check the old header.** UPDATE keeps an error that was already in the header: if the old checksum was wrong, the new one is wrong by the same amount. A full recompute would hide that error by making a corrupted header look valid.

## Variants and improvements

- **Eqn. 4.** $HC' = HC - \lnot m - m'$ with ones' complement subtraction, that is, subtraction with an end-around borrow. It gives the same results as Eqn. 3. It suits a machine whose primitive is subtraction, such as the CDC 6000 series that RFC 1624 Section 6 mentions.
- **Several words.** For an address change from $a_1 a_2$ to $a'_1 a'_2$, compute $\lnot HC \oplus \lnot a_1 \oplus \lnot a_2 \oplus a'_1 \oplus a'_2$ and complement once.
- **UDP.** A UDP checksum of 0x0000 means "no checksum" over IPv4. A NAT box must leave such a field alone, and must turn a computed 0x0000 into 0xFFFF (RFC 768).
- **Other checksums.** The same idea works for any checksum that is linear in the data. For a CRC the patch depends on the position of the change. For [Adler-32](/adler-32/) and the [Fletcher checksum](/fletcher-checksum/), the second sum needs the position too.

## When to use it

Use it whenever a node changes a few fields of a packet and forwards it: routers (TTL), NAT and load balancers (addresses and ports), and MPLS or tunnel endpoints. Use Eqn. 3 or Eqn. 4, not Eqn. 2. Recompute from scratch when many fields change, so that the update would cost more than a pass over the header.

## Pitfalls

- **Using RFC 1141.** It gives 0xFFFF where the recompute gives 0x0000. A receiver that sums the whole header accepts both, but a strict check that compares the field with a recompute does not, and so do tests that compare against a recompute.
- **Forgetting the end-around carry.** A two's complement add in line L2 or L3 gives a wrong result whenever the addition carries out of bit 15.
- **Forgetting to mask the complement.** In C or Python, `~m` of a 16-bit value is a negative or a 32-bit value. Mask it with 0xFFFF.
- **Patching the wrong half of a word.** The TTL is the high byte of the word at bytes 8 and 9, so the change is $-0x100$, not $-1$.
- **The UDP zero.** Over IPv4, a UDP checksum field of 0 must stay 0, and a computed 0x0000 must be sent as 0xFFFF.

## Implementations

## History

RFC 1071 (1988) gave the incremental update in Section 2 (4) as $C' = C + (-m) + m'$, for the ones' complement sum $C$. In January 1990, Mallory and Kullberg of BBN published RFC 1141, which wrote the update for the stored checksum, $\lnot C' = \lnot(C + (-m) + m') = \lnot C + m + \lnot m'$, and noted that a TTL decrement adds 0x0100 to the checksum. In May 1994, RFC 1624, edited by Anil Rijsinghani, showed that this form can produce $-0$, which a full computation of the header checksum never produces for a header with a nonzero word, and gave Eqn. 3 and Eqn. 4. Its Section 6 notes that the CDC 6000 series computers used subtraction as their primitive operation, which is the setting of Eqn. 4.

## References

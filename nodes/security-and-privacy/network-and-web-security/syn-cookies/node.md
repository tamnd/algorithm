---
tag: Z3NQ59
kind: algorithm
slug: syn-cookies
name: SYN cookies
aliases:
- SYN cookie
area: security-and-privacy/network-and-web-security
level: core
summary: Encodes the connection state in the server's initial sequence number as a keyed hash, so that the server keeps no state until the handshake ends.
model: word-ram
complexity:
  vars: {n: the number of SYN segments that have no final ACK yet}
  time: {worst: O(1), average: O(1), best: O(1)}
  space: {extra: O(1)}
properties: {deterministic: true, stateless: true, online: true}
history:
  year: 1996
  people: [Daniel J. Bernstein, Eric Schenk]
  note: Bernstein proposed the idea in September 1996 during SYN floods against an internet service provider, and worked out the details with Schenk. RFC 4987 documents the layout.
prereqs: [syn-flooding, hmac, pseudorandom-function]
see_also: [syn-flooding, ingress-filtering, message-authentication-code, siphash, birthday-paradox, union-bound]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc4987"
    title: Wesley M. Eddy, TCP SYN flooding attacks and common mitigations, RFC 4987, August 2007
    locator: Section 3.6 (SYN cookies and the lost TCP options), Section 4 (analysis and advice on defaults) and Appendix A (the 32-bit layout of the cookie)
  - url: "https://cr.yp.to/syncookies.html"
    title: Daniel J. Bernstein, SYN cookies
    locator: the whole page (the history from September 1996, the time counter and why the cookie depends on time)
  - url: "https://www.rfc-editor.org/rfc/rfc9293"
    title: Wesley M. Eddy (editor), Transmission Control Protocol (TCP), RFC 9293, August 2022
    locator: Section 3.4.1 (initial sequence numbers from a keyed pseudorandom function, after RFC 6528) and Section 3.5 (the three-way handshake)
---

SYN cookies let a TCP server answer a connection request without storing anything about it. The server puts the state it needs into its own initial sequence number: a time counter, a code for the maximum segment size, and a keyed [message authentication code](/message-authentication-code/) of the connection's addresses and ports. A real client sends that number back, plus one, in the last message of the handshake, and the server checks it and only then builds the connection. This makes the server immune to [SYN flooding](/syn-flooding/): a flood costs it one hash per packet and no memory.

## In plain words

A cloakroom runs out of hooks when many people hand in coats and never come back. So the attendant stops taking coats at the door. Instead, each visitor gets a ticket with the time, and a stamp that only the attendant can make and that depends on the visitor's name. When the visitor comes back with the ticket, the attendant checks the stamp and the time, and only then gives a hook.

The server does the same. To the first message of a connection it answers with a number that holds a stamp, the time and one small setting. It writes nothing down. A real client sends the number back in its last message. The server makes the stamp again from the message and compares. A forged ticket has the wrong stamp, and an old ticket has a time that is too old.

## The problem

A server receives SYN segments from clients and must answer each with a SYN-ACK. A client is identified by the 4-tuple $c = (\text{client address}, \text{client port}, \text{server address}, \text{server port})$. The server must accept a final ACK from $c$ if and only if it sent a SYN-ACK to $c$ recently, and it must recover the maximum segment size (MSS) that it chose for $c$. It must do this with memory that does not grow with the number of open requests.

The threat model is an off-path adversary: it can send segments with any source address, but it cannot see the SYN-ACKs that the server sends to other addresses, and it does not know the key $K$. Under this model the server accepts a forged ACK with probability at most $2^{-24}$ per attempt, plus the advantage of a distinguisher against the keyed hash. An adversary that sees the SYN-ACK, for example on the path to the client, can complete the handshake; SYN cookies do not stop it, and they are not meant to.

## The algorithm

Let $F_K$ be a [pseudorandom function](/pseudorandom-function/) with key $K$, here [HMAC](/hmac/)-SHA256. Let $t$ be a counter that the server steps every 64 seconds, and let $T[0 \ldots 7]$ be a fixed table of eight MSS values. Each SYN-ACK carries the cookie $y$ as the server's initial sequence number, and the final ACK of a real client carries $a = y + 1 \bmod 2^{32}$. The layout follows RFC 4987, Appendix A: 5 bits of time, 3 bits of MSS code, 24 bits of hash.

```pseudo id=main
MAKE-COOKIE(K, c, t, m)          ▷ on a SYN from c; m is the index of the MSS in T
L1  h ← F_K(c, t) mod 2^24
L2  return (t mod 32)·2^27 + m·2^24 + h

CHECK-COOKIE(K, c, a, now, A)    ▷ on an ACK from c with acknowledgment number a; A < 32
L3  y ← (a - 1) mod 2^32
L4  t5 ← ⌊y / 2^27⌋, m ← ⌊y / 2^24⌋ mod 8, h ← y mod 2^24
L5  t ← now - ((now - t5) mod 32)
L6  if now - t > A or t < 0 then return REJECT
L7  if F_K(c, t) mod 2^24 ≠ h then return REJECT
L8  return ACCEPT with MSS T[m]
```

MAKE-COOKIE runs on each SYN while the backlog is full, or on each SYN if the server always uses cookies. The server picks $m$ as the largest index with $T[m]$ at most the client's MSS, sends the SYN-ACK and forgets the request. CHECK-COOKIE runs on an ACK that matches no stored connection. Line L3 undoes the $+1$ of the client, modulo $2^{32}$. Line L4 splits the three fields. The cookie holds only $t \bmod 32$, so line L5 takes the latest counter value at or before $now$ that has these 5 bits; it is the right one whenever the cookie is less than 32 steps old. Line L6 rejects cookies whose rebuilt age is more than $A$ steps. A cookie $32j + a$ steps old with $j \ge 1$ and $a \le A$ rebuilds an age of $a$ and passes line L6; line L7 rejects it, because the hash was made with the older counter value, except with probability $2^{-24}$. Line L7 makes the hash again and compares it in constant time. If it matches, the server builds the TCB from the ACK and the MSS $T[m]$.

## Example

Take the key $K = $ the 16 bytes 0x00, 0x01, ..., 0x0f, the client $c = $ (203.0.113.7, 49152, 192.0.2.10, 443) from the documentation ranges, the counter $t = 1000$ and a client MSS of 1460. The table is $T = (536, 1220, 1300, 1400, 1440, 1460, 4312, 8960)$, so $m = 5$. Then $t \bmod 32 = 8$, the truncated hash is $h = $ 0xd79c4e, and

$$
y = 8 \cdot 2^{27} + 5 \cdot 2^{24} + \text{0xd79c4e} = \text{0x45d79c4e} = 1171758158 .
$$

The real client answers with $a = $ 0x45d79c4f. The server checks it with $A = 2$:

| case | $a$ | $now$ | $t$ from line L5 | age | line L7 | result |
|---|---|---|---|---|---|---|
| real ACK | 0x45d79c4f | 1000 | 1000 | 0 | match | accept, MSS 1460 |
| real ACK | 0x45d79c4f | 1001 | 1000 | 1 | match | accept, MSS 1460 |
| real ACK | 0x45d79c4f | 1002 | 1000 | 2 | match | accept, MSS 1460 |
| late ACK | 0x45d79c4f | 1003 | 1000 | 3 | not run | reject at line L6 |
| wrong number | 0x45d79c50 | 1000 | 1000 | 0 | 0xd79c4f ≠ 0xd79c4e | reject |
| other port 49153 | 0x45d79c4f | 1000 | 1000 | 0 | hash of another tuple | reject |
| other key | 0x45d79c4f | 1000 | 1000 | 0 | hash under another key | reject |

At $now = 1003$, line L5 gives $1003 - ((1003 - 8) \bmod 32) = 1003 - 3 = 1000$, so the counter is rebuilt even though the server never stored it.

## Correctness

**Theorem.** (1) For every key $K$, tuple $c$, counter $t \ge 0$, index $m \in \{0, \ldots, 7\}$ and time $now$ with $0 \le now - t \le A < 32$, CHECK-COOKIE$(K, c, $ MAKE-COOKIE$(K, c, t, m) + 1, now, A)$ accepts and returns $T[m]$. (2) If $F_K$ is a random function, then for any fixed $c$, $a$ and $now$, chosen without seeing a value $F_K(c, t')$ for the $t'$ that line L5 computes, CHECK-COOKIE accepts with probability at most $2^{-24}$. An adversary that sends $q$ such ACKs succeeds with probability at most $q \cdot 2^{-24}$ by the [union bound](/union-bound/); with a real PRF, add the PRF distinguishing advantage.

The key fact for (1) is that line L5 returns the unique $t'$ with $t' \equiv t_5 \pmod{32}$ and $now - 31 \le t' \le now$, so it returns $t$ when $0 \le now - t \le 31$. For (2), $a$ and $now$ fix one value $t'$, and acceptance needs 24 bits of a uniform value to equal a fixed $h$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

All costs are in the [word RAM](/word-ram/) model, with one call of $F_K$ on an input of at most 45 bytes counted as $O(1)$ (HMAC-SHA256 on that input runs a fixed number of SHA-256 blocks).

- **Time per SYN.** Line L1 is one hash and line L2 is a few shifts: $O(1)$.
- **Time per ACK.** Lines L3 to L6 are constant arithmetic and line L7 is one hash: $O(1)$.
- **Space.** The server keeps $K$, the counter and the table $T$. It keeps nothing per request, so the space is $O(1)$ for any number $n$ of pending requests. A SYN cache keeps $\Theta(n)$ entries, up to its limit.

## Properties

- **Stateless.** No memory per request until the ACK arrives. This is the only defense of RFC 4987 that removes the backlog entirely.
- **Deterministic.** The same $K$, $c$, $t$ and $m$ always give the same cookie, so a retransmitted SYN gets the same SYN-ACK within one counter step.
- **Time-bound.** A cookie is valid for at most $A + 1$ counter steps. Bernstein made the cookie depend on time so that an adversary cannot collect valid cookies from one place and replay them later from another.
- **Lossy.** The 32 bits hold only an MSS code. Window scaling, selective acknowledgment and timestamps from the SYN are lost unless the server encodes them elsewhere (RFC 4987, Section 3.6).

## Variants and improvements

- **Client ISN in the cookie.** Schenk added the client's initial sequence number to the cookie, so that the server's sequence numbers increase with the client's as TCP expects. Linux follows this design.
- **Options in the timestamp.** If the client sends the timestamp option, the server can keep the window scale and the SACK flag in the low bits of the timestamp value that the client echoes. Linux does this, so it loses fewer options.
- **Hybrid with a SYN cache.** Store requests in a small hash table while there is room and switch to cookies only when it is full (RFC 4987, Section 3.7). Normal traffic keeps every option, and floods hit the stateless path.
- **A faster keyed hash.** HMAC-SHA256 is more than the cookie needs. A short keyed hash such as [SipHash](/siphash/) is enough, because the proof needs only that the keyed function is a PRF.
- **Key rotation.** Change $K$ from time to time and check against the current and the previous key, so that a leaked key ends.

## When to use it

Use SYN cookies on any server that can be reached by unauthenticated clients, at least as the fallback when the backlog is full. Use a SYN cache first when you need full TCP options for normal traffic, as RFC 4987 advises for defaults. SYN cookies do not help against a flood that fills the link, against an attacker that completes handshakes from real addresses (then [ingress filtering](/ingress-filtering/) and rate limits matter), or against an on-path adversary.

## Pitfalls

- **No key, or a guessable key.** If line L1 uses a plain hash of $c$ and $t$ with no secret, anyone can compute cookies, and a forged ACK passes. Line L1 must use a keyed PRF with a secret $K$ of at least 128 bits, drawn from a cryptographic source.
- **Rebuilding the counter wrong.** Writing line L5 as $t \leftarrow t_5$ or as $now - (now \bmod 32) + t_5$ gives a wrong counter when the 5-bit time wraps, and line L7 then rejects real clients just after each multiple of 32. Line L5 must take $now - ((now - t_5) \bmod 32)$.
- **Forgetting the $+1$.** Line L3 must undo the client's increment modulo $2^{32}$. Using $a$ itself, or $a - 1$ without the modulus, rejects every client, or the one with $a = 0$.
- **Comparing with an early exit.** Line L7 should compare in constant time. A byte-by-byte comparison that stops at the first difference leaks, through time, how many leading bytes of a guess are right (see [timing attack](/timing-attack/)).
- **No age limit.** Without line L6 a cookie stays valid until the 5-bit time comes round again, 32 steps later, and captured cookies can be replayed for longer than needed.

## Implementations

The code works on abstract 4-tuples with documentation addresses (RFC 5737 and RFC 3849) and takes the time counter as an argument. It opens no socket, reads no clock and sends no packet. The test compares CHECK-COOKIE with a server that stores every SYN-ACK it sends.

## History

Bernstein proposed SYN cookies on 16 September 1996, after a SYN flood had stopped the mail service of a New York internet service provider earlier that month, and he and Eric Schenk worked out the details in the following weeks. Bernstein made the cookie depend on time, and Schenk added the client's sequence number. Implementations for SunOS and for Linux followed within months. RFC 4987 (2007) describes the cookie layout used here and the trade-offs against the SYN cache.

## References

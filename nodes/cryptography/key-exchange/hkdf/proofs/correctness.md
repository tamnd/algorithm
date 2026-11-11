---
title: HKDF returns exactly L bytes of the RFC 5869 chain, and equal inputs give equal keys
proves: [correctness]
status: full
---

We use the notation of the page. HMAC is a deterministic function that returns $h$ bytes for any key and message. RFC 5869 defines $\mathrm{PRK} = \mathrm{HMAC}(\mathrm{salt}, \mathrm{IKM})$, with an empty salt replaced by $h$ zero bytes, and

$$T(0) = \text{empty}, \quad T(i) = \mathrm{HMAC}(\mathrm{PRK}, T(i - 1) \,\|\, \mathrm{info} \,\|\, \mathrm{byte}(i)) \text{ for } 1 \le i \le N,$$

with $\mathrm{OKM}$ the first $L$ bytes of $T(1) \,\|\, \cdots \,\|\, T(N)$ and $N = \lceil L/h \rceil \le 255$.

**Lemma 1 (Extract).** Lines L1 and L2 compute the PRK of RFC 5869.

*Proof.* Line L1 replaces an empty salt by $h$ zero bytes and leaves any other salt unchanged; line L2 applies HMAC with the salt as the key and IKM as the message. This is the definition. $\blacksquare$

**Lemma 2 (loop invariant).** After iteration $i$ of the loop in lines L6 and L7, $T = T(i)$ and $\mathrm{OKM} = T(1) \,\|\, \cdots \,\|\, T(i)$, which has $ih$ bytes.

*Proof.* By induction on $i$. Before the loop, line L5 sets $T$ and OKM to the empty string, which is $T(0)$ and the empty concatenation. If the claim holds after iteration $i - 1$, then line L7 sets $T \leftarrow \mathrm{HMAC}(\mathrm{PRK}, T(i - 1) \,\|\, \mathrm{info} \,\|\, \mathrm{byte}(i)) = T(i)$ and appends it to OKM. Each block has $h$ bytes, so OKM has $ih$ bytes. The byte $\mathrm{byte}(i)$ is defined because $i \le N \le 255$ by line L4. $\blacksquare$

**Theorem 1 (output).** For $1 \le L \le 255h$, HKDF returns exactly the OKM of RFC 5869, of length $L$; for $L > 255h$ it returns an error.

*Proof.* Line L3 sets $N = \lceil L/h \rceil$, and line L4 raises an error exactly when $N > 255$, that is when $L > 255h$. Otherwise, by Lemma 2 after iteration $N$, OKM is $T(1) \,\|\, \cdots \,\|\, T(N)$ with $Nh \ge L$ bytes, so the first $L$ bytes exist, and line L8 returns them. With Lemma 1, the PRK used is the one of the RFC. $\blacksquare$

**Theorem 2 (prefix property).** For fixed salt, IKM and info, and $L' \le L \le 255h$, the output of length $L'$ is the first $L'$ bytes of the output of length $L$.

*Proof.* The blocks $T(i)$ depend only on PRK, info and $i$, not on $L$. With $N' = \lceil L'/h \rceil \le N$, both outputs are prefixes of the same string $T(1) \,\|\, \cdots \,\|\, T(N)$, so the shorter is a prefix of the longer. $\blacksquare$

**Theorem 3 (agreement).** If two parties call HKDF with the same salt, IKM, info, $L$ and hash function, they obtain the same output.

*Proof.* Every step is a deterministic function of these inputs: HMAC is deterministic, and the loop runs the same number of times by line L3. So by Theorem 1 both outputs equal the OKM of RFC 5869 for these inputs. $\blacksquare$

**Remark.** These statements are about the function that HKDF computes. Its security, that OKM is indistinguishable from random when IKM has enough min-entropy and HMAC is a good extractor and pseudorandom function, is the theorem of Krawczyk (CRYPTO 2010), which we do not prove here. $\blacksquare$

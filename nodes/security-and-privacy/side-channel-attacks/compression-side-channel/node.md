---
tag: 9H216H
kind: technique
slug: compression-side-channel
name: Compression side channel
aliases:
- CRIME attack
- BREACH attack
area: security-and-privacy/side-channel-attacks
level: advanced
summary: A secret compressed together with data that an attacker chooses makes the compressed length depend on how well the two match, and encryption does not hide the length.
prereqs: [lz77, side-channel-attack]
see_also: [deflate, huffman-coding, lz77, authenticated-encryption, padding-oracle-attack, chosen-plaintext-attack, kolmogorov-complexity, timing-attack]
sources:
  - paper: "John Kelsey, Compression and information leakage of plaintext, FSE 2002, LNCS 2365, pages 263-276"
    locator: the observation that the length of a compressed and then encrypted message leaks information about the plaintext, and the attacks with partly chosen plaintext
  - url: "https://www.rfc-editor.org/rfc/rfc7541"
    title: "R. Peon and H. Ruellan, RFC 7541, HPACK, header compression for HTTP/2, 2015"
    locator: the security considerations on probing the state of the dynamic table, and the literals that must never be indexed
  - url: "https://www.rfc-editor.org/rfc/rfc8446"
    title: "E. Rescorla, RFC 8446, The Transport Layer Security (TLS) Protocol Version 1.3, 2018"
    locator: the handshake messages, in which the only compression method allowed is none
---

A compression side channel leaks a secret through the length of compressed data. A compressor such as [LZ77](/lz77/) writes a string that repeats an earlier string as a short reference. So when a secret and data that an attacker chooses are compressed together, the output is shorter when the chosen data repeats part of the secret. Encryption hides the bytes but not the length, so an observer of the encrypted traffic who can also choose part of the plaintext learns how well his choice matches the secret. Kelsey (2002) described the leak, and attacks in 2012 and 2013 used it to read secret tokens from encrypted web traffic. The defense is simple to state: do not compress secrets together with data that an attacker controls.

## In plain words

A packing service puts your letters into boxes and charges by the size of the box. To save space, it writes "same as above" instead of a line that already appeared. Someone else can add one line of his own to your letter, and he sees only the size of the box, never the letter.

If his line is the same as a line in your letter, the box gets smaller, because the service writes "same as above". If it is different, the box stays big. So the size of the box tells him whether he guessed part of your letter. The cure is to pack your secret lines in a box of their own.

## When it applies

### Threat model

The attacker sees the length of each encrypted message, for example as a network observer, and he can make the victim send messages that contain data he chooses, for example by making the victim's browser send requests. He cannot read the plaintext or break the encryption. The defenses below are stated against this attacker.

### Conditions

1. **COMBINE.** The secret and the chosen data go through one compressor in one context, so that one can refer back to the other.
2. **MATCH.** The compressor writes a repeat more briefly than new data, as every dictionary compressor does.
3. **LENGTH.** The attacker learns the length of the output, because the encryption keeps it: a stream cipher or an [authenticated encryption](/authenticated-encryption/) scheme gives a ciphertext of the length of the plaintext plus a constant.
4. **REPEAT.** The attacker can cause many messages with different chosen data while the secret stays the same.

### What removes a condition

| defense | condition it removes | cost |
|---|---|---|
| no compression of messages that hold secrets, or no compression at all | 1 | more bytes on the wire |
| separate compression contexts for secrets and for chosen data | 1 | a worse compression ratio |
| a compressor that never refers back to sensitive fields, as for the never-indexed literals of HPACK | 1, for those fields | the fields are sent in full |
| masking the secret with a fresh random value in each message | 4: the transmitted value changes each time | the work of the mask and a longer token |
| padding to a fixed length or to a few length classes | 3, fully for a fixed length, partly otherwise (heuristic) | more bytes; random padding can be averaged out over many messages |
| limits on the number of requests | 4, partly | can stop correct clients |

**Claim (theorem, in an abstract model of the defense).** Model the observable as the length $L(\cdot)$ of the compressed output, where $L$ is any function of the input string. (a) If the secret $s$ and the chosen data $g$ are compressed in separate contexts, the observer sees $L(s) + L(g)$. For a fixed secret this is $L(g)$ plus a constant, so the observations over all choices of $g$ give no more about $s$ than the single number $L(s)$. (b) If the message carries $t = s \oplus r$ in place of $s$, for a fresh uniform $r$ of the length of $s$ that is not in the same compression context, then for every $s$ the distribution of $L(g \parallel t)$ is the same. *Proof.* (a) follows from the form of the sum. (b) is the one-time pad argument: for a fixed $s$, the map $r \mapsto s \oplus r$ is a bijection, so $t$ is uniform for every $s$, and so is any function of $g$ and $t$.

In practice the mask $r$ is often sent next to $t$, in the same context. Then the two parts can match each other, with a probability that depends on $s$. For a long random mask that probability is very small, so there the masking is a heuristic, not the theorem (b).

## The template

The block is the shape of the class: each line is a condition, and the comment names the defense that removes it. It is not a recipe and it holds no strings.

```pseudo id=main
COMPRESSION-LEAK-CLASS(sender A, compressor C, channel E)
L1  require COMBINE: A gives the secret and the chosen data to C in one context   ▷ removed by separate contexts or no compression
L2  require MATCH: C writes a repeat of earlier input more briefly             ▷ hole C: any dictionary compressor
L3  require LENGTH: E reveals the length of the output of C                     ▷ removed by padding to a fixed length
L4  require REPEAT: the secret stays the same over many messages               ▷ removed by masking it in each message
L5  if every condition holds then each length is a function of how well the chosen data matches the secret
```

### An abstract model

Take a made-up compressor that replaces each repeat of an earlier string of at least $m$ symbols by one reference token, and let $L$ count tokens. Let the message be the secret $s$ followed by the chosen data $g$. If $g$ repeats a substring of $s$ of length $r \ge m$, that part of $g$ costs one token; otherwise it costs about one token for each symbol. So $L(s \parallel g)$ falls when the match is longer, and the length reveals the length of the longest match of $g$ with $s$. This is the leak of Kelsey (2002). In the same model, with $s$ in its own context, $L(s) + L(g)$ does not change with the match, and the leak is gone.

### The compression side channel and other length channels

The same pattern appears whenever a length is a function of the content: the size of the packets of a web page, studied as [website fingerprinting](/website-fingerprinting/); the bit rate of a voice call compressed at a variable rate; the size of an encrypted file in a backup that removes duplicates. In each case the cure is the same: make the length a function of public data only. A [padding oracle attack](/padding-oracle-attack/) is a different channel: it leaks through an error, not through a length.

## Classic examples

- **Kelsey, 2002.** Kelsey pointed out that compressing before encrypting leaks information about the plaintext through the length, and that an attacker who controls part of the plaintext can learn the rest. His lesson was not to compress secrets together with data that an attacker chooses.
- **TLS and SPDY compression, 2012.** Rizzo and Duong used the channel against the compression of request headers in TLS and in SPDY, where a session cookie and headers that the attacker could cause were compressed together. Browsers turned off TLS compression and the header compression of SPDY. HTTP/2 got a new header compressor, HPACK, built with this attack in mind, and TLS 1.3 allows no compression at all.
- **HTTP response compression, 2013.** Gluck, Harris and Prado showed that compression of the body of HTTP responses, with [DEFLATE](/deflate/), leaks secret tokens in a page when the page also reflects input from the request. Turning off compression of all responses is costly, so the advice was to separate secrets from reflected input, to mask tokens in each response, and to limit requests.
- **Lengths without a network observer, 2016.** Later work showed that a script in a browser can learn the length of a response to another site from the timing of the transfer, so condition 3 does not need an observer on the network.

## Variations

- **By the compressor.** Any dictionary compressor shows the leak. Coders with a static table, such as a fixed [Huffman code](/huffman-coding/), leak less, because the length of each symbol does not depend on earlier input, but the length still depends on the symbols.
- **By the place.** Header compression, body compression, compression inside a protocol, compressed files in storage.
- **By the observer.** A network observer, or a script that learns lengths from timing.
- **Leaks of the decompressor.** The time or the memory used to decompress can also depend on the content.

## Pitfalls

- **Random padding as the only defense.** Random padding adds noise that the attacker averages out with more requests. Pad to a fixed size, or remove the shared context.
- **Thinking that encryption hides everything.** Standard encryption hides the content but not the length. That is in the definition of the security of most schemes.
- **Compressing a secret once per message.** A secret that is the same in every message gives the attacker the repeats he needs. Mask it, or rotate it.
- **Fixing one protocol only.** The leak follows the data. If a secret and chosen data are compressed together at any layer, the channel is there.

## References

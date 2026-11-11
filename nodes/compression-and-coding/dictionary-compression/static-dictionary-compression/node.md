---
tag: KH1XCA
kind: concept
slug: static-dictionary-compression
name: Static dictionary compression
aliases:
- preset dictionary compression
area: compression-and-coding/dictionary-compression
level: intro
summary: Dictionary compression with a dictionary that is fixed before coding and that both sides know, either agreed in advance or sent once.
prereqs: [dictionary-based-compression]
see_also: [adaptive-dictionary-compression, optimal-parsing, greedy-parsing, dag-shortest-paths, brotli, zstandard, deflate, byte-pair-encoding]
sources:
  - book: isbn:9780139119910
    title: Timothy C. Bell, John G. Cleary and Ian H. Witten, Text Compression, Prentice Hall, 1990
    locator: the chapter on dictionary techniques (static and semi-adaptive dictionaries, greedy and optimal parsing)
  - book: isbn:9780128094747
    title: Khalid Sayood, Introduction to Data Compression, fifth edition, Morgan Kaufmann, 2017
    locator: Chapter 5, Dictionary Techniques (the section on static dictionaries and digram coding)
  - url: https://www.rfc-editor.org/rfc/rfc1950
    title: P. Deutsch and J-L. Gailly, RFC 1950, ZLIB Compressed Data Format Specification version 3.3, May 1996
    locator: Section 2.2 (FLG bit 5 FDICT and the DICTID field) and Section 2.3 (an unknown dictionary is an error)
  - url: https://www.rfc-editor.org/rfc/rfc7932
    title: J. Alakuijala and Z. Szabadka, RFC 7932, Brotli Compressed Data Format, July 2016
    locator: Section 8, Static Dictionary; Appendix A (the dictionary data) and Appendix B (the word transforms)
  - url: https://www.rfc-editor.org/rfc/rfc8878
    title: Y. Collet and M. Kucherawy, RFC 8878, Zstandard Compression and the 'application/zstd' Media Type, February 2021
    locator: Section 3.1.1.1.3 Dictionary_ID, Section 5 Dictionary Format, Section 6 Use of Dictionaries
  - url: https://www.rfc-editor.org/rfc/rfc7541
    title: R. Peon and H. Ruellan, RFC 7541, HPACK, Header Compression for HTTP/2, May 2015
    locator: Section 2.3.1 Static Table and Appendix A, Static Table Definition
---

Static dictionary compression is [dictionary-based compression](/dictionary-based-compression/) with a dictionary that does not change while a message is coded. The encoder and the decoder get the same dictionary before the message: it is part of the format, it is agreed between the two sides, or it is sent once at the start. A static dictionary helps most on short messages of a known kind, where an [adaptive dictionary](/adaptive-dictionary-compression/) has seen too little text to find repeats.

## In plain words

Two people who send each other many short notes can agree on a list of common words and phrases before they start. Each note then uses the number of a phrase in place of the phrase. The list costs nothing per note, because both people already have it.

The list must fit the notes. A list of English words does not help with notes full of numbers. So a good list is made from many sample notes of the same kind.

The list does not grow while a note is coded. A word that is not in the list must be spelled out letter by letter, or the method must also copy from the earlier part of the same note.

## The idea

Let $D$ be a fixed set of strings over the alphabet $\Sigma$, with all single symbols in $D$ so that every text can be coded. The encoder cuts the text $T$ into phrases from $D$ and writes the code of each phrase. Since $D$ does not depend on $T$, the decoder needs no information about $D$ from the message.

**Three ways to fix the dictionary.**

- **Built into the format.** The dictionary is part of the specification, and every encoder and decoder holds a copy.
- **Agreed out of band.** The two sides share a dictionary for one application, and each message names it by an identifier. A message that names a dictionary the decoder does not have cannot be decoded.
- **Semi-static.** The encoder chooses a dictionary for this message, sends it first, and then codes the message with it. The cost of sending $D$ is part of the output. [Byte pair encoding](/byte-pair-encoding/), [Re-Pair](/re-pair/) and other [grammar-based](/grammar-based-compression/) methods are of this kind.

**Parsing.** With $D$ fixed, the cheapest parse is a shortest path in a DAG on the positions $1, \ldots, n+1$ (see [optimal parsing](/optimal-parsing/)). [Greedy parsing](/greedy-parsing/) is faster but can lose: with $D = \{a, b, ab, bbbb\}$ and $T = abbbb$ it takes four phrases where two are enough. Greedy parsing gives the fewest phrases when $D$ has the *suffix property*: every suffix of a word in $D$ is also in $D$. The reason: if greedy is at position $g$ and another parse has a phrase that starts at or before $g$ and ends after $g$, the part of that phrase from $g$ on is in $D$, so greedy reaches at least as far with its next phrase. The LZ77 dictionary of all earlier substrings has this property, and the counterexample above does not ($bbbb$ is in $D$ but $bbb$ is not).

**Static and adaptive together.** Most modern formats with a static dictionary also have an adaptive part. The static dictionary is a block of text that sits before the message, and back-references can point into it, as into any earlier text. This gives the benefit of known content at the start of a message, and the adaptive part takes over as the message grows.

**Training.** A dictionary for a class of messages is made from samples. A simple method takes the substrings that occur in many samples and that save the most bytes, up to a size limit. The Zstandard tools have a `--train` mode for this. A trained dictionary that does not fit the data costs nothing in the output but gives no gain.

## Examples

**Greedy against optimal.** With $D = \{a, b, ab, bbbb\}$, all codes of 2 bits, and $T = abbbb$, the greedy parse $ab \cdot b \cdot b \cdot b$ costs 8 bits and the optimal parse $a \cdot bbbb$ costs 4 bits. Add $bbb$ and $bb$ to $D$ to get the suffix property; then the greedy parse is $ab \cdot bbb$, two phrases, as good as the optimum.

**zlib preset dictionary.** In the zlib format (RFC 1950), bit 5 of the FLG byte is FDICT. When it is set, a 4-byte DICTID follows the header; it is the Adler-32 checksum of the dictionary. The compressor fills the window with the dictionary before it codes the data, so the first [back-references](/back-reference/) can point into it. A DEFLATE distance is at most 32,768, so only the last 32 KiB of a preset dictionary can be reached. The decompressor must return an error if it does not know the dictionary.

**Brotli built-in dictionary.** Brotli (RFC 7932) has a dictionary of 122,784 bytes in the specification (Appendix A). It holds words of length 4 to 24. A back-reference with a distance larger than the largest distance into the window refers to the dictionary: the copy length gives the word length, and the extra distance selects a word and one of 121 *transforms* (Appendix B), for example "add a space after the word" or "make the first letter upper case".

**Zstandard dictionaries.** A Zstandard frame header can hold a Dictionary_ID (RFC 8878, Section 3.1.1.1.3). The dictionary (Section 5) holds content that acts as earlier text and can also hold entropy tables, so even the first block of a frame can use tuned Huffman and FSE tables. The dictionary is agreed out of band; Zstandard does not send it in the frame.

**HPACK.** HTTP/2 header compression (RFC 7541) has a static table of 61 common header fields, such as `:method: GET`, that a header block can name by index. It also has a dynamic table of recent fields. HPACK does not copy substrings; it replaces whole header fields by indexes.

## Where it is used

- **Short messages of a known kind.** Web pages and HTTP headers (Brotli, HPACK), small records in a database or a log, and many small messages between the same two services (Zstandard dictionaries, zlib preset dictionaries).
- **Text with a fixed vocabulary.** Word-based coders and digram coders for natural language, and token tables in program file formats.
- **Semi-static coding.** Grammar compressors such as [Re-Pair](/re-pair/) and the vocabulary of [byte pair encoding](/byte-pair-encoding/) in language-model tokenizers, where the dictionary is made once from the data and then stored with it.

## References

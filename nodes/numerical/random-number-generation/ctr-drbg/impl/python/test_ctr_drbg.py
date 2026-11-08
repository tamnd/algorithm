# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ctr-drbg/. The authors are listed in prov/D8PPZT.jsonl.

import pytest

from ctr_drbg import (MAX_REQUEST_BITS, SBOX, CtrDRBG, ReseedRequired, aes_encrypt, aes_expand_key,
                      bcc, block_cipher_df)

h = bytes.fromhex


def test_aes_fips197_appendix_c():
    pt = h("00112233445566778899aabbccddeeff")
    assert aes_encrypt(bytes(range(16)), pt).hex() == "69c4e0d86a7b0430d8cdb78070b4c55a"
    assert aes_encrypt(bytes(range(24)), pt).hex() == "dda97ca4864cdfe06eaf70a0ec0d7191"
    assert aes_encrypt(bytes(range(32)), pt).hex() == "8ea2b7ca516745bfeafc49904b496089"


def test_aes_fips197_appendix_b_and_sbox():
    key = h("2b7e151628aed2a6abf7158809cf4f3c")
    assert aes_encrypt(key, h("3243f6a8885a308d313198a2e0370734")).hex() == "3925841d02dc09fbdc118597196a0b32"
    assert aes_expand_key(key)[10] == list(h("d014f9a8c9ee2589e13f0cc8b6630ca6"))
    assert (SBOX[0x00], SBOX[0x01], SBOX[0x53], SBOX[0xFF]) == (0x63, 0x7C, 0xED, 0x16)
    assert sorted(SBOX) == list(range(256))


# Vectors from the NIST CAVP file drbgtestvectors.zip (CAVS 14.3, CTR_DRBG.rsp), COUNT = 0 of each section.
# Procedure: instantiate, [reseed], generate, generate; ReturnedBits is the output of the second generate.
# Fields: keylen, use_df, entropy, nonce, personalization, (reseed entropy, reseed additional) or None,
# (additional 1, additional 2), expected.
CAVP = [
    (16, True, "890eb067acf7382eff80b0c73bc872c6", "aad471ef3ef1d203", "", None, ("", ""),
     "a5514ed7095f64f3d0d3a5760394ab42062f373a25072a6ea6bcfd8489e94af6cf18659fea22ed1ca0a9e33f718b115ee536b12809c31b72b08ddd8be1910fa3"),
    (16, True, "cae48dd80d298103ef1ec0bf1bb96270", "d827f91613e0b47f", "cc928f3d2df31a29f4e444f3df08be21", None,
     ("7eaa1bbec79393a7f4a8227b691ecb68", "6869c6c7b9e6653b3977f0789e94478a"),
     "920132cd284695b868b5bc4b703afea4d996624a8f57e9fbf5e793b509cb15b4beaf702dac28712d249ae75090a91fd35775294bf24ddebfd24e45d13f4a1748"),
    (32, False, "df5d73faa468649edda33b5cca79b0b05600419ccb7a879ddfec9db32ee494e5531b51de16a30f769262474c73bec010", "", "", None, ("", ""),
     "d1c07cd95af8a7f11012c84ce48bb8cb87189e99d40fccb1771c619bdf82ab2280b1dc2f2581f39164f7ac0c510494b3a43c41b7db17514c87b107ae793e01c5"),
    (32, True, "36401940fa8b1fba91a1661f211d78a0b9389a74e5bccfece8d766af1a6d3b14", "496f25b0f1301b4f501be30380a137eb", "", None, ("", ""),
     "5862eb38bd558dd978a696e6df164782ddd887e7e9a6c9f3f1fbafb78941b535a64912dfd224c6dc7454e5250b3d97165e16260c2faf1cc7735cb75fb4f07e1d"),
    (32, True, "87b56e964eba227154724bb9484b812d3e2c0c43b3d17f6098d9526e16e6d0ef", "9bea6a7ff2358df142e6c23e2157fb83",
     "9860b432edd58d1ccbfeecbce99ffaee7d935a614860d4e965bd67041403096b", None,
     ("99a5cc87924e8ea65a596f81fd17d63f5b4542fe6e8e1511b5d35c835dfadb0b", "9a8dec54734a34582a2332f3452e82313524c3e0dfb485faeac6ca5fc0ff504d"),
     "dbc6a2330b19b5cddd8cd6392ec1fb508678c805e87d1aca07ac265007632503044a00610c79d98375afa7ab4cca1a90989cbfe7c674af5d823ced11c47e9af6"),
    (16, True, "0f65da13dca407999d4773c2b4a11d85", "5209e5b4ed82a234", "", ("1dea0a12c52bf64339dd291c80d8ca89", ""), ("", ""),
     "2859cc468a76b08661ffd23b28547ffd0997ad526a0f51261b99ed3a37bd407bf418dbe6c6c3e26ed0ddefcb7474d899bd99f3655427519fc5b4057bcaf306d4"),
    (16, True, "e14ed7064a97814dd326b9a05bc44543", "876240c1f7de3dba", "26ccf56848a048721d0aad87d6fc65f0",
     ("7ec4ac660fa0bbfa66ac3802e511901f", "8835d28e7f85a4e95087bdd1bb7ad57e"),
     ("2a9bd50bbb20fefe24649f5f80eede66", "f7ce3d5c6c381e56b25410c6909c1074"),
     "d2f3130d309bed1da65545b9d793e035fd2564303d1fdcfb6c7fee019500d9f5d434fab2d3c8d15e39a25f965aaa804c7141407e90c4a86a6c8d303ce83bfb34"),
    (32, False, "e4bc23c5089a19d86f4119cb3fa08c0a4991e0a1def17e101e4c14d9c323460a7c2fb58e0b086c6c57b55f56cae25bad", "", "",
     ("fd85a836bba85019881e8c6bad23c9061adc75477659acaea8e4a01dfe07a1832dad1c136f59d70f8653a5dc118663d6", ""), ("", ""),
     "b2cb8905c05e5950ca31895096be29ea3d5a3b82b269495554eb80fe07de43e193b9e7c3ece73b80e062b1c1f68202fbb1c52a040ea2478864295282234aaada"),
    (32, False, "ae7ebe062971f5eb32e5b21444750785de816595ad2cbe80a209c8f8ab04b5468166de8c6ae522d8f10b56386a3b424f", "",
     "55860dae57fcac297087c137efb796878a75868f6e7681114e9b73ed0c67e3c62bfc9f5d77e8caa59bcdb223f4ffd247",
     ("a42407931bfeca70e6ee5dd197021a129525051c07468e8b25587c5ad50abe9204e882fe847b8fd47cf7b4360e5aa034",
      "ee4c88d1eb05f4853663eada501d2fc4b4984b283a88db579af2113031e03d9bc570de943dd168918f3ba8065581fea7"),
     ("4b4b03ef19b0f259dca2b3ee3ae4cd86c3895a784b3d8eee043a2003c08289f8fffdad141e6b1ab2174d8d5d79c1e581",
      "3062b33f116b46e20fe3c354726ae9b2a3a4c51922c8107863cb86f1f0bdad7554075659d91c371e2b11b1e8106a1ed5"),
     "0d270518baeafac160ff1cb28c11ef68712c764c0c01674e6c9ca2cc9c7e0e8accfd3c753635ee070081eee7628af6187fbc2854b3c204461a796cf3f3fcb092"),
    (32, True, "2d4c9f46b981c6a0b2b5d8c69391e569ff13851437ebc0fc00d616340252fed5", "0bf814b411f65ec4866be1abb59d3c32", "",
     ("93500fae4fa32b86033b7a7bac9d37e710dcc67ca266bc8607d665937766d207", ""), ("", ""),
     "322dd28670e75c0ea638f3cb68d6a9d6e50ddfd052b772a7b1d78263a7b8978b6740c2b65a9550c3a76325866fa97e16d74006bc96f26249b9f0a90d076f08e5"),
]


@pytest.mark.parametrize("keylen,use_df,ent,nonce,pers,reseed,adds,expected", CAVP)
def test_cavp(keylen, use_df, ent, nonce, pers, reseed, adds, expected):
    d = CtrDRBG(keylen, h(ent), h(nonce), h(pers), use_df=use_df)
    if reseed is not None:
        d.reseed(h(reseed[0]), h(reseed[1]))
    n = len(expected) // 2
    d.generate(n, h(adds[0]))
    assert d.generate(n, h(adds[1])).hex() == expected


PRED_RES = [
    ("5d4041942bcf68864a4997d8171f1f9f", "d4f1f4ae08bcb3e1", "", ("", ""),
     ("ef55a769b7eaf03fe082029bb32a2b9d", "8239e865c0a42e14b964b9c09de85a20"),
     "4155320287eedcf7d484c2c2a1e2eb64b9c9ce77c87202a1ae1616c7a5cfd1c687c7a0bfcc85bda48fdd4629fd330c22d0a76076f88fc7cd04037ee06b7af602"),
    ("92898f31fa1cff6d182f260643dff818", "c2a4d972c3b9b697", "ea65ee60264e7eb60e8268c4373c5c0b",
     ("1a40fae3cc6c7ca0f8daba59236dad1d", "9f72766cc746e5ed2e532012bc59318c"),
     ("20728a06f86f8dd441e272b7c42ce810", "3db0f094f305503317863e2208f7a501"),
     "5a3539870f4d22a40924ee71c96fac720ad6f08882d0832873ec3f93d8ab4523f07eac45145e939fb1d676433db6e80888f6da89087742fe1af43fc423c51f68"),
]


@pytest.mark.parametrize("ent,nonce,pers,adds,ents,expected", PRED_RES)
def test_cavp_prediction_resistance_aes128_df(ent, nonce, pers, adds, ents, expected):
    d = CtrDRBG(16, h(ent), h(nonce), h(pers))
    d.generate(64, h(adds[0]), entropy=h(ents[0]))
    assert d.generate(64, h(adds[1]), entropy=h(ents[1])).hex() == expected


def test_acvp_aes256_no_df_long_output():
    # ACVP vector carried in the Go standard library (crypto/internal/fips140test/ctrdrbg_test.go):
    # AES-256 without df, personalization string, reseed with additional input, two 512-byte requests.
    d = CtrDRBG(32, h("9fcbb4ccc0135c484bded061da9fd70748682fe84166b97ff53f9aa1909b2e95d3d529c0f453b3ac575d12aa441cc5cd"),
                personalization=h("2c9fed0b39556cdbe699ebca2a0ec7eecb287e8744475050c572fa8ae9ed0a4a7d6f1cabf1c4278532fb20af7d64bd32"),
                use_df=False)
    d.reseed(h("913c0da19b010eddd55a7a4f3f713eef5b1534d34360a7ec376ae71a6b340043cc7726f762cb853453f399b3a645062a"),
             h("2d9d4ec141a22e6cd2f6ee4f6719cf6bdf95cfe50b8d5ea6c87d38b4b872706fff80b0380bb90e9c42d11d6526e56c29"))
    d.generate(512, h("a642f06d327828f3e84564a3e37d60c157073b95864ca07981b0189668a0d978cd5dc68f06801ceff0dc839a312b028e"))
    out = d.generate(512, h("9db14babfa9107c88ba92073c0b4a65e89147ea06d74b894142979482f452915b35b5636f9b8a951759735ade7c8d5d1"))
    assert out.hex() == "f10c645683ff0131254052ed4c698122b46b563654c29d728ac191ca4aaefe649eefe4c6fc33b25bb739294dd5cf578099f856c98d98000cbf971f1e6ea900822ff8c110118f6520471744d3f8a3f5c7d568494240e57f5488af9c9f9f4e7322f56ccd843c0dbfce9170c02e205389420527f23edb3369d9fcc5e34901b5ba4eb71b973fc7982ffe0899ff7fe53ee0c4f51a3ef93ef9c6d4d279dd7536f8776be94aaa05e89ef6e6aee8832b4b42ffca5fb91ec0273f9ef945865512889b0c5ee141d1b38df827d2a694835561628c6f9b093a01a835f07adbb9e03febf93389e8f3b86e1e0abf1f9958fa286ad995289c2f606d1a9043a166c1afe8d00769c712650819c9068a4bd22717c98338395a7ba6e95b5178bfbf4efb0f05a91713ba8bf2127a6ba1edfa6d1cab05c03ee0d2afe1da4eb8f2c579ec872ff4b602027ef4bdcf2f4b01423f8e600a13d7cacb6ab83263ba58f907694af614a6724fd0e4c627a0d91ddc6716c697face6f4808a4f37b731de4e0cd4766ceadaaaf47992505299c72ac1a6e9a8335b8d7e501b3841188d0da4de5267674444dc2b0cf9f010756fa865a25ca3f1b24c34e845b2259926b6a867a7684de68a6137c4fb0f47a2e54ae9e6455beba0b0a9629644fe9e378ee95386443ba977124ffd1192e9f460684c7b09fa99f5f93f04f56fd7955e042187887ce696f1934017e458b16b5c9"


def test_update_and_generate_match_definition():
    d = CtrDRBG(16, bytes(range(32)), use_df=False)
    key, V = d.key, d.V
    blocks = [aes_encrypt(key, ((V + j) % 2 ** 128).to_bytes(16, "big")) for j in (1, 2, 3, 4, 5)]
    out = d.generate(40)  # three blocks of output, then an Update with two more blocks
    assert out == b"".join(blocks)[:40]
    temp = blocks[3] + blocks[4]
    assert (d.key, d.V, d.reseed_counter) == (temp[:16], int.from_bytes(temp[16:], "big"), 2)


def test_counter_wraps_modulo_2_128():
    d2 = CtrDRBG(16, bytes(range(32)), use_df=False)
    key = d2.key
    d2.V = 2 ** 128 - 1
    assert d2.generate(16) == aes_encrypt(key, bytes(16))


def test_block_cipher_df_structure():
    # BCC is CBC-MAC with zero IV; the df output depends on input length and on the requested length
    k = aes_expand_key(bytes(range(16)))
    b1, b2 = h("00" * 16), h("11" * 16)
    assert bcc(k, b1 + b2) == aes_encrypt(bytes(range(16)), bytes(x ^ y for x, y in zip(aes_encrypt(bytes(range(16)), b1), b2)))
    assert block_cipher_df(16, b"abc", 32)[:16] != block_cipher_df(16, b"abc", 16)
    assert block_cipher_df(16, b"abc\x00", 32) != block_cipher_df(16, b"abc", 32)
    assert len(block_cipher_df(32, b"", 48)) == 48


def test_reseed_interval_and_limits():
    d = CtrDRBG(16, bytes(32), use_df=False, reseed_interval=2)
    d.generate(16)
    d.generate(16)
    with pytest.raises(ReseedRequired):
        d.generate(16)
    d.reseed(bytes(range(32)))
    d.generate(16)
    with pytest.raises(ValueError):
        d.generate(MAX_REQUEST_BITS // 8 + 1)
    with pytest.raises(ValueError):
        CtrDRBG(16, bytes(31), use_df=False)  # no df needs exactly seedlen bytes of full-entropy input
    with pytest.raises(ValueError):
        CtrDRBG(32, bytes(16), bytes(8))  # 128 entropy bits for a 256-bit strength


def test_byte_frequencies_chi_square():
    # 65536 bytes; chi-square with 255 degrees of freedom, 0.999 quantile 330.52
    d = CtrDRBG(16, bytes(range(16)), bytes(8))
    data = b"".join(d.generate(4096) for _ in range(16))
    counts = [0] * 256
    for byte in data:
        counts[byte] += 1
    e = len(data) / 256
    chi2 = sum((c - e) ** 2 / e for c in counts)
    assert chi2 < 330.52

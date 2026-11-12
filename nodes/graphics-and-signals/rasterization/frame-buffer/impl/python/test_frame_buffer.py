# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frame-buffer/. The authors are listed in prov/RBDXB5.jsonl.

import random

import pytest

from frame_buffer import FrameBuffer


def pixels_from_bytes(fb: FrameBuffer) -> dict[tuple[int, int], tuple[int, ...]]:
    """Decode the buffer independently: walk the bytes row by row, C bytes per pixel, skipping the pad."""
    out = {}
    for j in range(fb.height):
        for i in range(fb.width):
            base = j * fb.pitch + i * fb.channels
            out[(i, j)] = tuple(fb.data[base + k] for k in range(fb.channels))
    return out


def pad_bytes(fb: FrameBuffer) -> bytes:
    return b"".join(bytes(fb.data[j * fb.pitch + fb.width * fb.channels:(j + 1) * fb.pitch]) for j in range(fb.height))


def test_example() -> None:
    fb = FrameBuffer(3, 2, channels=3)  # 9 pixel bytes per row, padded to a pitch of 12
    assert fb.pitch == 12 and len(fb.data) == 24
    fb.clear((0, 0, 0))
    assert fb.write_pixel(2, 1, (255, 0, 0))
    assert fb.offset(2, 1) == 18 and fb.data[18:21] == bytes((255, 0, 0))
    assert fb.fill_rect(0, 0, 2, 1, (0, 0, 255)) == 2
    assert fb.data.hex() == "0000ff0000ff000000000000" + "000000000000ff0000000000"
    assert fb.row(1) == bytes((0, 0, 0, 0, 0, 0, 255, 0, 0))
    assert not fb.write_pixel(3, 0, (1, 1, 1)) and fb.read_pixel(3, 0) is None
    assert fb.read_pixel(0, 1) == (0, 0, 0)
    # the sizes of common buffers at 4 bytes per pixel, and the scanout rate at 60 frames per second
    assert FrameBuffer(1920, 0).pitch * 1080 == 8_294_400
    assert 3840 * 4 * 2160 == 33_177_600 and 1920 * 1080 * 4 * 60 == 497_664_000


def test_bad_arguments() -> None:
    with pytest.raises(ValueError):
        FrameBuffer(4, 4, channels=4, pitch=15)
    fb = FrameBuffer(2, 2)
    with pytest.raises(ValueError):
        fb.write_pixel(0, 0, (1, 2, 3))
    with pytest.raises(ValueError):
        fb.write_pixel(0, 0, (1, 2, 3, 256))


def test_random_operations_against_a_dict_model() -> None:
    rng = random.Random(1973)
    for trial in range(60):
        w, h, c = rng.randint(1, 9), rng.randint(1, 7), rng.choice((1, 2, 3, 4))
        pitch = rng.choice((None, w * c, w * c + rng.randint(1, 5)))
        fb = FrameBuffer(w, h, channels=c, pitch=pitch, align=rng.choice((1, 4, 8)))
        model = {(i, j): (0,) * c for i in range(w) for j in range(h)}

        def color() -> tuple[int, ...]:
            return tuple(rng.randrange(256) for _ in range(c))

        for _ in range(150):
            op = rng.random()
            i, j = rng.randint(-2, w + 1), rng.randint(-2, h + 1)
            if op < 0.45:
                col = color()
                inside = (i, j) in model
                assert fb.write_pixel(i, j, col) == inside
                if inside:
                    model[(i, j)] = col
            elif op < 0.75:
                assert fb.read_pixel(i, j) == model.get((i, j))
            elif op < 0.95:
                i1, j1 = rng.randint(-2, w + 2), rng.randint(-2, h + 2)
                col = color()
                cells = [(x, y) for x in range(i, i1) for y in range(j, j1) if (x, y) in model]
                assert fb.fill_rect(i, j, i1, j1, col) == len(cells)
                for p in cells:
                    model[p] = col
            else:
                col = color()
                fb.clear(col)
                model = {p: col for p in model}
            fb.check_invariant()
        assert pixels_from_bytes(fb) == model
        assert pad_bytes(fb) == bytes(len(pad_bytes(fb)))
        for j in range(h):
            assert fb.row(j) == b"".join(bytes(model[(i, j)]) for i in range(w))


def test_offsets_are_a_bijection_onto_the_pixel_bytes() -> None:
    rng = random.Random(1971)
    for _ in range(500):
        w, h, c = rng.randint(1, 12), rng.randint(1, 12), rng.randint(1, 4)
        fb = FrameBuffer(w, h, channels=c, pitch=w * c + rng.randint(0, 6))
        used = [fb.offset(i, j) + k for j in range(h) for i in range(w) for k in range(c)]
        assert len(set(used)) == w * h * c
        assert all(0 <= u < len(fb.data) and u % fb.pitch < w * c for u in used)

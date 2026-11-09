"""Text Editor in the PicoDeck simulator. Moved from PicoDeck's tests/e2e
(test_idle_apps.py, test_terminal.py) when the app got this repo.

It starts in the file browser; Esc there opens a new, empty file."""
import time

from conftest import APP, stage


def _presents_while_idle(sim, seconds=2.0):
    start = sim.present_count()
    time.sleep(seconds)
    return sim.present_count() - start


def _lit_changed_by(sim, key):
    before = sim.screenshot_pil().convert("RGB").tobytes()
    seq = sim.keypress(key)["input_seq"]
    sim.wait_input_consumed(seq)
    time.sleep(0.3)
    return sim.screenshot_pil().convert("RGB").tobytes() != before


def _open_new_file(sim):
    stage(sim)
    sim.launch_app(APP)
    time.sleep(0.6)
    sim.keypress("esc")     # the file browser it starts in
    time.sleep(0.3)


# Waiting for a key must not redraw and flush the screen flat out: a loop with
# no wait keeps Core 0 and the panel's bus busy on a battery device.

def test_editor_sleeps_until_a_key(simulator):
    _open_new_file(simulator)
    # Twice a second, for the cursor's blink.
    assert _presents_while_idle(simulator) <= 8
    assert _lit_changed_by(simulator, "x")
    simulator.exit_app()
    simulator.wait_for_exit(timeout=10)


def test_editor_cursor_still_blinks_while_idle(simulator):
    _open_new_file(simulator)
    frames = {simulator.screenshot_pil().convert("RGB").tobytes()}
    for _ in range(12):
        time.sleep(0.15)
        frames.add(simulator.screenshot_pil().convert("RGB").tobytes())
    assert len(frames) >= 2
    simulator.exit_app()
    simulator.wait_for_exit(timeout=10)


def _typed_line_shows(sim, first_row_y, last_row):
    """Type more lines than fit, then one more of marks: its row must show."""
    _open_new_file(sim)
    for _ in range(last_row + 6):
        seq = sim.keypress("enter")["input_seq"]
        sim.wait_input_consumed(seq)
    before = sim.screenshot_pil().convert("RGB")
    for ch in "#####":
        seq = sim.keypress(ch)["input_seq"]
        sim.wait_input_consumed(seq)
    time.sleep(0.3)
    after = sim.screenshot_pil().convert("RGB")
    y0 = first_row_y + last_row * 12
    changed = sum(1 for y in range(y0, y0 + 12) for x in range(320)
                  if before.getpixel((x, y)) != after.getpixel((x, y)))
    sim.exit_app()
    sim.wait_for_exit(timeout=10)
    return changed


def test_editor_shows_the_row_it_is_typing_on(simulator):
    """It asked for 24 rows inside bounds that hold 23, so its last row never
    drew: the line being typed at the bottom of the window was invisible."""
    assert _typed_line_shows(simulator, 21, 22) > 20

import asyncio, time

marks = {}                                    # trick 3: time every link of the chain

def mark(name):
    marks.setdefault(name, time.perf_counter())

async def connect(name):                      # stand-in for opening a TLS connection to an API (slow)
    await asyncio.sleep(0.3)
    return name

warm = {}

def warm_up():                                # trick 2: start opening connections the moment the button is pressed
    for name in ("speech_to_text", "language_model", "voice"):
        warm[name] = asyncio.ensure_future(connect(name))

async def transcribe():                       # stand-in: speech to text, then the model, then the voice
    await warm["speech_to_text"]; await asyncio.sleep(0.25); mark("text")
    await warm["language_model"]; await asyncio.sleep(0.8); mark("first_character")
    await warm["voice"]; await asyncio.sleep(0.6); mark("voice")

async def main():
    mark("press"); warm_up()
    await asyncio.sleep(1.0)                  # the person is talking
    mark("release")
    job = asyncio.ensure_future(transcribe()) # trick 1: start the work the moment the button is released
    await asyncio.sleep(0.1)
    pressed_again = False                     # set True if the finger comes back: throw the work away
    if pressed_again:
        job.cancel(); return
    await job
    t0 = marks["release"]
    for k in ("text", "first_character", "voice"):
        print(f"{k:16s} {marks[k] - t0:.2f} s after release")

asyncio.run(main())

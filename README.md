#

## Install

There is a requirements.txt to setup python.

Be warn, the libraries are HUGE.

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Structure

The system is in multiple part. The core design is that there is a
first program that generates the information about an animation. This
is the code that a user would write in order to generate their own
animation. That code outputs a JSON that describe the animation.

Then there is a renderer that will take that JSON and produce a video.

## Running

```bash
python3 MST.py myMST.json
```

## Rendering

```bash
python3 Renderer/Renderer.py myMST.json
ls media/videos/*/Renderer.mp4
```

## Support and Implementation

See Implementation.md

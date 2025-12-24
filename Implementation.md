## Architecture

The architecture of the project is built out of two main components.

The animations are written by the end-user. They are written using an
Animation library. That animation library will define components like
Graphs, TTS, Arrays, or what not. When the animation code is run,
it outputs a description of the animation encoded in a JSON format.

That JSON description is given to the Renderer. It will parse the JSON
and generate the different frames of the animation using Manim for most
of the visual elements and with coqui-ai/TTS for the voice
generation. It outputs a video.

### Why separate in two?

We separate into two components for multiple reasons:

1. It makes the development of the animations a lot easier. You can
   write the code for the animation as well as you would write
   the algorithm you are generating.

2. It allows to work on the Renderer independently from the animation.

3. It enables the renderer to be configured for a particular purpose.
   You could easily take an animation and re-render it at a different
   resolution, or in a different format.
   
4. It enables styling the animation. (Even though this is not
   supported yet). Eventually you should be able to have style sheets
   applied to the renderer for default values and for visual
   attributes. Just like you apply CSS on a webpage to style it, you
   would be able to apply a style to your animation. At a basic level
   you would be able to change background color or fonts. But
   eventually, you should be able to express your algorithm in terms of
   states, say vertices being marked, and the visual interpretation of
   that would be done at styling time.

## Organization

The animation library is in `Animations/` while the renderer is in
`Renderer`.

You will see that the files in there are named in a very similar
way. This is because most of the `AnimatedObject`s are encoded to JSON
in the Animation library and then decoded in the Renderer. So there is
a one-to-one mapping between the objects in the library and the
objects in the renderer

There are two main parts to the JSON intermediate representation. The
representation is a dictionary that contains two parts:

1. initial state of the world at the beginning of the animation. The
   world is described by a set of objects with names. They can be of a
   whole lot of types.

2. animations that describe the modifications of the state of the
   object. The animation data is organized in groups. In JSON terms,
   animations is a list of lists of animation steps.  The animations
   that are happening in a group are simultaneous. Let's say you want to
   change the color of vertices A, B and C. You could put them in a
   single group and all three vertices would change color at the same
   time. You could put them in three different groups and they would
   change color one at a time. Or you could put A in one group and B
   and C in a subsequent group: A would change color first, and then B
   and C would change color at the same time.

Note that TTS is an animation object like a graph is. Though because
of implementation details, TTS can only say a single thing within an
animation group.

## Animation library

In the animation library, everything that will get rendered is a child
object of `AnimatedObject`. The animation objects have an initial
state. And they will expose a set of functions that enable to modify
the animated object. The `AnimatedObject` store the changes to the
object in a buffer of some sort and that buffer can be flushed to
output the animation.

In other words, if you want to group multiple animations, you only
flush between groups.

At the moment only 2 types of objects are defined:


### NetworkXGraph

It is constructed by passing a NetworkX graph object to it. Note that
the object can be given position in order to control where on the
frame the vertices will be.

The object currently only supports 2 operations, coloring vertices, and
coloring edges.

### TTS

Currently only supports a single operation `say`ing a piece of text.

## Renderer

The renderer is the more complex piece of software. It needs to
interact with manim to make the thing work. It deserialize first the
object in their initial state and build mobjects. These mobjects it
creates are all inherited from `AnimatedObject` (the renderer version
of the object).

Note that anything that renders in manim is a mobject,
including groups of things. So in a graph, a vertex is a mobject, its
label is a mobject, and there is probably a group that contains
both. (It's a bit like SVG in a way.)





### TTS

TTS is a bit complicated. It turns out that manim has minimal support
for sound processing. So the TTS object uses coqui-ai/TTS to generate
wav file for the text that is being said. And that sound is then
played.

Except there is no good way in Manim to do that within the animation
framework. So the solution for synchornization to work is to play the
sound and insert a manim wait animation object. 

Also for stupid caching reasons, a fake text is inserted but made
invisible to avoid breaking caching. That means that any animation (a
video file in manim internal structure) that uses TTS can't be cached
and has to be regenerated. There is probably a work around; but
haven't found one yet.

This is why (somehow) you can't play two sounds at teh same time. So
in particular, you can't play 2 TTS messages.x


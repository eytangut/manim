Troubleshooting
===============

This section covers common issues and their solutions when using Manim.

Installation Issues
-------------------

**FFmpeg not found**

If you get an error about FFmpeg not being found:

On Windows:
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract and add to your PATH
3. Restart your terminal

On macOS:
.. code-block:: bash

    brew install ffmpeg

On Ubuntu/Debian:
.. code-block:: bash

    sudo apt update
    sudo apt install ffmpeg

**LaTeX errors**

If you encounter LaTeX-related errors:

1. Install a LaTeX distribution:
   - Windows: MiKTeX
   - macOS: MacTeX (via ``brew install mactex``)
   - Linux: TexLive (``sudo apt install texlive-full``)

2. Ensure LaTeX is in your PATH
3. Try using ``Text`` instead of ``Tex`` for simple text

Runtime Issues
--------------

**Scene not rendering**

If your scene appears blank or doesn't render:

1. Check that you're calling ``self.add()`` to add objects to the scene
2. Verify object positions aren't outside the frame
3. Check that colors aren't the same as the background

**Performance issues**

For slow rendering:

1. Use lower quality settings during development:
   .. code-block:: bash

       manimgl scene.py MyScene -l  # low quality

2. Reduce the number of points in complex curves
3. Use simpler objects during testing
4. Consider using ``--skip_animations`` (``-s``) to see final frames quickly

**Memory issues**

If you run out of memory:

1. Break complex scenes into smaller parts
2. Use ``self.remove()`` to clean up objects no longer needed
3. Avoid creating too many objects simultaneously

Animation Issues
----------------

**Animations don't play**

1. Ensure you're using ``self.play()`` not just ``self.add()``
2. Check that animation ``run_time`` isn't too small
3. Verify the object exists before animating it

**Objects appear in wrong positions**

1. Use ``.move_to()`` for absolute positioning
2. Use ``.shift()`` for relative positioning
3. Check coordinate system: positive Y is up, positive X is right

**Animations are too fast/slow**

1. Adjust ``run_time`` parameter:
   .. code-block:: python

       self.play(Transform(obj1, obj2), run_time=3)

2. Use rate functions to control timing:
   .. code-block:: python

       self.play(Transform(obj1, obj2), rate_func=smooth)

Common Error Messages
---------------------

**"ModuleNotFoundError: No module named 'manimlib'"**

- Ensure you installed manimgl: ``pip install manimgl``
- If developing, install in editable mode: ``pip install -e .``

**"TypeError: Animation only works for Mobjects"**

- Ensure you're passing Mobject instances, not raw numbers or lists
- Convert to appropriate Mobject types (e.g., ``DecimalNumber`` for numbers)

**"AttributeError: 'str' object has no attribute 'interpolate'"**

- Check that you're passing animation objects to ``self.play()``, not strings
- Ensure proper import of animation classes

Getting Help
------------

If you can't resolve an issue:

1. Check the `GitHub issues <https://github.com/3b1b/manim/issues>`_
2. Ask on the `Discord server <https://discord.com/invite/bYCyhM9Kz2>`_
3. Post on the `r/manim subreddit <https://www.reddit.com/r/manim/>`_
4. Review the `example scenes <https://github.com/3b1b/manim/blob/master/example_scenes.py>`_

When reporting issues, include:
- Your operating system
- Python and manim versions
- Complete error messages
- Minimal code example that reproduces the issue
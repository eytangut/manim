# Troubleshooting Guide

This section covers common issues and their solutions when using Manim.

## Installation Issues

### FFmpeg not found

If you get an error about FFmpeg not being found:

**Windows:**
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract and add to your PATH environment variable
3. Restart your terminal and IDE

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Verification:**
```bash
ffmpeg -version
```

### LaTeX errors

If you encounter LaTeX-related errors when using `Tex` objects:

**Install LaTeX Distribution:**
- **Windows**: [MiKTeX](https://miktex.org/)
- **macOS**: MacTeX via `brew install mactex`
- **Linux**: TexLive via `sudo apt install texlive-full`

**Common Solutions:**
1. Ensure LaTeX is in your PATH
2. Try using `Text` instead of `Tex` for simple text
3. For simple math, use `MathTex` instead of `Tex`

**Test LaTeX Installation:**
```bash
latex --version
```

### Python Package Issues

**ModuleNotFoundError: No module named 'manimlib'**

1. Ensure you installed manimgl: `pip install manimgl`
2. If developing from source: `pip install -e .`
3. Check your Python environment: `which python` and `python --version`

**Dependency Conflicts:**

1. Create a virtual environment:
   ```bash
   python -m venv manim_env
   source manim_env/bin/activate  # On Windows: manim_env\Scripts\activate
   pip install manimgl
   ```

2. Update outdated packages:
   ```bash
   pip install --upgrade manimgl
   ```

## Runtime Issues

### Scene not rendering

If your scene appears blank or doesn't render:

**Check Object Addition:**
```python
# Wrong - object not added to scene
circle = Circle()
self.play(Create(circle))  # Won't show anything

# Correct - add object first
circle = Circle()
self.add(circle)  # or use self.play(Create(circle))
```

**Verify Object Positions:**
```python
# Check if objects are in frame
circle = Circle().move_to(UP * 10)  # Might be outside visible area
print(circle.get_center())  # Debug position
```

**Color Visibility:**
```python
# Make sure colors aren't same as background
circle = Circle(color=BLACK)  # Won't show on black background
```

### Performance issues

For slow rendering or long build times:

**Use Lower Quality During Development:**
```bash
manimgl scene.py MyScene -l  # Low quality
manimgl scene.py MyScene -m  # Medium quality  
manimgl scene.py MyScene     # High quality (default)
```

**Optimization Techniques:**
1. Reduce points in complex curves:
   ```python
   # Instead of default high resolution
   curve = ParametricCurve(func, t_range=[0, 1])
   
   # Use fewer points for development
   curve = ParametricCurve(func, t_range=[0, 1], step_size=0.1)
   ```

2. Use simpler objects during testing
3. Skip animations to see final frames: `--skip_animations` or `-s`
4. Preview specific parts: `--start_at_animation_number N`

**System-Specific Tips:**
- **Windows**: Use Windows Subsystem for Linux (WSL) for better performance
- **macOS**: Ensure you have sufficient memory for complex scenes
- **Linux**: Consider using GPU acceleration if available

### Memory issues

If you run out of memory with complex scenes:

**Memory Management:**
```python
class MemoryEfficientScene(Scene):
    def construct(self):
        # Create objects as needed
        for i in range(100):
            dot = Dot()
            self.play(Create(dot), run_time=0.1)
            
            # Remove when no longer needed
            if i > 10:
                self.remove(self.mobjects[-11])
```

**Best Practices:**
1. Break complex scenes into smaller parts
2. Use `self.remove()` to clean up objects
3. Avoid creating too many objects simultaneously
4. Use object pooling for repeated elements

## Animation Issues

### Animations don't play

**Common Causes and Solutions:**

1. **Missing self.play():**
   ```python
   # Wrong
   circle = Circle()
   self.add(circle)  # Static - no animation
   
   # Correct
   circle = Circle()
   self.play(Create(circle))  # Animated
   ```

2. **Zero or negative run_time:**
   ```python
   # Wrong
   self.play(Transform(obj1, obj2), run_time=0)
   
   # Correct
   self.play(Transform(obj1, obj2), run_time=1)
   ```

3. **Object doesn't exist:**
   ```python
   # Wrong - using undefined object
   self.play(Create(undefined_circle))
   
   # Correct - create object first
   circle = Circle()
   self.play(Create(circle))
   ```

### Objects appear in wrong positions

**Positioning Methods:**

1. **Absolute positioning with move_to():**
   ```python
   circle.move_to(UP * 2 + RIGHT * 3)  # Specific coordinates
   circle.move_to([1, 2, 0])            # Direct coordinates
   ```

2. **Relative positioning with shift():**
   ```python
   circle.shift(UP + RIGHT)  # Move relative to current position
   ```

3. **Edge positioning:**
   ```python
   text.to_edge(UP)     # Move to top edge
   text.to_corner(UL)   # Move to upper-left corner
   ```

**Coordinate System Reference:**
- Positive Y is up, negative Y is down
- Positive X is right, negative X is left
- Center of screen is [0, 0, 0]
- Default frame width is 14.22, height is 8

### Animation timing issues

**Animations too fast/slow:**

1. **Adjust run_time:**
   ```python
   # Slow animation
   self.play(Transform(obj1, obj2), run_time=3)
   
   # Fast animation  
   self.play(Transform(obj1, obj2), run_time=0.5)
   ```

2. **Use rate functions:**
   ```python
   from manimlib import *
   
   # Smooth easing
   self.play(Transform(obj1, obj2), rate_func=smooth)
   
   # Linear timing
   self.play(Transform(obj1, obj2), rate_func=linear)
   
   # Custom rate function
   def custom_rate(t):
       return t * t  # Quadratic easing
   
   self.play(Transform(obj1, obj2), rate_func=custom_rate)
   ```

**Available Rate Functions:**
- `smooth`: Default smooth easing
- `linear`: Constant speed
- `rush_into`: Fast start, slow end
- `rush_from`: Slow start, fast end
- `slow_into`: Very slow start
- `double_smooth`: Extra smooth transitions

## Common Error Messages

### TypeError: Animation only works for Mobjects

**Problem:** Trying to animate non-Mobject types

```python
# Wrong - can't animate raw numbers
number = 5
self.play(Transform(number, 10))

# Correct - use DecimalNumber
number = DecimalNumber(5)
new_number = DecimalNumber(10)
self.play(Transform(number, new_number))
```

### AttributeError: 'str' object has no attribute 'interpolate'

**Problem:** Passing strings instead of animation objects

```python
# Wrong - passing string
self.play("Create(circle)")

# Correct - passing animation object
self.play(Create(circle))
```

### ImportError or ModuleNotFoundError

**Common Solutions:**

1. **Check import statements:**
   ```python
   # Preferred
   from manimlib import *
   
   # Or specific imports
   from manimlib import Scene, Circle, Create
   ```

2. **Verify installation:**
   ```bash
   pip list | grep manim
   python -c "import manimlib; print('Success')"
   ```

### OpenGL or Rendering Errors

**Graphics Issues:**

1. **Update graphics drivers**
2. **Try software rendering:**
   ```bash
   manimgl scene.py MyScene --use_opengl_renderer
   ```

3. **Check system requirements:**
   - OpenGL 3.3+ support
   - Updated graphics drivers
   - Sufficient VRAM for complex scenes

## Getting Help

If you can't resolve an issue:

### Community Resources

1. **GitHub Issues**: [3b1b/manim issues](https://github.com/3b1b/manim/issues)
2. **Discord Server**: [Manim Community Discord](https://discord.com/invite/bYCyhM9Kz2)
3. **Reddit**: [r/manim subreddit](https://www.reddit.com/r/manim/)
4. **Documentation**: [Official Manim Docs](https://docs.manim.community/)

### When Reporting Issues

Include the following information:

**System Information:**
```bash
# Get system info
python --version
pip list | grep manim
# Your operating system and version
```

**Error Details:**
- Complete error messages and stack traces
- Minimal code example that reproduces the issue
- Expected vs. actual behavior
- Screenshots or videos if relevant

**Example Bug Report Template:**
```
**Environment:**
- OS: [e.g., Windows 11, macOS 12.0, Ubuntu 20.04]
- Python: [e.g., 3.9.7]
- Manim: [version number]

**Issue:**
[Clear description of the problem]

**Code:**
```python
# Minimal example that reproduces the issue
```

**Error:**
```
[Complete error message]
```

**Expected Behavior:**
[What you expected to happen]
```

### Debugging Tips

1. **Use print statements:**
   ```python
   print(f"Object position: {circle.get_center()}")
   print(f"Object in scene: {circle in self.mobjects}")
   ```

2. **Check object properties:**
   ```python
   print(f"Color: {circle.color}")
   print(f"Radius: {circle.radius}")
   ```

3. **Test step by step:**
   - Comment out complex parts
   - Test with simple objects first
   - Add complexity gradually

4. **Use the debugger:**
   ```python
   import pdb; pdb.set_trace()  # Python debugger
   ```

Remember: Most issues have simple solutions. Don't hesitate to ask the community for help!
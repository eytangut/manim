# Graph Theory Animation

This directory contains a comprehensive Manim animation covering fundamental graph theory concepts for educational purposes.

## Overview

The `graph_theory_animation.py` file contains a complete educational animation that covers:

1. **Basic Definitions**
   - Vertices (nodes) and edges
   - Visual representation with examples

2. **Types of Graphs**
   - Undirected graphs
   - Directed graphs (with arrows)
   - Memory aids for distinction

3. **Graph Traversal Algorithms**
   - Depth-First Search (DFS) - "Go deep first!"
   - Breadth-First Search (BFS) - "Go wide first!"
   - Visual demonstrations with step-by-step traversals

4. **Important Graph Properties**
   - Connected vs disconnected graphs
   - Visual examples and memory aids

5. **Special Graph Types**
   - Trees (connected + no cycles)
   - Complete graphs (every vertex connected to every other)
   - Bipartite graphs (two sets with edges only between sets)

6. **Key Takeaways**
   - Summary of all concepts with memory aids

## How to Run

### Prerequisites
1. Install ManimGL (3Blue1Brown's version):
   ```bash
   pip install manimgl
   ```

2. Ensure you have the required dependencies:
   - Python 3.7+
   - NumPy
   - OpenGL
   - FFmpeg (for video output)

### Running the Animation

1. **Interactive Mode** (recommended for development):
   ```bash
   manimgl graph_theory_animation.py GraphTheoryEducation
   ```

2. **Generate Video**:
   ```bash
   manimgl graph_theory_animation.py GraphTheoryEducation -w
   ```

3. **Save Final Frame**:
   ```bash
   manimgl graph_theory_animation.py GraphTheoryEducation -s
   ```

4. **Full Screen**:
   ```bash
   manimgl graph_theory_animation.py GraphTheoryEducation -f
   ```

## Educational Features

### Memory Aids Included
- **DFS vs BFS**: "Deep first" vs "Wide first"
- **Connected Graphs**: "All vertices reachable"
- **Trees**: "Connected + No cycles"
- **Directed Graphs**: "Arrows show direction"
- **Complete Graphs**: "Every vertex connected to every other"
- **Bipartite Graphs**: "Two sets, edges only between sets"

### Visual Learning Elements
- Color-coded vertices and edges
- Step-by-step algorithm animations
- Progressive concept building
- Clear labeling and annotations
- Smooth transitions between concepts

## Customization

The animation is modular and can be easily customized:

1. **Modify timing**: Adjust `self.wait()` calls to change pacing
2. **Add concepts**: Create new methods following the existing pattern
3. **Change colors**: Modify color constants (RED, BLUE, GREEN, etc.)
4. **Adjust positions**: Change vertex positions and layouts

## File Structure

```
graph_theory_animation.py    # Main animation file
README_GRAPH_THEORY.md      # This documentation
```

## Advanced Usage

The file also includes a placeholder for `AdvancedGraphConcepts` class which can be extended to include:
- Shortest path algorithms (Dijkstra, Floyd-Warshall)
- Minimum spanning trees (Kruskal, Prim)
- Network flow algorithms
- Graph coloring
- Planarity concepts

## Educational Context

This animation is designed to help students memorize fundamental graph theory concepts through:
- **Visual associations**: Connecting abstract concepts with visual representations
- **Memorable phrases**: Short, catchy descriptions for key concepts
- **Progressive complexity**: Building from simple to complex concepts
- **Interactive elements**: Allowing for pause and review during presentation

## Troubleshooting

1. **Import errors**: Ensure ManimGL is properly installed
2. **Performance issues**: Try running with lower resolution or fewer objects
3. **Display issues**: Check OpenGL compatibility
4. **Audio/Video sync**: Ensure FFmpeg is properly configured

## Contributing

To add new concepts or improve existing animations:
1. Follow the existing method structure
2. Include clear visual examples
3. Add memory aids where appropriate
4. Test thoroughly before committing

## License

This educational content follows the same license as the parent Manim repository (MIT License).
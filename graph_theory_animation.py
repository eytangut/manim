"""
Graph Theory Concepts Animation

This manim animation covers fundamental graph theory concepts
that are essential for computer science and mathematics students.
It includes visual explanations and memory aids for key definitions,
algorithms, and properties.
"""

# Note: This is designed to work with the manimgl library
# Run with: manimgl graph_theory_animation.py GraphTheoryEducation

from manimlib import *
import numpy as np
import math

class GraphTheoryEducation(Scene):
    def construct(self):
        # Title and introduction
        self.introduce_graph_theory()
        self.wait(1)
        
        # Basic definitions
        self.show_basic_definitions()
        self.wait(1)
        
        # Types of graphs
        self.show_graph_types()
        self.wait(1)
        
        # Graph traversal algorithms
        self.show_traversal_algorithms()
        self.wait(1)
        
        # Important properties
        self.show_graph_properties()
        self.wait(1)
        
        # Special graph types
        self.show_special_graphs()
        self.wait(1)
        
        # Conclusion
        self.show_conclusion()

    def introduce_graph_theory(self):
        """Introduction to graph theory with animated title"""
        title = Text("Graph Theory", font_size=64, color=BLUE)
        subtitle = Text("Fundamental Concepts for Memorization", font_size=36, color=WHITE)
        
        title.move_to(UP * 1.5)
        subtitle.move_to(DOWN * 0.5)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(2)
        
        # Transition out
        self.play(FadeOut(title), FadeOut(subtitle))

    def show_basic_definitions(self):
        """Show basic graph theory definitions with visual examples"""
        # Section title
        section_title = Text("Basic Definitions", font_size=48, color=YELLOW)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # Create a simple graph
        vertices = [
            Dot(LEFT * 2 + UP, color=RED, radius=0.15),
            Dot(RIGHT * 2 + UP, color=RED, radius=0.15), 
            Dot(LEFT * 2 + DOWN, color=RED, radius=0.15),
            Dot(RIGHT * 2 + DOWN, color=RED, radius=0.15)
        ]
        
        # Add vertex labels
        vertex_labels = [
            Tex("A").next_to(vertices[0], UP),
            Tex("B").next_to(vertices[1], UP),
            Tex("C").next_to(vertices[2], DOWN),
            Tex("D").next_to(vertices[3], DOWN)
        ]
        
        # Create edges
        edges = [
            Line(vertices[0].get_center(), vertices[1].get_center(), color=WHITE),
            Line(vertices[0].get_center(), vertices[2].get_center(), color=WHITE),
            Line(vertices[1].get_center(), vertices[3].get_center(), color=WHITE),
            Line(vertices[2].get_center(), vertices[3].get_center(), color=WHITE)
        ]
        
        # Show vertices first
        vertex_def = Text("Vertex (Node): A point in the graph", font_size=24)
        vertex_def.to_edge(LEFT).shift(DOWN * 2)
        
        self.play(Write(vertex_def))
        for vertex, label in zip(vertices, vertex_labels):
            self.play(FadeIn(vertex), Write(label))
        
        self.wait(1)
        
        # Show edges
        edge_def = Text("Edge: A connection between two vertices", font_size=24)
        edge_def.next_to(vertex_def, DOWN)
        
        self.play(Write(edge_def))
        for edge in edges:
            self.play(ShowCreation(edge))
        
        self.wait(2)
        
        # Cleanup
        all_objects = [section_title, vertex_def, edge_def] + vertices + vertex_labels + edges
        self.play(*[FadeOut(obj) for obj in all_objects])

    def show_graph_types(self):
        """Show different types of graphs"""
        section_title = Text("Types of Graphs", font_size=48, color=GREEN)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # Undirected Graph
        undirected_title = Text("Undirected Graph", font_size=32, color=WHITE)
        undirected_title.move_to(LEFT * 4 + UP * 1.5)
        
        # Simple undirected graph
        uv1 = Dot(LEFT * 5 + UP * 0.5, color=BLUE, radius=0.1)
        uv2 = Dot(LEFT * 3 + UP * 0.5, color=BLUE, radius=0.1)
        uv3 = Dot(LEFT * 4 + DOWN * 0.5, color=BLUE, radius=0.1)
        
        ue1 = Line(uv1.get_center(), uv2.get_center(), color=WHITE)
        ue2 = Line(uv1.get_center(), uv3.get_center(), color=WHITE)
        ue3 = Line(uv2.get_center(), uv3.get_center(), color=WHITE)
        
        self.play(Write(undirected_title))
        self.play(*[FadeIn(v) for v in [uv1, uv2, uv3]])
        self.play(*[ShowCreation(e) for e in [ue1, ue2, ue3]])
        
        # Directed Graph
        directed_title = Text("Directed Graph", font_size=32, color=WHITE)
        directed_title.move_to(RIGHT * 4 + UP * 1.5)
        
        # Simple directed graph with arrows
        dv1 = Dot(RIGHT * 3 + UP * 0.5, color=RED, radius=0.1)
        dv2 = Dot(RIGHT * 5 + UP * 0.5, color=RED, radius=0.1)
        dv3 = Dot(RIGHT * 4 + DOWN * 0.5, color=RED, radius=0.1)
        
        # Create arrows for directed edges
        de1 = Arrow(dv1.get_center(), dv2.get_center(), color=WHITE, buff=0.1, tip_length=0.15)
        de2 = Arrow(dv1.get_center(), dv3.get_center(), color=WHITE, buff=0.1, tip_length=0.15)
        de3 = Arrow(dv3.get_center(), dv2.get_center(), color=WHITE, buff=0.1, tip_length=0.15)
        
        self.play(Write(directed_title))
        self.play(*[FadeIn(v) for v in [dv1, dv2, dv3]])
        self.play(*[ShowCreation(e) for e in [de1, de2, de3]])
        
        self.wait(3)
        
        # Memory aid
        memory_aid = Text("Memory Aid: Arrows show direction!", font_size=28, color=YELLOW)
        memory_aid.move_to(DOWN * 2.5)
        self.play(Write(memory_aid))
        
        self.wait(2)
        
        # Cleanup
        all_objects = [section_title, undirected_title, directed_title, memory_aid,
                      uv1, uv2, uv3, ue1, ue2, ue3, dv1, dv2, dv3, de1, de2, de3]
        self.play(*[FadeOut(obj) for obj in all_objects])

    def show_traversal_algorithms(self):
        """Demonstrate graph traversal algorithms"""
        section_title = Text("Graph Traversal Algorithms", font_size=48, color=ORANGE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # Create a graph for traversal demonstration
        positions = {
            'A': LEFT * 2 + UP * 2,
            'B': RIGHT * 2 + UP * 2,
            'C': LEFT * 2 + DOWN * 0.5,
            'D': RIGHT * 2 + DOWN * 0.5,
            'E': ORIGIN + DOWN * 2
        }
        
        vertices = {}
        labels = {}
        for name, pos in positions.items():
            vertices[name] = Dot(pos, color=GRAY, radius=0.15)
            labels[name] = Tex(name).move_to(pos)
        
        # Create edges
        edges = [
            Line(positions['A'], positions['B'], color=WHITE),
            Line(positions['A'], positions['C'], color=WHITE),
            Line(positions['B'], positions['D'], color=WHITE),
            Line(positions['C'], positions['E'], color=WHITE),
            Line(positions['D'], positions['E'], color=WHITE)
        ]
        
        # Show the graph
        for vertex in vertices.values():
            self.play(FadeIn(vertex), run_time=0.3)
        for label in labels.values():
            self.play(Write(label), run_time=0.3)
        for edge in edges:
            self.play(ShowCreation(edge), run_time=0.3)
        
        # DFS demonstration
        dfs_title = Text("Depth-First Search (DFS)", font_size=32, color=BLUE)
        dfs_title.move_to(LEFT * 4 + DOWN * 3.5)
        self.play(Write(dfs_title))
        
        # DFS order: A -> B -> D -> E -> C
        dfs_order = ['A', 'B', 'D', 'E', 'C']
        dfs_memory = Text("Memory: Go DEEP first!", font_size=24, color=BLUE)
        dfs_memory.next_to(dfs_title, DOWN)
        self.play(Write(dfs_memory))
        
        # Animate DFS traversal
        for i, vertex_name in enumerate(dfs_order):
            vertices[vertex_name].set_color(BLUE)
            self.play(vertices[vertex_name].animate.scale(1.5), run_time=0.5)
            self.wait(0.5)
        
        self.wait(1)
        
        # Reset colors for BFS
        for vertex in vertices.values():
            vertex.set_color(GRAY)
            self.play(vertex.animate.scale(1/1.5), run_time=0.3)
        
        # BFS demonstration
        bfs_title = Text("Breadth-First Search (BFS)", font_size=32, color=GREEN)
        bfs_title.move_to(RIGHT * 4 + DOWN * 3.5)
        self.play(Write(bfs_title))
        
        # BFS order: A -> B -> C -> D -> E
        bfs_order = ['A', 'B', 'C', 'D', 'E']
        bfs_memory = Text("Memory: Go WIDE first!", font_size=24, color=GREEN)
        bfs_memory.next_to(bfs_title, DOWN)
        self.play(Write(bfs_memory))
        
        # Animate BFS traversal
        for i, vertex_name in enumerate(bfs_order):
            vertices[vertex_name].set_color(GREEN)
            self.play(vertices[vertex_name].animate.scale(1.5), run_time=0.5)
            self.wait(0.5)
        
        self.wait(2)
        
        # Cleanup
        all_objects = ([section_title, dfs_title, bfs_title, dfs_memory, bfs_memory] + 
                      list(vertices.values()) + list(labels.values()) + edges)
        self.play(*[FadeOut(obj) for obj in all_objects])

    def show_graph_properties(self):
        """Show important graph properties"""
        section_title = Text("Important Graph Properties", font_size=48, color=PURPLE)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # Connected vs Disconnected
        connected_label = Text("Connected Graph", font_size=28, color=WHITE)
        connected_label.move_to(LEFT * 4 + UP * 1)
        
        # Connected graph
        cv1 = Dot(LEFT * 5 + UP * 0.5, color=GREEN, radius=0.1)
        cv2 = Dot(LEFT * 3 + UP * 0.5, color=GREEN, radius=0.1)
        cv3 = Dot(LEFT * 4 + DOWN * 0.5, color=GREEN, radius=0.1)
        ce1 = Line(cv1.get_center(), cv2.get_center(), color=GREEN)
        ce2 = Line(cv2.get_center(), cv3.get_center(), color=GREEN)
        
        self.play(Write(connected_label))
        self.play(*[FadeIn(v) for v in [cv1, cv2, cv3]])
        self.play(*[ShowCreation(e) for e in [ce1, ce2]])
        
        # Disconnected graph
        disconnected_label = Text("Disconnected Graph", font_size=28, color=WHITE)
        disconnected_label.move_to(RIGHT * 4 + UP * 1)
        
        dv1 = Dot(RIGHT * 3 + UP * 0.5, color=RED, radius=0.1)
        dv2 = Dot(RIGHT * 5 + UP * 0.5, color=RED, radius=0.1)
        dv3 = Dot(RIGHT * 4 + DOWN * 1, color=RED, radius=0.1)  # Isolated vertex
        de1 = Line(dv1.get_center(), dv2.get_center(), color=RED)
        
        self.play(Write(disconnected_label))
        self.play(*[FadeIn(v) for v in [dv1, dv2, dv3]])
        self.play(ShowCreation(de1))
        
        # Memory aid
        memory_text = Text("Memory: Connected = All vertices reachable", 
                          font_size=24, color=YELLOW)
        memory_text.move_to(DOWN * 2.5)
        self.play(Write(memory_text))
        
        self.wait(3)
        
        # Cleanup
        all_objects = [section_title, connected_label, disconnected_label, memory_text,
                      cv1, cv2, cv3, ce1, ce2, dv1, dv2, dv3, de1]
        self.play(*[FadeOut(obj) for obj in all_objects])

    def show_special_graphs(self):
        """Show special types of graphs"""
        section_title = Text("Special Graph Types", font_size=48, color=TEAL)
        section_title.to_edge(UP)
        self.play(Write(section_title))
        
        # Tree
        tree_label = Text("Tree", font_size=32, color=WHITE)
        tree_label.move_to(LEFT * 5 + UP * 1.5)
        
        # Simple tree structure
        root = Dot(LEFT * 5 + UP * 0.5, color=BROWN, radius=0.1)
        left_child = Dot(LEFT * 6 + DOWN * 0.5, color=BROWN, radius=0.1)
        right_child = Dot(LEFT * 4 + DOWN * 0.5, color=BROWN, radius=0.1)
        
        tree_edges = [
            Line(root.get_center(), left_child.get_center(), color=BROWN),
            Line(root.get_center(), right_child.get_center(), color=BROWN)
        ]
        
        self.play(Write(tree_label))
        self.play(*[FadeIn(v) for v in [root, left_child, right_child]])
        self.play(*[ShowCreation(e) for e in tree_edges])
        
        tree_memory = Text("Connected + No cycles", font_size=20, color=BROWN)
        tree_memory.next_to(tree_label, DOWN)
        self.play(Write(tree_memory))
        
        # Complete Graph
        complete_label = Text("Complete Graph", font_size=32, color=WHITE)
        complete_label.move_to(ORIGIN + UP * 1.5)
        
        # K4 (complete graph with 4 vertices)
        angle_step = TAU / 4
        complete_vertices = []
        for i in range(4):
            angle = i * angle_step
            pos = np.array([np.cos(angle), np.sin(angle), 0]) * 0.8
            complete_vertices.append(Dot(pos, color=PINK, radius=0.08))
        
        complete_edges = []
        for i in range(4):
            for j in range(i + 1, 4):
                edge = Line(complete_vertices[i].get_center(), 
                           complete_vertices[j].get_center(), color=PINK)
                complete_edges.append(edge)
        
        self.play(Write(complete_label))
        self.play(*[FadeIn(v) for v in complete_vertices])
        self.play(*[ShowCreation(e) for e in complete_edges])
        
        complete_memory = Text("Every vertex connected\nto every other vertex", 
                              font_size=20, color=PINK)
        complete_memory.next_to(complete_label, DOWN)
        self.play(Write(complete_memory))
        
        # Bipartite Graph
        bipartite_label = Text("Bipartite Graph", font_size=32, color=WHITE)
        bipartite_label.move_to(RIGHT * 5 + UP * 1.5)
        
        # Two sets of vertices
        set1 = [Dot(RIGHT * 4 + UP * i, color=YELLOW, radius=0.08) for i in [0.5, -0.5]]
        set2 = [Dot(RIGHT * 6 + UP * i, color=BLUE, radius=0.08) for i in [0.5, -0.5]]
        
        # Cross connections only
        bipartite_edges = [
            Line(set1[0].get_center(), set2[0].get_center(), color=WHITE),
            Line(set1[0].get_center(), set2[1].get_center(), color=WHITE),
            Line(set1[1].get_center(), set2[0].get_center(), color=WHITE)
        ]
        
        self.play(Write(bipartite_label))
        self.play(*[FadeIn(v) for v in set1 + set2])
        self.play(*[ShowCreation(e) for e in bipartite_edges])
        
        bipartite_memory = Text("Two sets, edges only\nbetween sets", 
                               font_size=20, color=YELLOW)
        bipartite_memory.next_to(bipartite_label, DOWN)
        self.play(Write(bipartite_memory))
        
        self.wait(4)
        
        # Cleanup
        all_objects = ([section_title, tree_label, complete_label, bipartite_label,
                       tree_memory, complete_memory, bipartite_memory, root, left_child, right_child] +
                      tree_edges + complete_vertices + complete_edges + set1 + set2 + bipartite_edges)
        self.play(*[FadeOut(obj) for obj in all_objects])

    def show_conclusion(self):
        """Show conclusion with key takeaways"""
        title = Text("Key Graph Theory Concepts", font_size=48, color=GOLD)
        title.move_to(UP * 2.5)
        
        concepts = VGroup(
            Text("• Vertex = Node, Edge = Connection", font_size=28),
            Text("• Directed vs Undirected graphs", font_size=28),
            Text("• DFS = Depth first, BFS = Breadth first", font_size=28),
            Text("• Connected = All vertices reachable", font_size=28),
            Text("• Tree = Connected + No cycles", font_size=28),
            Text("• Complete = All vertices connected", font_size=28),
            Text("• Bipartite = Two separate sets", font_size=28)
        )
        concepts.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        concepts.move_to(DOWN * 0.5)
        
        self.play(Write(title))
        self.wait(1)
        
        for concept in concepts:
            self.play(Write(concept), run_time=0.8)
        
        self.wait(3)
        
        # Final message
        final_message = Text("Practice these concepts for better memorization!", 
                           font_size=32, color=GREEN)
        final_message.move_to(DOWN * 3)
        self.play(Write(final_message))
        
        self.wait(3)


# Additional helper scene for more advanced concepts
class AdvancedGraphConcepts(Scene):
    def construct(self):
        """Advanced graph theory concepts"""
        title = Text("Advanced Graph Theory", font_size=64, color=BLUE)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        # Could add: shortest path algorithms, minimum spanning trees, etc.
        self.show_shortest_path()
        
    def show_shortest_path(self):
        """Demonstrate shortest path concept"""
        # Implementation for shortest path visualization
        pass


if __name__ == "__main__":
    # This allows the file to be run directly for testing
    print("Graph Theory Animation Module")
    print("Run with: manimgl graph_theory_animation.py GraphTheoryEducation")
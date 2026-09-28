"""2D Rigid Body SAT Collision & Impulse Dynamics Engine.
100% Python Standard Library.
"""

import math

class RigidBody2DResolver:
    """2D Convex Polygon SAT collision detection and contact impulse resolver."""
    @staticmethod
    def project_polygon(vertices, axis):
        dots = [v[0]*axis[0] + v[1]*axis[1] for v in vertices]
        return min(dots), max(dots)

    @classmethod
    def sat_collision_check(cls, poly_a, poly_b):
        edges = []
        for p in [poly_a, poly_b]:
            n = len(p)
            for i in range(n):
                j = (i + 1) % n
                edge = (p[j][0] - p[i][0], p[j][1] - p[i][1])
                length = math.hypot(edge[0], edge[1])
                normal = (-edge[1] / length, edge[0] / length)
                edges.append(normal)

        min_overlap = float("inf")
        best_axis = None

        for axis in edges:
            min_a, max_a = cls.project_polygon(poly_a, axis)
            min_b, max_b = cls.project_polygon(poly_b, axis)
            overlap = min(max_a, max_b) - max(min_a, min_b)
            if overlap < 0:
                return False, (0, 0), 0.0
            if overlap < min_overlap:
                min_overlap = overlap
                best_axis = axis

        return True, best_axis, min_overlap

    @staticmethod
    def resolve_impulse(m1, m2, v1, v2, normal, restitution=0.8):
        rel_vel = (v1[0] - v2[0]) * normal[0] + (v1[1] - v2[1]) * normal[1]
        if rel_vel > 0:
            return v1, v2
        j = -(1 + restitution) * rel_vel / (1.0 / m1 + 1.0 / m2)
        v1_new = (v1[0] + (j / m1) * normal[0], v1[1] + (j / m1) * normal[1])
        v2_new = (v2[0] - (j / m2) * normal[0], v2[1] - (j / m2) * normal[1])
        return v1_new, v2_new

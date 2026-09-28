from client import RigidBody2DResolver

box_a = [(0, 0), (2, 0), (2, 2), (0, 2)]
box_b = [(1.5, 0), (3.5, 0), (3.5, 2), (1.5, 2)]

colliding, normal, pen = RigidBody2DResolver.sat_collision_check(box_a, box_b)
print(f"SAT Collision Check: {colliding} | Penetration Depth: {pen:.2f}")

v1_new, v2_new = RigidBody2DResolver.resolve_impulse(1.0, 1.0, (1.0, 0.0), (-1.0, 0.0), (-1.0, 0.0), restitution=0.8)
print(f"Post-Collision Velocities: Body 1={v1_new}, Body 2={v2_new}")

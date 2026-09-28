# genpark-rigid-body-2d-impulse-collision-resolver-skill

Agent Skill implementing **Separating Axis Theorem (SAT) convex polygon collision detection** and restitution impulse resolution for 2D rigid body dynamics.

## Architectural Overview
```mermaid
flowchart TD
    PolyA["Convex Polygon A"] & PolyB["Convex Polygon B"] --> SAT["Project onto Edge Normal Axes"]
    SAT --> Overlap{"All Axes Overlap ?"}
    Overlap -- No --> Separated["No Collision"]
    Overlap -- Yes --> Impulse["Compute Minimum Translation Vector & Contact Normal"]
    Impulse --> Elastic["Newtonian Impulse Resolution with Restitution e"]
    Elastic --> Vel["Post-Collision Linear Velocities v1', v2'"]
```

import sys
import json
from client import RigidBody2DResolver

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-rigid-body-2d-impulse-collision-resolver-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "check_and_resolve_collision",
                        "description": "Perform SAT polygon collision detection and compute impulse velocity restitution",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "poly_a": {"type": "array", "items": {"type": "array", "items": {"type": "number"}}},
                                "poly_b": {"type": "array", "items": {"type": "array", "items": {"type": "number"}}},
                                "m1": {"type": "number", "default": 1.0},
                                "m2": {"type": "number", "default": 1.0},
                                "v1": {"type": "array", "items": {"type": "number"}, "default": [1.0, 0.0]},
                                "v2": {"type": "array", "items": {"type": "number"}, "default": [-1.0, 0.0]},
                                "restitution": {"type": "number", "default": 0.8}
                            },
                            "required": ["poly_a", "poly_b"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "check_and_resolve_collision":
            poly_a = [tuple(p) for p in args.get("poly_a", [])]
            poly_b = [tuple(p) for p in args.get("poly_b", [])]
            colliding, normal, pen = RigidBody2DResolver.sat_collision_check(poly_a, poly_b)
            v1_new, v2_new = None, None
            if colliding:
                m1 = args.get("m1", 1.0)
                m2 = args.get("m2", 1.0)
                v1 = tuple(args.get("v1", [1.0, 0.0]))
                v2 = tuple(args.get("v2", [-1.0, 0.0]))
                restitution = args.get("restitution", 0.8)
                v1_new, v2_new = RigidBody2DResolver.resolve_impulse(m1, m2, v1, v2, normal, restitution)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"colliding": colliding, "penetration": pen, "v1_post": v1_new, "v2_post": v2_new})}]
                }
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()

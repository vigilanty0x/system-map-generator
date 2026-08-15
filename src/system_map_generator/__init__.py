import argparse,hashlib,json,re
def generate(data):
 nodes=data.get("nodes") if isinstance(data,dict) else None;edges=data.get("edges") if isinstance(data,dict) else None
 if not isinstance(nodes,list) or not isinstance(edges,list) or len(nodes)>200 or len(edges)>1000:return {"ok":False,"errors":["bounds"]}
 ids=[n.get("id") for n in nodes if isinstance(n,dict)]
 if len(ids)!=len(nodes) or len(ids)!=len(set(ids)) or any(not isinstance(x,str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,63}",x) for x in ids):return {"ok":False,"errors":["invalid_nodes"]}
 bad=[e for e in edges if not isinstance(e,dict) or e.get("from") not in ids or e.get("to") not in ids]
 if bad:return {"ok":False,"errors":["dangling_edges"]}
 labels={n["id"]:str(n.get("label",n["id"])).replace('"',"'")[:100] for n in nodes};lines=["flowchart TD"]+[f'  {i}["{labels[i]}"]' for i in sorted(ids)]+[f"  {e['from']} --> {e['to']}" for e in sorted(edges,key=lambda e:(e["from"],e["to"]))];body="\n".join(lines);return {"ok":True,"mermaid":body,"sha256":hashlib.sha256(body.encode()).hexdigest(),"nodes":len(ids),"edges":len(edges)}
def probe():
 g=generate({"nodes":[{"id":"a"},{"id":"b"}],"edges":[{"from":"a","to":"b"}]});b=generate({"nodes":[{"id":"a"}],"edges":[{"from":"a","to":"x"}]});return {"ok":g["ok"] and not b["ok"],"dangling_counter_proof":not b["ok"]}
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument("command",choices=("generate","probe"));p.add_argument("--input");a=p.parse_args(argv);o=probe() if a.command=="probe" else generate(json.load(open(a.input)));print(json.dumps(o,sort_keys=True));return 0 if o["ok"] else 2

import matplotlib; matplotlib.use("Agg")
from flask import Flask, render_template, request
import networkx as nx, matplotlib.pyplot as plt, os
app = Flask(__name__); N=28

edges = [("A","B",17),("A","C",18),("A","D",15),("B","C",18),("B","G",27),("B","E",18),("C","E",15),("C","F",10),("D","F",14),("D","I",29),("F","I",13),("E","F",4),("E","G",6),("G","J",15),("E","H",12),("F","H",17),("H","J",11),("I","H",3),("I","J",13)]
node_layout = {"A":(0,2),"B":(1.5,3.2),"C":(1,2),"D":(0.2,0.6),"E":(3,2.6),"F":(3,1.1),"G":(5,3.2),"H":(4.2,1.9),"I":(3.8,0.2),"J":(5.8,1.9)}
def grid_pos(layout, N, m=0.5):
    xs,ys=zip(*layout.values())
    sx,Sx,sy,Sy=min(xs),max(xs),min(ys),max(ys)
    s=lambda v,l,h:m+(v-l)*(N-1-2*m)/(h-l) if h!=l else (N-1)/2
    return {k:(int(round(s(x,sx,Sx))),int(round(s(y,sy,Sy)))) for k,(x,y) in layout.items()}
positions = grid_pos(node_layout, N)
net_pairs = set(tuple(sorted((u,v))) for u,v,_ in edges)
gates = sorted(set(k for p in positions for k in p))

@app.route("/", methods=["GET", "POST"])
def index():
    s=e=pt=c=None
    img_out=os.path.join(app.root_path, "static", "chip.jpg")
    G = nx.grid_2d_graph(N, N)
    if request.method=="POST":
        s,e = request.form.get("start"), request.form.get("end")
        if s and e and s!=e and tuple(sorted((s,e))) in net_pairs:
            pt = nx.shortest_path(G, positions[s], positions[e])
            c = len(pt)-1
    plt.figure(figsize=(8,8))
    for i in range(N):
        plt.plot([0,N-1],[i,i],c="gray",lw=0.4)
        plt.plot([i,i],[0,N-1],c="gray",lw=0.4)
    for k,(x,y) in positions.items():
        plt.plot(x,y,"ko",ms=11)
        plt.text(x,y,k,color="w",fontsize=12,ha="center",va="center")
    if pt:
        xs,ys=zip(*pt);plt.plot(xs,ys,c="red",lw=3);plt.scatter(xs[0],ys[0],c="lime",s=50);plt.scatter(xs[-1],ys[-1],c="cyan",s=50)
    plt.xlim(-1,N);plt.ylim(-1,N);plt.axis("off");plt.tight_layout();plt.savefig(img_out,dpi=120,bbox_inches="tight");plt.close()
    return render_template("index.html", gates=gates, start=s, end=e, path=pt, path_hops=c)

if __name__=="__main__":
    os.makedirs(os.path.join(app.root_path,"static"),exist_ok=True)
    app.run(debug=True)

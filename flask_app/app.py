from flask import Flask, render_template

app = Flask(__name__)

gates = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", gates=gates)

if __name__ == "__main__":
    app.run(debug=True)

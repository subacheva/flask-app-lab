from flask import Flask, render_template

app = Flask(__name__)


@app.get("/")
def resume():
    return render_template("resume.html", title="Резюме | Уляна Субачева")


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request

app = Flask(__name__)


@app.get("/")
def resume():
    return render_template("resume.html", title="Резюме | Уляна Субачева")


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    sent = request.method == "POST"
    return render_template(
        "contacts.html",
        title="Контакти | Уляна Субачева",
        sent=sent,
    )


if __name__ == "__main__":
    app.run(debug=True)

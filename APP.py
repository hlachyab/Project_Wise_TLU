from flask import Flask, render_template

# Serve templates and static assets directly from the Frontend directory
app = Flask(
    __name__,
    static_folder="Frontend",
    static_url_path="",
    template_folder="Frontend",
)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

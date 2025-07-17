from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    book_text = "Awesome! "
    return render_template('index.html', text=book_text)

if __name__ == '__main__':
    app.run(debug=True)

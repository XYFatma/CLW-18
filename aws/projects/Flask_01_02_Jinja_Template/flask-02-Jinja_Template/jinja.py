from flask import Flask, render_template

app = Flask(__name__)








if __name__== "__main__":
    app.run(debug=True, port=30000)
    # app.run(host= '0.0.0.0', port=8081)
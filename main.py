from flask import Flask, redirect, request, render_template, url_for



app = Flask(__name__)
#Bootstrap(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        #f.save(secure_filename(f.filename))
        return 'file uploaded successfully'
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template, request

app = Flask(__name__)

# Replace this logic with email verification
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_email = request.form['email']

        # Perform email verification here

        link = None  # Replace with code to fetch the reset link

        if link:
            return render_template('result.html', link=link)
        else:
            return render_template('result.html', message='Email not found.')

    return render_template('index.html')

if __name__ == '__main__':
    app.run()

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process-file', methods=['POST'])
def process_file():
    data = request.get_json()
    file_content = data.get('content')
    bank = data.get('bank')
    user = data.get('user')

    if file_content and bank and user:
        # Process the file content, bank, and user as needed
        print(f"Received file content: {file_content}")
        print(f"Bank: {bank}")
        print(f"User: {user}")
        return jsonify({"message": "Data received and processed."}), 200
    else:
        return jsonify({"error": "Missing data."}), 400


if __name__ == '__main__':
    app.run(debug=True)

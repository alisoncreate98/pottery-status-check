from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CLICKUP_API_TOKEN = "pk_2538350_OC44G1Z33JAFIRE2GL47RI1QXSK863VD"
LIST_ID = "901504602115"

@app.route('/check-status', methods=['GET'])
def check_status():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"
    headers = {"Authorization": CLICKUP_API_TOKEN}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch tasks"}), 500

    tasks = response.json().get('tasks', [])
    for task in tasks:
        custom_fields = task.get('custom_fields', [])
        for field in custom_fields:
            if field.get('name') == 'Email' and field.get('value') == email:
                return jsonify({
                    "status": task['status']['status'],
                    "name": task['name'],
                    "email": email
                })

    return jsonify({"error": "No order found for this email"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

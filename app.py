<<<<<<< HEAD

=======
>>>>>>> 776e018ab02f2f1402d9fdaa7665717815745a73
from flask import Flask
import os

app = Flask(__name__)

<<<<<<< HEAD

@app.route("/")
def home():
    return "Hello Venky 👋 Your Flask App is running on Azure App Service 🚀"

=======
@app.route("/")
def home():
    return "Hello from Azure App Service!"
>>>>>>> 776e018ab02f2f1402d9fdaa7665717815745a73

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

# webhook-repo
## Flask Web App for GitHub Webhooks

This Flask web app is designed to receive GitHub webhook post requests for **pull_request,push, and merge** from the repository `/ionstone/action-repo`, and save the details to a remote MongoDB database.

### Instructions

To use this app, follow these steps:

1. Clone the repository.
2. Install Python, ngrok, and Flask.
3. Set up MongoDB.
4. Install the required dependencies by running `pip install -r requirements.txt`.
5. Run the Flask app by executing `flask run`.
6. Run ngrok with the command `ngrok http 5000`. Copy the ngrok URL generated.
7. Append `/action` to the ngrok URL and paste it in your GitHub repository's webhook settings.
8. Access the app's UI by visiting the `/` route.

That's it! You're now ready to receive and process GitHub webhook events using this Flask web app.

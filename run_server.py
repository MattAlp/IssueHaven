from server.app import app
import config


if __name__ == "__main__":
    if config.DEV_MODE:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=8080)

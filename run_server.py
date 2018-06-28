from server.app import app
import config


if __name__ == "__main__":
    app.run(debug=config.DEV_MODE)

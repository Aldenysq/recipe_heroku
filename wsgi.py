from app.main import app
import os

if __name__ == "__main__":
        p = int(os.environ.get('PORT', 33507))
        app.run(port=p)
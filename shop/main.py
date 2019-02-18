from app import app
import manage


with app.app_context():
    import blueprints.admin.views


if __name__ == '__main__':
    app.run()
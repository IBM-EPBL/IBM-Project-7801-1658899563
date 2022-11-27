from website import create_app
import os

app = create_app()
port=os.getenv('VCAP_APP_PORT', '8080')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)

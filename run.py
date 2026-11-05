import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Switch server based on environment variable (default to 'development')
    server_mode = os.getenv('SERVER_MODE', 'development').lower()
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')

    if server_mode == 'production':
        print(f"[*] Starting Waitress PRODUCTION server on http://{host}:{port}")
        from waitress import serve
        serve(app, host=host, port=port)
    else:
        print(f"[*] Starting Flask DEVELOPMENT server on http://127.0.0.1:{port}")
        app.run(host=host, port=port, debug=True)
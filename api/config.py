from fastapi.middleware.cors import CORSMiddleware

# CORS setup
def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # frontend URL
        allow_credentials=True,
        allow_methods=["*"],  # allow POST, GET, OPTIONS, etc.
        allow_headers=["*"],
    )

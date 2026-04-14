"""
app.py
Flask application template for the warm-up assignment

Students need to implement the API endpoints as specified in the assignment.
"""

from flask import Flask, request, jsonify, render_template
from starter_preprocess import TextPreprocessor
import traceback

app = Flask(__name__)
preprocessor = TextPreprocessor()


@app.route('/')
def home():
    """Render a simple HTML form for URL input"""
    return render_template('index.html')


@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Text preprocessing service is running"
    })


@app.route('/api/clean', methods=['POST'])
def clean_text():

    try:
        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({
                "success": False,
                "error": "Missing URL"
            })

        url = data["url"]

        raw_text = preprocessor.fetch_from_url(url)

        cleaned_text = preprocessor.clean_gutenberg_text(raw_text)

        normalized_text = preprocessor.normalize_text(cleaned_text)

        stats = preprocessor.get_text_statistics(normalized_text)

        summary = preprocessor.create_summary(normalized_text)

        return jsonify({
            "success": True,
            "cleaned_text": normalized_text[:500],
            "statistics": stats,
            "summary": summary
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


@app.route('/api/analyze', methods=['POST'])
def analyze_text():

    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({
                "success": False,
                "error": "Missing text"
            })

        text = data["text"]

        stats = preprocessor.get_text_statistics(text)

        return jsonify({
            "success": True,
            "statistics": stats
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


@app.errorhandler(500)
def internal_error(error):

    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    print("🚀 Starting Text Preprocessing Web Service...")
    print("📖 Available endpoints:")
    print(" GET / - Web interface")
    print(" GET /health - Health check")
    print(" POST /api/clean - Clean text from URL")
    print(" POST /api/analyze - Analyze raw text")
    print()
    print("🌐 Open your browser to: http://localhost:5000")
    print("⏹️ Press Ctrl+C to stop the server")

    app.run(debug=True, port=5000, host='0.0.0.0')

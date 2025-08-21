from flask import Flask, render_template, request
from model import infer_mood_from_text, get_movies_by_mood

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    mood_text = request.form.get('mood_text', '').strip()
    if not mood_text:
        return render_template('recommendations.html', title='', recommendations=[], error="Please describe how you're feeling.")

    detected_mood = infer_mood_from_text(mood_text)
    print(f"Inferred Mood: {detected_mood}")

    recommendations = get_movies_by_mood(detected_mood)
    if not recommendations:
        error = "No movies found for your mood."
    else:
        error = None

    return render_template(
        'recommendations.html',
        title=f"Movies for your mood ({detected_mood.title()})",
        recommendations=recommendations,
        error=error
    )

if __name__ == '__main__':
    app.run(debug=True)

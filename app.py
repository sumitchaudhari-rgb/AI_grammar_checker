# Import necessary libraries and modules
import difflib
import html
import re
from flask import Flask, render_template, request, jsonify
from language_tool_python import LanguageTool

# Create a Flask application instance
app = Flask(__name__)

# Create a LanguageTool object for grammar and spell checking
tool = LanguageTool('en-US')


def format_matches(raw_matches):
    """Format LanguageTool Match objects into JSON-serializable dictionaries."""
    formatted = []
    for m in raw_matches:
        rule_id = getattr(m, 'rule_id', None) or getattr(m, 'ruleId', '')
        error_length = getattr(m, 'error_length', None) or getattr(m, 'errorLength', 0)
        rule_issue_type = getattr(m, 'rule_issue_type', None) or getattr(m, 'ruleIssueType', 'grammar')
        matched_text = getattr(m, 'matched_text', None) or getattr(m, 'matchedText', '')

        category = getattr(m, 'category', 'GENERAL') or 'GENERAL'
        replacements = getattr(m, 'replacements', []) or []

        formatted.append({
            'rule_id': str(rule_id),
            'message': getattr(m, 'message', ''),
            'replacements': replacements[:6],
            'offset': getattr(m, 'offset', 0),
            'error_length': error_length,
            'category': str(category),
            'rule_issue_type': str(rule_issue_type),
            'context': getattr(m, 'context', ''),
            'matched_text': str(matched_text)
        })
    return formatted


def generate_annotated_html(orig, corr):
    """
    Generate annotated HTML:
    - input text with erroneous/spelling words underlined in red.
    - corrected text with corrected replacement words underlined in green.
    """
    if not orig:
        return '', ''

    tokens_orig = re.findall(r'\w+|[^\w\s]|\s+', orig)
    tokens_corr = re.findall(r'\w+|[^\w\s]|\s+', corr)
    s = difflib.SequenceMatcher(None, tokens_orig, tokens_corr)

    in_parts = []
    out_parts = []

    for tag, i1, i2, j1, j2 in s.get_opcodes():
        orig_chunk = ''.join(tokens_orig[i1:i2])
        corr_chunk = ''.join(tokens_corr[j1:j2])

        if tag == 'equal':
            in_parts.append(html.escape(orig_chunk))
            out_parts.append(html.escape(corr_chunk))
        elif tag == 'replace':
            in_parts.append(
                f'<span class="red-line" title="Suggested correction: {html.escape(corr_chunk.strip())}">{html.escape(orig_chunk)}</span>'
            )
            out_parts.append(
                f'<span class="green-line" title="Corrected from: {html.escape(orig_chunk.strip())}">{html.escape(corr_chunk)}</span>'
            )
        elif tag == 'delete':
            in_parts.append(
                f'<span class="red-line" title="Unnecessary word/phrase">{html.escape(orig_chunk)}</span>'
            )
        elif tag == 'insert':
            out_parts.append(
                f'<span class="green-line" title="Added correction">{html.escape(corr_chunk)}</span>'
            )

    return ''.join(in_parts), ''.join(out_parts)


def compute_stats(text, matches):
    """Compute text statistics and issue counts."""
    words = len(text.split()) if text.strip() else 0
    chars = len(text)
    sentences = len([s for s in text.replace('!', '.').replace('?', '.').split('.') if s.strip()])
    reading_time_sec = round(max(1, words / 200 * 60)) if words > 0 else 0

    spelling_count = sum(
        1 for m in matches
        if 'misspelling' in m['rule_issue_type'].lower()
        or 'typo' in m['category'].lower()
        or 'spelling' in m['category'].lower()
    )
    grammar_count = sum(
        1 for m in matches
        if 'grammar' in m['rule_issue_type'].lower()
        or 'grammar' in m['category'].lower()
    )
    style_count = max(0, len(matches) - spelling_count - grammar_count)

    accuracy_score = 100
    if words > 0:
        error_rate = min(1.0, len(matches) / words)
        accuracy_score = max(10, round((1.0 - error_rate) * 100))

    return {
        'words': words,
        'chars': chars,
        'sentences': sentences,
        'reading_time_sec': reading_time_sec,
        'issues_total': len(matches),
        'issues_spelling': spelling_count,
        'issues_grammar': grammar_count,
        'issues_style': style_count,
        'accuracy_score': accuracy_score
    }


# Define a route for the root URL ('/') that renders an HTML template
@app.route('/')
def index():
    return render_template(
        'index.html',
        text='',
        corrected_text='',
        annotated_input_html='',
        annotated_corrected_html='',
        matches=[],
        stats=None
    )


# Define a route for the '/spell' URL that handles traditional POST requests
@app.route('/spell', methods=['POST'])
def spell_check():
    text = request.form.get('text', '')
    if not text.strip():
        return render_template(
            'index.html',
            text='',
            corrected_text='',
            annotated_input_html='',
            annotated_corrected_html='',
            matches=[],
            stats=None
        )

    # Perform spell and grammar checking using LanguageTool
    raw_matches = tool.check(text)
    matches = format_matches(raw_matches)

    # Generate corrected text with spelling and grammar suggestions
    corrected_text = tool.correct(text)
    annotated_input, annotated_corrected = generate_annotated_html(text, corrected_text)
    stats = compute_stats(text, matches)

    return render_template(
        'index.html',
        text=text,
        corrected_text=corrected_text,
        annotated_input_html=annotated_input,
        annotated_corrected_html=annotated_corrected,
        matches=matches,
        stats=stats
    )


# API endpoint for asynchronous checks via AJAX/Fetch
@app.route('/api/check', methods=['POST'])
def api_check():
    data = request.get_json(silent=True) or {}
    text = data.get('text', '')

    if not text.strip():
        return jsonify({
            'success': True,
            'text': '',
            'corrected_text': '',
            'annotated_input_html': '',
            'annotated_corrected_html': '',
            'matches': [],
            'stats': compute_stats('', [])
        })

    raw_matches = tool.check(text)
    matches = format_matches(raw_matches)
    corrected_text = tool.correct(text)
    annotated_input, annotated_corrected = generate_annotated_html(text, corrected_text)
    stats = compute_stats(text, matches)

    return jsonify({
        'success': True,
        'text': text,
        'corrected_text': corrected_text,
        'annotated_input_html': annotated_input,
        'annotated_corrected_html': annotated_corrected,
        'matches': matches,
        'stats': stats
    })


# Run the Flask application if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)

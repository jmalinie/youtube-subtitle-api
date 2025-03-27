from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import os

app = Flask(__name__)

@app.route('/subtitles')
def get_subtitles():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'Missing video_id parameter'}), 400
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcripts.find_transcript(['en'])
        result = {
            'language': transcript.language,
            'language_code': transcript.language_code,
            'subtitles': transcript.fetch()
        }
        return jsonify(result)
    except TranscriptsDisabled:
        return jsonify({'error': 'Subtitles are disabled for this video.'}), 403
    except NoTranscriptFound:
        return jsonify({'error': 'No transcript found for the requested video.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

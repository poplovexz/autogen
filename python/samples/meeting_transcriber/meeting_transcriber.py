"""Sample script: capture audio from microphone, convert to text, and extract requirements."""

from __future__ import annotations

import logging
from typing import List

import speech_recognition as sr

logger = logging.getLogger(__name__)


def listen_from_microphone() -> str:
    """Capture audio from the microphone and convert it to text using Google's speech API."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        logger.info("Listening... speak now.")
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        logger.warning("Speech was unintelligible.")
        return ""
    except sr.RequestError as exc:
        raise RuntimeError(f"Speech recognition service error: {exc}") from exc


def analyze_requirements(transcript: str) -> List[str]:
    """Convert raw transcript text into a list of requirement statements.

    This simple heuristic splits the transcript into sentences and uses them as
    requirements. In a production system, natural language processing or LLMs
    could be used for more advanced analysis.
    """
    sentences = [s.strip() for s in transcript.replace("?", ".").split(".")]
    return [s for s in sentences if s]


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    transcript = listen_from_microphone()
    if not transcript:
        return
    requirements = analyze_requirements(transcript)
    logger.info("Detected requirements:")
    for req in requirements:
        logger.info("- %s", req)


if __name__ == "__main__":
    main()

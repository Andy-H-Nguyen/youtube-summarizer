
# YoutubeSummarizer

![CI Test Suite](https://github.com/your-username/your-repo/actions/workflows/ci.yml/badge.svg)

YoutubeSummarizer allows you to easily convert a YouTube video to text and summarize its content.

## Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/your-repo.git
    ```

2. Change into the project directory:
    ```bash
    cd youtube-summarizer
    ```

3. Install the required dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```

4. Run the app locally with Streamlit:
    ```bash
    streamlit run app.py
    ```

5. Open `http://localhost:8501` in your browser.

## Running the Tests

To run the test suite, you can use the following command:

```bash
python -m unittest discover -s tests
```

This command will automatically discover and run all test cases in the `tests` directory.

## Continuous Integration

This project uses [GitHub Actions](https://github.com/features/actions) for continuous integration (CI). Each time you push code or open a pull request, the CI workflow will automatically run the tests.

![CI Test Suite](https://github.com/your-username/your-repo/actions/workflows/ci.yml/badge.svg)

## Environment Setup

This project uses both OpenAI and Firebase. Ensure the following environment variables are set:

- **OPENAI_API_KEY**: Your OpenAI API key
- **FIREBASE_CREDENTIALS**: Your Firebase credentials

To configure Firebase:

1. Add a `serviceAccountKey.json` file with your Firebase credentials, or set the credentials as environment variables as shown in the `.env.example` file.

## License

This project is licensed under the MIT license.

## Acknowledgments

- OpenAI Whisper: [Link](https://github.com/openai/whisper)

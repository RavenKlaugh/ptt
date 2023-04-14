# PTT (Push To Talk)
Push To Talk for ChatGPT

This project provides a web interface to interact with OpenAI's ChatGPT using text or voice input. The interface is designed using Flask and is deployed using Docker. With this project, you can have a seamless experience with ChatGPT, receiving text and audio responses to your queries.

## Prerequisites

- Docker Desktop
- OpenAI API Key
- AWS Access Key and AWS Secret Access Key (see https://docs.aws.amazon.com/polly/latest/dg/getting-started.html) 

## How to Deploy

1. Clone the repository:

```
git clone https://github.com/your_github_username/chatgpt-web-interface.git
```

2. Build the Docker image:

```
cd ptt
docker build -t ptt .
```

3. Run the Docker container, passing the OpenAI API key, AWS Access key, and AWS Secret Access key as environment variables:

```
docker run -p 5000:5000 -e OPENAI_API_KEY=youropenaiapikey -e AWS_ACCESS_KEY_ID=youracceskey -e AWS_SECRET_ACCESS_KEY=yoursecretacceskey ptt
```

  Replace `your_openai_api_key` with your actual OpenAI API key.

4. Access the web interface:

Open your web browser and navigate to http://localhost:5000.

## Usage

- Type your message into the text input field and click the "Submit Text" button to send a text prompt to ChatGPT.
- Press and hold the "Hold to Record" button to record a voice prompt. Release the button to send the voice prompt to ChatGPT.
- The audio response from ChatGPT will automatically play at 1.5x speed.
- Chat history, including prompts and responses, is displayed in the "Chat History" textarea.

## Contributing

Pull requests and suggestions are welcome. Please create an issue to discuss your proposed changes.


## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE License - see the [LICENSE](LICENSE) file for details.

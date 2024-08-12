from google.cloud import aiplatform

def initialize_ai_platform():
    aiplatform.init(project='gen-lang-client-0248637689', location='us-central1')
    print("Google Cloud AI Platform SDK is installed and configured!")

def main():
    initialize_ai_platform()

if __name__ == '__main__':
    main()

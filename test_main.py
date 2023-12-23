import pytest
from fastapi.testclient import TestClient
from main import app  # Assuming your FastAPI app is in a file named main.py

@pytest.fixture
def client():
    return TestClient(app)

def test_process_text(client):
    # Define your test input data
    test_data = {"text": """Videos that say approved vaccines are dangerous and cause autism, cancer or infertility are among those that will be taken down, the company said.  The policy includes the termination of accounts of anti-vaccine influencers.  Tech giants have been criticised for not doing more to counter false health information on their sites.  In July, US President Joe Biden said social media platforms were largely responsible for people's scepticism in getting vaccinated by spreading misinformation, and appealed for them to address the issue.  YouTube, which is owned by Google, said 130,000 videos were removed from its platform since last year, when it implemented a ban on content spreading misinformation about Covid vaccines.  In a blog post, the company said it had seen false claims about Covid jabs "spill over into misinformation about vaccines in general". The new policy covers long-approved vaccines, such as those against measles or hepatitis B.  "We're expanding our medical misinformation policies on YouTube with new guidelines on currently administered vaccines that are approved and confirmed to be safe and effective by local health authorities and the WHO," the post said, referring to the World Health Organization."""}

    # Make a mock request to the /text endpoint
    response = client.post("/text", json=test_data)

    # Check if the response is successful (status code 200)
    assert response.status_code == 200

    # Get the length of the original input text
    input_text_length = len(test_data["text"])

    # Get the length of the generated audio text
    # Assuming the content is a dictionary with a "text" key
    generated_audio_text = response.json()["text"]
    generated_audio_length = len(generated_audio_text)

    # Assert that the generated audio is shorter than the input text
    assert generated_audio_length < input_text_length

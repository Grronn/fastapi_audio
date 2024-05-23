import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_process_text_endpoint(client):
    response = client.post("/text", json={"text": "Videos that say approved vaccines are dangerous and cause autism, cancer or infertility are among those that will be taken down, the company said.  The policy includes the termination of accounts of anti-vaccine influencers.  Tech giants have been criticised for not doing more to counter false health information on their sites.  In July, US President Joe Biden said social media platforms were largely responsible for people's scepticism in getting vaccinated by spreading misinformation, and appealed for them to address the issue.  YouTube, which is owned by Google, said 130,000 videos were removed from its platform since last year, when it implemented a ban on content spreading misinformation about Covid vaccines.  In a blog post, the company said it had seen false claims about Covid jabs spill over into misinformation about vaccines in general. The new policy covers long-approved vaccines, such as those against measles or hepatitis B.  We're expanding our medical misinformation policies on YouTube with new guidelines on currently administered vaccines that are approved and confirmed to be safe and effective by local health authorities and the WHO, the post said, referring to the World Health Organization."})

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "audio/wav"
    assert "generated_audio.wav" in response.headers["Content-Disposition"]

    assert response.content

def test_process_text_endpoint(client):
    response = client.post("/taras", json={"text": "Meet my family. There are five of us – my parents, my elder brother, my baby sister and me. First, meet my mum and dad, Jane and Michael. My mum enjoys reading and my dad enjoys playing chess with my brother Ken. My mum is slim and rather tall. She has long red hair and big brown eyes. She has a very pleasant smile and a soft voice. My mother is very kind and understanding. We are real friends. She is a housewife. As she has three children, she is always busy around the house. She takes care of my baby sister Meg, who is only three months old. My sister is very small and funny. She sleeps, eats and sometimes cries. We all help our mother and let her have a rest in the evening. Then she usually reads a book or just watches TV. My father is a doctor. He is tall and handsome. He has short dark hair and gray eyes. He is a very hardworking man. He is rather strict with us, but always fair. My elder brother Ken is thirteen, and he is very clever. He is good at Maths and always helps me with it, because I can hardly understand all these sums and problems. Ken has red hair and brown eyes. My name is Jessica. I am eleven. I have long dark hair and brown eyes. I am not as clever as my brother, though I try to do my best at school too. I am fond of dancing. Our dancing studio won The Best Dancing Studio 2015 competition last month. I am very proud of it. I also like to help my mother with my little sister very much. Our family is very united. We love each other and always try to spend more time together."})

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "audio/wav"
    assert "generated_audio.wav" in response.headers["Content-Disposition"]

    assert response.content

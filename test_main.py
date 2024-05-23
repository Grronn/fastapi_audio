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
    response = client.post("/olegtext", json={"text": """Отжимания — одно из основных и наиболее распространенных упражнений. Они полезны не только
для мышц груди, но также очень хороши для пресса, трицепсов, плечевых мышц и корпуса в целом.
Отжимания можно делать в любом месте, и что самое замечательное — они совершенно бесплатны, вам
не понадобятся ни дорогие тренажеры, ни абонемент в спортзал. Если вы хотите хорошо развить
грудные и плечевые мышцы, то данная программа может стать замечательным началом. К тому же это
здорово разовьет вашу силу воли.
Чтобы улучшить свою форму и здоровье, вам нужно всего лишь посвятить упражнениям около 30
минут в неделю и придерживаться этой программы как можно точнее. Обещаю, что вы станете
чувствовать себя гораздо лучше и увереннее после пары первых тренировок. """})

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "audio/wav"
    assert "generated_audio.wav" in response.headers["Content-Disposition"]

    assert response.content
# %promoters - % detractores = NPS(Net Promoter Score)
# Documentação Oficial da API OpenAI: https://platform.openai.com/docs/api-reference/introduction
# Informações sobre o Período Gratuito: https://help.openai.com/en/articles/4936830

# Para gerar uma API Key:
# 1. Crie uma conta na OpenAI
# 2. Acesse a seção "API Keys"
# 3. Clique em "Create API Key"
# Link direto: https://platform.openai.com/account/api-keys

# Integrar com o ChatGPT e usá-lo como um modelo para análise de sentimentos dos nossos comentários.
# Seguem alguns links úteis:
# 1. Endpoint que vamos consumir: https://platform.openai.com/docs/api-reference/chat/create
# 2. Collection Postman da OpenAI: https://www.postman.com/devrel/workspace/openai/documentation/13183464-90abb798-cb85-43cb-ba3a-ae7941e968da

import pandas as pd
import gdown
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import openai

openai_api_key = "AquiDeveConterUmaChaveDeAPIdoCHATGPT...Pago:("

openai.api_key = openai_api_key


def analisar_sentimentos(feedbacks):

    comentarios_formatados = "/n".join(
        f"- {feedback.comentario}" for feedback in feedbacks)
    prompt = f"Analise os seguintes comentários e faça um texto resumo sobre os comentários analisados: /n{comentarios_formatados}"

    resposta_api = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Você é um modelo de análide de sentimentos com foco em feedbacks sobre experiências educacionais."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return resposta_api.choices[0].message.content


# Declaração das CONSTANTES para Nomes, valores e cores das zonas nos gráficos
NPS_ZONAS = ["Crítico", "Aperfeiçonamento", "Qualidade", "Exelência"]
NPS_VALORES = [-100, 0, 50, 75, 100]
NPS_CORES = ["#FF595E", "#FFCA3A", "#8AC926", "#1982C4"]

# Download do arquivo CSV para a pasta local do projeto
file_id = "Aqui deve ter o ID do arquivo no gogle drive"
gdown.download(f"https://drive.google.com/uc?id={file_id}", "feedbacks.csv")
dados = pd.read_csv(
    "C:/Users/tasilva/OneDrive/Codigos_Fonte/PYTHONFONTES/PYTHON3/IfoodDevWeek/feedbacks.csv", delimiter=";")

# Classe de Feedback para atribuír os objetos nota e comentário dos feedbacks


class Feedback:
    def __init__(self, nota, comentario):
        self.nota = nota
        self.comentario = comentario

# Classe AnalisadorFeedback que atribui os valores dos feedback para chamar a função calcular_nps


class AnalisadorFeedback:
    def __init__(self, feedbacks):
        self.feedbacks = feedbacks

    # Função que calcula o NPS
    def calcular_nps(self):
        detratores = sum(
            [1 for feedback in self.feedbacks if feedback.nota <= 6])
        promotores = sum(
            [1 for feedback in self.feedbacks if feedback.nota >= 9])

        return (promotores - detratores) / len(self.feedbacks) * 100

# Função que cria o gráfico


def criar_grafico_nps(nps):
    # Define a largura(x) e a altura(y) do gráfico
    fig, ax = plt.subplots(figsize=(10, 2))

    # Enumera as zonas e preenche o gráfico com suas cores
    for i, zona in enumerate(NPS_ZONAS):
        ax.barh([0], width=NPS_VALORES[i+1]-NPS_VALORES[i],  # Parâmetro width: Informa o tamanho da área preenchida, ou seja, a diferença entre o valor inicial e o final
                left=NPS_VALORES[i], color=NPS_CORES[i])  # Parâmetro left: Informa de onde a área deve começar, ou seja, qual valor horizontal a zona deve começar

    # Barra preta que indica onde o NPS está no gráfico
    ax.barh([0], width=0.75, left=nps, color="black")
    ax.set_yticks([])  # Remove os valores presentes na vertical do gráfico
    # Limita a exibição dos valores de x entre -100 e 100
    ax.set_xlim(-100, 100)
    # Exibe na parte horizontal do gráfico apenas os valores presentes no NPS_VALORES
    ax.set_xticks(NPS_VALORES)

    # Adiciona o valor do NPS no gráfico
    plt.text(nps, 0, f"{nps:.2f}", ha="center", va="center",
             color="white", bbox=dict(facecolor="black"))

    # Cria o objeto patches para depois atribuílo no método plt.legend() que cria as legendas.
    patches = [mpatches.Patch(color=NPS_CORES[i], label=NPS_ZONAS[i])
               for i in range(len(NPS_ZONAS))]
    nps_patch = mpatches.Patch(color="black", label="NPS")
    patches.append(nps_patch)
    plt.legend(handles=patches, bbox_to_anchor=(0, 1))

    # Dá título ao gráfico
    plt.title("Gráfico de NPS - Bootcamp DIO")

    # Ajusta a janela ao tamanho do gráfico
    plt.tight_layout()
    # Exibe o gráfico
    plt.show()


# Atribui os valores da classe Feedback à variável feedbacks
feedbacks = [Feedback(linha['nota'], linha['comentario'])
             for i, linha in dados.iterrows()]

analisador = AnalisadorFeedback(feedbacks)
nps = analisador.calcular_nps()

criar_grafico_nps(nps)

insigths = analisar_sentimentos(feedbacks)
print(insigths)

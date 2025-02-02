# Debate IA: Lucas vs Luiz

Este projeto é uma simulação de debate entre duas IAs com pontos de vista distintos, usando o modelo **Google Gemini** para gerar conteúdo e **Google Text-to-Speech (gTTS)** para converter as respostas em fala. O debate ocorre entre **Lucas**, um quimbandeiro, e **Luiz**, um católico conservador, ambos argumentando sobre temas fornecidos pelo usuário.

O objetivo deste projeto é criar um ambiente de debate automatizado que simula como diferentes perspectivas podem ser argumentadas sobre temas diversos.

## Funcionalidades

- **Geração de Respostas:** O modelo **Google Gemini** é usado para gerar respostas de Lucas e Luiz, com base em prompts que representam suas perspectivas.
- **Conversão de Texto em Fala:** As respostas das IAs são convertidas para áudio usando **gTTS**, para que o debate possa ser ouvido, além de lido.
- **Simulação de Debate Final:** Após a primeira rodada de respostas, a IA simula mais trocas de argumentos entre Lucas e Luiz, com base nas respostas anteriores.
- **Salvamento de Respostas:** O usuário pode salvar as respostas geradas e a conclusão do debate em arquivos de texto.
- **Feedback do Usuário:** O sistema coleta feedback do usuário sobre a qualidade do debate e armazena em um arquivo JSON.

## Requisitos

Antes de rodar o projeto, você precisa garantir que possui as seguintes dependências instaladas:

- Python 3.x
- **tkinter** - Para a interface gráfica.
- **google-generativeai** - Biblioteca para interagir com o modelo **Google Gemini**.
- **gTTS** - Para converter texto em fala.
- **playsound** - Para reproduzir o áudio gerado.

### Instalação das Dependências

Use o seguinte comando para instalar as dependências necessárias:

```bash
pip install google-generativeai gtts playsound

debate-ia-gemini/
├── main.py                 # Script principal da aplicação
├── feedback.json           # Armazenamento dos feedbacks dos usuários
├── debate_lucas.txt        # Respostas geradas para Lucas (Quimbandeiro)
├── debate_luiz.txt         # Respostas geradas para Luiz (Católico)
├── debate_conclusao.txt    # Conclusão final do debate
└── README.md               # Este arquivo

No arquivo main.py, substitua "GOOGLE_API_KEY" pela sua chave de API do Google Gemini:

Para rodar a aplicação, basta executar o script Python:
*
python main.py
*


Se você gostaria de contribuir para este projeto, sinta-se à vontade para abrir uma issue ou enviar um pull request. Toda contribuição é bem-vinda!

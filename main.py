import tkinter as tk
from tkinter import ttk
import json
from tkinter import messagebox
import google.generativeai as genai
from gtts import gTTS
import os
from playsound import playsound

# **ATENÇÃO:** Nunca compartilhe sua chave de API publicamente!
GOOGLE_API_KEY = "GOOGLE_API_KEY"  # Substitua pela sua nova chave da API Google Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Criar uma instância do modelo generativo
model = genai.GenerativeModel('gemini-1.5-flash')

# Função para converter texto em fala
def text_to_speech(text, filename="output.mp3"):
    try:
        tts = gTTS(text=text, lang='pt')
        tts.save(filename)
        playsound(filename)
    except Exception as e:
        print(f"Erro ao reproduzir áudio: {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)

# Função para fazer a chamada à API de IA
def generate_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro na resposta da IA: {str(e)}"

# Função para iniciar o debate
def start_debate():
    topic = user_input.get()

    if not topic.strip():
        messagebox.showwarning("Entrada Vazia", "Por favor, insira um tema para o debate.")
        return

    # Primeira rodada de argumentos
    prompt_lucas = f"Lucas, argumente do ponto de vista de um profesor sobre o seguinte tema. Sempre em português do Brasil: {topic}"
    response_lucas = generate_response(prompt_lucas)

    prompt_luiz = f"Luiz, argumente do ponto de vista de um aluno conservador sobre o seguinte tema. Sempre em português do Brasil: {topic}"
    response_luiz = generate_response(prompt_luiz)

    # Atualiza os Text widgets com as respostas da IA
    lucas_response_text.config(state=tk.NORMAL)
    lucas_response_text.delete("1.0", tk.END)
    lucas_response_text.insert(tk.END, f"**Lucas (profesor):**\n{response_lucas}")
    lucas_response_text.config(state=tk.DISABLED)

    luiz_response_text.config(state=tk.NORMAL)
    luiz_response_text.delete("1.0", tk.END)
    luiz_response_text.insert(tk.END, f"**Luiz (aluno):**\n{response_luiz}")
    luiz_response_text.config(state=tk.DISABLED)

    # Converter as respostas em fala, se a opção estiver ativada
    if audio_var.get():
        text_to_speech(response_lucas, "lucas.mp3")
        text_to_speech(response_luiz, "luiz.mp3")

    # Iniciar o debate final
    initiate_conclusion_debate(topic, response_lucas, response_luiz)

# Função para iniciar o debate final entre Lucas e Luiz
def initiate_conclusion_debate(topic, initial_lucas_response, initial_luiz_response):
    # Iniciar a conversa com as respostas iniciais
    conversation = f"**Lucas:** {initial_lucas_response}\n\n**Luiz:** {initial_luiz_response}\n\n"

    previous_lucas = initial_lucas_response
    previous_luiz = initial_luiz_response

    # Simular a conversa final com 3 trocas de respostas
    for i in range(3):
        # Lucas responde a Luiz
        prompt_conclusion_lucas = (
            f"Lucas, levando em consideração o que Luiz disse anteriormente, responda de forma construtiva sobre o tema '{topic}'. "
            f"Sua resposta deve refletir sua perspectiva como um profesor."
        )
        response_conclusion_lucas = generate_response(prompt_conclusion_lucas)
        conversation += f"**Lucas:** {response_conclusion_lucas}\n\n"
        previous_lucas = response_conclusion_lucas

        # Luiz responde a Lucas
        prompt_conclusion_luiz = (
            f"Luiz, levando em consideração o que Lucas disse anteriormente, responda de forma construtiva sobre o tema '{topic}'. "
            f"Sua resposta deve refletir sua perspectiva como um aluno conservador."
        )
        response_conclusion_luiz = generate_response(prompt_conclusion_luiz)
        conversation += f"**Luiz:** {response_conclusion_luiz}\n\n"
        previous_luiz = response_conclusion_luiz

    # Atualiza o Text widget com a conversa final
    conclusion_response_text.config(state=tk.NORMAL)
    conclusion_response_text.delete("1.0", tk.END)
    conclusion_response_text.insert(tk.END, conversation)
    conclusion_response_text.config(state=tk.DISABLED)

    # Converter a conversa final em fala, se a opção estiver ativada
    if audio_var.get():
        text_to_speech(conversation, "conclusao_debate.mp3")

# Função para salvar as respostas em arquivos de texto com codificação UTF-8
def save_responses():
    lucas_response = lucas_response_text.get("1.0", tk.END)
    luiz_response = luiz_response_text.get("1.0", tk.END)
    conclusion_response = conclusion_response_text.get("1.0", tk.END)

    with open("debate_lucas.txt", "w", encoding="utf-8") as file_lucas:
        file_lucas.write(lucas_response)

    with open("debate_luiz.txt", "w", encoding="utf-8") as file_luiz:
        file_luiz.write(luiz_response)

    with open("debate_conclusao.txt", "w", encoding="utf-8") as file_conclusao:
        file_conclusao.write(conclusion_response)

    messagebox.showinfo("Salvo", "As respostas foram salvas com sucesso.")

# Função para coletar feedback do usuário
def submit_feedback():
    feedback_data = {
        "pergunta": user_input.get(),
        "resposta_lucas": lucas_response_text.get("1.0", tk.END),
        "resposta_luiz": luiz_response_text.get("1.0", tk.END),
        "conclusao_debate": conclusion_response_text.get("1.0", tk.END),
        "feedback": feedback.get()
    }

    with open("feedback.json", "a", encoding="utf-8") as feedback_file:
        json.dump(feedback_data, feedback_file, ensure_ascii=False)
        feedback_file.write("\n")

    messagebox.showinfo("Feedback", "Obrigado pelo seu feedback!")

    # Limpar campos de feedback
    feedback.set("")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Debate de IAs: Lucas vs Luiz")
root.geometry("900x700")
root.resizable(False, False)

# Aplicar um tema moderno
style = ttk.Style(root)
style.theme_use('clam')  # Você pode experimentar outros temas como 'alt', 'default', 'classic'

# Definição de cores
main_bg = "#2E4053"
frame_bg = "#1F618D"
label_bg = "#2874A6"
button_bg = "#1ABC9C"
button_fg = "#FFFFFF"
text_bg = "#D6EAF8"
text_fg = "#1C2833"

# Fonte
title_font = ("Helvetica", 16, "bold")
label_font = ("Helvetica", 12, "bold")
text_font = ("Helvetica", 11)
button_font = ("Helvetica", 11, "bold")

root.configure(bg=main_bg)

# Frame Principal
main_frame = ttk.Frame(root, padding="20 20 20 20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Definir estilos personalizados
style.configure('Custom.TCheckbutton', font=text_font)
style.configure('Custom.TButton', font=button_font, foreground=button_fg, background=button_bg)
style.configure('TLabel', font=label_font)

# Campo de entrada do usuário
input_label = ttk.Label(main_frame, text="Insira o tema do debate:", font=label_font)
input_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

user_input = tk.StringVar()
user_input_entry = ttk.Entry(main_frame, width=60, textvariable=user_input, font=text_font)
user_input_entry.grid(row=0, column=1, columnspan=4, padx=5, pady=5, sticky=tk.W)

# Opção para habilitar ou desabilitar áudio
audio_var = tk.BooleanVar(value=True)  # Padrão: áudio ativado
audio_check = ttk.Checkbutton(main_frame, text="Ativar Áudio", variable=audio_var, style='Custom.TCheckbutton')
audio_check.grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)

# Botões de Ação
debate_button = ttk.Button(main_frame, text="Iniciar Debate", command=start_debate, style='Custom.TButton')
debate_button.grid(row=1, column=0, padx=5, pady=15, sticky=tk.W)

save_button = ttk.Button(main_frame, text="Salvar Respostas", command=save_responses, style='Custom.TButton')
save_button.grid(row=1, column=1, padx=5, pady=15, sticky=tk.W)

# Separador
separator = ttk.Separator(main_frame, orient='horizontal')
separator.grid(row=2, column=0, columnspan=6, sticky='ew', pady=10)

# Labels das IAs
lucas_label = ttk.Label(main_frame, text="Lucas (profesor)", background=label_bg, foreground="white", font=title_font, anchor="center", padding=5)
lucas_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky=(tk.W, tk.E))

luiz_label = ttk.Label(main_frame, text="Luiz (aluno)", background=label_bg, foreground="white", font=title_font, anchor="center", padding=5)
luiz_label.grid(row=3, column=3, columnspan=3, padx=5, pady=5, sticky=(tk.W, tk.E))

# Frames para separar as respostas
lucas_frame = ttk.Frame(main_frame, borderwidth=2, relief="groove", padding="10")
lucas_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

luiz_frame = ttk.Frame(main_frame, borderwidth=2, relief="groove", padding="10")
luiz_frame.grid(row=4, column=3, columnspan=3, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

# Text widgets com barras de rolagem para mostrar as respostas da IA
lucas_response_text = tk.Text(lucas_frame, wrap=tk.WORD, height=10, width=45, state=tk.DISABLED, font=text_font, bg=text_bg, fg=text_fg)
lucas_scrollbar = ttk.Scrollbar(lucas_frame, orient=tk.VERTICAL, command=lucas_response_text.yview)
lucas_response_text['yscrollcommand'] = lucas_scrollbar.set
lucas_response_text.grid(row=0, column=0, pady=5, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
lucas_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

luiz_response_text = tk.Text(luiz_frame, wrap=tk.WORD, height=10, width=45, state=tk.DISABLED, font=text_font, bg=text_bg, fg=text_fg)
luiz_scrollbar = ttk.Scrollbar(luiz_frame, orient=tk.VERTICAL, command=luiz_response_text.yview)
luiz_response_text['yscrollcommand'] = luiz_scrollbar.set
luiz_response_text.grid(row=0, column=0, pady=5, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
luiz_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

# Label para a seção de conclusão do debate
conclusion_label = ttk.Label(main_frame, text="Conclusão do Debate", background=label_bg, foreground="white", font=title_font, anchor="center", padding=5)
conclusion_label.grid(row=5, column=0, columnspan=6, padx=5, pady=10, sticky=(tk.W, tk.E))

# Frame para a conclusão do debate
conclusion_frame = ttk.Frame(main_frame, borderwidth=2, relief="groove", padding="10")
conclusion_frame.grid(row=6, column=0, columnspan=6, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

# Text widget com barra de rolagem para mostrar a conclusão do debate
conclusion_response_text = tk.Text(conclusion_frame, wrap=tk.WORD, height=10, width=85, state=tk.DISABLED, font=text_font, bg=text_bg, fg=text_fg)
conclusion_scrollbar = ttk.Scrollbar(conclusion_frame, orient=tk.VERTICAL, command=conclusion_response_text.yview)
conclusion_response_text['yscrollcommand'] = conclusion_scrollbar.set
conclusion_response_text.grid(row=0, column=0, pady=5, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
conclusion_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

# Campo de feedback
feedback_label = ttk.Label(main_frame, text="Seu Feedback:", font=label_font)
feedback_label.grid(row=7, column=0, padx=5, pady=10, sticky=tk.W)

feedback = tk.StringVar()
feedback_entry = ttk.Entry(main_frame, width=70, textvariable=feedback, font=text_font)
feedback_entry.grid(row=7, column=1, columnspan=4, padx=5, pady=10, sticky=tk.W)

# Botão para enviar feedback
feedback_button = ttk.Button(main_frame, text="Enviar Feedback", command=submit_feedback, style='Custom.TButton')
feedback_button.grid(row=7, column=5, padx=5, pady=10, sticky=tk.W)

# Configurar redimensionamento das colunas para melhor adaptação
for i in range(6):
    main_frame.columnconfigure(i, weight=1)

root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tarefas")      
        

        # Tamanho inicial mais compacto
        self.root.geometry("500x400")
        
        # Permitir redimensionamento
        self.root.resizable(True, True)

        # Configurar as colunas e linhas para expandirem
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(4, weight=1)

        # Lista para armazenar as tarefas
        self.tasks = []

        # Widgets da interface
        self.create_widgets()

    def create_widgets(self):
        """Criação e posicionamento dos widgets da interface."""
        # Título personalizado com fonte vermelha e negrito
        title_label = tk.Label(self.root, text="To-Do List", font=("Arial", 16, "bold"), fg="red")
        title_label.grid(row=0, column=0, columnspan=5, pady=10)

        # Label para descrever a tarefa
        tk.Label(self.root, text="Descreva a Tarefa:").grid(row=1, column=0, padx=(5, 2), pady=5, sticky='w')

        # Campo de entrada de tarefa (agora abaixo do rótulo)
        self.task_entry = tk.Entry(self.root, width=50)
        self.task_entry.grid(row=2, column=0, columnspan=5, padx=(5, 5), pady=5, sticky='we')

        # Calendário personalizado
        self.calendar = Calendar(self.root, date_pattern='dd/mm/y',
                                 background='lightcoral',  # Vermelho claro para o fundo
                                 foreground='white',       # Texto branco
                                 selectbackground='red',   # Fundo vermelho para seleção
                                 selectforeground='white') # Texto branco para seleção
        self.calendar.grid(row=3, column=0, padx=5, pady=5)

        # Label "Horário" ao lado da Combobox
        tk.Label(self.root, text="Horário:").grid(row=3, column=2, padx=5, pady=5, sticky='e')

        # Combobox para selecionar o horário
        self.time_combobox = ttk.Combobox(self.root, values=[f"{h:02d}:00" for h in range(24)], width=5)
        self.time_combobox.grid(row=3, column=3, padx=5, pady=5, sticky='w')

        # Botão para adicionar tarefa ao lado do calendário
        add_button = tk.Button(self.root, text="Adicionar Tarefa", command=self.add_task)
        add_button.grid(row=3, column=4, padx=5)

        # Personalização do botão adicionar tarefa
        add_button.config(bg="lightgreen", fg="black", font=("Arial", 10, "bold"))

        # Caixa de texto personalizada para a lista de tarefas (expansível)
        self.task_textbox = tk.Text(self.root, width=75, height=10, bg="cyan", fg="black", font=("Arial", 12))
        self.task_textbox.grid(row=4, column=0, columnspan=5, padx=5, pady=5, sticky='nsew')

        # Estilos para a formatação personalizada
        self.task_textbox.tag_configure('header', foreground='red', font=('Comic Sans MS', 12, 'bold'))

        # Botão de excluir tarefa com estilo personalizado
        delete_button = tk.Button(self.root, text="Excluir Tarefa", command=self.delete_task)
        delete_button.grid(row=5, column=0, columnspan=5, padx=5, pady=5)

        # Personalização do botão excluir tarefa (fundo vermelho, texto negrito preto)
        delete_button.config(bg="red", fg="black", font=("Arial", 10, "bold"))

    def add_task(self):
        """Adiciona uma nova tarefa à lista."""
        task_description = self.task_entry.get()
        task_date = self.calendar.get_date()
        task_time = self.time_combobox.get()

        if task_description and task_time:
            # Criar um datetime para ordenação
            task_datetime_str = f"{task_date} {task_time}"
            task_datetime = datetime.strptime(task_datetime_str, "%d/%m/%Y %H:%M")

            task = {
                "descrição": task_description,
                "data": task_date,
                "horário": task_time,
                "datetime": task_datetime,  # Usado para ordenar
                "criada_em": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            self.tasks.append(task)
            self.update_task_textbox()
            self.clear_entries()
        else:
            messagebox.showwarning("Entrada inválida", "Por favor, preencha todos os campos.")

    def delete_task(self):
        """Exclui a tarefa selecionada."""
        try:
            task_lines = self.task_textbox.get("1.0", tk.END).split('\n\n')
            if task_lines:
                self.tasks.pop()
                self.update_task_textbox()
        except IndexError:
            messagebox.showwarning("Seleção inválida", "Por favor, selecione uma tarefa para excluir.")

    def update_task_textbox(self):
        """Atualiza a lista de tarefas na interface."""
        # Ordenar as tarefas pela data e hora de agendamento
        self.tasks.sort(key=lambda x: x["datetime"])

        # Limpar o Text widget antes de atualizar
        self.task_textbox.delete(1.0, tk.END)
        for task in self.tasks:
            self.insert_task_in_textbox(task)

    def insert_task_in_textbox(self, task):
        """Insere uma tarefa formatada no Text widget."""
        # Insere "Tarefa" e "Criada em" na mesma linha
        self.task_textbox.insert(tk.END, "Tarefa: ", 'header')
        self.task_textbox.insert(tk.END, f"{task['descrição']}    ")
        self.task_textbox.insert(tk.END, "Criada em: ", 'header')
        self.task_textbox.insert(tk.END, f"{task['criada_em']}\n")

        # Insere o agendamento em linhas separadas
        self.task_textbox.insert(tk.END, "Agendamento:\n", 'header')
        self.task_textbox.insert(tk.END, f"  Data: {task['data']}\n")
        self.task_textbox.insert(tk.END, f"  Horário: {task['horário']}\n\n")

    def clear_entries(self):
        """Limpa os campos de entrada após adicionar uma tarefa."""
        self.task_entry.delete(0, tk.END)
        self.time_combobox.set('')


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()

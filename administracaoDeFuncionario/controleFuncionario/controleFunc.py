import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

#função para conectar o banco de dados
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='empresa_db'
    )

#função para adicionar funcionario
def add_funcionario():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO funcionarios (funcionario, cargo, salario, empresa) VALUES (%s, %s, %s, %s)",
            (entry_funcionario.get(), entry_cargo.get(), entry_salario.get(), entry_empresa.get())
        )
        conn.commit()
        load_data()
        clear_entries()
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", str(err))
    finally:
        cursor.close()
        conn.close()

#função para mostrar os funcionarios na tabela
def load_data():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM funcionarios")
        rows = cursor.fetchall()
        for row in tree.get_children():
            tree.delete(row)
        for row in rows:
            tree.insert("", tk.END, values=row)
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", str(err))
    finally:
        cursor.close()
        conn.close()

#função para deletar funcionarios
def delete_funcionario():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Aviso", "Nenhum item selecionado")
        return
    item_id = tree.item(selected_item)['values'][0]
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM funcionarios WHERE id = %s", (item_id,))
        conn.commit()
        load_data()
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", str(err))
    finally:
        cursor.close()
        conn.close()

#função delete
def clear_entries():
    entry_funcionario.delete(0, tk.END)
    entry_cargo.delete(0, tk.END)
    entry_salario.delete(0, tk.END)
    entry_empresa.delete(0, tk.END)

# Criando a interface gráfica
root = tk.Tk()
root.title("Gestão de Funcionários")

root.configure(bg="#ADD8E6")  # Define a cor de fundo como azul clarinho

# Frame para o formulário e a logo
frame_form = tk.Frame(root, bg="#ADD8E6")  # Define a cor de fundo do frame
frame_form.pack(pady=10)


# Alterando o ícone da janela
root.iconbitmap("img/technology.ico")  # Substitua pelo caminho do seu arquivo .ico

# Criar os campos de entrada
frame_form = tk.Frame(root)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Funcionário").grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_form, text="Cargo").grid(row=1, column=0, padx=5, pady=5)
tk.Label(frame_form, text="Salário").grid(row=2, column=0, padx=5, pady=5)
tk.Label(frame_form, text="Empresa").grid(row=3, column=0, padx=5, pady=5)

entry_funcionario = tk.Entry(frame_form)
entry_cargo = tk.Entry(frame_form)
entry_salario = tk.Entry(frame_form)
entry_empresa = tk.Entry(frame_form)

entry_funcionario.grid(row=0, column=1, padx=5, pady=5)
entry_cargo.grid(row=1, column=1, padx=5, pady=5)
entry_salario.grid(row=2, column=1, padx=5, pady=5)
entry_empresa.grid(row=3, column=1, padx=5, pady=5)

btn_add = tk.Button(frame_form, text="Adicionar", command=add_funcionario)
btn_add.grid(row=4, column=0, columnspan=2, pady=10)

frame_table = tk.Frame(root)
frame_table.pack(pady=10)

columns = ("ID", "Funcionário", "Cargo", "Salário", "Empresa")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack()

btn_delete = tk.Button(root, text="Excluir", command=delete_funcionario)
btn_delete.pack(pady=10)

load_data()

root.mainloop()

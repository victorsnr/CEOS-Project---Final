import { useState } from 'react';
import TodoItem from '../components/TodoItem';

export default function TodoListPage() {
  const [todos, setTodos] = useState([
    { id: 1, title: 'Finalizar o protótipo no Figma', completed: true },
    { id: 2, title: 'Configurar o Tailwind CSS', completed: true },
    { id: 3, title: 'Criar a tela de Login e Cadastro', completed: false },
    { id: 4, title: 'Integrar a API com o fetch', completed: false },
  ]);

  const [searchTerm, setSearchTerm] = useState('');
  const [newTaskTitle, setNewTaskTitle] = useState('');

  // Função que simula o POST (Adicionar)
  const handleAddTodo = () => {
    if (newTaskTitle.trim() === '') return;

    const newTask = {
      id: Date.now(), 
      title: newTaskTitle,
      completed: false
    };

    setTodos([...todos, newTask]);
    setNewTaskTitle('');
  };

  // Função que simula o DELETE (Excluir)
  const handleDeleteTodo = (idToRemove) => {
    // Retorna todos os itens cujo ID seja DIFERENTE do ID que queremos remover
    const updatedTodos = todos.filter((todo) => todo.id !== idToRemove);
    // Atualiza o estado com a nova lista
    setTodos(updatedTodos);
  };

  const filteredTodos = todos.filter((todo) =>
    todo.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-50 p-8 flex justify-center">
      <div className="w-full max-w-2xl bg-white p-6 rounded-xl shadow-md h-fit">
        
        <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">
          Minha TODO List
        </h1>

        <div className="mb-6">
          <input
            type="text"
            placeholder="Pesquisar tarefas pelo nome..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          />
        </div>

        <div className="flex gap-2 mb-6 p-4 bg-blue-50 rounded-lg border border-blue-100">
          <input
            type="text"
            placeholder="O que precisa ser feito?"
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleAddTodo()} 
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button 
            onClick={handleAddTodo}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition"
          >
            Adicionar
          </button>
        </div>

        <div className="flex flex-col gap-3">
          {filteredTodos.length > 0 ? (
            filteredTodos.map((todo) => (
              <TodoItem 
                key={todo.id} 
                title={todo.title} 
                completed={todo.completed} 
                // Passamos a função enviando o ID específico desta tarefa
                onDelete={() => handleDeleteTodo(todo.id)} 
              />
            ))
          ) : (
            <div className="p-4 border border-gray-200 rounded-lg text-gray-500 text-center bg-gray-50">
              Nenhuma tarefa encontrada.
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
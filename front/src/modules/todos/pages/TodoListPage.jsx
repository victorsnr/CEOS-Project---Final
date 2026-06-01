import { useState, useEffect } from 'react';
import TodoItem from '../components/TodoItem';

export default function TodoListPage() {
  const [todos, setTodos] = useState([]);

  const [searchTerm, setSearchTerm] = useState('');
  
  
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');

  const handleLoadTodos = async () => {
      try {
        const token = localStorage.getItem("token");

        const response = await fetch("http://localhost:5000/api/tasks/me", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        const data = await response.json();

        const formattedTodos = data.map((task) => ({
          id: task.id,
          title: task.title,
          description: task.description,
          completed: task.status === "concluido"
        }));

        setTodos(formattedTodos);
      } catch (error) {
        console.error("Erro ao buscar tarefas:", error);
        alert("Erro ao conectar ao servidor.");
      }
    };

  useEffect(() => {
    handleLoadTodos();
  }, []);

  const handleAddTodo = async () => {

    const token = localStorage.getItem("token"); 

    const response = await fetch("http://localhost:5000/api/tasks/me", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: newTaskTitle,
        description: newTaskDescription
      })
    });

    const data = await response.json();

    if (!response.ok) {
      console.error("Erro ao adicionar tarefa:", data);
      alert("Erro ao adicionar tarefa.");
      return;
    }

    await handleLoadTodos();

    setNewTaskTitle('');
    setNewTaskDescription('');
  };

  const handleDeleteTodo = async (idToRemove) => {
    const token = localStorage.getItem("token");

    const response = await fetch(`http://localhost:5000/api/tasks/me/${idToRemove}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!response.ok) {
      const data = await response.json();
      alert(data.message);
      return;
    }

    await handleLoadTodos();
  };

  const handleEditTodo = async (idToEdit, newTitle, newDescription) => {
    const token = localStorage.getItem("token");
    
    const response = await fetch(`http://localhost:5000/api/tasks/me/${idToEdit}`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        title: newTitle,
        description: newDescription
      })
    });

    if (!response.ok) {
      const data = await response.json();
      alert(data.message);
      return;
    }

    await handleLoadTodos();
  };

  const handleToggleComplete = async (idToToggle) => {
    const token = localStorage.getItem("token");
    const response = await fetch(`http://localhost:5000/api/tasks/me/${idToToggle}/status`, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        status: "concluido"
      })
    });

    if (!response.ok) {
      const data = await response.json();;
      alert(data.message);
      return;
    }

    await handleLoadTodos();
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

        <div className="flex flex-col gap-3 mb-6 p-4 bg-blue-50 rounded-lg border border-blue-100">
          <input
            type="text"
            placeholder="Título da tarefa *"
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <textarea
            placeholder="Descrição..."
            value={newTaskDescription}
            onChange={(e) => setNewTaskDescription(e.target.value)}
            rows="2"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />
          <button 
            onClick={handleAddTodo}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium transition self-end"
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
                description={todo.description} 
                completed={todo.completed} 
                onDelete={() => handleDeleteTodo(todo.id)}
                onEdit={(newTitle, newDescription) => handleEditTodo(todo.id, newTitle, newDescription)}
                onToggle={() => handleToggleComplete(todo.id)}
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
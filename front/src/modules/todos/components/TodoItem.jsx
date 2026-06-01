import { useState } from 'react';

// aqui exporta o titulo, descriçao e outros atributos
export default function TodoItem({ title, description, completed, onDelete, onEdit, onToggle }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(title);
  const [editDescription, setEditDescription] = useState(description);

  // 2. Novo estado para controlar se a descrição está visível
  const [isExpanded, setIsExpanded] = useState(false);

  const cofirmDelete = (title) => {
    const confirmation = window.confirm(`Tem certeza que deseja excluir a tarefa "${title}"?`);
    if (confirmation) {
      onDelete();
    }
  };

  const handleSave = () => {
    if (editTitle.trim() !== '' && editDescription.trim() !== '') {
      onEdit(editTitle, editDescription);
      setIsEditing(false);
    }
  };

  return (
    <div className="flex flex-col p-4 border border-gray-200 rounded-lg bg-white hover:shadow-sm transition">
      
      {/* CABEÇALHO DA TAREFA */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3 flex-1">
          <input 
            type="checkbox" 
            checked={completed}
            disabled={completed} // desabilita o checkbox se a tarefa já estiver concluída
            onChange={onToggle}
            className="w-5 h-5 text-blue-600 rounded focus:ring-blue-500 cursor-pointer"
          />
          
          {isEditing ? (
            <div className="flex-1 flex flex-col gap-2">
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                className="px-2 py-1 border border-blue-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                autoFocus
              />

              <textarea
                value={editDescription}
                onChange={(e) => setEditDescription(e.target.value)}
                rows="2"
                className="px-2 py-1 border border-blue-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              />
            </div>
          ) : (
            //botão titulo ao clicar, mostra a descrição ou esconde a descrição
            <button 
              onClick={() => setIsExpanded(!isExpanded)}
              className={`text-gray-800 hover:text-blue-600 text-left font-medium transition ${completed ? 'line-through text-gray-400' : ''}`}
            >
              {title}
            </button>
          )}
        </div>

        <div className="flex gap-2 ml-4">
          {isEditing ? (
            <button onClick={handleSave} className="text-sm px-3 py-1 bg-green-100 text-green-700 rounded hover:bg-green-200 transition">
              Salvar
            </button>
          ) : (
            <button onClick={() => { setEditTitle(title); setEditDescription(description); setIsEditing(true); }} className="text-sm px-3 py-1 bg-yellow-100 text-yellow-700 rounded hover:bg-yellow-200 transition">
              Editar
            </button>
          )}
          <button onClick={() => cofirmDelete(title)} className="text-sm px-3 py-1 bg-red-100 text-red-700 rounded hover:bg-red-200 transition">
            Excluir
          </button>
        </div>
      </div>

      {/* detalhes da tarefa */}
      {isExpanded && !isEditing && (
        <div className="mt-4 pt-3 border-t border-gray-100 text-gray-600 text-sm pl-8">
          {/* Descrição da tarefa ou o padrão se n tiver descrição */}
          {description ? description : <span className="italic text-gray-400">Nenhuma descrição adicionada para esta tarefa.</span>}
        </div>
      )}

    </div>
  );
}
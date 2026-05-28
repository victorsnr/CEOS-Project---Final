export default function TodoItem({ title, completed}){
    return (
        <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg bg-white hover:shadow-sm transition">

            <div className="flex items-center gap-3">
                <input
                    type="checkbox"
                    defaultChecked={completed}
                    className="w-5 h-5 text-blue-600 rounded focus:ring-blue-500 cursor-pointer"
                    />
                    <span className={`text-gray-800 ${completed ? 'line-through text-gray-400' : ''}`}>
                        {title}
                    </span>
            </div>
            <div className="flex gap-2">
                <button className="text-sm px-3 py-1 bg-yellow-100 text-yellow-700 rounded hover:bg-yellow-200 transition">
                    Editar
                </button>
                {/* conectamos o ato do clique no botão de excluir*/}
                <button onClick={onDelete}
                className="text-sm px-3 py-1 bg-red-100 text-red-700 rounded hover:bg-red-200 transition">
                    Excluir
                </button>
            </div>

        </div>
    );
}
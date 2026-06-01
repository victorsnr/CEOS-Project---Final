import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginPage from './modules/auth/pages/LoginPage.jsx';
import TodoListPage from './modules/todos/pages/TodoListPage';

// gerenciador de rotas da aplicação, mostra qual tela com base no URL
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Quando a URL for apenas "/", mostra o Login */}
        <Route path="/" element={<LoginPage />} />
        
        {/* Quando a URL for "/todos", mostra a Lista */}
        <Route path="/todos" element={<TodoListPage />} />
      </Routes>
    </BrowserRouter>
  );
}
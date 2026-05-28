import { useState } from "react"; // useState para saber qual modo está, serve para tanto para login quanto para cadastro
import { useNavigate } from "react-router-dom";

export default function LoginPage(){
    const[isLogin, setIsLogin] = useState(true); // define que a tela vai carregar inicialmente no login
    // Inicializa a ferramenta de navegação
    const navigate = useNavigate();
    //Função que será chamada ao clicar em entrar ou cadastrar
    const handleAuth = () => {
        //Futuramente, aqui será a integração com API
        navigate('/todo');
    }

    // return contém o contéudo da pagina em si
    return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-xl shadow-md p-8">
        
        <h2 className="text-2xl font-bold text-center text-gray-800 mb-8">
          {isLogin ? 'Entrar na sua conta' : 'Criar nova conta'} {/* IF/ELSE para  opções de entrar ou criar conta*/}
        </h2>

        <form className="flex flex-col gap-4">
          {/* O campo de Nome só aparece se for a tela de Cadastro */}
          {!isLogin && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Nome</label>
              <input
                type="text"
                placeholder="Seu nome completo"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">E-mail</label>
            <input
              type="email"
              placeholder="seu@email.com"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Senha</label>
            <input
              type="password"
              placeholder="••••••••"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <button
            type="button"
            onClick={handleAuth}
            className="w-full bg-blue-600 text-white font-medium py-2 px-4 rounded-lg hover:bg-blue-700 transition mt-2"
          >
            {isLogin ? 'Entrar' : 'Cadastrar'}
          </button>
        </form>

        {/* Botão para alternar entre os modos */}
        <div className="mt-6 text-center text-sm text-gray-600">
          {isLogin ? 'Ainda não tem uma conta?' : 'Já possui uma conta?'}
          <button
            onClick={() => setIsLogin(!isLogin)}
            className="ml-1 text-blue-600 font-semibold hover:underline focus:outline-none"
          >
            {isLogin ? 'Cadastre-se' : 'Faça login'}
          </button>
        </div>

      </div>
    </div>
    )
}
import requests

BASE_URL = "http://localhost:5000/api"

token = None
task1_id = None
task2_id = None
headers = {"Authorization": f"Bearer {token}"}


# =========================================================
# 1. CRIAÇÃO DE USUÁRIO
# =========================================================

def test_criar_usuario():
    response = requests.post(
        f"{BASE_URL}/users",
        json={
            "nome": "Victor Samuel",
            #"username": "victor",
            "email": "victor@gmail.com",
            #"cpf": "12345678900",
            #"dt_nasc": "2004-08-15",
            "password": "12345678"
        }
    )

    assert response.status_code == 201


# =========================================================
# 2. LOGIN
# =========================================================

def test_login():
    global token, headers

    response = requests.post(
        f"{BASE_URL}/login",
        json={
            "email": "victor@gmail.com",
            "password": "12345678"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data

    token = data["access_token"]
    headers["Authorization"] = f"Bearer {token}"

# =========================================================
# 3. CRIAR TASK 1
# =========================================================

def test_criar_task_1():
    global task1_id, headers
    
    response = requests.post(
        f"{BASE_URL}/tasks/me",
        json={"title": "Estudar Flask",
              "description": "Aprender JWT",
              "prazo": "2026-06-01"},
        
        headers=headers
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data

    task1_id = data["id"]


# =========================================================
# 4. CRIAR TASK 2
# =========================================================

def test_criar_task_2():
    global task2_id, headers
    response = requests.post(
        f"{BASE_URL}/tasks/me",
        json={
            "title": "Treinar PostgreSQL",
            "description": "Praticar relacionamentos",
            "prazo": "2026-06-10"
        },
        headers=headers
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data

    task2_id = data["id"]


# =========================================================
# 5. LISTAR TASKS PENDENTES
# =========================================================

def test_listar_tasks_pendentes():
    global headers
    response = requests.get(
        f"{BASE_URL}/tasks/me?status=pendente",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) >= 2


# =========================================================
# 6. ATUALIZAR TASK 1
# =========================================================

def test_atualizar_task_1():
    global headers
    response = requests.put(
        f"{BASE_URL}/tasks/me/{task1_id}",
        json={
            "title": "Estudar Flask Avançado",
            "description": "Aprender Flask, JWT e Docker",
            "prazo": "2026-06-15"
        },
        headers=headers
    )

    assert response.status_code == 200


# =========================================================
# 7. CONCLUIR TASK 2
# =========================================================

def test_concluir_task_2():
    global headers

    response = requests.patch(
        f"{BASE_URL}/tasks/me/{task2_id}/status",
        json={
            "status": "concluido"
        },
        headers=headers
    )

    assert response.status_code == 200


# =========================================================
# 8. LISTAR TASKS CONCLUÍDAS
# =========================================================

def test_listar_tasks_concluidas():
    global headers

    response = requests.get(
        f"{BASE_URL}/tasks/me?status=concluido",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) >= 1


# =========================================================
# 9. DELETAR TASK 1
# =========================================================

def test_deletar_task_1():
    global headers

    response = requests.delete(
        f"{BASE_URL}/tasks/me/{task1_id}",
        headers=headers
    )

    assert response.status_code == 200


# =========================================================
# 10. DELETAR TASK 2
# =========================================================

def test_deletar_task_2():
    global headers

    response = requests.delete(
        f"{BASE_URL}/tasks/me/{task2_id}",
        headers=headers
    )

    assert response.status_code == 200


# =========================================================
# 11. DELETAR USUÁRIO
# =========================================================

def test_deletar_usuario():
    global headers

    response = requests.delete(
        f"{BASE_URL}/users/me",
        headers=headers
    )

    assert response.status_code == 200
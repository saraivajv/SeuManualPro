def test_fluxo_completo_materiais(client):
    """
    Testa o ciclo de vida: 
    1. Criar Materiais
    2. Criar Manutenção
    3. Adicionar Materiais à Manutenção
    4. Verificar Cálculo de Custo
    """
    
    resp_cimento = client.post("/materiais/", json={"nome": "Cimento", "precoUnitario": 50.0})
    assert resp_cimento.status_code == 201
    id_cimento = resp_cimento.json()["id"]

    resp_areia = client.post("/materiais/", json={"nome": "Areia", "precoUnitario": 10.0})
    assert resp_areia.status_code == 201
    id_areia = resp_areia.json()["id"]

    resp_manut = client.post("/manutencao/", json={"resumo": "Consertar Muro"})
    assert resp_manut.status_code == 201
    id_manut = resp_manut.json()["id"]

    client.post(f"/manutencao/{id_manut}/materiais", json={
        "materialId": id_cimento,
        "quantidade": 2
    })

    client.post(f"/manutencao/{id_manut}/materiais", json={
        "materialId": id_areia,
        "quantidade": 5
    })

    resp_final = client.get(f"/manutencao/{id_manut}")
    dados = resp_final.json()

    assert dados["custoTotalMateriais"] == 150.0
    assert len(dados["materiais"]) == 2
    
    # Verifica se os detalhes do material estão no JSON
    nomes_materiais = [m["nome"] for m in dados["materiais"]]
    assert "Cimento" in nomes_materiais
    assert "Areia" in nomes_materiais


def test_bloqueio_manutencao_finalizada(client):
    """
    Testa a Regra de Negócio:
    Não deve ser possível adicionar material se status for 'concluida'
    """
    m_resp = client.post("/materiais/", json={"nome": "Tinta", "precoUnitario": 100.0})
    id_mat = m_resp.json()["id"]

    manut_resp = client.post("/manutencao/", json={"resumo": "Pintura", "status": "concluida"})
    id_manut = manut_resp.json()["id"]

    resp = client.post(f"/manutencao/{id_manut}/materiais", json={
        "materialId": id_mat,
        "quantidade": 1
    })

    assert resp.status_code == 400
    assert "finalizada" in resp.json()["detail"].lower()
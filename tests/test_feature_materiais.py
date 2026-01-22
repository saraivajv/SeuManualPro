def test_ciclo_completo_com_delecoes_e_updates(client):
    # Criar Cimento (R$ 50)
    resp_cimento = client.post("/materiais/", json={"nome": "Cimento", "precoUnitario": 50.0})
    assert resp_cimento.status_code == 201
    id_cimento = resp_cimento.json()["id"]

    # Criar Areia (R$ 10)
    resp_areia = client.post("/materiais/", json={"nome": "Areia", "precoUnitario": 10.0})
    assert resp_areia.status_code == 201
    id_areia = resp_areia.json()["id"]

    # Criar Material Extra (R$ 100)
    resp_extra = client.post("/materiais/", json={"nome": "Tijolo", "precoUnitario": 100.0})
    id_extra = resp_extra.json()["id"]

    # Criar Manutenção
    resp_manut = client.post("/manutencao/", json={"resumo": "Muro Frontal"})
    assert resp_manut.status_code == 201
    id_manut = resp_manut.json()["id"]

    # Adicionar 2 Cimentos (2 * 50 = 100)
    client.post(f"/manutencao/{id_manut}/materiais", json={"materialId": id_cimento, "quantidade": 2})
    
    # Adicionar 5 Areias (5 * 10 = 50)
    client.post(f"/manutencao/{id_manut}/materiais", json={"materialId": id_areia, "quantidade": 5})

    # Verificar custo total: 150.0
    resp_get = client.get(f"/manutencao/{id_manut}")
    assert resp_get.json()["custoTotalMateriais"] == 150.0

    # O preço do Cimento subiu para R$ 60.0
    resp_patch = client.patch(f"/materiais/{id_cimento}", json={"precoUnitario": 60.0})
    assert resp_patch.status_code == 200
    assert resp_patch.json()["precoUnitario"] == 60.0

    # Verificar se o custo da manutenção atualizou automaticamente
    # Novo cálculo: (2 Cimentos * 60) + (5 Areias * 10) = 120 + 50 = 170.0
    resp_get_updated = client.get(f"/manutencao/{id_manut}")
    assert resp_get_updated.json()["custoTotalMateriais"] == 170.0

    # Tentar apagar o Cimento
    # DEVE FALHAR (Regra de Negócio)
    resp_del_fail = client.delete(f"/materiais/{id_cimento}")
    assert resp_del_fail.status_code == 400
    assert "vinculado" in resp_del_fail.json()["detail"]

    # Tentar apagar o Tijolo (Material Extra)
    # DEVE FUNCIONAR
    resp_del_ok = client.delete(f"/materiais/{id_extra}")
    assert resp_del_ok.status_code == 204
    
    # Apagar a manutenção
    resp_del_manut = client.delete(f"/manutencao/{id_manut}")
    assert resp_del_manut.status_code == 204

    # Verificar se sumiu
    resp_404 = client.get(f"/manutencao/{id_manut}")
    assert resp_404.status_code == 404
    
    # Agora que a manutenção foi apagada, o vínculo sumiu.
    # Deve ser possível apagar o Cimento agora.
    resp_del_cimento = client.delete(f"/materiais/{id_cimento}")
    assert resp_del_cimento.status_code == 204


def test_bloqueio_manutencao_finalizada(client):
    """Teste isolado para a regra de status finalizada"""
    m_resp = client.post("/materiais/", json={"nome": "Tinta", "precoUnitario": 100.0})
    id_mat = m_resp.json()["id"]

    manut_resp = client.post("/manutencao/", json={"resumo": "Pintura", "status": "finalizada"})
    id_manut = manut_resp.json()["id"]

    # Tentar adicionar
    resp = client.post(f"/manutencao/{id_manut}/materiais", json={"materialId": id_mat, "quantidade": 1})
    assert resp.status_code == 400
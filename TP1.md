# TP1 — Mini-TP Réplication automatique et récupération

**Durée : 1h à 1h15**  
**Technologies : Docker, Docker Compose, Python, Flask**

## Objectifs

À la fin du TP, vous devez savoir :

- expliquer la réplication distribuée ;
- observer plusieurs copies d'une même donnée ;
- simuler la panne d'un nœud ;
- continuer les écritures avec les réplicas disponibles ;
- reconstruire automatiquement le contenu d'un nœud après sa disparition.

## 1. Démarrer le cluster

```bash
docker compose up -d
docker ps
```

Tester :

```bash
curl http://localhost:8080/health
curl http://localhost:8081/health
curl http://localhost:8082/health
```

## 2. Écrire une donnée

```bash
curl -X POST http://localhost:8080/data   -H "Content-Type: application/json"   -d '{"key":"order-1","value":"Laptop - quantity=2 - price=1200"}'
```

Observez la réponse de réplication.

Puis :

```bash
curl http://localhost:8080/data
curl http://localhost:8081/data
curl http://localhost:8082/data
```

**Question :** combien de copies de `order-1` existe-t-il ?

## 3. Simuler une panne

```bash
docker stop replication-node-2
```

Vérifier :

```bash
curl http://localhost:8080/data
curl http://localhost:8082/data
```

Puis écrire :

```bash
curl -X POST http://localhost:8080/data   -H "Content-Type: application/json"   -d '{"key":"order-2","value":"Smartphone - quantity=1 - price=800"}'
```

**Questions :**
1. Quels nœuds possèdent `order-2` ?
2. Pourquoi la donnée n'a-t-elle pas pu être envoyée à Node 2 ?
3. Le système reste-t-il disponible ?

## 4. Supprimer complètement le nœud

```bash
docker rm -f replication-node-2
```

Vérifier :

```bash
docker ps
```

Les deux autres réplicas doivent rester disponibles.

## 5. Recréer Node 2

```bash
docker compose up -d replication-node-2
```

Attendre quelques secondes puis :

```bash
curl http://localhost:8081/data
```

Le nouveau nœud doit récupérer automatiquement les données depuis un réplica disponible.

## 6. Synthèse

Compléter :

```text
Réplication =
Panne d'un nœud =
Réplica =
Resynchronisation =
```

### Questions finales

- Pourquoi avoir plusieurs copies ?
- Que se passe-t-il lorsqu'un nœud devient indisponible ?
- Quelle différence entre réplication et partitionnement ?
- Pourquoi un vrai SGBD distribué doit-il gérer la cohérence ?

## Transition

Dans la suite du cours, nous allons voir comment un véritable SGBD distribué, notamment Cassandra, gère ces problématiques à une échelle supérieure.

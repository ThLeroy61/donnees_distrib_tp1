# Notes enseignant — TP1 Session 2 V2

## Intention pédagogique

Ce TP est volontairement construit avant Cassandra.

Il permet de faire comprendre :

1. réplication ;
2. disponibilité ;
3. panne d'un nœud ;
4. écritures sur les réplicas disponibles ;
5. resynchronisation d'un nœud nouvellement créé.

## Point important

Ce n'est PAS une implémentation de production.

La réplication est réalisée par de simples appels HTTP entre applications Flask. La resynchronisation récupère l'état d'un pair disponible.

Cela permet de visualiser le principe avant d'étudier Cassandra, ses facteurs de réplication, son partitionnement, ses mécanismes de cohérence et son architecture distribuée.

## Démonstration recommandée

1. Écrire `order-1`.
2. Montrer les trois copies.
3. Arrêter Node 2.
4. Écrire `order-2`.
5. Montrer que Node 1 et Node 3 restent disponibles.
6. Supprimer Node 2 avec `docker rm -f`.
7. Recréer uniquement Node 2 avec `docker compose up -d replication-node-2`.
8. Attendre 2 à 5 secondes.
9. Interroger `localhost:8081/data`.
10. Montrer la récupération des données.

## Message clé

> La réplication permet de conserver plusieurs copies d'une donnée afin de mieux résister à la panne d'un nœud.

> La récupération d'un nœud consiste à resynchroniser son état à partir d'une copie disponible.

## Limites à expliciter

Cette simulation ne gère pas :

- consensus ;
- quorum ;
- conflits d'écriture avancés ;
- versionnement des données ;
- transactions distribuées ;
- persistance disque ;
- sécurité inter-nœuds ;
- garanties de cohérence d'un vrai SGBD.

Ces limites constituent justement la transition vers Cassandra et les systèmes distribués réels.

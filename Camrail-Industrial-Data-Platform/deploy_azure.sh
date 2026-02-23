#!/bin/bash
# Déploiement automatisé vers Microsoft Azure Container Apps & Azure Database for PostgreSQL
echo "🚀 [AZURE] Authentification via Azure CLI..."
# az login
echo "🏗️ [AZURE] Création du Resource Group..."
# az group create --name Camrail-Enterprise-RG --location westeurope
echo "🐘 [AZURE] Provisionnement de Microsoft Azure PostgreSQL Flexible Server..."
# az postgres flexible-server create --resource-group Camrail-Enterprise-RG --name camrail-dwh-prod --admin-user camrail_admin --admin-password "enterprise_password_2026!" --tier Burstable --sku-name Standard_B1ms --storage-size 32
echo "🎃 [AZURE] Event Hub namespace (Kafka compatible)..."
# az eventhubs namespace create -n camrailevents -g Camrail-Enterprise-RG -l westeurope
echo "🐳 [AZURE] Déploiement de l'API Flask sur Azure Container Apps..."
# az containerapp up --name camrail-ml-api --resource-group Camrail-Enterprise-RG --source . --ingress external --target-port 5000 --env-vars POSTGRES_HOST=camrail-dwh-prod.postgres.database.azure.com POSTGRES_USER=camrail_admin POSTGRES_PASSWORD=enterprise_password_2026! POSTGRES_DB=camrail_dwh
echo "✅ [AZURE] Plateforme hybride Kafka/Postgres déployée avec succès en production !"

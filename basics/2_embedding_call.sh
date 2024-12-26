
AZURE_OPENAI_API_KEY=$(grep AZURE_OPENAI_API_KEY ../.env | awk '{print $3}')
AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME=$(grep AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME ../.env | awk '{print $3}')

curl https://sergiopruebaopenai2.openai.azure.com/openai/deployments/$AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME/embeddings?api-version=2022-12-01\
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{"input": "I love AI a lot"}'
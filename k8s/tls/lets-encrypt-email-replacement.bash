EMAIL="user@email.com"
sed "s/REPLACE_ME@example.com/$EMAIL/" clusterissuer.yaml | kubectl apply -f -

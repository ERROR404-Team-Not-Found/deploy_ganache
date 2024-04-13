# deploy_ganache

Add repo: helm repo add ethereum-helm-charts <https://ethpandaops.github.io/ethereum-helm-charts>

Update repo: helm repo update

Install chart: helm install my-ganache ethereum-helm-charts/ganache --version 0.1.2 --namespace hackathon

## Install guide

helm install blockchain-service ./helmChart --namespace hackathon

## Usage guides

Api endpoints: <http://blockchain-service:8093/transactions/{user_address}>
               <http://blockchain-service:8093/balance/{user_address}>

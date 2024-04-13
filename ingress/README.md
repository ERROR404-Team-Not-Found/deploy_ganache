helm repo update

helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace tc-namespace --values ./ingress/values.yaml

kubectl apply -f ./ingress/ingress.yaml --namespace hackathon
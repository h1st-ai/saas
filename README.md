## Note

### Treafik

Traefik is used as a gateway to route URL to the right ECS container.
Currently, Traefik is setup on `10.30.0.142`, and `/project/*` is redirect to that instance.

Later on, we can try to use ECS service but now this setup takes too much time.

### Keycloak

Keycloak is ran using ECS. Push image to ECR `h1st/keycloak:latest` to update the keycloak image.

The service will pick it up by itself, or you can delete it manually. If you do it manually, it may take up to 5m when update the keycloak to be ready again.

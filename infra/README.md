## H1st Terraform Infrastructure

The infrastructure is setup using Terraform, there are some components were setup manually. Need to migrate back to terraform later.

Folder structure

```
common: shared information for both environment (vpc, subnet, ...)
staging: dev & test environment
prod: production environment
```

Note:
 * DNS is hosted under namecheap account. @khoama can access it via 1Password.
 * Keycloak instances are shared for both prod & staging environment
 * Current default SSH key is `bao`, and configured to allow SSH certificate. Make sure to change it to the approriate owner later.

### ECS Cluster

[ECS Autoscaling / Capacity provider](https://us-west-1.console.aws.amazon.com/ecs/home?region=us-west-1#/clusters/H1st-staging/capacityProviders) is manually configured via the UI.

Currently the ECS Workbench container definition for prod is configure to `v0.2.0` and staging to `latest`. If we want to update the prod image, we need to change the container definition, or use a convention for production.


### EFS 


### Treafik

Traefik is used as a gateway to route URL to the right ECS container.
Currently, Traefik is setup on `10.30.0.142`, and `/project/*` is redirect to that instance.

Later on, we can try to use ECS service but now this setup takes too much time.

### Keycloak

Keycloak is ran using ECS. Push image to ECR `394497726199.dkr.ecr.us-west-1.amazonaws.com/h1st/keycloak:latest` to update the keycloak image.

The service will pick it up by itself, or you can delete it manually. If you do it manually, it may take up to 5m when update the keycloak to be ready again.

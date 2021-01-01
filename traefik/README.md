# Treafik

For local setup:

  * Download from traefik page
  * Run following commands

```
ln -s ../workbench-controller/traefik-config conf
cp common.yml conf/
cp dashboard.yml conf/
./traefik --configfile local.yml
```
